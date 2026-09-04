from pathlib import Path
from uuid import uuid4

import boto3

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.config import settings
from app.dependencies import get_db, get_current_user
from app.models import (
    DiagnosticLog,
    ServiceCall,
    User,
    UserRole,
)
from app.schemas.diagnostic_log import DiagnosticLogRead


router = APIRouter(
    prefix="/diagnostic_logs",
    tags=["diagnostic_logs"],
)


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def can_upload_diagnostic(user: User) -> bool:
    return user.role in {
        UserRole.OPERATIONS_ADMIN,
        UserRole.FIELD_TECHNICIAN,
    }


@router.get(
    "",
    response_model=list[DiagnosticLogRead],
)
async def list_diagnostic_logs(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[DiagnosticLog]:

    statement = (
        select(DiagnosticLog)
        .order_by(DiagnosticLog.created_at.desc())
    )

    result = await db.execute(statement)

    return list(result.scalars().all())


@router.post(
    "",
    response_model=DiagnosticLogRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_diagnostic_report(
    service_call_id: int = Form(...),
    notes: str | None = Form(default=None),
    file: UploadFile = File(...),

    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticLog:

    # ---------------------------------------------------------
    # RBAC
    # ---------------------------------------------------------

    if not can_upload_diagnostic(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Operations Admins and Field Technicians may upload diagnostic reports",
        )

    # ---------------------------------------------------------
    # Make sure service call exists
    # ---------------------------------------------------------

    service_call = await db.get(
        ServiceCall,
        service_call_id,
    )

    if service_call is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service call {service_call_id} not found",
        )

    # ---------------------------------------------------------
    # Validate filename
    # ---------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported file type. "
                "Allowed: txt, pdf, png, jpg, jpeg, gif, webp"
            ),
        )

    # ---------------------------------------------------------
    # Validate file size
    # ---------------------------------------------------------

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Diagnostic report cannot exceed 10 MB",
        )

    # Return to beginning of file before boto3 reads it.
    await file.seek(0)

    # ---------------------------------------------------------
    # Unique S3 key
    #
    # diagnostics/12/<uuid>-inspection.pdf
    # ---------------------------------------------------------

    safe_filename = Path(file.filename).name

    s3_key = (
        f"diagnostics/"
        f"{service_call_id}/"
        f"{uuid4()}-{safe_filename}"
    )

    bucket_name = settings.diagnostics_bucket_name

    s3_client = boto3.client(
        "s3",
        region_name="us-east-1",
    )

    # ---------------------------------------------------------
    # Upload file to S3
    # ---------------------------------------------------------

    try:
        await run_in_threadpool(
            s3_client.upload_fileobj,
            file.file,
            bucket_name,
            s3_key,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not upload diagnostic report to S3",
        ) from exc

    file_url = f"s3://{bucket_name}/{s3_key}"

    # ---------------------------------------------------------
    # Create PostgreSQL row
    # ---------------------------------------------------------

    diagnostic_log = DiagnosticLog(
        service_call_id=service_call_id,
        file_url=file_url,
        notes=notes,
    )

    db.add(diagnostic_log)

    try:
        await db.commit()
        await db.refresh(diagnostic_log)

    except Exception:
        await db.rollback()

        # DB failed after S3 succeeded. Clean up the S3 object.
        try:
            await run_in_threadpool(
                s3_client.delete_object,
                Bucket=bucket_name,
                Key=s3_key,
            )
        except Exception:
            pass

        raise

    return diagnostic_log

@router.get("/{diagnostic_log_id}/download")
async def get_diagnostic_download_url(
    diagnostic_log_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:

    log = await db.get(
        DiagnosticLog,
        diagnostic_log_id,
    )

    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnostic log {diagnostic_log_id} not found",
        )

    prefix = f"s3://{settings.diagnostics_bucket_name}/"

    if not log.file_url.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnostic report has an invalid S3 location",
        )

    s3_key = log.file_url.removeprefix(prefix)

    s3_client = boto3.client(
        "s3",
        region_name="us-east-1",
    )

    download_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.diagnostics_bucket_name,
            "Key": s3_key,
        },
        ExpiresIn=900,
    )

    return {
        "download_url": download_url,
    }
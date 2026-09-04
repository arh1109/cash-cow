"""
RoboPulse Command Center
Day 4 Answer Key - ServiceCall endpoints.

Day 5 - Phase B challenge answer key
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select, case, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db, require_role
from app.models import ServiceCall, ServiceCallPriority, Technician, ATM, ServiceCallStatus, User, UserRole
from app.schemas.service_call import DiscrepancyRead, ServiceCallRead, ServiceCallStatusUpdate, ReliabilityMetric

router = APIRouter(prefix="/service_calls", tags=["service_calls"])


@router.get("/discrepancies", response_model=list[DiscrepancyRead])
async def list_colocation_discrepancies(
    priority: ServiceCallPriority | None = Query(
        default=None,
        description="Only return discrepancies for service_calls of this priority.",
    ),
    db: AsyncSession = Depends(get_db),
    ##Day 5 code here
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN, UserRole.FIELD_TECHNICIAN)),
):
    """
    Business Question #2: Co-Location Discrepancy - a fourth time.
    Day 1: Python. Day 2: raw SQL. Day 3: async ORM script. Today:
    the same three-table JOIN, reachable at
    GET /service_calls/discrepancies, with an optional priority filter.

    Selects only the four columns the response actually needs,
    rather than full ServiceCall/ATM/Technician objects, to reduce 
    the amount of data sent over the wire.
    """
    statement = (
        select(
            ServiceCall.id.label("service_call_id"),
            ServiceCall.title,
            ATM.branch_id.label("atm_branch_id"),
            Technician.branch_id.label("technician_branch_id"),
        )
        .join(ATM, ATM.id == ServiceCall.atm_id)
        .join(Technician, Technician.id == ServiceCall.technician_id)
        .where(ATM.branch_id != Technician.branch_id)
    )

    #if a priority filter was provided, add it to the WHERE clause
    if priority is not None:
        statement = statement.where(ServiceCall.priority == priority)

    statement = statement.order_by(ServiceCall.id)

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]


##Day 5 - Phase B Answer Key
@router.patch("/{service_call_id}/status", response_model=ServiceCallRead)
async def update_service_call_status(
    service_call_id: int,
    payload: ServiceCallStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN, UserRole.FIELD_TECHNICIAN)),
) -> ServiceCall:
    service_call = await db.get(ServiceCall, service_call_id)
    if service_call is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ServiceCall '{service_call_id}' not found",
        )
    if payload.status == ServiceCallStatus.COMPLETED:
        service_call.mark_completed()
    elif payload.status == ServiceCallStatus.FAILED:
        service_call.mark_failed()
    else:
        service_call.status = payload.status

    await db.commit()
    await db.refresh(service_call)
    return service_call


@router.get("/reliability", response_model=list[ReliabilityMetric])
async def reliability_metrics(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Business Question #3: Reliability Metrics.
    Any authenticated role can view this - it's an analytics endpoint,
    matching the problem statement's "Auditor can view analytics
    dashboards" requirement, same as /service_calls/discrepancies.
    """
    statement = (
        select(
            ATM.model,
            func.count(ServiceCall.id).label("total_service_calls"),
            func.sum(case((ServiceCall.status == ServiceCallStatus.COMPLETED, 1), else_=0)).label("completed_count"),
            func.sum(case((ServiceCall.status == ServiceCallStatus.FAILED, 1), else_=0)).label("failed_count"),
        )
        .join(ServiceCall, ServiceCall.atm_id == ATM.id)
        .group_by(ATM.model)
        .order_by(ATM.model)
    )
    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]
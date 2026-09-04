"""
RoboPulse Fleet Command Center
Day 4 - Robot endpoints.
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models import ATM, ATMStatus, User, UserRole
from app.schemas.atm import ATMCreate, ATMRead, ATMUpdate

#our FastAPI router for the /robots endpoints. The prefix argument means that
#  all routes defined in this router will be prefixed with /robots, and the 
# tags argument is used for documentation purposes in the OpenAPI schema.
router = APIRouter(prefix="/atms", tags=["atms"])


#our GET /robots endpoint, which returns a list of robots, optionally filtered by battery level.
@router.get("", response_model=list[ATMRead])
async def list_atms(
    max_cash: Decimal | None = Query(
        default=None,
        ge=0,
        le=100,
        description="Only return robots strictly below this battery percentage.",
    ),
    db: AsyncSession = Depends(get_db),
    # Day 5 Addition here:
    _: User = Depends(get_current_user)
) -> list[ATM]:
    """
    Business Question #1: Low Battery Alert - a fourth time.
    GET /robots?max_battery=20 answers the exact same question
    Day 1's Python, Day 2's SQL, and Day 3's ORM query already
    answered - now reachable over HTTP, with the threshold supplied
    by whoever calls the API instead of hardcoded in a script.
    """
    statement = select(ATM).where(ATM.status != ATMStatus.OFFLINE)
    if max_cash is not None:
        statement = statement.where(ATM.cash_level < max_cash)
    statement = statement.order_by(ATM.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

#our GET /robots/{robot_id} endpoint, which returns a single robot by ID.
@router.get("/{atm_id}", response_model=ATMRead)
# Day 5 Addition
async def get_atm(atm_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)) -> ATM:
    atm = await db.get(ATM, atm_id)
    if atm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM {atm_id} not found",
        )
    return atm

#our POST /robots endpoint, which creates a new robot.
@router.post("", response_model=ATMRead, status_code=status.HTTP_201_CREATED)
async def create_robot(payload: ATMCreate, db: AsyncSession = Depends(get_db),
        # Day 5 Addition
        _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN))) -> ATM:
    atm = ATM(**payload.model_dump())
    db.add(atm)
    await db.commit()
    await db.refresh(atm)
    return atm

@router.put("/{atm_id}", response_model=ATMRead)
async def update_atm(
    atm_id: int,
    payload: ATMUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> ATM:

    atm = await db.get(ATM, atm_id)

    if atm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM {atm_id} not found",
        )

    atm.serial_number = payload.serial_number
    atm.model = payload.model
    atm.cash_level = payload.cash_level
    atm.status = payload.status
    atm.branch_id = payload.branch_id

    await db.commit()
    await db.refresh(atm)

    return atm

@router.delete("/{atm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_atm(
    atm_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> None:

    atm = await db.get(ATM, atm_id)

    if atm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM {atm_id} not found",
        )

    await db.delete(atm)
    await db.commit()
'''
Day 3 Demo Script - Robopulse Command Center

Queries the same robopulse_dev_2478 data from Day 2's seed.sql already loaded.
Nothing gets re-seeded today, this script just proves the ORM models line up with the data that already exists.

Script to run from \backend:
    python -m scripts.day3_demo
'''

import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models import ATM, ATMStatus

async def find_low_cash_atms(session, threshold: int = 20) -> list[ATM]:
    """
    Answering Business question #1: Low cash alert (3rd time answering it)
    """

    # statement object: a SQLAlchemy construct that represents a SQL SELECT statement
    statement = (
        select(ATM)
        .options(selectinload(ATM.branch))
        .where(ATM.status != ATMStatus.OFFLINE, ATM.cash_level < threshold)
        .order_by(ATM.id)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())

async def main() -> None:
    async with AsyncSessionLocal() as session:
        print("== Full ATM Registry (via ORM)==")
        all_atms_stmt = select(ATM).options(selectinload(ATM.branch)).order_by(ATM.id)

        all_atms = await session.execute(all_atms_stmt)
        for atm in all_atms.scalars():
            print(f"{atm!r} -> branch: {atm.branch.name}")

        print("\n== Low Battery Alert (<20%) ==")
        alerts = await find_low_cash_atms(session, threshold=20)
        if not alerts:
            print('No ATMs below threshold ')
        for atm in alerts:
            print(f" ALERT: {atm.serial_number} at {atm.cash_level}% "
                  f"(Branch : {atm.branch.name})")

if __name__ == "__main__":
    asyncio.run(main())
"""
Day Model - Day 3 SQL?Alchemy ORM version
"""
from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import ATMStatus
if TYPE_CHECKING:
    from .branch import Branch
    from .service_call import ServiceCall

class ATM(Base):
    __tablename__ = "atms"

    # here is  atable-level constraint where the battery_level column is ALWAYS between 0 and 100
    __table_args__ = (
        CheckConstraint("cash_level BETWEEN 0 AND 100", name="cash_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key = True)
    serial_number: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[ATMStatus] = mapped_column(
        SqlEnum(ATMStatus, name="atm_status",
            # giving defintiion for how enum values are stored in the database
            # we are using the string representation of enum members
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=ATMStatus.OPERATIONAL
    )
    cash_level: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))

    branch: Mapped["Branch"] = relationship(back_populates="atms")
    service_calls: Mapped[list["ServiceCall"]] = relationship(back_populates="atm")
    LOW_CASH_THRESHOLD: int = 20

    def is_low_battery(self, threshold: int | None= None) -> bool:
        limit = threshold if threshold is not None else ATM.LOW_CASH_THRESHOLD

    def needs_maintenance(self) -> bool:
        return self.status == ATMStatus.MAINTENANCE

    def __repr__(self) -> str:
        return (f"Robot(serial={self.serial_number!r}, model={self.model!r},"
                f"Battery={self.cash_level}%, status={self.status.value}")


# from typing import ClassVar
# from .enums import ATMStatus

# class ATM:
#     """
#     This is a class attribute that will hold all instances of Facility
#     A class attribute is shared across all instances of the class, and
#     can be accessedc using the class name (Facility.registry) or using 
#     an instance of the class (facility_instance.registry).
#     While an instance attribute belongs to a specific instance of the class,
#     a class attribute belongs to the class itself.
#     """
#     registry: ClassVar[list["ATM"]] = []

#     LOW_BATTERY_THRESHOLD: ClassVar[int] = 20

#     # the constructor for the Facility class
#     def __init__(self, atm_id: int, serial_number: str, model: str,
#                 cash_level: int, branch_id: int, atm_status: ATMStatus = ATMStatus.MAINTENANCE):
#         self.id = atm_id
#         self.serial_number = serial_number
#         self.model = model
#         self.status = atm_status
#         self.cash_level = cash_level
#         self.branch_id = branch_id
#         ATM.registry.append(self)

#     """
#     A static method that validates the battery level of a robot
#     The @staticmethod annotation just indicates that is its a static method,
#     meaning it can be called on the class itself, rather than just an instance of a class.
#     """
#     @staticmethod
#     def _validate_cash_level(level: float) -> float:
#         if level < 0:
#             print(f"Warning: cash_level {level} below 0, clamping to 0.")
#             return 0.0
#         if level > 100:
#             print(f"Warning: cash_level {level} above 100, clamping to 100")
#             return 100.0

#         return float(level)

#     # A method to check if the robots battery level is below a certain threshold
#     # if no threshold is provided, it sues the class attribute LOW_BATTERY_THRESHOLD value
#     def is_low_cash(self, threshold: int | None = None) -> bool:
#         limit = threshold if threshold is not None else ATM.LOW_BATTERY_THRESHOLD
#         return self.cash_level < limit

#     def needs_maintenance(self) -> bool:
#         return self.status == ATMStatus.MAINTENANCE

#     # The __repr__ method provides a string representation of the Facility instance equivealent
#     # to the Java toString method, but mostly used for debuggina dn logging
#     def __repr__(self) -> str:
#         return (f"ATM(serial={self.serial_number!r}, model={self.model!r},"
#                 f"Cash={self.cash_level}%, status={self.status.value}")

#     ''' A class method that finds the facility instance by its ID
#     @classmethod annotation - indicates that this method is a class method
#     which means it can be called on the class itself, not just an instance of the class.
#     '''
#     @classmethod
#     def find_by_id(cls, atm_id: int) -> "ATM | None":
#         for atm in cls.registry:
#             if atm.id == atm_id:
#                 return atm
#         return None
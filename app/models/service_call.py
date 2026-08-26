"""
Robot Model - Day 3 SQLAlchemy ORM version
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import ServiceCallPriority, ServiceCallStatus
if TYPE_CHECKING:
    from .diagnostic_log import DiagnosticLog
    from .technician import Technician
    from .atm import ATM

class ServiceCall(Base):
    __tablename__ = "service_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    priority: Mapped[ServiceCallPriority]= mapped_column(
        SqlEnum(
            ServiceCallPriority,
            name="service_call_priority",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        )
    )
    status: Mapped[ServiceCallStatus] = mapped_column(
        SqlEnum(
            ServiceCallStatus,
            name="service_call_status",
            values_callable = lambda enum_cls: [member.value for member in enum_cls]
        ),
        default=ServiceCallStatus.PENDING,
    )
    atm_id: Mapped[int] = mapped_column(Integer, ForeignKey("atms.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))

    atm: Mapped["ATM"] = relationship(back_populates="service_calls")
    technician: Mapped["Technician"] = relationship(back_populates="service_calls")
    # because this is a list, "mission" is singular
    diagnostic_logs: Mapped[list["DiagnosticLog"]] = relationship(back_populates="service_call")

        # update the mission status to completed
    def mark_completed(self) -> None:
        self.status = ServiceCallStatus.COMPLETED

    # updtae the mission status to Failed
    def mark_failed(self) -> None:
        self.status = ServiceCallStatus.FAILED

    def __repr__(self) -> str:
            return (f"Service Call id={self.id}, title={self.title!r}, "
                    f"priority={self.priority.value}, status={self.status.value})")



# from typing import ClassVar
# from .enums import ServiceCallStatus, ServiceCallPriority

# class ServiceCall:
#     """
#     This is a class attribute that will hold all instances of Facility
#     A class attribute is shared across all instances of the class, and
#     can be accessedc using the class name (Facility.registry) or using 
#     an instance of the class (facility_instance.registry).
#     While an instance attribute belongs to a specific instance of the class,
#     a class attribute belongs to the class itself.
#     """
#     registry: ClassVar[list["ServiceCall"]] = []

#     # the constructor for the Facility class
#     def __init__(self, service_call_id: int, title: str, 
#                 atm_id: int, technician_id: int, service_call_priority: ServiceCallPriority, 
#                 service_call_status: ServiceCallStatus = ServiceCallStatus.PENDING):
#         self.id = service_call_id
#         self.title = title
#         self.priority = service_call_priority
#         self.status = service_call_status
#         self.atm_id = atm_id
#         self.technician_id = technician_id
#         ServiceCall.registry.append(self)

#     # The __repr__ method provides a string representation of the Facility instance equivealent
#     # to the Java toString method, but mostly used for debuggina dn logging
#     def __repr__(self) -> str:
#         return (f"Branch(id={self.id}), name={self.name!r},"
#                  f"region={self.location_region!r}")

#     ''' A class method that finds the facility instance by its ID
#     @classmethod annotation - indicates that this method is a class method
#     which means it can be called on the class itself, not just an instance of the class.
#     '''
#     @classmethod
#     def find_by_id(cls, service_call_id: int) -> "ServiceCall | None":
#         for service_call in cls.registry:
#             if service_call.id == service_call_id:
#                 return service_call
#         return None
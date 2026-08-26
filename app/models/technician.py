"""
Operator Model - Day 1 Phase B Challenge Answer Key
Not part of the original problem statement's expected entity list.
However, an operator model is implied by Mission.operator_id.
Follow the same pattern as the other models with a registry/find_by_id

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .branch import Branch
    from .service_call import ServiceCall

class Technician(Base):
    __tablename__ = "technicians"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # foreign key
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))

    branch: Mapped["Branch"] = relationship(back_populates="technicians")
    service_calls: Mapped[list["ServiceCall"]] = relationship(back_populates="technician")

    def __repr__(self) -> str:
            return (f"Technician(id={self.id}, name={self.name!r}, "
                    f"branch_id={self.branch_id})")



# from typing import ClassVar

# class Technician:
#     registry: ClassVar[list["Technician"]] = []

#     def __init__(self, technician_id: int, name: str, branch_id: int):
#         self.id = technician_id
#         self.name = name
#         self.branch_id = branch_id
#         Technician.registry.append(self)

#     @classmethod
#     def find_by_id(cls, technician_id: int) -> "Technician | None":
#         for technician in cls.registry:
#             if technician.id == technician_id:
#                 return technician
#         return None

#     def __repr__(self) -> str:
#         return (f"Technician(id={self.id}, name={self.name!r}, "
#                 f"branch_id={self.branch_id})")
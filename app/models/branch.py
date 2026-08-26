
# tells python to treat every annotation as a string literal, allowing forward refernces
# to classes that are defined later in the file or in other modules
from __future__ import annotations

# Loading the TYPE_CHECKING constant form the typing modules which is used to indicate that certain
# imports are only needed for type checking and not at runtime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String#ORM = Object Relational Mapper
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .technician import Technician
    from .atm import ATM

class Branch(Base):
    # setting the table name for the branch model in the database
    __tablename__ = "branches"

    # define our columns
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(50))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] =  mapped_column(Integer)

    # creating our relatinships with other tables
    atms: Mapped[list["ATM"]] = relationship(back_populates="branch")
    technicians: Mapped[list["Technician"]] = relationship(back_populates="branch")

    def __repr__(self) -> str:
        return (f"Branch(id={self.id}, name={self.name!r}, "
                f"region={self.location_region!r})")

# from typing import ClassVar

# class Branch:
#     """
#     This is a class attribute that will hold all instances of Facility
#     A class attribute is shared across all instances of the class, and
#     can be accessedc using the class name (Facility.registry) or using 
#     an instance of the class (facility_instance.registry).
#     While an instance attribute belongs to a specific instance of the class,
#     a class attribute belongs to the class itself.
#     """
#     registry: ClassVar[list["Branch"]] = []

#     # the constructor for the Facility class
#     def __init__(self, branch_id: int, name: str, location_region: str,
#                 capacity: int, supervisor_id: int):
#         self.id = branch_id
#         self.name = name
#         self.location_region = location_region
#         self.capacity = capacity
#         self.supervisor_id = supervisor_id
#         Branch.registry.append(self)

#     # The __repr__ method provides a string representation of the Facility instance equivealent
#     # to the Java toString method, but mostly used for debuggina dn logging
#     def __repr__(self) -> str:
#         return (f"Branch(id={self.id}), name={self.name!r},"
#                  f"location_region={self.location_region!r}")

#     ''' A class method that finds the facility instance by its ID
#     @classmethod annotation - indicates that this method is a class method
#     which means it can be called on the class itself, not just an instance of the class.
#     '''
#     @classmethod
#     def find_by_id(cls, branch_id: int) -> "Branch | None":
#         for branch in cls.registry:
#             if branch.id == branch_id:
#                 return branch
#         return None
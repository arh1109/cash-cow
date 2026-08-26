"""
Diagnostic Log Model - Day 3 SQLALchemy ORM version
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .service_call import ServiceCall

class DiagnosticLog(Base):
    __tablename__ = "diagnostic_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_call_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_calls.id"))
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    #server_default=func.now() sets the default value of the created_at column
    #to the current timestamp when a new record is inserted into the database
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    service_call: Mapped["ServiceCall"] = relationship(back_populates="diagnostic_logs")

    def __repr__(self) -> str:
        return (f"DiagnosticLog(id={self.id}, service_call_id={self.service_call_id}, "
                f"file_url={self.file_url!r})")

# """
# Diagnostic log model - day 1 plain python version
# """

# from datetime import datetime
# from typing import ClassVar

# class DiagnosticLog:
#     registry: ClassVar[list["DiagnosticLog"]] = []

#     def __init__(self, log_id: int, service_call_id: int, file_url: str,
#                 notes: str | None = None, created_at: datetime | None = None):
#         self.id = log_id
#         self.service_call_id = service_call_id
#         self.file_url = file_url 
#         self.notes = notes 
#         self.created_at = created_at or datetime.now()
#         DiagnosticLog.registry.append(self)

#         def __repr__(self) -> str:
#             return (f"DiagnosticLog(id={self.id}, "
#                     f"file_url={self.file_url!r})")
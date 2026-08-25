"""
Diagnostic log model - day 1 plain python version
"""

from datetime import datetime
from typing import ClassVar

class DiagnosticLog:
    registry: ClassVar[list["DiagnosticLog"]] = []

    def __init__(self, log_id: int, service_call_id: int, file_url: str,
                notes: str | None = None, created_at: datetime | None = None):
        self.id = log_id
        self.service_call_id = service_call_id
        self.file_url = file_url 
        self.notes = notes 
        self.created_at = created_at or datetime.now()
        DiagnosticLog.registry.append(self)

        def __repr__(self) -> str:
            return (f"DiagnosticLog(id={self.id}, "
                    f"file_url={self.file_url!r})")
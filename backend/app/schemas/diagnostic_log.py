from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DiagnosticLogRead(BaseModel):
    id: int
    service_call_id: int
    file_url: str
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
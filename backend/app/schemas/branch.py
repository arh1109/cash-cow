"""
CashCow Command Center
Reference implementation - Pydantic schemas for Branch-level
analytics (Business Questions #4 and #5). No Branch CRUD schemas
exist yet - this file only covers the analytical read models these
two endpoints need.
"""

from pydantic import BaseModel


class MaintenanceFlag(BaseModel):
    branch_id: int
    branch_name: str
    total_atms: int
    maintenance_count: int
    maintenance_percentage: float


class TechnicianActiveServiceCalls(BaseModel):
    technician_id: int
    technician_name: str
    active_service_call_count: int


class ReportingLineResult(BaseModel):
    supervisor_id: int
    technician_count: int
    technicians: list[TechnicianActiveServiceCalls]
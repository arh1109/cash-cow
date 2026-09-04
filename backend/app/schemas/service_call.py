"""
RoboPulse Fleet Command Center
Day 4 Answer Key - Pydantic v2 schema for the discrepancy report.
"""

from pydantic import BaseModel, ConfigDict

from app.models import ServiceCallPriority, ServiceCallStatus

class ServiceCallStatusUpdate(BaseModel):
    status: ServiceCallStatus

class ServiceCallRead(BaseModel):
    id: int
    title: str
    priority: ServiceCallPriority
    status: ServiceCallStatus
    atm_id: int
    technician_id: int

    model_config = ConfigDict(from_attributes=True)


class DiscrepancyRead(BaseModel):
    service_call_id: int
    title: str
    atm_branch_id: int
    technician_branch_id: int

    model_config = ConfigDict(from_attributes=True)


class ReliabilityMetric(BaseModel):
    model: str
    total_service_calls: int
    completed_count: int
    failed_count: int

class ServiceCallCreate(BaseModel):
    title: str
    priority: ServiceCallPriority
    status: ServiceCallStatus = ServiceCallStatus.PENDING
    atm_id: int
    technician_id: int


class ServiceCallUpdate(BaseModel):
    title: str
    priority: ServiceCallPriority
    status: ServiceCallStatus
    atm_id: int
    technician_id: int
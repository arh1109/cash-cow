'''
Need status - Operational | Low-Cash | Maintenance | Offline
Need location_region possibly
priority - Low | Medium | High
'''
from enum import Enum

class ATMStatus(str, Enum):
    OPERATIONAL = "Operational"
    LOW_CASH = "Low-Cash"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"

class ServiceCallStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class ServiceCallPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    CRITICAL = "Critical"
from typing import ClassVar
from .enums import ServiceCallStatus, ServiceCallPriority

class ServiceCall:
    """
    This is a class attribute that will hold all instances of Facility
    A class attribute is shared across all instances of the class, and
    can be accessedc using the class name (Facility.registry) or using 
    an instance of the class (facility_instance.registry).
    While an instance attribute belongs to a specific instance of the class,
    a class attribute belongs to the class itself.
    """
    registry: ClassVar[list["ServiceCall"]] = []

    # the constructor for the Facility class
    def __init__(self, service_call_id: int, title: str, 
                atm_id: int, technician_id: int, service_call_priority: ServiceCallPriority, 
                service_call_status: ServiceCallStatus = ServiceCallStatus.PENDING):
        self.id = service_call_id
        self.title = title
        self.priority = service_call_priority
        self.status = service_call_status
        self.atm_id = atm_id
        self.technician_id = technician_id
        ServiceCall.registry.append(self)

    # The __repr__ method provides a string representation of the Facility instance equivealent
    # to the Java toString method, but mostly used for debuggina dn logging
    def __repr__(self) -> str:
        return (f"Branch(id={self.id}), name={self.name!r},"
                 f"region={self.location_region!r}")

    ''' A class method that finds the facility instance by its ID
    @classmethod annotation - indicates that this method is a class method
    which means it can be called on the class itself, not just an instance of the class.
    '''
    @classmethod
    def find_by_id(cls, service_call_id: int) -> "ServiceCall | None":
        for service_call in cls.registry:
            if service_call.id == service_call_id:
                return service_call
        return None
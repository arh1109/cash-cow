from typing import ClassVar
from .enums import ATMStatus

class ATM:
    """
    This is a class attribute that will hold all instances of Facility
    A class attribute is shared across all instances of the class, and
    can be accessedc using the class name (Facility.registry) or using 
    an instance of the class (facility_instance.registry).
    While an instance attribute belongs to a specific instance of the class,
    a class attribute belongs to the class itself.
    """
    registry: ClassVar[list["ATM"]] = []

    LOW_BATTERY_THRESHOLD: ClassVar[int] = 20

    # the constructor for the Facility class
    def __init__(self, atm_id: int, serial_number: str, model: str,
                cash_level: int, branch_id: int, atm_status: ATMStatus = ATMStatus.MAINTENANCE):
        self.id = atm_id
        self.serial_number = serial_number
        self.model = model
        self.status = atm_status
        self.cash_level = cash_level
        self.branch_id = branch_id
        ATM.registry.append(self)

    """
    A static method that validates the battery level of a robot
    The @staticmethod annotation just indicates that is its a static method,
    meaning it can be called on the class itself, rather than just an instance of a class.
    """
    @staticmethod
    def _validate_cash_level(level: float) -> float:
        if level < 0:
            print(f"Warning: cash_level {level} below 0, clamping to 0.")
            return 0.0
        if level > 100:
            print(f"Warning: cash_level {level} above 100, clamping to 100")
            return 100.0

        return float(level)

    # A method to check if the robots battery level is below a certain threshold
    # if no threshold is provided, it sues the class attribute LOW_BATTERY_THRESHOLD value
    def is_low_cash(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else ATM.LOW_BATTERY_THRESHOLD
        return self.cash_level < limit

    def needs_maintenance(self) -> bool:
        return self.status == ATMStatus.MAINTENANCE

    # The __repr__ method provides a string representation of the Facility instance equivealent
    # to the Java toString method, but mostly used for debuggina dn logging
    def __repr__(self) -> str:
        return (f"ATM(serial={self.serial_number!r}, model={self.model!r},"
                f"Cash={self.cash_level}%, status={self.status.value}")

    ''' A class method that finds the facility instance by its ID
    @classmethod annotation - indicates that this method is a class method
    which means it can be called on the class itself, not just an instance of the class.
    '''
    @classmethod
    def find_by_id(cls, atm_id: int) -> "ATM | None":
        for atm in cls.registry:
            if atm.id == atm_id:
                return atm
        return None
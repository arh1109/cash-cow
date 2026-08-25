from typing import ClassVar

class Technician:
    registry: ClassVar[list["Technician"]] = []

    def __init__(self, technician_id: int, name: str, branch_id: int):
        self.id = technician_id
        self.name = name
        self.branch_id = branch_id
        Technician.registry.append(self)

    @classmethod
    def find_by_id(cls, technician_id: int) -> "Technician | None":
        for technician in cls.registry:
            if technician.id == technician_id:
                return technician
        return None

    def __repr__(self) -> str:
        return (f"Technician(id={self.id}, name={self.name!r}, "
                f"branch_id={self.branch_id})")
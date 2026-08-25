'''
Day 1 Demo script - Cash Cow ATM app
Run from backend/ with the venv active:
    python -m scripts.day1_demo
'''

from app.models import DiagnosticLog, ATM, Branch, ServiceCall, Technician, ATMStatus, ServiceCallPriority, ServiceCallStatus

def find_low_cash_atms(atms: list[ATM], threshold: int=20) -> list[ATM]:
    '''
    Business question #1: Low cash alert
    Which ACTIVE ATMs are operating below the low battery threshold?
    '''
    return [
        atm for atm in atms
        if atm.status != ATMStatus.OFFLINE and atm.is_low_cash(threshold)
    ]

'''
for atim in atms:
    if atm....
    return atm
'''

def find_colocation_discrepancies(
        service_calls: list[ServiceCall],
        atms: list[ATM],
        technicians: list[Technician],
) -> list[tuple[ServiceCall, ATM, Technician]]:
    """
    Here we answer business question #2: Co-location Discrepancy
    Which missions assign a robot to an operator who is NOT at the same facility as that robot?
    
    Takes robots/operators as parameters rather than reaching into Robot.registry or Operator.registry
    directly, so that the function stays testable against any data set, not just whatever has been seeded
    at the time.
    """
    discrepancies: list[tuple[ServiceCall, ATM, Technician]] = []

    for service_call in service_calls:
        atm = ATM.find_by_id(service_call.atm_id)
        technician = Technician.find_by_id(service_call.technician_id)

        """
        Defensive guard: a mission referencing a robot_id or operator_id that DOES NOT EXIST in the registry
        isn't a co-location discrepency, it is a data integrity problem.
        Skip it here, Week 2's validation layer handles this issue properly.
        """
        if technician is None or atm is None:
            continue
        if atm.branch_id != technician.branch_id:
            discrepancies.append((service_call, atm, technician))
    return discrepancies



# create some dummy seed data for the demo, including facilities, robots, missions, and dianostic logs
def seed_demo_data() -> None:
    Branch(1, "Houston Fabrication Plant", "US-South", capacity=40, supervisor_id=101)
    Branch(2, "Rotterdam Logistics Hub", "EU-East", capacity=25, supervisor_id=102)

    ATM(1, "CX-1001", "Sentinel-V2", cash_level=18.5, branch_id=1, atm_status=ServiceCallStatus.COMPLETED)
    ATM(2, "CX-1002", "Sentinel-V2", cash_level=76.0, branch_id=1, atm_status=ServiceCallStatus.IN_PROGRESS)
    ATM(3, "AT-2050", "SkyHawk-Drone", cash_level=9.0, branch_id=2, atm_status=ServiceCallStatus.COMPLETED)
    ATM(4, "CS-1003", "Sentinel-V2", cash_level=42.0, branch_id=2, atm_status=ServiceCallStatus.FAILED)

    Technician(201, "J. Alvarez", branch_id=1)
    # a deliberate co-location discrepancy
    Technician(202, "M. Chen", branch_id=1)

    ServiceCall(service_call_id=1, title="Server Bug", service_call_priority=ServiceCallPriority.CRITICAL, atm_id=1, technician_id=201)
    ServiceCall(service_call_id=2, title="Backward Compatibility Issue", service_call_priority=ServiceCallPriority.LOW, atm_id=3, technician_id=202)

    DiagnosticLog(1, service_call_id=1, file_url="s3://robopulse-diagnostics/rx1001-001.pdf", notes="Vibration sensor reading normal")

# main function to actually run our seed demo runction to create the data and run our low battery check.
def main() -> None:
    seed_demo_data()

    print("== Full ATM Registry ==")
    for atm in ATM.registry:
        print(atm)

    print("\n== Low Battery Alert (< 20%) ==")
    alerts = find_low_cash_atms(ATM.registry, threshold=20)
    if not alerts:
        print("No robots below threshold")
    for atm in alerts:
        print(f" ALERT: {atm.serial_number} at {atm.cash_level}% "
              f"(branch{atm.branch_id})")

    print("\n== Co-location Discrepancies ==")
    discrepancies= find_colocation_discrepancies(
        ServiceCall.registry, ATM.registry, ServiceCall.registry
    )
    if not discrepancies:
        print("No Discrepancies Found ")
    for service_call, atm, technician in discrepancies:
        print(f" Mission {service_call.id} ({service_call.title}): "
              f"robot at facility {atm.branch_id}, "
              f"operator at facility {technician.branch_id}")

# entry point for the script
if __name__ == "__main__":
    main()
import pytest_asyncio

from app.models import ServiceCall, ServiceCallPriority, ServiceCallStatus, Operator, ATM, ATMStatus
from tests.conftest import auth_header

"""
ServiceCall object has 2 foreign keys (atm_id, technician_id) - this fixture
builds the full chain that a real ServiceCall actually needs: a ATM and an Operator,
both need to be tied to the shared seeded_branch fixture we already created
"""
@pytest_asyncio.fixture
async def seeded_service_call(db_session, seeded_branch):
    atm = ATM(
        serial_number="MX-0001",
        model="Test-Bot",
        status=ATMStatus.IDLE,
        cash_level=75,
        branch_id=seeded_branch.id,
    )
    technician = Operator(name="Test Operator", branch_id=seeded_branch.id)
    db_session.add_all([atm, technician])
    await db_session.commit()
    await db_session.refresh(atm)
    await db_session.refresh(technician)

    service_call = ServiceCall(
        title="Test ServiceCall",
        priority=ServiceCallPriority.LOW,
        status=ServiceCallStatus.PENDING,
        atm_id=atm.id,
        technician_id=technician.id,
    )
    db_session.add(service_call)
    await db_session.commit()
    await db_session.refresh(service_call)
    return service_call

"""
Ensure Fleet Admin has 'Full CRUD' according to the problem statement
"""
async def test_operations_admin_can_update_status(client, seeded_users, seeded_service_call):
    response = await client.patch(
        f"/service_calls/{seeded_service_call.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"

"""
Field Operator is the second role that can trigger service_call status changes
"""
async def test_field_technician_can_update_status(client, seeded_users, seeded_service_call):
    response = await client.patch(
        f"/service_calls/{seeded_service_call.id}/status",
        json={"status": "Failed"},
        headers=auth_header(seeded_users["technician"]),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Failed"

"""
Auditor is read-only according to the problem statement, so it should not be able to trigger
updates
"""
async def test_auditor_forbidden_from_updating_status(client, seeded_users, seeded_service_call):
    response = await client.patch(
        f"/service_calls/{seeded_service_call.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["auditor"]),
    )
    assert response.status_code == 403

"""
test if a service_call ID doesn't exist
"""
async def test_nonexistent_service_call_returns_404(client, seeded_users):
    response = await client.patch (
        "/service_calls/999999/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )
    assert response.status_code == 404
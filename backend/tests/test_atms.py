"""
Day 10 - endpoint tests for /atms
"""

from tests.conftest import auth_header

#if there is no authorization header at all, the request should be rejected before the route
#body ever runs
async def test_list_atms_requires_authentication(client):
    response = await client.get("/atms")
    assert response.status_code == 401

"""
the auditor role is the most restricted role in the app - if even Auditor can read the fleet list,
then every other authenticated role can too. This function proves GET /atms uses plain get_current_user
(any role), not require_role function.
"""
async def test_list_atms_any_authenticated_role(client, seeded_users):
    response = await client.get("/atms", headers=auth_header(seeded_users["auditor"]))
    assert response.status_code == 200

"""
Field technician is authenticated but NOT a fleet admin, then creating a atm should be blocked
"""
async def test_create_atm_forbidden_for_field_technician(client, seeded_users, seeded_branch):
    payload = {
        "serial_number": "TX-1001",
        "model": "Test-Bot",
        "cash_level": 50,
        "branch_id": seeded_branch.id,
        "status": "Idle",
    }
    response = await client.post("/atms", json=payload, headers=auth_header(seeded_users["technician"]))
    assert response.status_code == 403

"""
the matching positive test case for a genuine fleet admin to create a atm
"""
async def test_create_atm_succeeds_for_operations_admin(client, seeded_users, seeded_branch):
    payload = {
        "serial_number": "TX-1001",
        "model": "Test-Bot",
        "cash_level": 50,
        "branch_id": seeded_branch.id,
        "status": "Idle",
    }
    response = await client.post("/atms", json=payload, headers=auth_header(seeded_users["admin"]))
    assert response.status_code == 201
    assert response.json()["serial_number"] == "TX-1001"


"""
Verify cash level is within constraints
"""
async def test_low_cash_filter(client, seeded_users, seeded_branch):
    admin_headers = auth_header(seeded_users["admin"])
    low = {"serial_number": "LOW-01", "model":"Test-Bot", "cash_level": 10, "branch_id": seeded_branch.id, "status": "Idle"}
    high = {"serial_number": "HIGH-01", "model": "Test-Bot", "cash_level": 90, "branch_id": seeded_branch.id, "status": "Idle"}

    await client.post("/atms", json=low, headers=admin_headers)
    await client.post("/atms", json=high, headers=admin_headers)

    response = await client.get("/atms?max_cash=20", headers=admin_headers)
    serials = [atm["serial_number"] for atm in response.json()]

    assert "LOW-01" in serials
    assert "HIGH-01" not in serials
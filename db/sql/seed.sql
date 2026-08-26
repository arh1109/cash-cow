-- Robotpulse Command Center - Day 2 Seed Data
-- Reusing the same data from day 1 so todays SQL results can be copared directly with
-- the script results from our vanilla python
-- \i seed.sql

-- branches Records
INSERT INTO branches(id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Houston Fabrication Plant', 'US-South', 40, 101),
    (2, 'Rotterdam Logistics Hub', 'EU-West', 25, 102);

-- technicians records
INSERT INTO technicians(id, name, branch_id) VALUES
    (201, 'J. Alvarez', 1),
    (202, 'M. Chen', 1);

-- atm records
INSERT INTO atms(id, serial_number, model, status, cash_level, branch_id) VALUES
    (1, 'RX-1001', 'Sentinel-V2', 'Low-Cash', 18.5, 1),
    (2, 'RX-1002', 'Sentinel-V2', 'Maintenance', 70.6, 1),
    (3, 'RAD-2050', 'SkyHawk-Drone v2', 'Low-Cash', 9.0, 2),
    (4, 'RX-1003', 'Sentinel-V2', 'Maintenance', 42.0, 1);

-- service_call records
INSERT INTO service_calls(id, title, priority, status, atm_id, technician_id) VALUES
    (1, 'Pipeline Corrosion Sweep', 'Critical', 'Pending', 1, 201),
    (2, 'Warehouse Perimeter Patrol', 'Low', 'Pending', 3, 202),
    (3, 'Control Tower Inspection', 'Medium', 'Completed', 2, 201),
    (4, 'Fence Line Survey', 'Low', 'Failed', 4, 201);

-- diagnostic log records
INSERT INTO diagnostic_logs(service_call_id, file_url, notes) VALUES
    (1, 's3://robopulse-diagnostics/rx1001-001.pdf', 'Vibration sensor reading nominal');

-- SELECT statements AKA QUESTIES
SELECT setval('branches_id_seq', (SELECT MAX(ID) FROM branches));
SELECT setval('technicians_id_seq', (SELECT MAX(ID) FROM technicians));
SELECT setval('atms_id_seq', (SELECT MAX(ID) FROM atms));
SELECT setval('service_calls_id_seq', (SELECT MAX(ID) FROM service_calls));
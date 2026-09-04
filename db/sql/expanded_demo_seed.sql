-- Cash Cow - Expanded Demo Seed Data
-- Purpose: provide richer data for the five business questions.
--
-- This script preserves the users table and reseeds only:
--   diagnostic_logs, service_calls, atms, technicians, branches
--
-- Run against the intended database, for example:
--   psql -h <host> -U postgres -d cashcow -f expanded_demo_seed.sql

BEGIN;

-- Delete dependent rows first.
TRUNCATE TABLE diagnostic_logs, service_calls, atms, technicians, branches RESTART IDENTITY CASCADE;

-- ---------------------------------------------------------------------------
-- Branches
-- supervisor_id is intentionally just an integer on branches.
-- Supervisor 101 oversees two branches so Reporting Lines has a richer example.
-- ---------------------------------------------------------------------------
INSERT INTO branches (id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Houston Fabrication Plant', 'US-South', 40, 101),
    (2, 'Rotterdam Logistics Hub', 'EU-West', 25, 102),
    (3, 'Raleigh Operations Center', 'US-East', 35, 101),
    (4, 'Phoenix Service Hub', 'US-West', 30, 103);

-- ---------------------------------------------------------------------------
-- Technicians
-- ---------------------------------------------------------------------------
INSERT INTO technicians (id, name, branch_id) VALUES
    (201, 'J. Alvarez', 1),
    (202, 'M. Chen', 1),
    (203, 'S. Patel', 2),
    (204, 'R. Johnson', 3),
    (205, 'L. Garcia', 3),
    (206, 'T. Williams', 4);

-- ---------------------------------------------------------------------------
-- ATMs
--
-- Business Question #1:
--   Low-cash ATMs below 20% include ids 1, 5, 8, and 11.
--
-- Business Question #4:
--   Houston:   2 of 4 in Maintenance = 50.0%  -> FLAGGED
--   Rotterdam: 1 of 3 in Maintenance = 33.3% -> FLAGGED
--   Raleigh:   0 of 3 in Maintenance = 0.0%   -> not flagged
--   Phoenix:   1 of 3 in Maintenance = 33.3%  -> FLAGGED
-- ---------------------------------------------------------------------------
INSERT INTO atms (id, serial_number, model, status, cash_level, branch_id) VALUES
    (1,  'RX-1001', 'Sentinel-V2',      'Low-Cash',    18.5, 1),
    (2,  'RX-1002', 'Sentinel-V2',      'Maintenance', 70.6, 1),
    (3,  'RX-1003', 'Sentinel-V2',      'Maintenance', 42.0, 1),
    (4,  'NX-1100', 'Guardian-X1',      'Operational', 83.0, 1),

    (5,  'RAD-2050','SkyHawk-Drone v2', 'Low-Cash',     9.0, 2),
    (6,  'RAD-2051','SkyHawk-Drone v2', 'Maintenance', 61.0, 2),
    (7,  'NX-2200', 'Guardian-X1',      'Operational', 56.5, 2),

    (8,  'RX-3001', 'Sentinel-V2',      'Low-Cash',    12.0, 3),
    (9,  'RX-3002', 'Sentinel-V2',      'Operational', 77.5, 3),
    (10, 'NX-3300', 'Guardian-X1',      'Operational', 47.0, 3),

    (11, 'RAD-4100','SkyHawk-Drone v2', 'Low-Cash',    15.0, 4),
    (12, 'RAD-4101','SkyHawk-Drone v2', 'Maintenance', 66.0, 4),
    (13, 'NX-4400', 'Guardian-X1',      'Operational', 92.0, 4);

-- ---------------------------------------------------------------------------
-- Service Calls
--
-- Active means Pending or In-Progress.
--
-- Business Question #2:
--   Deliberate co-location discrepancies:
--     id 2: ATM branch 2, technician branch 1
--     id 6: ATM branch 3, technician branch 2
--     id 9: ATM branch 4, technician branch 3
--     id 12: ATM branch 1, technician branch 4
--
-- Business Question #3:
--   Multiple models have Completed / Failed history so reliability metrics vary.
--
-- Business Question #5:
--   Supervisor 101 oversees branches 1 and 3.
--   Technicians 201, 202, 204, and 205 have active service calls.
-- ---------------------------------------------------------------------------
INSERT INTO service_calls
    (id, title, priority, status, atm_id, technician_id)
VALUES
    -- Houston / Supervisor 101
    (1,  'Cash Cassette Inspection',        'Critical', 'Pending',     1, 201),
    (2,  'Warehouse Perimeter Patrol',      'Low',      'Pending',     5, 202), -- discrepancy
    (3,  'Dispenser Motor Replacement',     'Medium',   'Completed',   2, 201),
    (4,  'Card Reader Failure Review',      'Low',      'Failed',      3, 202),

    -- Rotterdam / Supervisor 102
    (5,  'Drone Sensor Calibration',        'Medium',   'In-Progress', 5, 203),
    (6,  'Remote Cash Module Inspection',   'Critical', 'Pending',     8, 203), -- discrepancy
    (7,  'Rotor Assembly Service',          'Medium',   'Completed',   6, 203),

    -- Raleigh / Supervisor 101
    (8,  'Network Connectivity Audit',      'Low',      'In-Progress', 9, 204),
    (9,  'Phoenix Emergency Dispatch',      'Critical', 'Pending',    11, 205), -- discrepancy
    (10, 'Preventive Maintenance Review',   'Medium',   'Completed',  10, 204),
    (11, 'Cash Sensor Diagnostic',          'Medium',   'Failed',      8, 205),

    -- Phoenix / Supervisor 103
    (12, 'Houston Cross-Branch Repair',     'Critical', 'In-Progress', 4, 206), -- discrepancy
    (13, 'Aerial Unit Preventive Service',  'Low',      'Completed',  12, 206),
    (14, 'Guardian Power Supply Repair',    'Medium',   'Failed',     13, 206),

    -- Extra completed/failed calls to make model reliability totals meaningful
    (15, 'Sentinel Firmware Verification',  'Low',      'Completed',   9, 204),
    (16, 'SkyHawk Communications Failure',  'Critical', 'Failed',     11, 206),
    (17, 'Guardian Printer Replacement',    'Medium',   'Completed',   7, 203),
    (18, 'Sentinel Cash Path Repair',       'Medium',   'Completed',   1, 201);

-- ---------------------------------------------------------------------------
-- Diagnostic Logs
-- ---------------------------------------------------------------------------
INSERT INTO diagnostic_logs (service_call_id, file_url, notes) VALUES
    (1,  's3://cashcow-diagnostics/demo/rx1001-cash-cassette.pdf',
         'Cash reserve below threshold; cassette inspection requested.'),
    (3,  's3://cashcow-diagnostics/demo/rx1002-dispenser.pdf',
         'Dispenser motor replaced and validation cycle completed.'),
    (5,  's3://cashcow-diagnostics/demo/rad2050-calibration.pdf',
         'Sensor calibration started; unit remains in service workflow.'),
    (11, 's3://cashcow-diagnostics/demo/rx3001-cash-sensor.pdf',
         'Cash sensor diagnostic failed; follow-up service recommended.');

-- Keep serial sequences aligned with the explicitly inserted IDs.
SELECT setval('branches_id_seq',      (SELECT MAX(id) FROM branches));
SELECT setval('technicians_id_seq',   (SELECT MAX(id) FROM technicians));
SELECT setval('atms_id_seq',          (SELECT MAX(id) FROM atms));
SELECT setval('service_calls_id_seq', (SELECT MAX(id) FROM service_calls));

COMMIT;
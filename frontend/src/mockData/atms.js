/**
 * Robopulse Command Center 
 * Day 6 - mock robot data, mirroring day 2's seed.sql data exactly so that 
 * we can test our UI components with accurate data.
 */

export const mockATMs = [
    {id: 1, serialNumber: 'RX-1001', model: 'Sentinel-V2', cashLevel: 18.5, status: 'Low-Cash', branchId: 1},
    {id: 2, serialNumber: 'RX-1002', model: 'Sentinel-V2', cashLevel: 76.0, status: 'Maintenance', branchId: 1},
    {id: 3, serialNumber: 'AD-2050', model: 'SkyHawk-Drone', cashLevel: 9.0, status: 'Low-Cash', branchId: 2},
    {id: 4, serialNumber: 'RX-1003', model: 'Sentinel-v2', cashLevel: 42.0, status: 'Maintenance', branchId: 1},

];
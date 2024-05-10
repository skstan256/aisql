-- Insert data into VendingItem table
INSERT INTO VendingItem (Name, IsGlutenFree, IsLowDairy, IsNutFree, IsSoyFree) 
VALUES 
('Chips', 1, 0, 1, 1),
('Granola Bar', 1, 1, 1, 1),
('Peanuts', 1, 1, 0, 1),
('Chocolate Bar', 0, 0, 1, 1),
('Popcorn', 1, 1, 1, 1);

-- Insert data into VendingMachineLocation table
INSERT INTO VendingMachineLocation (Room, Building) 
VALUES 
('3202', 'WSC'),
('Cougar Den', 'WSC'),
('110', 'MARB'),
('030', 'JFSB');

-- Insert data into VendingItemLocation table
INSERT INTO VendingItemLocation (ItemID, LocationID) 
VALUES 
(1, 1),
(1, 3),
(1, 4),
(2, 2),
(2, 3),
(3, 1),
(3, 3),
(4, 2),
(4, 3),
(4, 4),
(5, 1),
(5, 2),
(5, 3);
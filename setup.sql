CREATE TABLE VendingItem (
  ID INTEGER PRIMARY KEY,
  Name TEXT,
  IsGlutenFree INTEGER,
  IsLowDairy INTEGER,
  IsNutFree INTEGER,
  IsSoyFree INTEGER
);

CREATE TABLE VendingMachineLocation (
  ID INTEGER PRIMARY KEY,
  Room TEXT,
  Building TEXT
);

CREATE TABLE VendingItemLocation (
  ItemID INTEGER,
  LocationID INTEGER,
  PRIMARY KEY (ItemID, LocationID),
  FOREIGN KEY (ItemID) REFERENCES VendingItem (ID),
  FOREIGN KEY (LocationID) REFERENCES VendingMachineLocation (ID)
);

CREATE TABLE Item (
  ID INTEGER PRIMARY KEY,
  Name TEXT,
  IsGlutenFree INTEGER,
  IsLowDairy INTEGER,
  IsNutFree INTEGER,
  IsSoyFree INTEGER
);

CREATE TABLE Location (
  ID INTEGER PRIMARY KEY,
  Name TEXT,
  Building TEXT
);

CREATE TABLE ItemLocation (
  ItemID INTEGER,
  LocationID INTEGER,
  PRIMARY KEY (ItemID, LocationID),
  FOREIGN KEY (ItemID) REFERENCES Item (ID),
  FOREIGN KEY (LocationID) REFERENCES Location (ID)
);
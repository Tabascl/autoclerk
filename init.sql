CREATE TABLE "Product" (
	"Product_Id"	INTEGER NOT NULL UNIQUE,
	"EAN"	TEXT NOT NULL UNIQUE,
	"Name"	TEXT,
	PRIMARY KEY("Product_Id" AUTOINCREMENT)
);

CREATE TABLE "Shop" (
	"Shop_Id"	INTEGER NOT NULL UNIQUE,
	"Name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("Shop_Id" AUTOINCREMENT)
);

CREATE TABLE "asks" (
	"Product_Id"	INTEGER NOT NULL,
	"Shop_Id"	INTEGER NOT NULL,
	"Price"	REAL NOT NULL,
	"Time"	INTEGER NOT NULL,
	PRIMARY KEY("Product_Id","Shop_Id", "Time"),
	FOREIGN KEY("Shop_Id") REFERENCES "Shop"("Shop_Id"),
	FOREIGN KEY("Product_Id") REFERENCES "Product"("Product_Id")
);

CREATE TABLE "sells" (
	"Product_Id"	INTEGER NOT NULL,
	"Shop_Id"	INTEGER NOT NULL,
	"Availability"	TEXT NOT NULL,
	"Link"	TEXT NOT NULL,
	PRIMARY KEY("Product_Id","Shop_Id"),
	FOREIGN KEY("Shop_Id") REFERENCES "Shop"("Shop_Id"),
	FOREIGN KEY("Product_Id") REFERENCES "Product"("Product_Id")
);

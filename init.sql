CREATE TABLE "product" (
	"ean"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"availability"	TEXT NOT NULL,
	PRIMARY KEY("ean")
);

CREATE TABLE "pricepoint" (
	"id"	INTEGER NOT NULL UNIQUE,
	"time"	INTEGER NOT NULL,
	"product_ean"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("product_ean") REFERENCES "product"("ean")
);

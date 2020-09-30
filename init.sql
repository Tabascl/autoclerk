CREATE TABLE "product" (
	"ean"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"availability"	TEXT NOT NULL,
	"product_link" TEXT,
	PRIMARY KEY("ean")
);

CREATE TABLE "pricepoint" (
	"time"	INTEGER NOT NULL,
	"product_ean"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	PRIMARY KEY("time","product_ean"),
	FOREIGN KEY("product_ean") REFERENCES "product"("ean")
);

CREATE TABLE IF NOT EXISTS Users (
    id      INTEGER NOT NULL PRIMARY KEY,
    name    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Listings (
    url             TEXT NOT NULL PRIMARY KEY,
    community       TEXT,
    address         TEXT,
    zip_code        TEXT,
    latitude        REAL,
    longitude       REAL,
    lot_size        TEXT,
    property_type   TEXT
);

CREATE TABLE IF NOT EXISTS ResidentialDetails (
    url             TEXT NOT NULL,
    square_feet     INTEGER,
    style           TEXT,
    stories         INTEGER,
    beds            INTEGER,
    baths           REAL,
    year_built      INTEGER,
    FOREIGN KEY(url) REFERENCES Listings(url)
);


CREATE TABLE IF NOT EXISTS Offers (
    url         TEXT NOT NULL,
    lookup_date TEXT NOT NULL,
    price       INTEGER,
    FOREIGN KEY(url) REFERENCES Listings(url),
    PRIMARY KEY(url, lookup_date)
);

CREATE TABLE IF NOT EXISTS ListingUserRelation (
    url                 TEXT NOT NULL, 
    user                INTEGER NOT NULL,
    submitted_datetime  TEXT,
    FOREIGN KEY(url) REFERENCES Listings(url),
    FOREIGN KEY(user) REFERENCES Users(id),
    PRIMARY KEY(url, user)
);

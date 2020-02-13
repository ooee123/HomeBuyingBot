CREATE TABLE IF NOT EXISTS Users (
    id      INTEGER PRIMARY KEY,
    name    TEXT NON NULL
);

CREATE TABLE IF NOT EXISTS Listings (
    url TEXT PRIMARY KEY,
    homeMainStats   BLOB,
    price INTEGER
);

CREATE TABLE IF NOT EXISTS ListingUserRelation (
    url             TEXT, 
    user            INTEGER,
    submitted_date  TEXT,
    FOREIGN KEY(url) REFERENCES Listings(url),
    FOREIGN KEY(user) REFERENCES Users(id),
    PRIMARY KEY(url, user)
);

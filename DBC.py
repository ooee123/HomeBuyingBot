import sqlite3

class DBC:

    def __init__(self, chatroom):
        self.chatroom = chatroom
        self.dbc = sqlite3.connect('HomeBuying.{}.db'.format(chatroom), check_same_thread=False)
        #self.dbc.row_factory = sqlite3.Row
        cursor = self.dbc.cursor()
        cursor.executescript(open('sdl.sql', 'r').read())
        self.dbc.commit()

    def addUser(self, user):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO Users VALUES (:id, :name) ON CONFLICT DO NOTHING", {"id": user.id, "name": user.first_name})
        self.dbc.commit()

    def addListing(self, url, community=None, address=None, zipCode=None, latitude=None, longitude=None, lotSize=None, propertyType=None):
        cursor = self.dbc.cursor()
        cursor.execute("""
        INSERT INTO Listings VALUES (:url, :community, :address, :zip_code, :latitude, :longitude, :lot_size, :property_type)
        ON CONFLICT DO NOTHING""", {"url": url, "community": community, "address": address, "zip_code": zipCode, "latitude": latitude, "longitude": longitude, "lot_size": lotSize, "property_type": propertyType}) 
        self.dbc.commit()

    def addResidentialDetails(self, url, squareFeet=None, style=None, stories=None, beds=None, baths=None, yearBuilt=None):
        cursor = self.dbc.cursor()
        cursor.execute("""
        INSERT INTO ResidentialDetails VALUES (:url, :square_feet, :style, :stories, :beds, :baths, :year_built) ON CONFLICT DO NOTHING""", {"url": url, "square_feet": squareFeet, "style": style, "stories": stories, "beds": beds, "baths": baths, "year_built": yearBuilt})
        self.dbc.commit()

    def addListingUserRelation(self, user, url):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO ListingUserRelation VALUES (:url, :user, datetime('now', 'localtime')) ON CONFLICT DO NOTHING", {"url": url, "user": user.id})
        self.dbc.commit()

    def addOffer(self, url, price=None):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO Prices VALUES (:url, date('now', 'localtime'), :price) ON CONFLICT DO NOTHING", {"url": url, "price": price})
        self.dbc.commit()

    def getListingsPerUser(self):
        cursor = self.dbc.cursor()
        cursor.execute("SELECT name, COUNT(*) AS Count FROM ListingUserRelation r, Users u WHERE r.user = u.id GROUP BY user ORDER BY COUNT DESC")
        return cursor.fetchall()

    def getListings(self, user):
        cursor = self.dbc.cursor()
        cursor.execute("SELECT * FROM Listings WHERE user = :user", {"user": user.id})
        return cursor.fetchall()

    def getFavoriteCommunity(self, user):
        cursor = self.dbc.cursor()
        cursor.execute("""
        SELECT l.community, COUNT(*) as Count
        FROM Listings l, Users u, ListingUserRelation lu
        WHERE u.id = lu.user AND lu.url = l.url AND u.id = :user AND l.community NOT NULL
        GROUP BY l.community
        """, {"user": user.id})
        return cursor.fetchall()

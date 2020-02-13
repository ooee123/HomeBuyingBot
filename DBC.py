import sqlite3

class DBC:

    def __init__(self, chatroom):
        self.chatroom = chatroom
        self.dbc = sqlite3.connect('HomeBuying.{}.db'.format(chatroom), check_same_thread=False)
        cursor = self.dbc.cursor()
        cursor.executescript(open('sdl.sql', 'r').read())
        self.dbc.commit()

    def addUser(self, user):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO Users VALUES (:id, :name) ON CONFLICT DO NOTHING", {"id": user.id, "name": user.first_name})
        self.dbc.commit()

    def addListing(self, url, homeMainStats, price):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO Listings VALUES (:url, :homeMainStats, :price) ON CONFLICT DO NOTHING", {"url": url, "homeMainStats": homeMainStats, "price": price})
        self.dbc.commit()

    def addListingUserRelation(self, user, url):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO ListingUserRelation VALUES (:url, :user, datetime('now', 'localtime')) ON CONFLICT DO NOTHING", {"url": url, "user": user.id})
        self.dbc.commit()

    def getListings(self, user):
        cursor = self.dbc.cursor()
        cursor.execute("SELECT * FROM Listings WHERE user = :user", {"user": user.id})
        return cursor.fetchall()

import time
import datetime
import statistics
import collections
import urllib.request
import lxml.html
import json
import sqlite3

#from plot import plot

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

class HomeBuyingBot:

    def __init__(self, token, chatroom, config):
        self.chatroom = chatroom
        self.dbc = sqlite3.connect('HomeBuying.{}.db'.format(chatroom), check_same_thread=False)
        cursor = self.dbc.cursor()
        cursor.executescript(open('sdl.sql', 'r').read())
        self.dbc.commit()

    def url(self, bot, update):
        user_id = update.message.from_user.id
        name = update.message.from_user.name
        url = self.getUrl(update)
        self.addUser(bot, update)
        self.addListing(url)
        self.addListingUserRelation(user_id, url)
        return
        doc = self.getXmlDocument(url)
        elements = doc.xpath("//div[contains(@class, 'HomeMainStats')]")[0].find('script')
        homeMainStats = json.loads((elements.text))
        print(homeMainStats['name'])
        print(homeMainStats['offers']['price'])
        print(homeMainStats['offers']['url'])

    def addUser(self, bot, update):
        user = update.message.from_user
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO Users VALUES (:id, :name) ON CONFLICT DO NOTHING", {"id": user.id, "name": user.first_name})
        self.dbc.commit()

    def addListing(self, url):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO Listings VALUES (:url, :price) ON CONFLICT DO NOTHING", {"url": url, "price": 0})
        self.dbc.commit()

    def addListingUserRelation(self, user_id, url):
        cursor = self.dbc.cursor()
        cursor.execute("INSERT INTO ListingUserRelation VALUES (:url, :user, datetime('now')) ON CONFLICT DO NOTHING", {"url": url, "user": user_id})
        self.dbc.commit()

    def getListings(self, user_id):
        cursor = self.dbc.cursor()
        cursor.execute("SELECT * FROM Listings WHERE user = :user", {"user": user_id})
        return cursor.fetchall()

    def getUrl(self, update):
        urlEntities = [entity for entity in update['message']['entities'] if entity['type'] == 'url'][0]
        url = update['message']['text'][urlEntities['offset']:(urlEntities['offset']+urlEntities['length'])]
        idx = url.find('?')
        if (idx > 0):
            return url[:url.find('?')]
        else:
            return url

    def getXmlDocument(self, url):
        request = urllib.request.Request(url, headers=USER_AGENT)
        contents = urllib.request.urlopen(request).read().decode('utf-8', 'ignore')
        return lxml.html.document_fromstring(contents)

    def morningGraph(self, bot, update, args={}):
        days = 30
        if args:
            try:
                days = int(args[0])
            except TypeError:
                pass 
        senderId = update.message.from_user.id 
        if senderId in self.users:
            senderName = self.users[senderId].getName()
            saveas = senderName + ".png"
            firstMorningPerDay = self.users[senderId].getFirstMorningPerDay(days)
            if senderId in self.earliestMornings:
                earliestMornings = self.earliestMornings[senderId]
                earliestMornings = [x for x in earliestMornings if x in firstMorningPerDay]
            else:
                earliestMornings = None
            plot.plotFirstMorningPerDay(firstMorningPerDay, saveas, senderName, earliestMornings)
            bot.send_photo(chat_id=self.chatroom, photo=open(saveas, "rb"))

    def morningGraphAll(self, bot, _):
        saveas = "everyone.png"
        plot.plotFirstMorningPerDayAll(self.users, saveas, "Everyone's Mornings")
        bot.send_photo(chat_id=self.chatroom, photo=open(saveas, "rb"))

    def downloadMornings(self, bot, update, args={}):
        senderId = update.message.from_user.id 
        if senderId in self.users:
            senderName = self.users[senderId].getName()
            saveas = senderName + ".txt"
            firstMorningPerDay = self.users[senderId].getFirstMorningPerDay()
            times = "\n".join([str(x) for x in firstMorningPerDay])
            f = open(saveas, "w")
            f.write(times)
            f.close()
            f = open(saveas, "rb")
            
            today = time.strftime("%Y-%m-%d")
            
            bot.send_document(chat_id=self.chatroom, document=f, filename=senderName + "." + today + ".txt")

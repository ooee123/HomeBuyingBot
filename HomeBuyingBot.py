import time
import datetime
import statistics
import collections
import urllib.request
import lxml.html
from Redfin import RedfinExtractor
from DBC import DBC

#from plot import plot

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

class HomeBuyingBot:

    def __init__(self, token, chatroom):
        self.chatroom = chatroom
        self.dbc = DBC(chatroom)

    def url(self, bot, update):
        url = self.getUrl(update)
        if not self.isRedfinUrl(url):
            return
        user = update.message.from_user
        name = user.name
        self.dbc.addUser(user)
        doc = self.getXmlDocument(url)
        extractor = RedfinExtractor(doc)
        self.saveListing(url, extractor)
        self.dbc.addListingUserRelation(user, url)

    def saveListing(self, url, extractor):
        self.dbc.addListing(url, extractor.getCommunity(), extractor.getAddress(), extractor.getZipCode(), extractor.getLatitude(), extractor.getLongitude(), extractor.getLotSize(), extractor.getPropertyType())
        if extractor.getPropertyType() == 'Residential':
            self.dbc.addResidentialDetails(url, extractor.getSquareFeet(), extractor.getStyle(), extractor.getStories(), extractor.getBeds(), extractor.getBaths(), extractor.getYearBuilt())

    def getUrl(self, update):
        urlEntities = [entity for entity in update['message']['entities'] if entity['type'] == 'url'][0]
        url = update['message']['text'][urlEntities['offset']:(urlEntities['offset']+urlEntities['length'])]
        idx = url.find('?')
        if (idx > 0):
            return url[:url.find('?')]
        else:
            return url

    def isRedfinUrl(self, url):
        return url.startswith("https://www.redfin.com")

    def getXmlDocument(self, url):
        request = urllib.request.Request(url, headers=USER_AGENT)
        contents = urllib.request.urlopen(request).read().decode('utf-8', 'ignore')
        #contents = open('contents', 'r').read()
        return lxml.html.document_fromstring(contents)

    def getLeaderboard(self, bot, update):
        listingsPerUser = self.dbc.getListingsPerUser()
        bot.sendMessage(self.chatroom, '<pre>{}</pre>'.format(str(listingsPerUser)), parse_mode='HTML')

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

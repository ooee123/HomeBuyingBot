import lxml.html
import re
import json

class RedfinExtractor:

    def __init__(self, doc):
        self.doc = doc
        self.factsTable = self.__extractFactsTable()
        self.keyDetails = self.__extractKeyDetails()
        self.homeMainStats = self.__extractHomeMainStats()
        self.homeMainStatsJson = self.__extractHomeMainStatsJson()

    def __extractFactsTable(self):
        factsTableXml = self.doc.xpath("//div[contains(@class, 'facts-table')]")[0]
        factsTable = {}
        for tableRow in factsTableXml:
            factsTable[tableRow[0].text] = tableRow[1].text
        return factsTable

    def __extractKeyDetails(self):
        keyDetailsListXml = self.doc.xpath("//div[contains(@class, 'keyDetailsList')]")[0]
        keyDetails = {}
        for keyDetail in keyDetailsListXml:
            keyDetails[keyDetail[0].text] = keyDetail[1].text
        return keyDetails

    def __extractHomeMainStatsJson(self):
        return json.loads(self.doc.xpath("//div[contains(@class, 'HomeMainStats')]")[0].find('script').text)

    def __extractHomeMainStats(self):
        divs = self.doc.xpath("//div[contains(@class, 'HomeMainStats')]")[0].findall('div')
        homeMainStats = {}
        for div in divs:
            label = self.getAllText(div.xpath('.//*[@class="statsLabel"]')[0])
            value = self.convertToNumber(self.getAllText(div.xpath('.//*[@class="statsValue"]')[0]))
            if 'sqft' in div.get('class'):
                label = 'squareFeet'
            homeMainStats[label] = value
        return homeMainStats

    def getCommunity(self):
        return self.keyDetails['Community']

    def getAddress(self):
        return self.homeMainStatsJson['name']

    def getZipCode(self):
        return self.homeMainStatsJson['address']['postalCode']

    def getLatitude(self):
        return self.homeMainStatsJson['geo']['latitude']

    def getLongitude(self):
        return self.homeMainStatsJson['geo']['longitude']

    def getLotSize(self):
        return self.keyDetails['Lot Size']

    def getPropertyType(self):
        return self.keyDetails['Property Type']

    def getSquareFeet(self):
        return self.homeMainStats['squareFeet']

    def getStyle(self):
        return self.factsTable['Style']

    def getStories(self):
        return self.factsTable['Stories']

    def getBeds(self):
        return self.factsTable['Beds']

    def getBaths(self):
        return self.factsTable['Baths']

    def getYearBuilt(self):
        return self.factsTable['Year Built']

    def getOffer(self):
        return

    def getAllText(self, element):
        text = ""
        for elem in element.iter():
            if elem.text != None:
                text = text + elem.text
        if text == "":
            return None
        return text

    def convertToNumber(self, value):
        value = re.sub("[^0-9\.]", "", value)
        if value == "":
            return None
        return value

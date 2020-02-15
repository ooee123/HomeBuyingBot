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
        self.topStats = self.__extractTopStats()

    def __extractFactsTable(self):
        factsTable = {}
        try:
            factsTableXml = self.doc.xpath("//div[contains(@class, 'facts-table')]")[0]
            for tableRow in factsTableXml:
                try:
                    key = tableRow[0].text
                    value = tableRow[1].text
                    if key == 'Lot Size':
                        value = self.convertToNumber(value.split()[0])
                    factsTable[key] = value
                except:
                    pass
        except:
            pass
        return factsTable

    def __extractKeyDetails(self):
        keyDetails = {}
        try:
            keyDetailsListXml = self.doc.xpath("//div[contains(@class, 'keyDetailsList')]")[0]
            for keyDetail in keyDetailsListXml:
                try:
                    key = keyDetail[0].text
                    value = keyDetail[1].text
                    if key == 'Lot Size':
                        value = self.convertToNumber(value.split()[0])
                    keyDetails[key] = value
                except:
                    pass
        except:
            pass
        return keyDetails

    def __extractHomeMainStatsJson(self):
        try:
            return json.loads(self.doc.xpath("//div[contains(@class, 'HomeMainStats')]")[0].find('script').text)
        except:
            return {}

    def __extractHomeMainStats(self):
        homeMainStats = {}
        try:
            divs = self.doc.xpath("//div[contains(@class, 'HomeMainStats')]")[0].findall('div')
            for div in divs:
                try:
                    label = self.getAllText(div.xpath('.//*[@class="statsLabel"]')[0])
                    value = self.convertToNumber(self.getAllText(div.xpath('.//*[@class="statsValue"]')[0]))
                    if 'sqft' in div.get('class'):
                        label = 'squareFeet'
                    homeMainStats[label] = value
                except:
                    pass
        except:
            pass
        return homeMainStats

    def __extractTopStats(self):
        try:
            return json.loads(self.doc.xpath('//div[contains(@class, "top-stats")]')[0].find('script').text)
        except:
            return {}

    def getCommunity(self):
        return self.keyDetails.get('Community')

    def getAddress(self):
        return self.topStats.get('address', {}).get('streetAddress')

    def getZipCode(self):
        return self.topStats.get('address', {}).get('postalCode')

    def getLatitude(self):
        return self.topStats.get('geo', {}).get('latitude')

    def getLongitude(self):
        return self.topStats.get('geo', {}).get('longitude')

    def getLotSize(self):
        return self.convertToNumber(self.factsTable.get('Lot Size'))

    def getPropertyType(self):
        return self.keyDetails.get('Property Type')

    def getSquareFeet(self):
        return self.convertToNumber(self.homeMainStats.get('squareFeet'))

    def getStyle(self):
        return self.factsTable.get('Style')

    def getStories(self):
        return self.convertToNumber(self.factsTable.get('Stories'))

    def getBeds(self):
        return self.convertToNumber(self.factsTable.get('Beds'))

    def getBaths(self):
        return self.convertToNumber(self.factsTable.get('Baths'))

    def getYearBuilt(self):
        return self.convertToNumber(self.factsTable.get('Year Built'))

    def getPrice(self):
        return self.homeMainStatsJson.get('offers', {}).get('price')

    def getAllText(self, element):
        text = ""
        for elem in element.iter():
            if elem.text != None:
                text = text + elem.text
        if text == "":
            return None
        return text

    def convertToNumber(self, value):
        if value is None:
            return None
        value = re.sub("[^0-9\.]", "", value)
        if value == "":
            return None
        return value

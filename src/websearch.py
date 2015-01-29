import json
import urllib, urllib2
import util

from googleasbrowser import search

class GoogleQuery:
    def __init__(self):
        self.__baseUrl = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0"
        self.numResults = 1
        self.restrictSite = "wikipedia.org"
        self.asBrowser = False

    def queryText(self, queryString):
        if (self.asBrowser):
            return self.queryAsBrowser(queryString)
        urls = []
        try:
            response = urllib.urlopen(self.__buildUrl(queryString))
            results = response.read()
            jsonData = json.loads(results)
            data = jsonData['responseData']

            #if data is None:
            #e    return []

            hits = data['results']
            for h in hits:
                urls.append(h['url'])
        except Exception, e:
            print "Invalid response from Google. Must wait ?  (%s)" % str(e)
            raise

        return urls
    
    def queryAsBrowser(self, queryString):
        urls = []
        qstring = queryString
        if not self.restrictSite is None or self.restrictSite != "":
            qstring = qstring + " site:" + self.restrictSite
        print "google as browser:", qstring
        for res in search(qstring, stop=10):
            urls.append(res)
        return urls
        
    def __buildUrl(self, queryString):
        queryString = unicode(queryString).encode('utf-8')
        query = urllib.urlencode({'q': queryString})
        site = ""
        if not self.restrictSite is None or self.restrictSite != "":
            site = "site:" + self.restrictSite

        return self.__baseUrl + "&hl=en&rsz=%d&%s %s" % (self.numResults, query, site)



class BingQuery:
    def __init__(self):
        self.__baseUrl = "https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?"
        self.numResults = 1
        self.restrictSite = "wikipedia.org"
        self.key = "" # Get your own key https://datamarket.azure.com/account/keys
        self.key = self.__readKey()
        if self.key == "":
            raise Exception("Join the dark side, get your key from https://datamarket.azure.com/account/keys")

    def queryText(self, queryString):
        urls = []

        credentials = (':%s' % self.key).encode('base64')[:-1] # Microsoft hardened security
        auth = 'Basic %s' % credentials

        try:
            request = urllib2.Request(self.__buildUrl(queryString))
            request.add_header('Authorization', auth)

            requestOpener = urllib2.build_opener()
            response = requestOpener.open(request)
            responseData = response.read()
            jsonData = json.loads(responseData)

            hits = jsonData['d']['results']
            for h in hits:
                urls.append(h['Url'])

        except Exception, e:
            print "Invalid response from Bing. Must wait ? (%s)" % str(e)
            raise

        return urls

    def __buildUrl(self, queryString):
        site = ""
        if not self.restrictSite is None or self.restrictSite != "":
            site = " site:" + self.restrictSite

        query = "%s%s" % (queryString, site)
        query = unicode(query).encode('utf-8')
        query = urllib.quote(query)
        url = self.__baseUrl + "Query=%27" + query + "%27&$top=" + str(self.numResults) + "&$format=json"
        return url

    def __readKey(self):
        with open("bing.key", 'r') as f:
            return f.read()

if __name__ == "__main__":
    q = BingQuery()
    print q.queryText("FlakPanzer V Coelian")
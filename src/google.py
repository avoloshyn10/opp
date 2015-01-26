import json
import urllib
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
            hits = data['results']
            for h in hits:
                urls.append(h['url'])
        except Exception, e:
            print "Invalid response from Google must wait ?"
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

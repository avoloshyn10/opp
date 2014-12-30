import textwrap
from urllib import quote, unquote

def unitNameToRegex(n):
	s = n.replace(" ", ".*?")
	s = s.replace("(", "\\\(")
	s = s.replace(")", "\\\)")
	return s

def wikiToDBpedia(url):
    token = "wiki/"
    p = url.find(token)
    p += len(token)
    page = url[p:]
    return "http://dbpedia.org/resource/%s" % page

def unquoteUrl(url):
    s = unquote(url.encode('utf-8')) # unquote spaces and other ascii special chars
    return unquote(s) # convert from utf8 %FF notation to \xff python notation

def dumpCommonData(data):
    width = 120
    print " ".rjust(width, "-")
    print data[0]["label"]["value"]
    print data[0]["thumbnail"]["value"]
    print "\n"
    print textwrap.fill(data[0]["abstract"]["value"], 120)
    print "\n"
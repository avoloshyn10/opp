
def unitNameToRegex(n):
	s = n.replace(" ", ".*?")
	s = s.replace("(", "\\\(")
	s = s.replace(")", "\\\)")
	return s


def wikiToDBpedia(s):
    token = "wiki/"
    p = s.find(token)
    p += len(token)
    page = s[p:]
    return "http://dbpedia.org/page/%s" % page

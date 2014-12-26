
def unitNameToRegex(n):
	s = n.replace(" ", ".*?")
	s = s.replace("(", "\\\(")
	s = s.replace(")", "\\\)")
	return s

from constant import *

def ft_input_word(pos, neg):
	if pos is None or neg is None:
		return ERROR, "", ""
	poslen = len(pos)
	neglen = len(neg)
	if ((0 < poslen < 30) and (0 < neglen < 30)) is False:
		return ERROR, "長すぎます", ""
	return SUCCESS, pos, neg

def ft_input_doc(doc):
	if doc is None:
		return ERROR, ""
	strlen = len(doc)
	if (0 < strlen < 1000) is False:
		return ERROR, "長すぎます"
	return SUCCESS, doc
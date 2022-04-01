from gensim.models import KeyedVectors
import make_model
import re
import math

def ft_tuple_to_list(l_ans):
	for i in range(len(l_ans)):
		l_ans[i] = list(l_ans[i])
	return l_ans

def ft_make_top3(l_ans):
	l_name = []
	l_prob = []
	for i in range(len(l_ans)):
		if i == 3:
			break
		l_name.append(l_ans[i][0])
		l_prob.append(math.floor(100 * l_ans[i][1]))
	return l_name, l_prob

def ft_calc_word(pos_str, neg_str):
	l_name = []
	l_prob = []
	try:
		wv = KeyedVectors.load('model/500m_model.vec.kv', mmap='r')
		pos = make_model.ft_input_text_modifier(pos_str)
		neg = make_model.ft_input_text_modifier(neg_str)
		l_ans = wv.most_similar(positive=pos, negative=neg)
		l_ans = ft_tuple_to_list(l_ans)
		l_name, l_prob = ft_make_top3(l_ans)
	except:
		return "", "", True
	return l_name, l_prob, False

def ft_calc_doc(str):
	model, documents = make_model.ft_make_model()
	words = make_model.ft_input_text_modifier(str)
	infer_vector = model.infer_vector(words, epochs=20)
	match = model.dv.most_similar(infer_vector, topn = 1)
	num = int(re.sub(r"\D", "", match[0][0]))
	match_doc = documents[num][0]
	match_prob = match[0][1]
	return match_doc, match_prob

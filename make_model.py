#coding:utf-8
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import re
import string
import unicodedata
import MeCab

mecab = MeCab.Tagger("-Owakati")

def ft_create_doc2vec(l_words, name):
	documents = []
	index = 0
	for words in l_words:
		index += 1
		document = TaggedDocument(words = words, tags = [f"doc{index}"])
		documents.append(document)
	model = Doc2Vec(documents = documents, min_count = 2, epochs = 20)
	model.save(name)
	return model

def ft_preprocess(text):
	text = ' '.join(text.splitlines())
	text = re.sub(r'[0-9]+', "", text)
	text = unicodedata.normalize("NFKC", text).translate(
	str.maketrans("", "", string.punctuation + "◯ 〇【】『』'「」、。・"))
	text = text.replace(" ", "")
	words = mecab.parse(text).split()
	return words

def ft_delete_words(words):
    words = [w for w in words if re.compile('[\u3041-\u309F]').fullmatch(w) == None]
    words = [w for w in words if not(w in ["月","日"])]
    return words

# for input text
def ft_input_text_modifier(text):
	words = ft_preprocess(text)
	words = ft_delete_words(words)
	return words

def ft_modify_text(training_data):
	l_words = []
	for line in training_data:
		words = ft_preprocess(line.rstrip())
		words = ft_delete_words(words)
		l_words.append(words)
	return l_words

def ft_make_documents(training_data):
	documents = []
	i = 0
	for line in training_data:
		documents.append([f"{line}", f"{i}"])
		i += 1
	return documents


def ft_strjoin(training_data):
	index = 0
	for i in range(len(training_data)):
		if training_data[i] == "\n":
			for j in range(i - index - 1):
				training_data[index] = training_data[index] + training_data[index + 1]
			training_data[index + 1] = ""
			index = i + 1
			continue
	return training_data


def ft_make_model():
	FILE = open('utils/training_data/es1000.txt', 'r')
	training_data = FILE.readlines()
	training_data = ft_strjoin(training_data)
	documents = ft_make_documents(training_data)
	l_words = ft_modify_text(training_data)
	model = ft_create_doc2vec(l_words, "./model/onecareer.model")
	FILE.close()
	return model, documents

ft_make_model()

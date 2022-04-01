from gensim.models import word2vec

model = word2vec.KeyedVectors.load_word2vec_format("../model/model.vec")
model.save('../model/500m_model.vec.kv')
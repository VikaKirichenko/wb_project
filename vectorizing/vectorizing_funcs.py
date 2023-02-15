import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import wget
import zipfile
from gensim.test.utils import datapath
from zipfile import ZipFile
import gensim
from gensim.models import word2vec


# df = pd.read_csv("../data/products.csv")
# countvect
# tf-idfvect
# word2vec (предобуч + дообуч)
# fasttext (предобуч + дообуч)
# glove
# elmo?
# doc2vec
# samples2vec
# BERT!

def check_sim_quality(model):
    wget.download('https://rusvectores.org/static/testsets/ru_simlex999_tagged.tsv')
    # ru_simlex = pd.read_csv('ru_simlex999_tagged.tsv', sep='\t')
    # see correlation or what?
    res = model.evaluate_word_pairs('ru_simlex999_tagged.tsv')
    # res[0] - accuracy? no, correlation?
    return res


def check_analog_quality(model):
    wget.download('https://rusvectores.org/static/testsets/ru_analogy_tagged.txt')
    res = model.evaluate_word_analogies('ru_analogy_tagged.txt')
    # accuracy score
    # res[0]
    return res[0]


def get_bow_vector(data_samples: list, ngram_range: tuple = (1, 1), n_features: int = 1000):
    vectorizer = CountVectorizer(max_features=n_features, ngram_range=ngram_range)
    x_vector = vectorizer.fit_transform(data_samples)
    return x_vector, vectorizer


def get_tfidf_vector(data_samples: list, ngram_range: tuple = (1, 1), n_features: int = 1000):
    vectorizer = TfidfVectorizer(max_features=n_features, ngram_range=ngram_range)
    x_vector = vectorizer.fit_transform(data_samples)
    return x_vector, vectorizer


def load_model():
    model_url = 'http://vectors.nlpl.eu/repository/20/180.zip'
    m = wget.download(model_url)
    model_file = model_url.split('/')[-1]
    with ZipFile(model_file, 'r') as zObject:
        zObject.extractall(
            path="temp/")
    word2vec_path = 'temp/model.bin'
    w2v_model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True)
    return w2v_model


# сделать 3 функции?:
# 1) качаем модель с rusvectores, готово
# 2) качаем модель с rusvectores + дообучаем на наших данных
# 3) обучаем только на наших данных
# get model from rusvectores (НКРЯ?)
# add our words to improve model
def get_pretrained_word2vec_vector():
    model = load_model()
    return model


# data - токенезированный, лемматизированный список текстов, подается в виде токенов!
def get_retrained_word2vec_vector(data):
    model = load_model()
    #
    model_path = "pretrained.model"
    model.save(model_path)

    model = word2vec.Word2Vec.load(model_path)

    model.build_vocab(data, update=True)
    model.train(data, total_examples=model.corpus_count, epochs=5)

    return model


# data - токенезированный, лемматизированный список текстов, подается в виде токенов!
def get_trained_word2vec_vector(data, workers=4, size=300, min_count=10, window=10, sample=1e-3):
    model_en = word2vec.Word2Vec(data, workers=workers, size=size, min_count=min_count, window=window, sample=sample)
    return model_en


def get_fasttext_vector():
    pass


# def get_glove_vector():
#     pass


# def get_doc2vec_vector():
#     pass


# def get_samples2vec_vector():
#     pass


# def get_elmo_vector():
#     pass


def get_bert_vector():
    pass

import spacy
import pandas as pd
import numpy as np
import nltk
import re
import ssl
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from keras.models import Sequential
from keras.layers import Dense
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, make_scorer
from sklearn.preprocessing import normalize

nlp = spacy.load('en_core_web_sm')

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('wordnet')
nltk.download('stopwords')
lst_stopwords = nltk.corpus.stopwords.words("english")


def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text

def get_spacy_vector(text,pre_proc=False):
    doc = nlp(text)
    return doc.vector

def get_pos_vector(text,pre_proc=False):
    pos_feature_dict = {'ADJ':0, 'SPACE':0, 'ADV':0, 'INTJ':0, 'SYM':0, 'VERB':0, 'SCONJ':0, 'PART':0, 'X':0, 'PUNCT':0, 'AUX':0, 'ADP':0, 'NUM':0, 'PRON':0, 'NOUN':0, 'DET':0, 'CCONJ':0, 'PROPN':0}
    if pre_proc:
        text = utils_preprocess_text(text, lst_stopwords=lst_stopwords)
    doc = nlp(text)
    for token in doc:
        pos = token.pos_
        if pos in pos_feature_dict:
            pos_feature_dict[pos] += 1
        else:
            pos_feature_dict[pos] = 1
    vals_list = []
    for k in list(pos_feature_dict.keys()):
        vals_list.append(pos_feature_dict[k])
    return vals_list

def get_tag_vector(text, pre_proc=False):
    pos_feature_dict = {'VBP':0, 'RBS':0, 'VBZ':0, 'WRB':0, 'VB':0, 'NNS':0, 'WDT':0, 'UH':0, '-RRB-':0, 'AFX':0, 'CC':0, 'WP':0, 'VBN':0, 'IN':0, 'PRP$':0, 'XX':0, 'WP$':0, 'RBR':0, 'PDT':0, 'HYPH':0, 'POS':0, '$':0, 'NNPS':0, 'MD':0, '.':0, 'VBD':0, 'JJR':0, 'NFP':0, ',':0, 'JJS':0, 'DT':0, '_SP':0, 'VBG':0, 'FW':0, 'RP':0, 'SYM':0, 'LS':0, 'CD':0, 'RB':0, 'EX':0, '``':0, 'PRP':0, "''":0, ':':0, 'TO':0, 'JJ':0, 'ADD':0, '-LRB-':0, 'NN':0, 'NNP':0}
    doc = nlp(text)
    for token in doc:
        pos = token.tag_
        if pos in pos_feature_dict:
            pos_feature_dict[pos] += 1
        else:
            pos_feature_dict[pos] = 1
    vals_list = []
    for k in list(pos_feature_dict.keys()):
        vals_list.append(pos_feature_dict[k])
    return vals_list

def get_tfidf(corpus):
    v = TfidfVectorizer(max_features=50)#, norm='l1')
    x = v.fit_transform(corpus)
    return pd.DataFrame(x.toarray())

def get_pos_tag_spacy_vector(text):
    pos_vector = get_pos_vector(text)
    tag_vector = get_tag_vector(text)
    spacy_vector = get_spacy_vector(text)
    pos_vector.extend(tag_vector)
    return pos_vector

def get_pos_tag_vector(text):
    pos_vector = get_pos_vector(text)
    tag_vector = get_tag_vector(text)
    pos_vector.extend(tag_vector)
    return pos_vector

def get_only_pos_vector(text):
    pos_vector = get_pos_vector(text)
    return pos_vector

def get_only_tag_vector(text):
    tag_vector = get_tag_vector(text)
    return tag_vector

def get_only_pos_vector_without_preprocessing(text):
    pos_vector = get_only_pos_vector(text)
    return pos_vector

def get_only_tag_vector_without_preprocessing(text):
    tag_vector = get_only_tag_vector(text)
    return tag_vector

def get_pos_tag_vector_without_preprocessing(text):
    pos_tag_vector = get_pos_tag_vector(text)
    return pos_tag_vector

def get_pos_tag_spacy_vector_without_preprocessing(text):
    pos_tag_spacy_vector = get_pos_tag_spacy_vector(text)
    return pos_tag_spacy_vector

def get_only_pos_vector_with_preprocessing(text):
    text = utils_preprocess_text(text, lst_stopwords=lst_stopwords)
    pos_vector = get_only_pos_vector(text)
    return pos_vector

def get_only_tag_vector_with_preprocessing(text):
    text = utils_preprocess_text(text, lst_stopwords=lst_stopwords)
    tag_vector = get_only_tag_vector(text)
    return tag_vector

def get_pos_tag_vector_with_preprocessing(text):
    text = utils_preprocess_text(text, lst_stopwords=lst_stopwords)
    pos_tag_vector = get_pos_tag_vector(text)
    return pos_tag_vector

def get_pos_tag_spacy_vector_with_preprocessing(text):
    text = utils_preprocess_text(text, lst_stopwords=lst_stopwords)
    pos_tag_spacy_vector = get_pos_tag_spacy_vector(text)
    return pos_tag_spacy_vector



def read(func, filename="train-data-prepared.json",nor=True):
    df = pd.read_json(filename)
    text_list = df['text'].to_list()
    vectors_list = [func(text) for text in text_list]
#     tf_idf_vectors = get_tfidf(text_list)
    df_vector_list = pd.DataFrame(vectors_list)
    text_id = df['id'].to_list()
    X = df_vector_list
#     X = pd.concat([df_vector_list, tf_idf_vectors], axis=1)
    X = normalize(X, axis=1, norm='l1') if nor == True else X
    y = df['label']
    return text_id, X, y

def evaluate(estimator):
    y_pred = estimator.fit(X,y).predict(X_test)
#    write_file(pd.DataFrame(y_pred))
    return f1_score(y_pred=y_pred, y_true=y_test)


# Set train and test data
func_list = [
    get_only_pos_vector_without_preprocessing,
    get_only_tag_vector_without_preprocessing,
    get_pos_tag_vector_without_preprocessing,
    get_pos_tag_spacy_vector_without_preprocessing,
    get_only_pos_vector_with_preprocessing,
    get_only_tag_vector_with_preprocessing,
    get_pos_tag_vector_with_preprocessing,
    get_pos_tag_spacy_vector_with_preprocessing,
]

normalization = [True, False]

model = {
            'SVM RBF': svm.SVC(kernel='rbf', C=10**4),
            'SVM Linear': svm.SVC(kernel='linear', C=100),
            'Perceptron': Perceptron(),
            'Logistic Regression':LogisticRegression(solver='liblinear', random_state=0),
            'KNN':KNeighborsClassifier(n_neighbors=1)
}

for func in func_list:
    for norm in normalization:
        print(func.__name__)
        print("Normalisation:",norm)
        id_train, X, y = read(func,filename="train-data-prepared.json",nor=norm)
        id_test, X_test, y_test = read(func,filename="val-data-prepared.json",nor=norm)
        id_test_df = pd.DataFrame(id_test)
        for key, value in model.items():
            print(f'{key} : {evaluate(value)}')


def write_file(y_pred):
    result = pd.concat([id_test_df, pd.DataFrame(y_pred)], axis=1)
    result.columns=['id','label']
    result.set_index('id')['label'].to_json(r'output.json')

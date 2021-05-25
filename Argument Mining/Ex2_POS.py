import spacy
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.metrics import f1_score, precision_score, recall_score, make_scorer

nlp = spacy.load('en_core_web_sm')


def get_pos_vector(text):
    pos_feature_dict = {'ADJ':0, 'SPACE':0, 'ADV':0, 'INTJ':0, 'SYM':0, 'VERB':0, 'SCONJ':0, 'PART':0, 'X':0, 'PUNCT':0, 'AUX':0, 'ADP':0, 'NUM':0, 'PRON':0, 'NOUN':0, 'DET':0, 'CCONJ':0, 'PROPN':0}
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


def get_tag_vector(text):
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

def get_pos_tag_vector(text):
    pos_vector = get_pos_vector(text)
    tag_vector = get_tag_vector(text)
    pos_vector.extend(tag_vector)
    return pos_vector

def get_set(text_list):
    s = []
    for text in text_list:
        doc = nlp(text)
        for token in doc:
            pos = token.tag_
            s.append(pos)
    s = set(s)
    print(s)
    return s

df_train = pd.read_json('train-data-prepared.json')
text_list = df_train['text'].to_list()
vectors_list = [get_pos_tag_vector(text) for text in text_list]
df_train['feature_vector'] = vectors_list

y = df_train['label']
X = np.stack(vectors_list,axis=0)

X = normalize(X, axis=1, norm='l1')
#X.shape

#LR
model = LogisticRegression(solver='liblinear', random_state=0)
model.fit(X,y)

df_test = pd.read_json('val-data-prepared.json')
text_list = df_test['text'].to_list()
vectors_list_test = [get_pos_tag_vector(text) for text in text_list]
df_test['feature_vector'] = vectors_list_test

X_test = np.stack(vectors_list_test,axis=0)
y_test = df_test['label']

#from sklearn.preprocessing import normalize
X_test = normalize(X_test, axis=1, norm='l1')

y_pred = model.predict(X_test)

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10)
scores = cross_val_score(
                estimator=model,
                X=X_test,
                y=y_test,
                cv=cv,
                scoring=make_scorer(f1_score)
            )
print("Logistic Regression")
print("F1 with cross validation:", scores.mean())
print("F1 without cross validation:", f1_score(y_true=y_test, y_pred=y_pred))

#SVM RBF
clf_rbf = svm.SVC(kernel='rbf', C=10000000000)
clf_rbf.fit(X,y)
y_pred_svm = clf_rbf.predict(X_test)

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10)
scores = cross_val_score(
                estimator=clf_rbf,
                X=X_test,
                y=y_test,
                cv=cv,
                scoring=make_scorer(f1_score)
            )
print("SVM RBF Kernel Classification")
print("F1 with cross validation:", scores.mean())
print("F1 without cross validation:", f1_score(y_true=y_test, y_pred=y_pred_svm))


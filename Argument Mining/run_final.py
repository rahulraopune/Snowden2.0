import numpy as np
import pandas as pd
import spacy
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.preprocessing import normalize

nlp = spacy.load('en_core_web_sm')

train_file = 'train-data-prepared.json'

# Change to test filename location
test_file = 'val-data-prepared.json'


def write_file(predictions, id_df):
    """Write the predictions to JSON file"""
    result = pd.concat([id_df, pd.DataFrame(predictions)], axis=1)
    result.columns = ['id', 'label']
    result.set_index('id')['label'].to_json(r'output.json')


def get_pos_vector(text):
    """Get the Parts-of-Speech feature vectors"""
    pos_feature_dict = {'ADJ': 0, 'SPACE': 0, 'ADV': 0, 'INTJ': 0, 'SYM': 0, 'VERB': 0, 'SCONJ': 0, 'PART': 0, 'X': 0,
                        'PUNCT': 0, 'AUX': 0, 'ADP': 0, 'NUM': 0, 'PRON': 0, 'NOUN': 0, 'DET': 0, 'CCONJ': 0,
                        'PROPN': 0}
    doc = nlp(text)
    for token in doc:
        pos = token.pos_
        if pos in pos_feature_dict:
            pos_feature_dict[pos] += 1
        else:
            pos_feature_dict[pos] = 1
    values_list = []
    for k in list(pos_feature_dict.keys()):
        values_list.append(pos_feature_dict[k])
    return values_list


def get_tag_vector(text):
    """Get a feature vector of parsed tree nodes."""
    pos_feature_dict = {'VBP': 0, 'RBS': 0, 'VBZ': 0, 'WRB': 0, 'VB': 0, 'NNS': 0, 'WDT': 0, 'UH': 0, '-RRB-': 0,
                        'AFX': 0, 'CC': 0, 'WP': 0, 'VBN': 0, 'IN': 0, 'PRP$': 0, 'XX': 0, 'WP$': 0, 'RBR': 0, 'PDT': 0,
                        'HYPH': 0, 'POS': 0, '$': 0, 'NNPS': 0, 'MD': 0, '.': 0, 'VBD': 0, 'JJR': 0, 'NFP': 0, ',': 0,
                        'JJS': 0, 'DT': 0, '_SP': 0, 'VBG': 0, 'FW': 0, 'RP': 0, 'SYM': 0, 'LS': 0, 'CD': 0, 'RB': 0,
                        'EX': 0, '``': 0, 'PRP': 0, "''": 0, ':': 0, 'TO': 0, 'JJ': 0, 'ADD': 0, '-LRB-': 0, 'NN': 0,
                        'NNP': 0}
    doc = nlp(text)
    for token in doc:
        pos = token.tag_
        if pos in pos_feature_dict:
            pos_feature_dict[pos] += 1
        else:
            pos_feature_dict[pos] = 1
    values_list = []
    for k in list(pos_feature_dict.keys()):
        values_list.append(pos_feature_dict[k])
    return values_list


def get_pos_tag_vector(text):
    """Get a combined feature vector of Parts-of-Speech and Tag"""
    pos_vector = get_pos_vector(text)
    tag_vector = get_tag_vector(text)
    pos_vector.extend(tag_vector)
    return pos_vector


def create_tf_idf_feature_vector(df, vectorizer, type):
    """Get tf/idf features."""
    x_train = df['text'].to_list()
    if type == 'train':
        X_train_vec = vectorizer.fit_transform(x_train)
    elif type == 'test':
        X_train_vec = vectorizer.transform(x_train)
    return X_train_vec.toarray()


def create_feature_vector(df, type, vectorizer):
    text_list = df['text'].to_list()
    vectors_list = [get_pos_tag_vector(text) for text in text_list]

    # Get tf/idf feature vector
    X_vec = create_tf_idf_feature_vector(df, vectorizer, type)

    for i in range(len(vectors_list)):
        vectors_list[i].extend(X_vec[i])

    df['feature_vector'] = vectors_list

    y = df['label']
    X = np.stack(vectors_list, axis=0)

    # Normalize the feature vector
    X = normalize(X, axis=1, norm='l1')
    return X, y, df


df_train = pd.read_json(train_file)

# Specify vectorizer
vectorizer = TfidfVectorizer()

# Create feature vector for training set
X_train, y_train, df_train = create_feature_vector(df_train, 'train', vectorizer)
df_test = pd.read_json(test_file)

# Create feature vector for test set
X_test, y_test, df_test = create_feature_vector(df_test, 'test', vectorizer)
id_test = df_test['id'].to_list()
id_test_df = pd.DataFrame(id_test)

print("SVM RBF")
clf_rbf = svm.SVC(kernel='rbf', C=10 ** 8)
clf_rbf.fit(X_train, y_train)
y_prediction_svm = clf_rbf.predict(X_test)
print(f1_score(y_true=y_test, y_pred=y_prediction_svm))

# Write the predictions to JSON file
write_file(y_prediction_svm, id_test_df)

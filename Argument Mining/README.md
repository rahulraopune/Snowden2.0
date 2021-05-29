# Computational Argumentation Assignment 2 
**Group : Snowden**

**Members :**

* Nihal Yadalam Murali Kumar
* Rahul Gururaja Rao
* Shivam Sharma
* Tejas Ravindra Dhawale

**Required Libraries :**

Make sure you have python and pip tool installed in your system. Below is the command to install all the necessary libraries required to run the project.

    pip install pandas
    pip install numpy
    pip install sklearn
    pip install spacy
  

**Approach :**

We choose combined features from POS Tag vectorizer and Tfidf vectorizer for our classification model. We choose those because the POS Tag features along with Tfidf which yielded good results (F1 Score). We trained our classification model with training data and later predicted with validation data (used cross validation for accuracy). We tried with several classification models such as knn, n-grams, random forest, SVM and many other models. Finally, we concluded with SVM as it is powerful and yielded good results on validation set i.e.,F1 Score of 0.54 with cross validation.  

1. Features used in POS vectorizer :
 
```python
  pos_feature_dict = {'ADJ': 0, 'SPACE': 0, 'ADV': 0, 'INTJ': 0, 'SYM': 0, 'VERB': 0, 'SCONJ': 0, 'PART': 0, 'X': 0,
                        'PUNCT': 0, 'AUX': 0, 'ADP': 0, 'NUM': 0, 'PRON': 0, 'NOUN': 0, 'DET': 0, 'CCONJ': 0,
                        'PROPN': 0}
```

These are the parts-of-speech feature vectors generated for every sentence in the input file. Along with this, we also create the parsed tree / tag feature vectors for every sentence and later create Tfidf vectors.

2. Features used in Tag / parsed tree vectorizer :

```python
  pos_feature_dict = {'VBP': 0, 'RBS': 0, 'VBZ': 0, 'WRB': 0, 'VB': 0, 'NNS': 0, 'WDT': 0, 'UH': 0, '-RRB-': 0,
                        'AFX': 0, 'CC': 0, 'WP': 0, 'VBN': 0, 'IN': 0, 'PRP$': 0, 'XX': 0, 'WP$': 0, 'RBR': 0, 'PDT': 0,
                        'HYPH': 0, 'POS': 0, '$': 0, 'NNPS': 0, 'MD': 0, '.': 0, 'VBD': 0, 'JJR': 0, 'NFP': 0, ',': 0,
                        'JJS': 0, 'DT': 0, '_SP': 0, 'VBG': 0, 'FW': 0, 'RP': 0, 'SYM': 0, 'LS': 0, 'CD': 0, 'RB': 0,
                        'EX': 0, '``': 0, 'PRP': 0, "''": 0, ':': 0, 'TO': 0, 'JJ': 0, 'ADD': 0, '-LRB-': 0, 'NN': 0,
                        'NNP': 0}
```

3. Creation of Tfidf vectorizer :

The Tfidf vectorizer will tokenize documents, learn the vocabulary and inverse document frequency weightings, and allows to encode new documents. It Transforms the text to feature vectors that can be used as input to estimator. vocabulary_ dc a dictionary that converts each token (word) to feature index in the matrix, each unique token gets a feature index. In each vector the numbers (weights) represent features tf-idf score.
    
   



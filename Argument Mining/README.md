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
    

**Project Installation :**

Once you install the required libraries using pip, you need to run the python file `run_final.py` using the python command `python run_final.py`. `output.json` file will be generated. `output.json` file is of the form :
    `{
        "<text_id_1>": "<label>",
        "<text_id_2>": "<label>",
        "<text_id_3>": "<label>",
        . . .
      }`
     
where, `text_id_x` is the unique identifier associated with each sentence and `label` is the predicted binary value by the SVM classifier can be `(0 / 1)`.
  

**Approach :**

We choose combined features from POS Tag vectorizer and Tfidf vectorizer for our classification model. We choose those because the POS Tag features along with Tfidf which yielded good results (F1 Score). We trained our classification model with training data and later predicted with validation data (used cross validation for accuracy). We tried with several classification models such as knn, n-grams, random forest, SVM and many other models. Finally, we concluded with SVM as it is powerful and yielded good results on validation set i.e.,F1 Score of 0.54 with cross validation.  

**1. Features used in POS vectorizer :**
 
```python
  pos_feature_dict = {'ADJ': 0, 'SPACE': 0, 'ADV': 0, 'INTJ': 0, 'SYM': 0, 'VERB': 0, 'SCONJ': 0, 'PART': 0, 'X': 0,
                        'PUNCT': 0, 'AUX': 0, 'ADP': 0, 'NUM': 0, 'PRON': 0, 'NOUN': 0, 'DET': 0, 'CCONJ': 0,
                        'PROPN': 0}
```

These are the parts-of-speech feature vectors generated for every sentence in the input file. Along with this, we also create the parsed tree / tag feature vectors for every sentence and later create Tfidf vectors.

**2. Features used in Tag / parsed tree vectorizer :**

```python
  pos_feature_dict = {'VBP': 0, 'RBS': 0, 'VBZ': 0, 'WRB': 0, 'VB': 0, 'NNS': 0, 'WDT': 0, 'UH': 0, '-RRB-': 0,
                        'AFX': 0, 'CC': 0, 'WP': 0, 'VBN': 0, 'IN': 0, 'PRP$': 0, 'XX': 0, 'WP$': 0, 'RBR': 0, 'PDT': 0,
                        'HYPH': 0, 'POS': 0, '$': 0, 'NNPS': 0, 'MD': 0, '.': 0, 'VBD': 0, 'JJR': 0, 'NFP': 0, ',': 0,
                        'JJS': 0, 'DT': 0, '_SP': 0, 'VBG': 0, 'FW': 0, 'RP': 0, 'SYM': 0, 'LS': 0, 'CD': 0, 'RB': 0,
                        'EX': 0, '``': 0, 'PRP': 0, "''": 0, ':': 0, 'TO': 0, 'JJ': 0, 'ADD': 0, '-LRB-': 0, 'NN': 0,
                        'NNP': 0}
```

**3. Creation of Tfidf vectorizer :**

The Tfidf vectorizer will tokenize documents, learn the vocabulary and inverse document frequency weightings, and allows to encode new documents. It Transforms the text to feature vectors that can be used as input to estimator. vocabulary_ dc a dictionary that converts each token (word) to feature index in the matrix, each unique token gets a feature index. In each vector the numbers (weights) represent features tf-idf score. We normalize the vector and send this to a classifier i.e., SVM for predicting the output `(0 / 1)`.


**4. SVM classifier using `sklearn` python library :**

Support Vector Machines are considered to be a classification approach and, can be employed in both types of classification and regression problems. It can easily handle multiple continuous and categorical variables. SVM constructs a hyperplane in multidimensional space to separate different classes. SVM generates optimal hyperplane in an iterative manner, which is used to minimize an error. The core idea of SVM is to find a maximum marginal hyperplane(MMH) that best divides the dataset into classes.

`sklearn` library has an in-built `SVMVectorizer` used to fit the model with input variable `x` and output variable `Y` in the training set. Later, we try to predict the validation set containing `x_test`. We write the predicted value i.e., `(0 / 1)` to the output `output.json` file.
   



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

Once you install the required libraries using pip, you need to run the python file run_final.py using the python command 
    
    python run_final.py 
    
   `output.json` file will be generated. `output.json` file is of the form :
    `{
        "<text_id_1>": "<label>",
        "<text_id_2>": "<label>",
        "<text_id_3>": "<label>",
        . . .
      }`
     
where, `text_id_x` is the unique identifier associated with each sentence and `label` is the predicted binary value by the SVM classifier can be `0/1`. 

**Note :**

Keep the training and the test files in the same folder where `run_final.py` file is present.
  

**Approach :**

We address the feature extraction at the token (word) level. We choose combined features from Parts-of-Speech (POS), TAG vectorizer, and TF-IDF vectorizer for our classification model. We used cross-validation on the training set to do model selection and tune the Hyper-parameters. We also tried the generation of feature vectors on every combination of POS, TAG, Tf-IDF, Spacy, and Universal Sentence Encoder (with and without pre-processing and normalization). Then we performed cross-validation on several classification models such as KNN, Perceptron, Neural Networks, Logistic Regression, Random Forest, SVM, and Decision Tree using every combination of the above-mentioned feature vectors. Finally, we chose the POS and TAG features along with TF-IDF and concluded that taking SVM as a classifier model yielded good results on the validation set i.e., F1 Score of 0.54

**1. Features used in POS vectorizer :**
 
```python
  pos_feature_dict = {'ADJ': 0, 'SPACE': 0, 'ADV': 0, 'INTJ': 0, 'SYM': 0, 'VERB': 0, 'SCONJ': 0, 'PART': 0, 'X': 0,
                        'PUNCT': 0, 'AUX': 0, 'ADP': 0, 'NUM': 0, 'PRON': 0, 'NOUN': 0, 'DET': 0, 'CCONJ': 0,
                        'PROPN': 0}
```

These are the parts-of-speech feature vectors generated for every sentence in the input file. We have POS because it is a syntactic feature.


**2. Features used in Tag / Nodes of parsed tree vectorizer :**

```python
  pos_feature_dict = {'VBP': 0, 'RBS': 0, 'VBZ': 0, 'WRB': 0, 'VB': 0, 'NNS': 0, 'WDT': 0, 'UH': 0, '-RRB-': 0,
                        'AFX': 0, 'CC': 0, 'WP': 0, 'VBN': 0, 'IN': 0, 'PRP$': 0, 'XX': 0, 'WP$': 0, 'RBR': 0, 'PDT': 0,
                        'HYPH': 0, 'POS': 0, '$': 0, 'NNPS': 0, 'MD': 0, '.': 0, 'VBD': 0, 'JJR': 0, 'NFP': 0, ',': 0,
                        'JJS': 0, 'DT': 0, '_SP': 0, 'VBG': 0, 'FW': 0, 'RP': 0, 'SYM': 0, 'LS': 0, 'CD': 0, 'RB': 0,
                        'EX': 0, '``': 0, 'PRP': 0, "''": 0, ':': 0, 'TO': 0, 'JJ': 0, 'ADD': 0, '-LRB-': 0, 'NN': 0,
                        'NNP': 0}
```

We use parse trees because they are constructed based on either the constituency relation of constituency grammars or the dependency relation of dependency grammars. We have used TAG because it is a semantic feature.


**3. Creation of TF-IDF vectorizer :**

We created TF-IDF feature vectors using `TfidfVectorizer` from `sklearn`. We built this feature vector on the whole text and then combined it with the POS+TAG feature vectors.
We later send this to a classifier i.e., SVM for predicting the output `0/1`.


**4. SVM classifier using `sklearn` python library :**

SVM can easily handle multiple continuous and categorical variables. SVM constructs a hyperplane in multidimensional space to separate different classes.

We chose the SVM model because of the following key features:
- SVM has regularization parameters that avoid overfitting.
- It is memory efficient.
- It is defined by convex optimization which results in no local minima.

We use `kernel=rbf` and `C=10**8` because these were the `best_params_` which our cross-validation experiment results. `sklearn` library has an in-built `svm.SVC` used to fit the model with input variable `x` and output variable `Y` in the training set. Later, we try to predict the validation set containing `x_test`. We write the predicted value i.e., `0/1` to the output `output.json` file.

**Note :**

No pre-processing was done in our implementation because we observed that with pre-processing (eg, removing stopwords/punctuation), words that are important in the context of POS feature vector like punctuation, conjunction (e.g., "and") were removed eventually giving us below-average performance. 
   


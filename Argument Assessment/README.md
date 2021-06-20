# Computational Argumentation Assignment 3 
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
    pip install nltk
    

**Project Installation :**

Once you install the required libraries using pip, you can run the jupyter notebook `CA_Ex3_Argument_Assessment.ipynb` on the local jupyter notebook server or on google collab. 

**Note :**

Keep the training and the test files in the same folder where `CA_Ex3_Argument_Assessment.ipynb` file is present. We are also submitting a negative keyword file, `negative_words.txt`[1], which contains all the NEGATIVE opinion words (or sentiment words). We have used this file to check the number of negative words in the text to create features. Keep this file in the same folder with `.ipynb` file as well.
    
After running the cell which calls the `write_file` function, `output.json` file will be generated.
  

**Approach :**

We address the feature extraction at the token level.
We have combined all the preceeding posts in a thread and used the following features:

- **Spacy word embeddings** because they represent implicit relationships between words
- **Total number of negative words** in the thread to identify ad-hominem in the next post.
- The **controversiality** parameter 
- Total number of **up votes** 
- **Parts of speech** vector because it is a syntactic feature.
- **violated_rule** parameter of each post.

We used 5-fold cross-validation on the training set to do model selection and tune the Hyper-parameters.
SVM is the classification model for this assignment.


**SVM classifier**

We chose the SVM model because of the following key features:
- SVM has regularization parameters that avoid overfitting.
- It is memory efficient.
- It is defined by convex optimization which results in no local minima.

**Note :**

In our implementation, there was no pre-processing because it was observed that pre-processing (e.g. removing stopwords/punctuation) removed words that are important in the context of spacy word embeddings and Parts of speech feature vectors.
   
**References**

[1] Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web." Proceedings of the 14th International World Wide Web conference (WWW-2005), May 10-14, 2005, Chiba, Japan.

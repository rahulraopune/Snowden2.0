# Computational Argumentation Assignment 4
**Group : Snowden**

**Members :**

* Nihal Yadalam Murali Kumar
* Rahul Gururaja Rao
* Shivam Sharma
* Tejas Ravindra Dhawale

**Required Libraries :**

Make sure you have python and pip tool installed in your system. Following libraries in python are required to run the project.
    
    pip install numpy
    pip install re
    pip install nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    pip install heapq
    pip install pandas
    pip install tqdm
    pip install json
    pip install unicodedata
    
    # Installing and Importing sumy
    !pip install sumy
    !pip install transformers
    !pip install SentencePiece 
    
    # Importing the parser and tokenizer
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer

    # Import the LexRank summarizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
    
**Approach**

**1. Introduction to Extractive Text Summarization :**

Text Summarization is a part of NLP involved in summarization of large texts without losing key aspects of text. Large texts are often found in news articles, tech blogs etc.
We use extractive text summarization approach to summarize the text. It is one of the traditional approaches used in real world applications. The core concept is to identify the important sentences of the text and add them to the summary text. Summaries obtained contains exact sentences from the original text.

**2. LexRank :**

LexRank is an extractive text summarization technique. A sentence which is similar to various other sentences of the text has a high probability of being important. Approach of LexRank is that a specific sentence is recommended by other similar sentences and hence it's rank tends to be higher. Higher the rank, higher is the priority of being included in the summarized text.

Working mechanism of LexRank is as follows:

**a)** We have to import `PlaintextParser` after generating pandas dataframe for the test_data. Here, we have an article stored as a string. Along with parser, we have to `import Tokenizer` for segmenting the raw text into tokens. We import the `LexRankSummarizer` available in `sumy.summarizers` to access the summaries of text/article.

**b)** Text source is in string format, so we need to use `PlainTextParser.from_string()` function to initialize the parser. We can specify the language used as an input to the Tokenizer. In our case, we use "English".

**c)** Now, we have to create a summarization model `lex_rank_summarizer` to fit our text. Syntax is given by `lex_rank_summarizer(document, sentences_count)`. We set the parameter `sentence_count` to 1, as we need a one-line summary.

**d)** We update the predicted entries of summaries to the `test_df['predicted']`. Later, we write the predicted summaries to the test_result_lex.json file.

**e)** The last step involves evaluation in the form of a BLEU-1 and BLEU-2 scores. In LexRank approach, we were able to achieve scores of `BLEU-1: 0.1523683483109674` and `BLEU-2: 0.030529159138909016`.

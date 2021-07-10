# Computational Argumentation Assignment 4
**Group : Snowden**

**Members :**

* Nihal Yadalam Murali Kumar
* Rahul Gururaja Rao
* Shivam Sharma
* Tejas Ravindra Dhawale

**Required Libraries :**

Run the first cell to install all the important library imports

![image](https://user-images.githubusercontent.com/26580082/125167584-a0482900-e1a1-11eb-8946-de77a97e0879.png)

    
**Approach**

**1. Introduction to Extractive Text Summarization :**

Text Summarization is a part of NLP involved in summarization of large texts without losing key aspects of text. Large texts are often found in news articles, tech blogs etc.
We use extractive text summarization approach to summarize the text. It is one of the traditional approaches used in real world applications. The core concept is to identify the important sentences of the text and add them to the summary text. Summaries obtained contains exact sentences from the original text.

**2. LexRank :**

LexRank is an extractive text summarization technique. A sentence which is similar to various other sentences of the text has a high probability of being important. Approach of LexRank is that a specific sentence is recommended by other similar sentences and hence it's rank tends to be higher. Higher the rank, higher is the priority of being included in the summarized text.

**Algorithm:**

LexRank algorithm consists of 6 steps namely:

**Step 1: Input to the algorithm**

Input to the LexRank algorithm can be an argument or a set of arguments in string format.

**Step 2: Word embeddings**

We need to convert the text input into a real-valued vectors. Word embeddings are computed such that the words that are represented as similar vectors are expected to be similar in meaning.

**Step 3: Cosine similarity within the sentence**

We use word embeddings in the sentence. However, in LexRank implementation an cosine similarity within a sentence is used. It computes the average of all word embeddings within a sentence that are used to compare to other sentences. The formula for computing cosine-similarity is given by `Cos(x, y) = x . y / ||x|| * ||y||`.

**Step 4: Connectivity matrix**

A connectivity matrix is usually a list of which vertex numbers have an edge between them. LexRank adds a count of connections from other sentences. To count the number of connections, LexRank applies a threshold. For example, it only counts sentences as similar to itself where cosine similarity is more than 0.3 or 0.1.

**Step 5: Eigenvector centrality**

To find out the most important sentences LexRank utilizes eigenvector centrality. The method is called power iteration method. It involves 3 steps:

**a)** In the first step each matrix row is multiplied by a 1.

**b)** In the second step, we square rows results and take a root from the sum.

**c)** We repeat the above steps until the normalized value does not change much between any iteration.

**Step 6: Output of the model**

Finally, we have the output i.e, the normalized value.


Working mechanism of LexRank is as follows:

**a)** We have to import `PlaintextParser` after generating pandas dataframe for the test_data. Here, we have an article stored as a string. Along with parser, we have to `import Tokenizer` for segmenting the raw text into tokens. We import the `LexRankSummarizer` available in `sumy.summarizers` to access the summaries of text/article.

**b)** Text source is in string format, so we need to use `PlainTextParser.from_string()` function to initialize the parser. We can specify the language used as an input to the Tokenizer. In our case, we use "English".

**c)** Now, we have to create a summarization model `lex_rank_summarizer` to fit our text. Syntax is given by `lex_rank_summarizer(document, sentences_count)`. We set the parameter `sentence_count` to 1, as we need a one-line summary.

**d)** We update the predicted entries of summaries to the `test_df['predicted']`. Later, we write the predicted summaries to the test_result_lex.json file.

**e)** The last step involves evaluation in the form of a BLEU-1 and BLEU-2 scores. In LexRank approach, we were able to achieve scores of `BLEU-1: 0.1523683483109674` and `BLEU-2: 0.030529159138909016`.

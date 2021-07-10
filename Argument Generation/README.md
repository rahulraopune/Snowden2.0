# Computational Argumentation Assignment 4
**Group : Snowden**

**Members :**

* Nihal Yadalam Murali Kumar
* Rahul Gururaja Rao
* Shivam Sharma
* Tejas Ravindra Dhawale

**Required Libraries :**

Run the first cell to install all the important library imports

![image](https://user-images.githubusercontent.com/26580082/125168914-19e31580-e1a8-11eb-8d2e-687c599133b7.png)
    
**Approach**

**1. Introduction to Extractive Text Summarization :**

Text Summarization is a part of NLP involved in summarization of large texts without losing key aspects of text. Large texts are often found in news articles, tech blogs etc.
We use extractive text summarization approach to generate conclusion of the argument. It is one of the traditional approaches used in real world applications. The core concept is to identify the important sentences of the text and add them to the summary text. Summaries obtained might contain exact sentences from the original text if the original text is less than two sentences.

**2. LexRank :**

LexRank is an unsupervised extractive text summarization technique. If a sentence is similar to several other sentences in the text, then it has a high possibility of being significant. By using LexRank, a specific sentence is recommended by similar sentences and therefore is likely to have a higher ranking. In summarizing a text, the higher the rank, the more priority it has.

**Algorithm:**

LexRank algorithm consists of 6 steps namely:

**Step 1: Input to the algorithm**

Input to the LexRank algorithm can be an argument or a set of arguments in string format.

**Step 2: Word embeddings**

The text input is converted into a real-valued vector. Word embeddings are computed such that the words that are represented as similar vectors are expected to be similar in meaning.

**Step 3: Cosine similarity within the sentence**

In LexRank word embeddings are used to calculate cosine similarity within sentences is used. It computes the average of all word embeddings within a sentence that are used to compare to other sentences. The formula for computing cosine-similarity is given by `Cos(x, y) = x . y / ||x|| * ||y||`.

**Step 4: Connectivity matrix**

A connectivity matrix is usually a list of which vertex numbers have an edge between them. LexRank adds a count of connections from other sentences. To count the number of connections, LexRank applies a threshold. If the similarity is greater than threshold, the entry in the connectivity matrix is 1 else 0.

**Step 5: Eigenvector centrality**

To find out the most important sentences LexRank utilizes eigenvector centrality. Power iteration method is used. It involves 3 steps:

**a)** Intially, entire matrix rows are  multiplied by 1.

**b)** Next, we square the row results and take a root from the sum.

**c)** The above steps are repeated until the normalized value does not change much between any iteration.

**Step 6: Output of the model**

Depending on the size of the summary, the sentences are sorted in descending order of normalisation values and the sentences with higher vales are added to the text summmary.


Working mechanism of LexRank is as follows:

**a)** We have to import `PlaintextParser` after generating pandas dataframe for the test_data. Here, we have an article stored as a string. Along with parser, we have to `import Tokenizer` for segmenting the raw text into tokens. We import the `LexRankSummarizer` available in `sumy.summarizers` to access the summaries of text/article.

**b)** Text source is in string format, so we need to use `PlainTextParser.from_string()` function to initialize the parser. We can specify the language used as an input to the Tokenizer. In our case, we use "English".

**c)** Now, we have to create a summarization model `lex_rank_summarizer` to fit our text. Syntax is given by `lex_rank_summarizer(document, sentences_count)`. We set the parameter `sentence_count` to 1, as we need a one-line summary.

**d)** We update the predicted entries of summaries to the `test_df['predicted']`. Later, we write the predicted summaries to the test_result_lex.json file.

**e)** The last step involves evaluation in the form of a BLEU-1 and BLEU-2 scores. In LexRank approach, we were able to achieve scores of `BLEU-1: 0.1523683483109674` and `BLEU-2: 0.030529159138909016`.

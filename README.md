# A Simple Search System for Phrase and Free Text Queries

Implementation of a document retrieval system for simple phrase and free
text queries using the positional inverted indexing scheme. The Reuters-21578 data set is used.
Reuters-21578 contains 21578 news stories from
Reuters newswire. There are 22 SGML files, each containing 1000 news articles, except the last
file, which contains 578 articles. 

The following steps are performed:
1) Pre-processing the Data Set: The text of a news story is enclosed under the <TEXT> tag.
The <TITLE> and the <BODY> fields are used to extract the text of a news story.
A tokenizer is implemented to get the tokens from the news texts and normalization operations are performed including case-folding, stopword removal, and punctuation removal.
2) Building the Inverted Index:
Each news article is indexed as a separate document and the NEW ID fields are used as document IDs.
An inverted index is created consisting of the dictionary and the postings lists. The inverted index as a file and during query processing only the inverted index is used. The inverted index
construction and query processor are designed as two separate modules.
3) Implementing a query processor: A query processor is implemented for phrase and
free text queries. That is, the queries are of the following two types (here wi
is a singleword keyword):
(i) Phrase query: “w1 w2...wn”
(ii) Free text query: w1 w2...wn
For phrase queries (expressed with double quotation marks), the query processor returns the IDs of the matching documents sorted in ascending order.
For free text queries, cosine similarity with (log-scaled) TF-IDF weighting is used.
The query processor returns the IDs of the documents as well as their cosine similarity scores, ranked by their cosine similarities to the query. Documents with zero cosine similarity are not returned.


### Running the program
Python requirement: Python 3.9.5 

Put the reuters21578 folder under the src folder.

Open the terminal in the src folder.

Run the following command to run the indexing module
```  python3 indexize.py ```

Run the following command to run the query processor
```  python3 query_processor.py  ```

Please enter the queries you would like to search into the command line, each line representing another query.
The program will output the results to the terminal as you press enter.

For phase queries, enter the query in double quotation marks:
```“w1 w2...wn”```
The program will print the IDs of the matching documents sorted in ascending order.

For free text queries, enter the query:
```w1 w2...wn```
The program will print the IDs of the documents as and their cosine similarity scores, in descending order of scores.

Then you want to quit press Ctrl+C.

<i> Developed for CMPE493 Introduction to Information Retrieval course, Bogazici University, Fall 2021 <i>


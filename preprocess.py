import re
from typing import List
import string

file_names = ['reut2-002', 'reut2-009', 'reut2-014', 'reut2-004', 'reut2-013', 'reut2-006', 'reut2-015', 'reut2-011',
              'reut2-005', 'reut2-000', 'reut2-007', 'reut2-001', 'reut2-012', 'reut2-010', 'reut2-008', 'reut2-003',
              'reut2-016', 'reut2-017', 'reut2-018', 'reut2-019', 'reut2-020', 'reut2-021']
folder_name = 'reuters21578'
stopwords_file_name = 'stopwords.txt'


# applies case-fold to input string, removes punctuation and returns the string as tokens
def normalize(text: str) -> [str]:
    text = text.casefold()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return [word for word in text.split()]


# removes the stopwords from the list
def tokenize(tokens: [str], stopwords: [str]) -> [str]:
    return [word for word in tokens if word not in stopwords]


# reads the stopwords from the file
def read_stopwords() -> List[str]:
    with open(stopwords_file_name) as reader:
        stopwords = [line.lower().replace('\n', '') for line in reader.readlines()]
        reader.close()
    return stopwords


# preprocesses the given data set, reads the files, extracts the tests, normalizes and stores into a dictionary
def preprocess():
    stopwords = read_stopwords()
    normalized_data = {}
    for file_name in file_names:
        # traverse the sgm files one by one, read the contents
        with open(f'{folder_name}/{file_name}.sgm', encoding="latin-1") as reader:
            content = reader.read().replace('\n', ' ')
            articles = re.findall("<TEXT(.*?)</TEXT>", content)  # find the texts of all news stories
            new_ids = re.findall("NEWID=\"(\d+)\"", content)  # find the new_ids for all articles
            # for each article, extract the title and body fields, normalize, tokenize and merge the texts
            for i, article in enumerate(articles):
                title_reg = re.findall("<TITLE(.*?)</TITLE>", article)
                title = title_reg[0] if len(title_reg) > 0 else ' '
                body_reg = re.findall("<BODY(.*?)</BODY>", article)
                body = body_reg[0] if len(body_reg) > 0 else ' '
                normalized_data[int(new_ids[i])] = [*tokenize(normalize(title), stopwords),
                                                    *tokenize(normalize(body), stopwords)]
    # returns the normalized, tokenized, stopwords removed version of texts in a dictionary, by new_id as a key
    return normalized_data

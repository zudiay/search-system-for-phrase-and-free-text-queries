import json
import math
from typing import List
from preprocess import normalize
import sys

N = 21578


# given a list of new ids and query, checks if the news contain the query in the exact order
# key_set contains possible documents that contain all the tokens in the query
# query_result contains for each token-new_id the positions of that token in that news article
def find_sequence(key_set: set, tokenized_normalized_query: List[str], query_result) -> List[int]:
    answer = set()
    for new_id in key_set:
        positions = []

        # append the positions in the documents with the same order as query
        for query_token in tokenized_normalized_query:
            positions.append(query_result[query_token][new_id]['positions'])
        # in the list of positions, check if consecutive elements form any consecutive position list
        for i in range(0, len(positions[0])):
            found = True
            pointer = positions[0][i]
            for j in range(1, len(positions)):
                if pointer + 1 in positions[j]:
                    pointer += 1
                else:
                    found = False
                    break
            if found:
                answer.add(int(new_id))
    return list(answer)


# calculates the length of a vector
def calculate_vector_length(vector: dict) -> float:
    length = 0
    for k, v in vector.items():
        length += v ** 2
    return math.sqrt(length)


if __name__ == "__main__":

    with open('index.json') as index_file:
        res = json.load(index_file)
        index_file.close()
    with open('documents.json') as documents_file:
        documents_index = json.load(documents_file)
        documents_file.close()

    # read the queries from the file, tokenize and normalize
    for line in sys.stdin:
        query = line.lower().replace('\n', '')
        phrase = query[0] == '"'
        tokenized_normalized_query = normalize(query)

        # For phrase queries, return the IDs of the matching documents sorted in ascending order.
        if phrase:
            query_result = {}  # {token_1: {new_id_1: [pos_1, pos_2]}, ..}
            key_set = set()  # smallest set of new_ids containing the tokens in the query
            # for every token in query, fetch the documents from the index, store them in query_result
            for i, token in enumerate(set(tokenized_normalized_query)):
                docs = res.get(token)  # {new_id_1: [pos_1, pos_2]}
                docs = docs['documents'] if docs is not None else {}
                query_result[token] = docs
                keys = set(list(docs.keys()))
                key_set = keys if i == 0 else key_set & keys

            # for each document, check if the tokens are in the correct order
            answer = find_sequence(key_set, tokenized_normalized_query, query_result)
            for item in sorted(answer):
                print(item)

        # For free text queries, cosine similarity with (log-scaled) TF-IDF weighting should be used.
        # The query processor should return the IDs of the documents as well as their cosine similarity scores.
        else:
            idf_vector = {}  # {token: (ls)IDF}

            # for each token, calculate idf
            for token, docs in res.items():
                df = docs.get('df')
                idf_weight = math.log((N + 1) / df, 10) if (df is not None and not df == 0) else 0.0
                idf_vector[token] = idf_weight

            # calculate idf-tf vector for the query
            query_idf_tf = {}  # {token: (ls)IDF-TF }
            for token in tokenized_normalized_query:
                query_tf = tokenized_normalized_query.count(token)
                query_tf_weight = 1.0 if query_tf == 0 else 1 + math.log(query_tf, 10)
                idf_value = idf_vector.get(token)
                idf_value = idf_value if idf_value is not None else 0.0
                query_idf_tf[token] = query_tf * idf_value
            query_vector_length = calculate_vector_length(query_idf_tf)

            # calculate idf-tf vector for each document
            document_idf_tfs = {}  # {new_id: {token: (ls)IDF-TF }}
            for new_id, document in documents_index.items():
                document_idf_tf = {}
                for token, tf in document.items():
                    document_tf = 1 + math.log(tf, 10) if (tf is not None and not tf == 0) else 0.0
                    idf_value = idf_vector.get(token)
                    idf_value = idf_value if idf_value is not None else 0.0
                    document_idf_tf[token] = document_tf * idf_value
                document_vector_length = calculate_vector_length(document_idf_tf)
                document_idf_tfs[int(new_id)] = {'length': document_vector_length, 'vectors': document_idf_tf}

            # calculate cosine similarity of each document idf-tf vector with the query idf-tf vector
            document_scores = {}
            for new_id, document_idf_tf in document_idf_tfs.items():
                cos_value = 0
                for token, doc_val in document_idf_tf['vectors'].items():
                    query_val = query_idf_tf.get(token)
                    query_val = query_val if query_val is not None else 0.0
                    cos_value += doc_val * query_val
                if cos_value > 0:
                    document_scores[new_id] = cos_value / (document_idf_tf['length'] * query_vector_length)

            sorted_dict = dict(sorted(document_scores.items(), key=lambda x: x[1], reverse=True))
            for new_id, cosine_score in sorted_dict.items():
                print(f'{new_id}: {cosine_score}')

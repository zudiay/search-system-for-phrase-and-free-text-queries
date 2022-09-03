import json
from collections import defaultdict
from preprocess import preprocess

'''
index_with_frequencies
{ token: 
    {
    'df': document frequency, 
    'documents': { new_id: { 'tf': term frequency, 'positions': list of positions } }
    }
}
'''

def build_frequency_index(index: dict):
    index_with_frequencies = {}
    for token, value in index.items():
        documents = {}
        for new_id, pos in value.items():
            documents[new_id] = {'tf': len(pos), 'positions': list(pos)}
        new_value = {'df': len(value), 'documents': documents}
        index_with_frequencies[token] = new_value
    return index_with_frequencies


# the module that builds the inverted index
if __name__ == "__main__":
    # calls the preprocess module to get the normalized version of data
    normalized = preprocess()  # {new_id : [token_1, token_2, ..]}
    inverted_index = defaultdict(lambda: defaultdict(list))  # {token: {new_id_1: [pos_1, pos_2]}, ..}
    document_index = defaultdict(lambda: defaultdict(int))  # { new_id: {token: document_frequency }}

    for new_id, tokens in normalized.items():
        for i, token in enumerate(tokens):
            inverted_index[token][new_id].append(i)
            document_index[new_id][token] += 1

    index_with_frequencies = build_frequency_index(inverted_index)

    with open('index.json', 'w') as index_file:
        json.dump(index_with_frequencies, index_file)
        index_file.close()

    with open('documents.json', 'w') as document_file:
        json.dump(document_index, document_file)
        document_file.close()

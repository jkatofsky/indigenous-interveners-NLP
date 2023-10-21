import sys
import glob
import re
import nltk


def process_document(document: str) -> str:
    document = document.lower()

    document = re.sub(r'\n', '', document)

    document = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(document)

    document = [word for word in document \
                if word.isalpha() and word not in nltk.corpus.stopwords.words('english')]
    
    lemmatizer = nltk.stem.WordNetLemmatizer()
    document = [lemmatizer.lemmatize(word) for word in document]
    
    return ' '.join(document)


def decision_factum_tfidf_cosine_similarity(decision: str, factum: str):
    pass


def decision_factum_word2vec_cosine_similarity(decision: str, factum: str):
    pass

if __name__ == '__main__':
    dir = sys.argv[1]

    with open(f'{dir}/decision.clean.txt', 'r') as fp:
        print("Processing decision text")
        decision = process_document(fp.read())

    factums = dict()
    for factum_filename in glob.glob(f'{dir}/interveners/*.clean.txt'):
        with open(factum_filename, 'r') as fp:
            print(f"Processing {factum_filename} text")
            factums[factum_filename.split('.')[0]] = process_document(fp.read())

    # TODO: similarity stuff!
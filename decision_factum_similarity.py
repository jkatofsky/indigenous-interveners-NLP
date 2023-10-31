import sys
import glob
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

def process_document(document: str) -> str:
    document = document.lower()

    document = re.sub(r'\n', '', document)

    document = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(document)

    document = [word for word in document \
                if word.isalpha() and word not in nltk.corpus.stopwords.words('english')]
    
    lemmatizer = nltk.stem.WordNetLemmatizer()
    document = [lemmatizer.lemmatize(word) for word in document]
    
    return ' '.join(document)


def tf_idf_cosine_similarity(decision: str, factums: dict):
    print("Computing TF-IDF Cosine Similarity...")

    # TODO: better logs; and verify that everything is checking out
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    decision_embedding = vectorizer.fit_transform([decision])

    for factum_key in factums:
        factum_embedding = vectorizer.transform([factums[factum_key]])
        similarity = cosine_similarity(factum_embedding, decision_embedding)
        print(f'Factum {factum_key} similarity with decision: {similarity}')


def word2vec_similarity(decision: str, factums: dict):
    # TODO
    pass


if __name__ == '__main__':
    for directory in sys.argv[1:]:
        print(f"Running on directory {directory}")

        with open(f'{directory}/decision.clean.txt', 'r') as fp:
            print("Processing decision text")
            decision = process_document(fp.read())

        factums = dict()
        for factum_filename in glob.glob(f'{directory}/interveners/*.clean.txt'):
            with open(factum_filename, 'r') as fp:
                print(f"Processing {factum_filename} text")
                factums[Path(factum_filename).name.split('.')[0]] = process_document(fp.read())

        tf_idf_cosine_similarity(decision, factums)
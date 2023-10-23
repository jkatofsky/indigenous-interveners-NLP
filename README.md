# Some exploratory data science/NLP stuff about indigenous supreme count interveners for my buddy Johnathon

This doc will document the steps I'm taking to get the results. Come on the jouney with me :D

## PDFs to plaintext

The first step in the process is extracting the raw text from the PDFs so they can be usable in NLP algorithms.

`pdfs_to_plaintext.py` extracts the text from the `.pdf` file passed to its standard input to a `.txt`  file of the same name. To extract all `.pdf`s at once, I passed it `data/**/*.pdf`.

*Note:* this looks to have an issue where some words get occaisonally cut up. I.e. `Canada` will be parsed to `Canad a` in the text file. Not sure why this happens, but I don't think it happens often enough to throw things off. Can investigate later, though.

## Factum/decision similarity

### Cleaning

I then manually cleaned the `.txt` files, resulting in the `*.clean.txt` files, to only keep the "body" of the document and remove sections that are irrelevant from a semantics perspective. I could have possibly automated this with some extractions in PyPDF, but the dataset is small enough to make manual cleaning viable. After this, there is still a bit of junk, namely inline/footnote citations and sub-section headers, but I don't think that will be too much to throw things off.

Taking in these "clean" documents, `decision_factum_similarity.py` is then the script that does the similarity computations. First, it does a pretty standard set of pre-processing on the text:

- lower-casing
- removal of whitespace
- removal of punctuation
- removal of numbers
- removal of [stop words](https://en.wikipedia.org/wiki/Stop_word)
- [lemmatization](https://en.wikipedia.org/wiki/Lemmatization)

### TF-IDF

...
# Some exploratory data science/NLP stuff about indigenous supreme court interveners for my buddy Johnathon

This doc will document my methodology. Come on the jouney with me :D

## References comparison

### Reference extraction

That title makes things sound kind of fancy, but I just went through all of the factums/decisions and manually copy-pasted their references to the `*.references.txt` files, with a reference per line. I figured this was the fastest way to do this, since there were multiple different document formats and I wanted to avoid a [common developer pitfall](https://devhumor.com/media/never-spend-6-minutes-doing-something-by-hand) (lol).

So, any errors found in these files are copy-paste mistakes that slipped through the cracks. But in general, the quality of the resulting data looks pretty good.

The only changes I made manually to the references (when I saw it) was to remove `-`s from linebreaks, and remove URLs when they chose to include that to an online item.

### Levenshtein distance

Given two short strings of letters, perhaps the most common metric of their similarity is Levenshtein distance. This makes it a very good metric to compare short things such as references (we'll see the more complicated methods used to comapre entire documents later).

It's equal to the number of letters that need to be changed in one string in order to transform it into the other. When you divide that number by the combined length of the strings being compared, you get a *ratio* that can be used to quantify how similar the two strings are on a scale from 0 to 1. Let's call this a *Levenshtein ratio*.

Hopefully not to state the obvious, but we need to use such a metric instead of just directly comparing the strings, because two strings that point to the same actual reference might be formatted differently.

<!-- TODO: more explanation? -->

### Reference matching

`decision_factum_similarity.py` does the reference comparisons using Levenshtein ratios. It takes as standard input a list of directories - which contain these `*.references.txt` files - and runs the following reference comparison process on all of them.

For all factums in the directory...

- for each of the factums's references
  - for each of the relevant decision's references
    - if the Levenshtein ratio of the two references is above a certain threshold (I used 0.5), mark them as "matching"

So, in the end, for each factum, this process gives a one-to-many mapping of its rerences to references in its decision, which is outputted as the first part of the `*-references-analysis.txt` files (along with the Levenshtein ratios as a sanity check).

### Missing references

Then, the second part of the `*-references-analysis.txt` files is simply a list of all of the factum's references that matched *no* references in the decision. This is the juicy part for the paper, I think.

### A note on false negative vs false positives

I set the Levenshtein ratio threshold for a "match" to the (admittedly pretty arbitirary) value of 0.5. From inspecting the results, this seems to give a lot of false positives (i.e., matched references in the decision that in reality are not the same reference). But this is the cost of having very few false negatives (i.e., reference matches that the we just miss). Given that you're  mainly looking to accurately indentify factum references that *do not* appear in the decision, I opted to minimize the false negatives.

So the takeaway is: the list of factum references that have no match will be very *accurate*, but it will likely *not be exhaustive*. So you should be able to assume that everything listed there is really missing from the decision, but I would caution against treating the *number* of references in the list as a definitive fact. There are likely some references missing from the list, as a result of false positives.

The data science nerd in me would complain if I didn't mention that technically, this means that this method has [high recall as opposed to high precision](https://en.wikipedia.org/wiki/Precision_and_recall).

## Factum/decision similarity

### PDFs to plaintext

The first step in the process is extracting the raw text from the PDFs so they can be usable in NLP algorithms.

`pdfs_to_plaintext.py` extracts the text from the `.pdf` file passed to its standard input to a `.txt`  file of the same name. To extract all `.pdf`s at once, I passed it `data/**/*.pdf`.

*Note:* this looks to have an issue where some words get occaisonally cut up. I.e. `Canada` will be parsed to `Canad a` in the text file. Not sure why this happens, but I don't think it happens often enough to throw things off. Can investigate later, though.

### Cleaning

Before using a script for anything, I manually cleaned the `.txt` versions of the decisions/factums, resulting in the `*.clean.txt` files, to only keep the "body" of the document and remove sections that are irrelevant from a semantics perspective. I could have possibly automated this with some extractions in PyPDF, but the dataset is small enough to make manual cleaning viable. After this, there is still a bit of junk, namely inline/footnote citations and sub-section headers, but I don't think that will be too much to throw things off.

Similarly structured to the reference analysis, `decision_factum_similarity.py` is then the script that does the similarity computations. It takes as standard input the directories - which contain these cleaned documents - on which to run the similarity computations in a sequence.

First, it does a pretty standard set of pre-processing on the text:

- lower-casing
- removal of whitespace
- removal of punctuation
- removal of numbers
- removal of [stop words](https://en.wikipedia.org/wiki/Stop_word)
- [lemmatization](https://en.wikipedia.org/wiki/Lemmatization)

### TF-IDF

...
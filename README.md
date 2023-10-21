# Some exploratory data science/NLP stuff about indigenous supreme count interveners for my buddy Johnathon

This doc will document the steps I'm taking to get the results. Come on the jouney with me :D

## Data parsing

### TODO
- [X] PDF -> plaintext
- [ ] Manual cleaning to produce "body" of the case
- [ ] Manual extraction of references to a seperate (semi-structured?) file

### Documentation

`pdf_to_plaintext.py` extracts the content of every pdf file passed in the standard input to a `.txt`  file of the same name. To do this for every `.pdf` file in the `data` directory, use it like this:

```bash
python3 pdf_to_plaintext.py data/**/*.pdf
```
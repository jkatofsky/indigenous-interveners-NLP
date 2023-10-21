from pypdf import PdfReader
import sys

def pdf_to_plaintext(pdf_filename: str):
    print(f"Extracting text from {pdf_filename} to a .txt file")
    reader = PdfReader(pdf_filename)
    with open(pdf_filename.replace('pdf', 'txt'), 'w') as fp:
        for page in reader.pages:
            fp.write(page.extract_text())

if __name__ == "__main__":
    for pdf_filename in sys.argv[1:]:
        pdf_to_plaintext(pdf_filename)

from pypdf import PdfReader
import glob

def pdf_to_plaintext(pdf_filename: str):
    print(f"Extracting text from {pdf_filename} to new file")
    reader = PdfReader(pdf_filename)
    with open(pdf_filename.replace('pdf', 'txt'), 'w') as fp:
        for page in reader.pages:
            fp.write(page.extract_text())

if __name__ == "__main__":
    pdf_filenames = glob.glob('./data/**/*.pdf', recursive=True)
    for pdf_filename in pdf_filenames:
        pdf_to_plaintext(pdf_filename)

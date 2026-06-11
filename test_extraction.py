from app.services.pdf_extractor import extract_pdf_data
from app.services.chunker import create_chunks

pdf = extract_pdf_data(
    "data/raw/VIVA QUESTION.pdf"
)

full_text = ""

for page in pdf["pages"]:
    full_text += page["text"]

chunks = create_chunks(full_text)

print("Total Chunks:", len(chunks))

print(chunks[0])
from src.pdf_reader import read_pdf
from src.chunker import chunk_text
from src.text_cleaner import clean_text
from src.database import (
    create_database, insert_document, insert_chunk, get_document_by_path,delete_chunks
    )
text = clean_text

create_database()
pdf_path = "data/pdfs/RSM.pdf"
pages, page_count = read_pdf(pdf_path)
text = "\n".join(page["text"]for page in pages)
text = clean_text(text)
chunks = chunk_text(pages)
# Check whether the document already exists
document_id = get_document_by_path(pdf_path)

if document_id is not None:
    delete_chunks(document_id)

if document_id is None:
    # Save document information to the database
    document_id = insert_document(
        file_name="RSM.pdf",
        file_path=pdf_path,
        page_count=page_count,
        character_count=len(text),
        upload_date="2026-08-03"
    )


    # Save each chunk to the database
for i, chunk in enumerate(chunks, start=1):
    print("CURRENT CHUNK: ",chunk)

    page_number = chunk.get ("page_number")
    chunk_text = chunk.get ("text")


    insert_chunk(
        document_id = document_id,
        chunk_number = i,
        page_number = page_number,
        chunk_text = chunk_text
    )

else:
    print("Document already exists in the database.")

chunk_count = len(chunks)
print("=" *50)
print("Engineering Knowledge Assistant")
print("=" * 50)

print(f"PDF File : {pdf_path}")
print(f"Pages : {page_count}")
print(f"Characters Extracted : {len(text)}")
print(f"Chunks    : {chunk_count}")

print("=" * 50)
print()
for i, chunk in enumerate(chunks, start =1):
    print (f"Chunk {i}")
    print("-" *50)
    print(repr(chunk["text"][:200]))
    print(f"Page : {chunk['page_number']}")
    print(f"\nCharacters: {len(chunk['text'])}")
    print("-"*50)

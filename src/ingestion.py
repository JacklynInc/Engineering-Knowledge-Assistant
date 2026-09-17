from pathlib import Path
from datetime import datetime

from src.pdf_reader import read_pdf
from src.text_cleaner import clean_text
from src.chunker import chunk_text
from src.database import (
    insert_document_with_chunks,
    get_document_by_path,
    delete_document,
)
from src.embedding import create_embeddings
from src.vector_database import (
    create_collection,
    upsert_embeddings,
    delete_vectors_by_document,
)


def ingest_pdf(pdf_path):
    """
    Process one PDF through the complete ingestion pipeline.

    PDF
      -> text extraction
      -> cleaning
      -> chunking
      -> SQLite transaction
      -> embeddings
      -> Qdrant
    """

    pdf_path = str(Path(pdf_path))

    # 1. Check whether this document already exists
    existing_document = get_document_by_path(pdf_path)

    if existing_document:
        raise ValueError(
            f"Document already exists in the database: {pdf_path}"
        )

    # 2. Read PDF
    pages, page_count = read_pdf(pdf_path)

    # 3. Calculate document character count
    full_text = "\n".join(
        page["text"]
        for page in pages
    )

    cleaned_text = clean_text(full_text)
    character_count = len(cleaned_text)

    if character_count == 0:
        raise ValueError(
            "The PDF contains no extractable text."
        )

    # 4. Create chunks
    chunks = chunk_text(pages)

    if not chunks:
        raise ValueError(
            "No text chunks could be created from the PDF."
        )

    # 5. Store document and chunks in one SQLite transaction
    document_id, stored_chunks = insert_document_with_chunks(
        file_name=Path(pdf_path).name,
        file_path=pdf_path,
        page_count=page_count,
        character_count=character_count,
        upload_date=datetime.now().isoformat(
            timespec="seconds"
        ),
        chunks=chunks,
    )

    try:
        # 6. Create embeddings
        texts = [
            chunk["text"]
            for chunk in stored_chunks
        ]

        embeddings = create_embeddings(texts)

        # 7. Make sure the Qdrant collection exists
        create_collection()

        # 8. Store embeddings and metadata in Qdrant
        upsert_embeddings(
            stored_chunks,
            embeddings
        )

    except Exception:
        # Remove vectors if any were created
        delete_vectors_by_document(document_id)

        # Remove the SQLite document and chunks
        delete_document(document_id)

        raise

    # 9. Return ingestion summary
    return {
        "document_id": document_id,
        "file_name": Path(pdf_path).name,
        "page_count": page_count,
        "chunk_count": len(stored_chunks),
        "character_count": character_count,
    }
from src.database import get_chunks_by_document
from src.embedding import create_embeddings
from src.vector_database import create_collection, upsert_embeddings


DOCUMENT_ID = 7


def main():
    print("Loading chunks from SQLite...")

    chunks = get_chunks_by_document(DOCUMENT_ID)

    print(f"Chunks loaded: {len(chunks)}")

    if not chunks:
        print("No chunks found.")
        return

    texts = [chunk["text"] for chunk in chunks]

    print("Creating embeddings...")

    embeddings = create_embeddings(texts)

    print(f"Embeddings created: {len(embeddings)}")

    create_collection()

    print("Storing vectors in Qdrant...")

    upsert_embeddings(chunks, embeddings)

    print("Vector indexing complete.")


if __name__ == "__main__":
    main()
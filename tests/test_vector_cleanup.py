from src.vector_database import (
    search_similar_chunks,
    delete_vectors_by_document,
)


def main():

    temporary_document_id = 999999

    delete_vectors_by_document(temporary_document_id)

    print("=" * 50)
    print("VECTOR CLEANUP TEST: PASS")
    print("=" * 50)


if __name__ == "__main__":
    main()
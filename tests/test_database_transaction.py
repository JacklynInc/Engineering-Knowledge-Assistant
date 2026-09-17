from src.database import (
    delete_document,
    get_chunks_by_document,
    insert_document_with_chunks,
)


def main():
    """Test atomic insertion of a document and its chunks."""

    test_file_path = (
        "data/pdfs/__transaction_test__.pdf"
    )

    test_chunks = [
        {
            "page_number": 1,
            "text": "Transaction test chunk one.",
        },
        {
            "page_number": 2,
            "text": "Transaction test chunk two.",
        },
    ]

    # Insert test document and chunks
    document_id, stored_chunks = (
        insert_document_with_chunks(
            file_name="__transaction_test__.pdf",
            file_path=test_file_path,
            page_count=2,
            character_count=58,
            upload_date="2026-09-15T00:00:00",
            chunks=test_chunks,
        )
    )

    print(
        f"Document ID created: {document_id}"
    )

    print(
        f"Chunks created: {len(stored_chunks)}"
    )

    # Verify chunks exist
    database_chunks = get_chunks_by_document(
        document_id
    )

    print(
        f"Chunks found in database: "
        f"{len(database_chunks)}"
    )

    assert len(stored_chunks) == 2
    assert len(database_chunks) == 2

    # Clean up test data
    delete_document(document_id)

    remaining_chunks = get_chunks_by_document(
        document_id
    )

    print(
        f"Chunks after cleanup: "
        f"{len(remaining_chunks)}"
    )

    assert len(remaining_chunks) == 0

    print()
    print("=" * 50)
    print("TRANSACTION TEST: PASS")
    print("=" * 50)


if __name__ == "__main__":
    main()
from src.embedding import create_embeddings
from src.vector_database import search_similar_chunks
from src.database import get_chunks_by_ids


TEST_CASES = [
    {
        "document_id": 7,
        "question": "What is response surface methodology?",
        "expected_pages": [5],
        "expected": "relevant",
    },
    {
        "document_id": 8,
        "question": "What is oil well abandonment?",
        "expected_pages": [3],
        "expected": "relevant",
    },
    {
        "document_id": 8,
        "question": "What is response surface methodology?",
        "expected_pages": [5],
        "expected": "irrelevant",
    },
    {
        "document_id": 8,
        "question": "What is the capital of Germany?",
        "expected_pages": [],
        "expected": "irrelevant",
    },
]


def main():

    questions = [
        test_case["question"]
        for test_case in TEST_CASES
    ]

    embeddings = create_embeddings(questions)

    passed = True

    print("=" * 70)
    print("SOURCE-AWARE RETRIEVAL EVALUATION")
    print("=" * 70)

    for test_case, embedding in zip(TEST_CASES, embeddings):

        results = search_similar_chunks(
            embedding,
            document_id=test_case["document_id"],
            limit=3,
            score_threshold=0.0
        )

        chunk_ids = [result.id for result in results]
        chunks = get_chunks_by_ids(chunk_ids)

        retrieved_pages = {
            chunk["page_number"]
            for chunk in chunks
        }

        top_score = results[0].score if results else 0.0

        if test_case["expected"] == "relevant":

            score_passed = top_score >= 0.5

            page_passed = any(
                page in retrieved_pages
                for page in test_case["expected_pages"]
            )

            test_passed = score_passed and page_passed

            expected = (
                "score >= 0.5 AND expected page retrieved"
            )

        else:

            score_passed = top_score < 0.5

            page_passed = not any(
                page in retrieved_pages
                for page in test_case["expected_pages"]
            )

            test_passed = score_passed and page_passed

            expected = (
                "score < 0.5 AND unrelated source not retrieved"
            )

        status = "PASS" if test_passed else "FAIL"

        if not test_passed:
            passed = False

        print()
        print(f"Document ID: {test_case['document_id']}")
        print(f"Question: {test_case['question']}")
        print(f"Top score: {top_score:.4f}")
        print(f"Retrieved pages: {sorted(retrieved_pages)}")
        print(f"Expected: {expected}")
        print(f"Result: {status}")

    print()
    print("=" * 70)

    if passed:
        print("OVERALL RESULT: PASS")
    else:
        print("OVERALL RESULT: FAIL")

    print("=" * 70)


if __name__ == "__main__":
    main()
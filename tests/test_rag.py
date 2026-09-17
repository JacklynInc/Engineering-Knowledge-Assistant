from src.rag import answer_question


TEST_CASES = [
    {
        "document_id": 7,
        "question": "What is response surface methodology?",
        "expected_page": 5,
        "expected": "answer",
    },
    {
        "document_id": 8,
        "question": "What is oil well abandonment?",
        "expected_page": 3,
        "expected": "answer",
    },
    {
        "document_id": 8,
        "question": "What is response surface methodology?",
        "expected_page": None,
        "expected": "no_information",
    },
    {
        "document_id": 8,
        "question": "What is the capital of Germany?",
        "expected_page": None,
        "expected": "no_information",
    },
]


def main():

    passed = True

    print("=" * 70)
    print("RAG ANSWER EVALUATION")
    print("=" * 70)

    for test_case in TEST_CASES:

        result = answer_question(
            question=test_case["question"],
            document_id=test_case["document_id"]
        )

        answer = result["answer"]
        sources = result["sources"]

        source_pages = {
            source["page"]
            for source in sources
        }

        if test_case["expected"] == "answer":

            answer_passed = (
                "not available" not in answer.lower()
            )

            page_passed = (
                test_case["expected_page"]
                in source_pages
            )

            test_passed = answer_passed and page_passed

        else:

            answer_passed = (
                answer.strip()
                == "No relevant information was found in the document."
            )

            page_passed = len(sources) == 0

            test_passed = answer_passed and page_passed

        status = "PASS" if test_passed else "FAIL"

        if not test_passed:
            passed = False

        print()
        print(f"Document ID: {test_case['document_id']}")
        print(f"Question: {test_case['question']}")
        print(f"Sources: {sorted(source_pages)}")
        print(f"Result: {status}")

        if test_case["expected"] == "answer":
            print(f"Expected page: {test_case['expected_page']}")

        print(f"Answer: {answer}")

    print()
    print("=" * 70)

    if passed:
        print("OVERALL RESULT: PASS")
    else:
        print("OVERALL RESULT: FAIL")

    print("=" * 70)


if __name__ == "__main__":
    main()
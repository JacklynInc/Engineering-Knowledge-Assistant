from src.embedding import create_embeddings
from src.vector_database import search_similar_chunks
from src.database import get_chunks_by_ids
from src.llm import generate_answer


def answer_question(
    question,
    document_id,
    limit=3,
    score_threshold=0.5,
    max_context_chars=6000
):
    # 1. Convert the question into an embedding
    query_embedding = create_embeddings([question])[0]

    # 2. Search Qdrant for relevant chunks
    results = search_similar_chunks(
    query_embedding,
    document_id=document_id,
    limit=limit,
    score_threshold=score_threshold
)

    if not results:
        return {
            "answer": "No relevant information was found in the document.",
            "sources": []
        }

    # 3. Get the corresponding chunk IDs
    chunk_ids = [result.id for result in results]

    # 4. Retrieve the actual text from SQLite
    chunks = get_chunks_by_ids(chunk_ids)

    chunks_by_id = {
        chunk["id"]: chunk
        for chunk in chunks
    }

    # 5. Build controlled context
    context_parts = []
    sources = []
    current_context_length = 0

    for result in results:
        chunk = chunks_by_id.get(result.id)

        if not chunk:
            continue

        chunk_text = chunk["text"]
        chunk_length = len(chunk_text)

        if current_context_length + chunk_length > max_context_chars:
            continue

        context_parts.append(
            f"[Page {chunk['page_number']}]\n"
            f"{chunk_text}"
        )

        sources.append({
            "file_name": chunk["file_name"],
            "page": chunk["page_number"],
            "chunk": chunk["chunk_number"],
            "score": result.score,
            "text": chunk["text"],
        })

        current_context_length += chunk_length

    # 6. Make sure we actually have context
    if not context_parts:
        return {
            "answer": "No relevant information was found in the document.",
            "sources": []
        }

    context = "\n\n".join(context_parts)

    # 7. Generate a grounded answer
    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "answer": answer,
        "sources": sources
    }
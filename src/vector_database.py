from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)


QDRANT_PATH = "data/embeddings/qdrant"
COLLECTION_NAME = "engineering_chunks"
VECTOR_SIZE = 1536


# Local persistent Qdrant database
client = QdrantClient(
    path=QDRANT_PATH
)


def create_collection():
    """Create the engineering chunks collection if it does not exist."""

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def get_collection_info():
    """Return information about the vector collection."""

    return client.get_collection(
        COLLECTION_NAME
    )


def search_similar_chunks(
    query_embedding,
    document_id=None,
    limit=3,
    score_threshold=0.5,
):
    """Search for semantically similar document chunks."""

    query_filter = None

    if document_id is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id
                    ),
                )
            ]
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=query_filter,
        limit=limit,
        score_threshold=score_threshold,
        with_payload=True,
    )

    return results.points


def upsert_embeddings(
    chunks,
    embeddings,
):
    """Store chunk embeddings and metadata in Qdrant."""

    points = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):
        points.append(
            PointStruct(
                id=chunk["id"],
                vector=embedding,
                payload={
                    "document_id": chunk["document_id"],
                    "chunk_number": chunk["chunk_number"],
                    "page_number": chunk["page_number"],
                },
            )
        )

    if not points:
        return

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def delete_vectors_by_document(
    document_id
):
    """Delete all vectors belonging to a document."""

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id
                    ),
                )
            ]
        ),
    )
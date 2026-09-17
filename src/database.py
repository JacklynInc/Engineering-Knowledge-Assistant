import sqlite3


DATABASE_PATH = "data/database/engineering_knowledge.db"


def create_database():
    """Create the database tables if they do not already exist."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Documents table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            page_count INTEGER,
            character_count INTEGER,
            upload_date TEXT
        )
        """
    )

    # Chunks table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_number INTEGER NOT NULL,
            page_number INTEGER,
            chunk_text TEXT NOT NULL,
            character_count INTEGER,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
        """
    )

    connection.commit()
    connection.close()


def insert_document(
    file_name,
    file_path,
    page_count,
    character_count,
    upload_date
):
    """Insert a document into the database."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents
        (file_name, file_path, page_count, character_count, upload_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            file_name,
            file_path,
            page_count,
            character_count,
            upload_date,
        )
    )

    connection.commit()

    document_id = cursor.lastrowid

    connection.close()

    return document_id


def insert_chunk(
    document_id,
    chunk_number,
    page_number,
    chunk_text
):
    """Insert one text chunk into the database."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chunks
        (document_id, chunk_number, page_number, chunk_text, character_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            document_id,
            chunk_number,
            page_number,
            chunk_text,
            len(chunk_text),
        )
    )

    connection.commit()

    chunk_id = cursor.lastrowid

    connection.close()

    return chunk_id


def get_document_by_path(file_path):
    """Return the document ID for a stored file path."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM documents
        WHERE file_path = ?
        """,
        (file_path,)
    )

    result = cursor.fetchone()

    connection.close()

    return result[0] if result else None


def delete_chunks(document_id):
    """Delete all chunks belonging to a document."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM chunks
        WHERE document_id = ?
        """,
        (document_id,)
    )

    connection.commit()
    connection.close()


def get_chunks_by_document(document_id):
    """Return all chunks belonging to a document."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            document_id,
            chunk_number,
            page_number,
            chunk_text
        FROM chunks
        WHERE document_id = ?
        ORDER BY chunk_number
        """,
        (document_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    chunks = []

    for row in rows:
        chunks.append(
            {
                "id": row[0],
                "document_id": row[1],
                "chunk_number": row[2],
                "page_number": row[3],
                "text": row[4],
            }
        )

    return chunks


def get_chunks_by_ids(chunk_ids):
    """Return chunks matching the supplied chunk IDs."""

    if not chunk_ids:
        return []

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    placeholders = ",".join("?" for _ in chunk_ids)

    cursor.execute(
        f"""
        SELECT
            c.id,
            c.document_id,
            d.file_name,
            c.chunk_number,
            c.page_number,
            c.chunk_text
        FROM chunks c
        JOIN documents d
            ON c.document_id = d.id
        WHERE c.id IN ({placeholders})
        """,
        chunk_ids
    )

    rows = cursor.fetchall()

    connection.close()

    chunks = []

    for row in rows:
        chunks.append(
            {
                "id": row[0],
                "document_id": row[1],
                "file_name": row[2],
                "chunk_number": row[3],
                "page_number": row[4],
                "text": row[5],
            }
        )

    return chunks


def get_all_documents():
    """Return all documents stored in the database."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            file_name,
            page_count,
            character_count,
            upload_date
        FROM documents
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    documents = []

    for row in rows:
        documents.append(
            {
                "id": row[0],
                "file_name": row[1],
                "page_count": row[2],
                "character_count": row[3],
                "upload_date": row[4],
            }
        )

    return documents


def delete_document(document_id):
    """Delete a document and all of its chunks."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM chunks
        WHERE document_id = ?
        """,
        (document_id,)
    )

    cursor.execute(
        """
        DELETE FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    connection.commit()
    connection.close()


def insert_document_with_chunks(
    file_name,
    file_path,
    page_count,
    character_count,
    upload_date,
    chunks
):
    """
    Insert a document and all its chunks in one SQLite transaction.

    If any database operation fails, the entire transaction is rolled back.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        # Insert document
        cursor.execute(
            """
            INSERT INTO documents
            (file_name, file_path, page_count, character_count, upload_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                file_name,
                file_path,
                page_count,
                character_count,
                upload_date,
            )
        )

        document_id = cursor.lastrowid

        stored_chunks = []

        # Insert chunks
        for chunk_number, chunk in enumerate(chunks, start=1):

            cursor.execute(
                """
                INSERT INTO chunks
                (
                    document_id,
                    chunk_number,
                    page_number,
                    chunk_text,
                    character_count
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    chunk_number,
                    chunk["page_number"],
                    chunk["text"],
                    len(chunk["text"]),
                )
            )

            stored_chunks.append(
                {
                    "id": cursor.lastrowid,
                    "document_id": document_id,
                    "chunk_number": chunk_number,
                    "page_number": chunk["page_number"],
                    "text": chunk["text"],
                }
            )

        # Commit document and chunks together
        connection.commit()

        return document_id, stored_chunks

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
def chunk_text(pages, chunk_size=1000):
    chunks = []

    for page in pages:
        page_number = page["page_number"]
        paragraphs = page["text"].split("\n")

        current_chunk = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()

            if not paragraph:
                continue

            if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
                current_chunk += paragraph + "\n"

            else:
                if current_chunk:
                    chunks.append({
                        "page_number": page_number,
                        "text": current_chunk.strip()
                    })

                current_chunk = paragraph + "\n"

        if current_chunk:
            chunks.append({
                "page_number": page_number,
                "text": current_chunk.strip()
            })

    return chunks
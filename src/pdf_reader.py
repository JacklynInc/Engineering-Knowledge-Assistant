import pymupdf


def read_pdf(pdf_path):
    with pymupdf.open(pdf_path) as document:

        pages = []

        for page_number, page in enumerate(document, start=1):
            pages.append({
                "page_number": page_number,
                "text": page.get_text()
             })

            page_count = len(document)

    return pages, page_count
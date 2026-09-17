from pathlib import Path

import streamlit as st

from src.database import (
    get_all_documents,
    get_document_by_path,
)
from src.ingestion import ingest_pdf
from src.rag import answer_question


st.set_page_config(
    page_title="Engineering Knowledge Assistant",
    page_icon="🔧",
    layout="wide",
)


st.title("🔧 Engineering Knowledge Assistant")

st.write(
    "Ask questions about engineering documents and get "
    "answers grounded in the available source material."
)


# ---------------------------------------------------------
# Document upload
# ---------------------------------------------------------

st.subheader("Add an engineering document")

uploaded_file = st.file_uploader(
    "Upload a PDF manual, SOP, or technical document",
    type=["pdf"],
)


if uploaded_file is not None:

    if st.button("Upload document"):

        upload_dir = Path("data/pdfs")
        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            upload_dir / Path(uploaded_file.name).name
        ).resolve()

        existing_document = get_document_by_path(
            str(file_path)
        )

        if existing_document:

            st.warning(
                "This document is already in the knowledge base."
            )

        elif file_path.exists():

            st.warning(
                "A file with this name already exists. "
                "Please rename the PDF and try again."
            )

        else:

            try:
                # Save the uploaded file
                file_path.write_bytes(
                    uploaded_file.getbuffer()
                )

                # Process the document
                with st.spinner(
                    "Processing document..."
                ):
                    result = ingest_pdf(
                        str(file_path)
                    )

                st.success(
                    f"Successfully added "
                    f"{result['file_name']} "
                    f"({result['page_count']} pages, "
                    f"{result['chunk_count']} chunks)."
                )

                st.rerun()

            except Exception as error:

                # Remove uploaded file if processing fails
                file_path.unlink(
                    missing_ok=True
                )

                st.error(
                    f"Document processing failed: {error}"
                )


# ---------------------------------------------------------
# Document selection
# ---------------------------------------------------------

documents = get_all_documents()

if not documents:

    st.error(
        "No engineering documents are available."
    )

    st.stop()


document_options = {
    document["file_name"]: document["id"]
    for document in documents
}


selected_document = st.selectbox(
    "Select an engineering document:",
    options=list(document_options.keys()),
)


selected_document_id = document_options[
    selected_document
]


# ---------------------------------------------------------
# Question and answer
# ---------------------------------------------------------

with st.form("question_form"):

    question = st.text_input(
        "Ask an engineering question:",
        placeholder=(
            "e.g. What is response surface methodology?"
        ),
    )

    ask = st.form_submit_button("Ask")


if ask:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching the document..."
        ):

            result = answer_question(
                question,
                document_id=selected_document_id,
            )

        st.subheader("Answer")

        st.write(
            result["answer"]
        )

        if result["sources"]:

            st.subheader("Sources")

            for source in result["sources"]:

                with st.expander(
                    f"📄 {source['file_name']} — "
                    f"Page {source['page']} — "
                    f"Similarity: {source['score']:.4f}"
                ):

                    st.write(source["text"])
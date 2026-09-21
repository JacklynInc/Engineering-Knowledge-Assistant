from pathlib import Path

import streamlit as st

from src.database import (
    get_all_documents,
    get_document_by_path,
)
from src.ingestion import ingest_pdf
from src.rag import answer_question


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Engineering Knowledge Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1 {
        letter-spacing: -0.03em;
        font-weight: 700;
    }

    h2 {
        margin-top: 1.8rem;
    }

    h3 {
        margin-top: 1.5rem;
    }

    [data-testid="stMetric"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
        background: #ffffff;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.25rem;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    [data-testid="stFileUploader"] {
        border-radius: 10px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.header("🔧 Engineering Knowledge Assistant")

st.caption(
    "Ask questions about engineering manuals, SOPs and technical "
    "documents using retrieval-augmented generation."
)

st.divider()


# =========================================================
# SIDEBAR — DOCUMENT MANAGEMENT
# =========================================================

with st.sidebar:

    st.header("📚 Knowledge Base")

    st.caption(
        "Upload an engineering PDF to add it to the knowledge base."
    )

    uploaded_file = st.file_uploader(
        "Select PDF document",
        type=["pdf"],
    )

    if uploaded_file is not None:

        if st.button(
            "➕ Add Document",
            use_container_width=True,
        ):

            upload_dir = Path("data/pdfs")

            upload_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path = (
                upload_dir
                / Path(uploaded_file.name).name
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

                    file_path.write_bytes(
                        uploaded_file.getbuffer()
                    )

                    with st.spinner(
                        "Processing document..."
                    ):

                        result = ingest_pdf(
                            str(file_path)
                        )

                    st.success(
                        f"Added {result['file_name']} "
                        f"({result['page_count']} pages, "
                        f"{result['chunk_count']} chunks)."
                    )

                    st.rerun()

                except Exception as error:

                    file_path.unlink(
                        missing_ok=True
                    )

                    st.error(
                        f"Document processing failed: {error}"
                    )


# =========================================================
# LOAD DOCUMENTS
# =========================================================

documents = get_all_documents()


if not documents:

    st.info(
        "No engineering documents are available yet. "
        "Upload a PDF from the sidebar to get started."
    )

    st.stop()


# =========================================================
# DOCUMENT SELECTION
# =========================================================

st.subheader("📄 Select Document")

document_options = {
    document["file_name"]: document["id"]
    for document in documents
}

selected_document = st.selectbox(
    "Choose the engineering document you want to query.",
    options=list(document_options.keys()),
)

selected_document_id = document_options[
    selected_document
]


# =========================================================
# DOCUMENT INFORMATION
# =========================================================

selected_document_data = next(
    document
    for document in documents
    if document["id"] == selected_document_id
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Document",
        value=selected_document_data["file_name"],
    )

with col2:
    st.metric(
        label="Pages",
        value=selected_document_data["page_count"],
    )

with col3:
    st.metric(
        label="Characters Indexed",
        value=f"{selected_document_data['character_count']:,}",
    )


# =========================================================
# QUESTION AREA
# =========================================================

st.subheader("💬 Ask the Engineering Assistant")

with st.form("question_form"):

    question = st.text_input(
        "Engineering question",
        placeholder=(
            "e.g. What is response surface methodology?"
        ),
    )

    ask = st.form_submit_button(
        "🔍 Search & Answer",
        use_container_width=True,
    )


# =========================================================
# ANSWER
# =========================================================

if ask:

    if not question.strip():

        st.warning(
            "Please enter an engineering question."
        )

    else:

        with st.spinner(
            "Searching the knowledge base and generating an answer..."
        ):

            result = answer_question(
                question,
                document_id=selected_document_id,
            )

        st.subheader("💡 Answer")

        st.write(
            result["answer"]
        )


        # =================================================
        # SOURCES
        # =================================================

        if result["sources"]:

            st.subheader("📚 Sources")

            st.caption(
                "Document sections retrieved to support the answer."
            )

            for source in result["sources"]:

                with st.expander(
                    f"📄 Page {source['page']}  •  "
                    f"Similarity {source['score']:.4f}"
                ):

                    st.write(
                        f"**Document:** {source['file_name']}"
                    )

                    st.write(
                        f"**Chunk:** {source['chunk']}"
                    )

                    st.divider()

                    st.write(
                        source["text"]
                    )

        else:

            st.info(
                "No supporting document sections were retrieved."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Engineering Knowledge Assistant • "
    "Python • RAG • OpenAI • Qdrant • SQLite"
)
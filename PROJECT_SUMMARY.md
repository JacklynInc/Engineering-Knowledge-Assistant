# Engineering Knowledge Assistant — Project Summary

## 1. Project Overview

The Engineering Knowledge Assistant is a Python-based AI application that allows users to upload engineering manuals, SOPs, and technical documents and ask questions about their contents in natural language.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant document sections before generating an answer. This keeps responses grounded in the available engineering source material and provides page-level source references.

---

## 2. Project Objectives

The project was designed to:

- Build an end-to-end RAG application.
- Process engineering PDF documents automatically.
- Preserve document and page metadata.
- Store structured document information in SQLite.
- Generate semantic embeddings using the OpenAI API.
- Store and search embeddings using Qdrant.
- Retrieve relevant engineering information using semantic similarity.
- Generate answers grounded in retrieved document context.
- Provide page-aware source references.
- Build a usable Streamlit interface.
- Evaluate retrieval and RAG behaviour with test cases.
- Develop practical AI engineering and software engineering skills.

---

## 3. System Architecture

```text
Engineering PDF
      ↓
PDF Text Extraction
      ↓
Text Cleaning
      ↓
Page-Aware Chunking
      ↓
SQLite
      ↓
OpenAI Embeddings
      ↓
Qdrant Vector Database
      ↓
Semantic Retrieval
      ↓
Relevant Chunks
      ↓
LLM
      ↓
Grounded Answer + Sources
      ↓
Streamlit Interface

## 5. End-to-End RAG Pipeline

The application follows this workflow:

### Step 1 — Document Upload

The user uploads an engineering PDF through the Streamlit interface.

### Step 2 — PDF Text Extraction

PyMuPDF extracts text from each page while preserving page numbers.

### Step 3 — Text Cleaning

Extracted text is cleaned before further processing.

### Step 4 — Chunking

The document is divided into smaller page-aware text chunks.

Each chunk retains:

- Document ID
- Chunk number
- Page number
- Chunk text
- Character count

### Step 5 — Relational Storage

Document and chunk metadata are stored in SQLite.

### Step 6 — Embedding Generation

Each chunk is converted into a vector embedding using:

`text-embedding-3-small`

### Step 7 — Vector Storage

The generated embeddings are stored in Qdrant.

The Qdrant collection uses cosine similarity for semantic search.

### Step 8 — User Question

The user asks a question in natural language.

### Step 9 — Query Embedding

The question is converted into an embedding using the same embedding model.

### Step 10 — Semantic Retrieval

Qdrant searches for chunks that are semantically similar to the question.

Retrieval can be restricted to the selected document.

### Step 11 — Context Construction

The most relevant retrieved chunks are assembled into a context window.

### Step 12 — LLM Generation

The retrieved context and question are passed to the language model.

The model is instructed to answer using only the supplied document context.

### Step 13 — Source Attribution

The application displays the retrieved document sections, including:

- Document name
- Page number
- Chunk number
- Similarity score
- Retrieved text


---

## 6. Technology Stack

### Programming

- Python 3.14.4
- SQLite
- Streamlit

### AI and RAG

- OpenAI API
- `text-embedding-3-small`
- GPT-5.6 Luna
- Retrieval-Augmented Generation
- Vector embeddings
- Semantic search
- Prompt-based grounding

### Vector Database

- Qdrant

### Document Processing

- PyMuPDF
- PDF text extraction
- Text cleaning
- Page-aware chunking

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Python virtual environment


---

## 7. Project Structure

```text
Engineering-Knowledge-Assistant/
│
├── .venv/
│
├── data/
│   ├── pdfs/
│   ├── database/
│   ├── embeddings/
│   └── exports/
│
├── screenshots/
│   ├── assistant-demo.png
│   └── assistant-demo1.png
│
├── src/
│   ├── pdf_reader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── database.py
│   ├── embedding.py
│   ├── vector_database.py
│   ├── rag.py
│   ├── llm.py
│   └── ingestion.py
│
├── tests/
│   ├── __init__.py
│   ├── test_database_transaction.py
│   ├── test_rag.py
│   ├── test_retrieval.py
│   └── test_vector_cleanup.py
│
├── app.py
├── main.py
├── index_vectors.py
├── README.md
├── PROJECT_SUMMARY.md
├── .env.example
└── .gitignore

## 8. Module Responsibilities

### `pdf_reader.py`

Responsible for extracting text from PDF documents while preserving page numbers.

### `text_cleaner.py`

Responsible for basic normalization of extracted document text.

### `chunker.py`

Responsible for dividing page content into manageable text chunks while preserving page metadata.

### `database.py`

Responsible for:

- Creating SQLite tables
- Storing documents
- Storing chunks
- Retrieving documents
- Retrieving chunks
- Deleting documents
- Managing transactional document ingestion

### `embedding.py`

Responsible for generating OpenAI embeddings for:

- Document chunks
- User queries

### `vector_database.py`

Responsible for:

- Creating the Qdrant collection
- Storing embeddings
- Performing semantic search
- Filtering retrieval by document
- Removing vectors associated with deleted documents

### `ingestion.py`

Coordinates the complete document ingestion workflow.

Processing flow:

    PDF
     ↓
    Extraction
     ↓
    Cleaning
     ↓
    Chunking
     ↓
    SQLite
     ↓
    Embeddings
     ↓
    Qdrant

It also handles cleanup if downstream processing fails.

### `rag.py`

Coordinates the question-answering workflow.

Processing flow:

    Question
     ↓
    Embedding
     ↓
    Qdrant Retrieval
     ↓
    SQLite Chunk Lookup
     ↓
    Context Construction
     ↓
    LLM
     ↓
    Answer + Sources

### `llm.py`

Responsible for communicating with the OpenAI Responses API and generating answers grounded in the retrieved document context.

### `app.py`

Provides the Streamlit user interface for:

- Document selection
- PDF upload
- Question input
- Answer display
- Source display
- Similarity scores

## 9. Database Design

The relational database contains two main tables.

### Documents

Stores document-level information:

    documents
    ├── id
    ├── file_name
    ├── file_path
    ├── page_count
    ├── character_count
    └── upload_date

### Chunks

Stores individual document sections:

    chunks
    ├── id
    ├── document_id
    ├── chunk_number
    ├── page_number
    ├── chunk_text
    └── character_count

The relationship is:

    Document
       │
       ├── Chunk 1
       ├── Chunk 2
       ├── Chunk 3
       └── ...

## 10. Vector Database Design

Qdrant stores the semantic representation of document chunks.

Each vector contains metadata such as:

- `document_id`
- `chunk_number`
- `page_number`

The project uses:

- Collection: `engineering_chunks`
- Vector size: `1536`
- Distance metric: `Cosine similarity`

This allows natural-language questions to be matched against document content based on semantic similarity rather than exact keyword matching.

## 11. Key Engineering Decisions

### SQLite + Qdrant

SQLite is used for structured document and chunk metadata, while Qdrant is used for vector similarity search.

This separates relational data management from semantic retrieval and allows each database to handle the type of data it is designed for.

### Page-Aware Chunks

Each chunk retains its original page number.

This makes retrieved information traceable to the original engineering document and allows the application to provide page-level source references.

### Document-Aware Retrieval

The retrieval layer can restrict semantic searches to the selected document.

This prevents unrelated documents from being returned when the user is querying a particular source.

### Transaction-Safe Database Ingestion

Document and chunk insertion can be performed within a single SQLite transaction.

If a database operation fails, the transaction is rolled back.

This prevents partially inserted document records.

### Vector Cleanup

If embedding generation or vector insertion fails after database insertion, the associated document and vectors are removed.

This reduces the possibility of inconsistent state between SQLite and Qdrant.

### Grounded LLM Generation

The language model receives the retrieved document context and is explicitly instructed to answer using that context.

The system also instructs the model not to invent technical information or page numbers.

### Cost-Conscious API Usage

The architecture was designed to minimize unnecessary OpenAI API usage.

Embeddings are generated during document ingestion rather than repeatedly.

At question time, API usage is limited to:

1. Query embedding generation
2. Final answer generation

Local components such as SQLite, Qdrant, PDF processing, and retrieval testing can be used without additional LLM calls.

## 12. Error Handling and Data Consistency

The ingestion pipeline includes protection against partial processing.

The intended workflow is:

    Database insertion
           ↓
    Embedding generation
           ↓
    Vector insertion
           ↓
        SUCCESS

If vector processing fails:

    Vector processing failure
           ↓
      Delete vectors
           ↓
      Delete document
           ↓
        Cleanup

This ensures that failed ingestion does not leave an incomplete knowledge-base entry or inconsistent data between SQLite and Qdrant.

## 13. Evaluation and Testing

The project includes dedicated evaluation scripts for different parts of the system.

### Retrieval Evaluation

`tests/test_retrieval.py`

Tests:

- Relevant engineering questions
- Expected source pages
- Wrong-document questions
- Unrelated questions
- Similarity thresholds

The evaluation successfully demonstrated that relevant questions could retrieve expected engineering content while unrelated questions were rejected.

### RAG Evaluation

`tests/test_rag.py`

Tests:

- Relevant engineering questions
- Generated answers
- Source pages
- No-information behaviour
- Unrelated questions

The system successfully produced grounded answers for relevant questions and returned a controlled no-information response when relevant content could not be retrieved.

### Database Transaction Test

`tests/test_database_transaction.py`

Tests:

- Document insertion
- Chunk insertion
- Database retrieval
- Cleanup

The transaction test successfully confirmed that document and chunk records could be created and removed correctly.

### Vector Cleanup Test

`tests/test_vector_cleanup.py`

Tests the vector deletion functionality used during document cleanup.

## 14. Evaluation Results

The retrieval evaluation produced successful results for the implemented test cases.

### Response Surface Methodology

    Document ID: 7
    Top similarity score: 0.7245
    Retrieved pages: 4, 5, 14
    Expected page: 5
    Result: PASS

### Oil Well Abandonment

    Document ID: 8
    Top similarity score: 0.6771
    Retrieved pages: 3, 4
    Expected page: 3
    Result: PASS

### Wrong Document

    Question:
    What is response surface methodology?

    Document:
    Oil well abandonment document

    Top similarity score:
    0.2354

    Expected source page:
    Not retrieved

    Result:
    PASS

### Unrelated Question

    Question:
    What is the capital of Germany?

    Top similarity score:
    0.0356

    Result:
    PASS

The RAG evaluation also passed for:

- Grounded engineering answers
- Correct source retrieval
- Unrelated questions
- Questions where information was unavailable

## 15. Engineering Challenges Solved

During development, several practical issues were encountered and resolved.

### Python Environment

The project initially encountered issues with the Python environment and virtual environment configuration.

The environment was recreated cleanly and dependencies were installed inside the project virtual environment.

### PyMuPDF API Changes

The PDF reader initially used an older import approach.

The implementation was updated to use:

    import pymupdf

This removed the deprecation warning associated with the previous import style.

### SQLite Document Lifecycle

The database layer required careful handling of:

- Document insertion
- Chunk insertion
- Document deletion
- Chunk deletion
- Transaction rollback

This resulted in a more robust ingestion architecture.

### Qdrant Filtering

The project encountered issues around Qdrant filter construction and document-specific retrieval.

The filtering logic was updated to use Qdrant's `Filter`, `FieldCondition`, and `MatchValue` models correctly.

### Qdrant Local Persistence

The project uses a local Qdrant database.

Development exposed lifecycle and shutdown warnings from the Qdrant client. These were distinguished from actual application failures so that functional problems were not confused with client shutdown behaviour.

### OpenAI API Authentication

The project encountered an API authentication issue during development.

The API key was regenerated and the environment configuration was corrected.

The secret was kept outside the Git repository using `.env`.

### OpenAI API Billing

The project also required configuring API billing before embedding generation could be tested successfully.

The application was subsequently tested successfully with the OpenAI API.

### Streamlit State

The application required careful handling of:

- Uploaded files
- Existing documents
- Reruns
- Document selection
- Question submission

The final interface provides a stable workflow for document selection and querying.

### Git and GitHub

The project was developed under Git version control and pushed to GitHub.

The repository contains the source code, documentation, screenshots, and configuration example while sensitive local files remain excluded.

## 16. Security and Configuration

The actual OpenAI API key is stored locally in:

    .env

The `.env` file is excluded from Git through `.gitignore`.

A safe configuration example is provided through:

    .env.example

Example:

    OPENAI_API_KEY=your_api_key_here

This allows another developer to understand the required configuration without exposing the actual secret.

Sensitive local files, databases, and generated data are excluded from the public repository through `.gitignore`.

## 17. Cost Optimization Approach

Because API usage has a direct cost, the project was deliberately designed to avoid unnecessary LLM calls.

The main principles were:

- Use local SQLite for structured storage.
- Use local Qdrant for vector storage.
- Generate embeddings during ingestion.
- Reuse stored embeddings.
- Use retrieval before generation.
- Avoid LLM calls during basic application testing.
- Use deterministic and local tests where possible.
- Use a smaller embedding model.
- Keep retrieved context controlled.

This approach provides a practical balance between AI capability and API cost.

## 18. Skills Demonstrated

### Python Development

- Modular Python architecture
- Functions
- Data structures
- File processing
- Exception handling
- Database integration
- Virtual environments
- API integration

### AI Engineering

- LLM integration
- Embeddings
- Retrieval-Augmented Generation
- Prompt engineering
- Context construction
- Grounded generation
- Semantic retrieval
- Similarity search

### Data Engineering

- SQLite
- Relational data modelling
- Metadata management
- Database transactions
- Data cleanup
- Vector databases

### AI Application Development

- PDF ingestion
- Semantic search
- Retrieval pipelines
- RAG pipelines
- Streamlit application development
- AI evaluation

### Software Engineering

- Git
- GitHub
- Testing
- Debugging
- Documentation
- Separation of concerns
- Error handling
- Data consistency
- Configuration management

## 19. What This Project Demonstrates

This project demonstrates practical experience building an AI application rather than simply consuming an AI tool.

The project connects several engineering layers:

    Engineering Domain Knowledge
                +
              Python
                +
       Document Processing
                +
            Databases
                +
          Vector Search
                +
               RAG
                +
              LLMs
                +
     Application Development

The result is a working engineering-focused AI knowledge system.

## 20. Current Limitations

The current implementation is intentionally a portfolio prototype rather than a production deployment.

Current limitations include:

- No OCR for scanned documents
- Basic page-aware chunking
- No hybrid keyword/vector retrieval
- No dedicated reranking model
- Local Qdrant storage
- No authentication
- No cloud deployment
- Limited automated evaluation dataset
- No production monitoring
- Single-user Streamlit workflow

These limitations are documented as potential future development rather than blockers to the current project milestone.

## 21. Future Improvements

Potential future development includes:

### Document Intelligence

- OCR for scanned PDFs
- Table extraction
- Image and diagram extraction
- Better document structure detection
- Section-aware chunking

### Retrieval

- Hybrid keyword + vector search
- Query expansion
- Reranking
- Improved metadata filtering
- Adaptive retrieval thresholds

### RAG

- Better context selection
- Context compression
- Citation validation
- Automated hallucination evaluation
- Multi-document reasoning

### Infrastructure

- Docker
- Cloud deployment
- API backend
- Authentication
- Persistent hosted vector database
- Production monitoring

### Evaluation

- Larger evaluation datasets
- Retrieval precision and recall
- Answer faithfulness
- Citation accuracy
- Automated regression testing

## 22. Portfolio Relevance

The project demonstrates the ability to build an AI-powered engineering application from the document ingestion layer through semantic retrieval, LLM generation, evaluation, and user interface development.

It combines:

**Engineering knowledge + Python + AI + RAG + databases + vector search + application development.**

The project is particularly relevant to roles involving:

- AI Engineering
- Python Development
- AI Automation
- RAG Systems
- Document Intelligence
- Technical Software
- Industrial AI
- Engineering Data
- Applied AI
- Intelligent Automation

## 24. GitHub Repository

**Repository:**

https://github.com/JacklynInc/Engineering-Knowledge-Assistant

The repository includes:

- Source code
- Test suite
- README documentation
- Project summary
- Screenshots
- Environment configuration example
- Git history

Sensitive configuration files and local databases are excluded through `.gitignore`.

## 25. Final Project Outcome

The Engineering Knowledge Assistant successfully evolved from a basic document-processing concept into a functional AI engineering application.

The completed system demonstrates the complete lifecycle of a practical RAG application:

    Engineering Document
            ↓
    Document Processing
            ↓
    Structured Storage
            ↓
    Vector Embeddings
            ↓
    Semantic Retrieval
            ↓
    Context Grounding
            ↓
    LLM Generation
            ↓
    Source Attribution
            ↓
    User Interface
            ↓
    Evaluation

The project provided practical experience across:

- AI engineering
- Python development
- Document processing
- Vector databases
- Relational databases
- RAG architecture
- API integration
- Testing
- Debugging
- Git/GitHub
- Application development

## 26. Project Completion Checklist

- [x] Project concept defined
- [x] Python environment configured
- [x] Git repository created
- [x] GitHub repository created
- [x] PDF extraction implemented
- [x] Text cleaning implemented
- [x] Chunking implemented
- [x] SQLite database implemented
- [x] OpenAI embeddings integrated
- [x] Qdrant vector database integrated
- [x] Semantic retrieval implemented
- [x] RAG pipeline implemented
- [x] LLM answer generation implemented
- [x] Source/page retrieval implemented
- [x] Streamlit interface implemented
- [x] Document upload implemented
- [x] Retrieval evaluation implemented
- [x] RAG evaluation implemented
- [x] Database transaction testing implemented
- [x] Vector cleanup testing implemented
- [x] README completed
- [x] Screenshots added
- [x] `.env.example` added
- [x] `.gitignore` configured
- [x] Application UI polished
- [x] Changes committed to Git
- [x] Changes pushed to GitHub

## 27. Key Takeaway

The main achievement of this project is not simply building a chatbot.

It is the ability to design and implement an end-to-end **AI-powered engineering information system** in which document processing, structured storage, vector search, retrieval, LLM generation, source attribution, testing, and user interaction work together as a single application.

**Project status: COMPLETE — Portfolio Milestone Reached.**
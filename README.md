# Dev Doc Assistant
#
**Live Demo:** [https://dev-doc-assistant.netlify.app/](https://dev-doc-assistant.netlify.app/)

Dev Doc Assistant is a developer-focused documentation assistant that allows you to upload any PDF, document file, or source code and interact with it using natural language queries. Instead of manually searching through files, the system retrieves relevant sections and generates precise, context-aware explanations similar to structured documentation.

## Features
- **Document Querying:** Upload PDF or document files and query them directly using natural language. The system retrieves relevant sections and generates structured answers based only on the provided content.
- **Code Understanding:** Upload source code files and ask questions about logic, functions, or workflows. The assistant explains implementation details, dependencies, and behavior in a developer-friendly format.
- **Context-Aware Answers:** All responses are generated using retrieval-augmented generation, ensuring that answers are grounded strictly in the uploaded files for accuracy and relevance.
- **Privacy & Session Isolation:** All uploaded files are processed within an isolated session. No documents, code, or queries are permanently stored. All data is cleared once the session ends, ensuring complete privacy.

## How It Works
1. **Upload Files:** Upload any PDF, document, or source code file. The system supports multiple formats and prepares them for structured processing.
2. **Content Processing:** Files are parsed, segmented, and transformed into semantic embeddings for efficient retrieval.
3. **Ask Questions:** Submit natural language queries. The system identifies relevant sections from the uploaded content using semantic search.
4. **Contextual Response:** Generates structured, documentation-style answers grounded strictly in the retrieved content.

## Technology Stack
- **Frontend:** Angular Signals for reactive state management
- **Backend:** FastAPI for high-performance APIs
- **AI/Workflow:** LangGraph for agent workflows, vector database for semantic retrieval
- **RAG:** Retrieval-Augmented Generation pipelines for accurate, documentation-style answers

## Privacy
- All data is processed in-memory and cleared after each session.
- No files or queries are stored or reused across sessions or users.

## Connect
- [GitHub](https://github.com/PranavPatil9765)
- [LinkedIn](https://www.linkedin.com/in/pranav-patil-87397028b)
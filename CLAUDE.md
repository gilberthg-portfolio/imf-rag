# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG (Retrieval-Augmented Generation) system for analyzing IMF World Economic Outlook PDF reports using LangChain, Claude AI, and ChromaDB.

## Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Run interactive mode
python imf_rag_system.py

# Run simple demo (3 example questions)
python simple_example.py
```

## Required Environment Variables

Create `.env` file:
```
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## Architecture

**IMF_RAG_System class** (`imf_rag_system.py`):
- `load_and_process_pdf()`: Loads PDF via PyPDFLoader, splits into ~1000 char chunks with 200 char overlap using RecursiveCharacterTextSplitter, creates OpenAI embeddings, stores in ChromaDB
- `load_existing_vectorstore()`: Loads persisted ChromaDB from `./chroma_db`
- `setup_qa_chain()`: Creates LangChain RetrievalQA chain with Claude LLM and custom prompt template
- `query()`: Returns answer + source documents from top 3 relevant chunks

**Data Flow**: PDF -> PyPDF extraction -> Text chunking -> OpenAI embeddings -> ChromaDB -> Semantic search -> Claude generates answer

**Key Configuration Points**:
- Chunk size/overlap: `RecursiveCharacterTextSplitter` in `load_and_process_pdf()`
- Number of retrieved chunks: `search_kwargs={"k": 3}` in `setup_qa_chain()`
- Claude model: `ChatAnthropic(model=...)` in `__init__()`

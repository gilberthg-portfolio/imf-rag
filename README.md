# 📊 IMF RAG System - Financial Document Analysis

A production-ready **Retrieval-Augmented Generation (RAG)** system for analyzing IMF World Economic Outlook reports using semantic search and Claude AI.

## Demo

https://github.com/user-attachments/assets/1efd9200-2825-4e66-94ca-8e6c643c6866



---

## ✨ Features

- **Semantic Search** - Understands meaning, not just keywords
- **100+ Page PDF Processing** - Handles large financial documents
- **Cited Responses** - Answers include page number references
- **Persistent Vector Store** - Process once, query forever
- **Interactive CLI** - Natural language Q&A interface

---

### Prerequisites
- Python 3.12+
- API Keys: [Anthropic](https://console.anthropic.com/) 

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | Claude API (Anthropic) | Answer generation |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Text → Vector conversion (local, free) |
| **Vector DB** | ChromaDB | Similarity search & persistence |
| **PDF Processing** | PyPDF | Text extraction |
| **Framework** | LangChain | RAG orchestration |

---

## ⚙️ Configuration

### Setting up your API Key

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)

2. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

3. Open `.env` and add your key:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```



## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        IMF RAG SYSTEM                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│   PDF File   │────▶│ Text Extract │────▶│   Chunking (~200)    │
│  (100+ pgs)  │     │   (PyPDF)    │     │  ~1000 chars each    │
└──────────────┘     └──────────────┘     └──────────┬───────────┘
                                                     │
                                                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│   ChromaDB   │◀────│  Embeddings  │◀────│   Text Chunks        │
│ Vector Store │     │   (OpenAI)   │     │   + Metadata         │
└──────┬───────┘     └──────────────┘     └──────────────────────┘
       │
       │  ┌─────────────────────────────────────────────────────┐
       │  │                   QUERY FLOW                        │
       │  └─────────────────────────────────────────────────────┘
       │
       │         ┌──────────────┐     ┌──────────────────────┐
       │         │    User      │────▶│   Embed Question     │
       │         │   Question   │     │     (OpenAI)         │
       │         └──────────────┘     └──────────┬───────────┘
       │                                         │
       ▼                                         ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│  Top K=3     │◀────│  Similarity  │◀────│   Question Vector    │
│   Chunks     │     │    Search    │     │                      │
└──────┬───────┘     └──────────────┘     └──────────────────────┘
       │
       │         ┌──────────────┐     ┌──────────────────────┐
       │         │   Claude AI  │────▶│   Answer + Sources   │
       └────────▶│   (Sonnet)   │     │   with Page Refs     │
                 └──────────────┘     └──────────────────────┘
```

---

## 🔧 How It Works

### 1. Document Ingestion
The system extracts text from the IMF PDF using PyPDF, then splits it into overlapping chunks of approximately 1,000 characters with 200-character overlap to maintain context across chunk boundaries.

### 2. Embedding Generation
Each chunk is converted to a 1,536-dimensional vector using OpenAI's text-embedding-ada-002 model. These vectors capture semantic meaning, enabling similarity-based retrieval.

### 3. Vector Storage
ChromaDB stores the vectors locally with metadata (page numbers, chunk IDs). The database persists to disk, eliminating reprocessing on subsequent runs.

### 4. Semantic Retrieval
When you ask a question, it's embedded using the same model. ChromaDB performs cosine similarity search to find the 3 most relevant chunks.

### 5. Answer Generation
The retrieved chunks are passed to Claude as context, along with your question. Claude generates a comprehensive answer citing specific page numbers.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- API Keys: [Anthropic](https://console.anthropic.com/) and [OpenAI](https://platform.openai.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/imf-rag-system.git
cd imf-rag-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### Download the IMF Report

```bash
# Download the World Economic Outlook Chapter 1
curl -o imf_weo_ch1_oct2024.pdf "https://www.imf.org/-/media/files/publications/weo/2024/october/english/ch1.pdf"
```

### Run

```bash
python imf_rag_system.py
```

**First run:** Processes PDF (~2-3 minutes)  
**Subsequent runs:** Instant (loads from ChromaDB)

---

## 💬 Example Queries

```
🎤 What is the global growth forecast for 2025?
🎤 What are the main inflation risks mentioned in the report?
🎤 Compare labor market conditions across different regions
🎤 What does the report say about monetary policy?
🎤 What sectors show elevated risk according to the IMF?
```

---

## 📁 Project Structure

```
imf-rag-system/
├── assets/
│   └── demo.gif              # Demo animation
├── chroma_db/                # Vector database (auto-generated)
├── imf_rag_system.py         # Main RAG implementation
├── requirements.txt          # Python dependencies
├── .env.example              # API keys template
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration

### Customize Chunk Size
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,      # Larger = more context per chunk
    chunk_overlap=300,    # More overlap = better continuity
)
```

### Adjust Retrieved Chunks
```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Return top 5 instead of 3
)
```

### Change Claude Model
```python
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",  # Default
    # model="claude-opus-4-20250514",  # More powerful
    # model="claude-haiku-4-20250320", # Faster/cheaper
)
```

---

## 🧠 Key Concepts Demonstrated

- **RAG Pattern** - Combining retrieval with generation for accurate, grounded responses
- **Vector Embeddings** - Semantic representation of text for similarity search
- **Chunking Strategies** - Balancing context preservation with retrieval precision
- **Prompt Engineering** - Structuring context for optimal LLM responses
- **Persistence Layer** - Efficient reuse of processed documents

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

---

## 📬 Contact

**Gilberth Gutierrez-Soto ** - [LinkedIn](https://cr.linkedin.com/in/gilberth) | [Udemy Instructor](https://www.udemy.com/user/gilberthg/)

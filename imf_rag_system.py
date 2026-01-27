"""
IMF World Economic Outlook RAG System
Complete implementation with LangChain + Claude API + ChromaDB

This system allows you to:
1. Load and process the IMF WEO PDF report
2. Create embeddings and store in vector database
3. Query the document using natural language
4. Get contextually relevant answers with citations

Requirements:
- Python 3.9+
- PDF file: IMF World Economic Outlook Chapter 1 (October 2024)
"""

import os
from typing import List
from dotenv import load_dotenv

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()


class IMF_RAG_System:
    """
    Retrieval-Augmented Generation system for IMF World Economic Outlook reports
    """
    
    def __init__(self, pdf_path: str, persist_directory: str = "./chroma_db"):
        """
        Initialize the RAG system
        
        Args:
            pdf_path: Path to the IMF PDF file
            persist_directory: Directory to persist the vector database
        """
        self.pdf_path = pdf_path
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None
        
        # Initialize Claude
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        print("[OK] IMF RAG System initialized")
    
    def load_and_process_pdf(self):
        """
        Load PDF, split into chunks, create embeddings, and store in vector DB
        """
        print(f"\n[PDF] Loading PDF from: {self.pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(self.pdf_path)
        pages = loader.load()
        print(f"[OK] Loaded {len(pages)} pages")
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # ~250 words per chunk
            chunk_overlap=200,  # Overlap to maintain context
            length_function=len,
        )
        chunks = text_splitter.split_documents(pages)
        print(f"[OK] Created {len(chunks)} text chunks")
        
        # Create embeddings and vector store
        print("\n[...] Creating embeddings and vector database...")
        print("   (This may take a few minutes for large documents)")
        
        # Using HuggingFace embeddings (free, runs locally)
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"[OK] Vector database created and persisted to: {self.persist_directory}")
        
    def load_existing_vectorstore(self):
        """
        Load an existing vector database (if you've already processed the PDF)
        """
        print(f"\n[DB] Loading existing vector database from: {self.persist_directory}")
        
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings
        )
        
        print("[OK] Vector database loaded successfully")
    
    def setup_qa_chain(self):
        """
        Setup the QA chain with custom prompt
        """
        # Create custom prompt template
        template = """You are an expert economic analyst answering questions about the IMF World Economic Outlook report.

Use the following pieces of context from the report to answer the question at the end.
If you don't know the answer based on the context, say so - don't make up information.
Always cite which part of the report your answer comes from when possible.

Context from IMF Report:
{context}

Question: {question}

Detailed Answer:"""

        PROMPT = PromptTemplate(
            template=template, 
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Return top 3 most relevant chunks
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        print("[OK] QA Chain configured")
    
    def query(self, question: str):
        """
        Query the RAG system
        
        Args:
            question: Your question about the IMF report
            
        Returns:
            dict with 'answer' and 'sources'
        """
        if not self.qa_chain:
            raise Exception("QA chain not set up. Run setup_qa_chain() first.")
        
        print(f"\n[Q] Question: {question}")
        print("[...] Searching relevant sections...")
        
        # Get answer
        result = self.qa_chain.invoke({"query": question})
        
        answer = result['result']
        sources = result['source_documents']
        
        print(f"\n[A] Answer:\n{answer}\n")

        print("[Sources] (relevant sections from the report):")
        for i, doc in enumerate(sources, 1):
            print(f"\n   Source {i} (Page {doc.metadata.get('page', 'Unknown')}):")
            print(f"   {doc.page_content[:200]}...")
        
        return {
            'answer': answer,
            'sources': sources
        }


def main():
    """
    Example usage of the IMF RAG System
    """
    print("=" * 80)
    print("IMF WORLD ECONOMIC OUTLOOK - RAG SYSTEM")
    print("=" * 80)
    
    # Configuration
    PDF_PATH = "imf_weo_ch1_oct2024.pdf"  # <-- PUT YOUR PDF HERE
    
    # Initialize system
    rag = IMF_RAG_System(pdf_path=PDF_PATH)
    
    # Check if vector DB already exists
    if os.path.exists(rag.persist_directory):
        print("\n[*] Found existing vector database, loading it...")
        rag.load_existing_vectorstore()
    else:
        print("\n[*] First time setup - processing PDF...")
        rag.load_and_process_pdf()
    
    # Setup QA chain
    rag.setup_qa_chain()
    
    print("\n" + "=" * 80)
    print("SYSTEM READY - You can now ask questions about the IMF report!")
    print("=" * 80)
    
    # Example queries
    example_questions = [
        "What is the global growth forecast for 2024 and 2025?",
        "What are the main risks to the economic outlook?",
        "What does the report say about inflation trends?",
        "What are the key policy recommendations?",
        "How is the labor market performing according to the report?"
    ]
    
    print("\nExample questions you can ask:")
    for i, q in enumerate(example_questions, 1):
        print(f"   {i}. {q}")
    
    # Interactive mode
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print("Type your questions (or 'quit' to exit)")
    print("=" * 80)
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not question:
            continue
        
        try:
            rag.query(question)
        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()

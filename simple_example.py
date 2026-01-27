"""
SIMPLE EXAMPLE - IMF RAG System
Quick demonstration of how to use the system
"""

from imf_rag_system import IMF_RAG_System
import os


def simple_demo():
    """
    Simple demonstration of the RAG system
    """
    print("=" * 70)
    print("SIMPLE IMF RAG DEMO")
    print("=" * 70)
    
    # Setup
    PDF_PATH = "imf_weo_ch1_oct2024.pdf"
    
    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"\n[ERROR] ERROR: PDF not found: {PDF_PATH}")
        print("\n[INFO] Please download the PDF from:")
        print("https://www.imf.org/-/media/files/publications/weo/2024/october/english/ch1.pdf")
        print(f"\nSave it as: {PDF_PATH}")
        return
    
    # Initialize RAG system
    rag = IMF_RAG_System(pdf_path=PDF_PATH)
    
    # Load or create vector database
    if os.path.exists(rag.persist_directory):
        print("\n[OK] Loading existing database...")
        rag.load_existing_vectorstore()
    else:
        print("\n[...] First run - processing PDF (this takes 2-3 minutes)...")
        rag.load_and_process_pdf()
    
    # Setup QA chain
    rag.setup_qa_chain()
    
    print("\n" + "=" * 70)
    print("ASKING 3 EXAMPLE QUESTIONS")
    print("=" * 70)
    
    # Example questions
    questions = [
        "What is the global economic growth forecast for 2024 and 2025?",
        "What are the main risks mentioned in the report?",
        "What does the report say about inflation?",
    ]
    
    # Query each question
    for i, question in enumerate(questions, 1):
        print(f"\n{'=' * 70}")
        print(f"QUESTION {i}/{len(questions)}")
        print(f"{'=' * 70}")
        
        result = rag.query(question)
        
        print("\n[*] SUMMARY:")
        print(f"   - Answer provided with context from the report")
        print(f"   - {len(result['sources'])} source passages cited")
        
        # Optional: Save to file
        with open(f"answer_{i}.txt", "w") as f:
            f.write(f"Question: {question}\n\n")
            f.write(f"Answer:\n{result['answer']}\n\n")
            f.write("Sources:\n")
            for j, doc in enumerate(result['sources'], 1):
                f.write(f"\nSource {j} (Page {doc.metadata.get('page', '?')}):\n")
                f.write(f"{doc.page_content}\n")
        
        print(f"   - Full answer saved to: answer_{i}.txt")
    
    print("\n" + "=" * 70)
    print("[OK] DEMO COMPLETE!")
    print("=" * 70)
    print("\n[*] What you learned:")
    print("   1. How to load and process a large PDF")
    print("   2. How to query it with natural language")
    print("   3. How to get answers with citations")
    print("\n[*] Next steps:")
    print("   - Run imf_rag_system.py for interactive mode")
    print("   - Modify questions in this file")
    print("   - Try your own PDF documents")
    print("\n")


if __name__ == "__main__":
    simple_demo()

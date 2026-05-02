import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq


load_dotenv()

# Load PDF
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages  = loader.load()
    return pages

# Chunks
def create_chunks(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks")
    return chunks

# Embeddings
def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings

# Vector Store
def create_vectorstore(chunks, embeddings):
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def setup_llm():
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),  # ← .env se aayega
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )
    return llm

# Main Function 1
def process_pdf(pdf_path):
    pages       = load_pdf(pdf_path)
    chunks      = create_chunks(pages)
    embeddings  = create_embeddings()
    vectorstore = create_vectorstore(chunks, embeddings)
    return vectorstore

# Main Function 2
def get_answer_from_rag(vectorstore, question):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 8}
    )
    docs    = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    llm     = setup_llm()

    prompt = f"""You are an expert assistant helping users understand PDF documents.

Instructions:
- Answer in DETAIL using the context
- If question asks to "explain all concepts", list and explain EACH concept found
- Use simple language
- If truly not in context, say "This topic is not covered in this PDF"
- NEVER say "I don't know" if context has relevant info

Context from PDF:
{context}

Question: {question}

Detailed Answer:"""

    response = llm.invoke(prompt)
    return response.content

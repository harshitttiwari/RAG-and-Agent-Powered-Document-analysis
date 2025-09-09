# vectordb.py  (LangChain v0.3.27)

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import API_KEY

VECTOR_DB_DIR = "./chroma_db"  
COLLECTION_NAME = "document_chunks"  # ye hum 

def create_vectordb_from_docs(docs, embedding_model: str) -> Chroma: 
    """
    Creates a new Chroma vector database from documents and persists it.
    """
    print(f"🧠 Creating embeddings with model: {embedding_model}")
    embedding_function = GoogleGenerativeAIEmbeddings(google_api_key=API_KEY, model=embedding_model)
    
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=VECTOR_DB_DIR, # ye hum log ko ye batata hai ki database kaha save karna hai
        collection_name=COLLECTION_NAME, # ye hum log ko ye batata hai ki collection ka naam kya hoga
    )
    print("✅ Vector database created and saved.")
    return vectordb

def load_existing_vectordb(embedding_model: str) -> Chroma:
    """
    Loads an existing Chroma vector database from disk.
    """
    print("✅ Loading existing vector database from disk.")
    embedding_function = GoogleGenerativeAIEmbeddings(google_api_key=API_KEY, model=embedding_model)
    
    vectordb = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embedding_function,
    )
    return vectordb






# import os
# import pickle # hum  ye use is liye kar rahe hain taki hum apne embeddings ko cache kar saken aur baar-baar re-embed na karna pade
# import hashlib # ye bas ye dekhne ke liye hai ki document change hua hai ya nahi if yes to dubara embed karta hai
# from datetime import datetime   # ye hum log ko ye batane ke liye kar rahe hain ki cache kab bana tha
# from langchain_chroma import Chroma # ye humra database hai jisme embeddings store hongi
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from config import API_KEY

# # ---- constants ----
# PERSIST_DIR = "./chroma_db"
# COLLECTION_NAME = "document_chunks"
# EMBEDDING_MODEL = "models/embedding-001"
# CACHE_FILE = "vectordb_meta.pkl"      # now using pickle
# CACHE_SCHEMA_VERSION = 1          #ye hum log ko ye batane ke liye kar rahe hain ki agar hum apne cache ka format badalte hain to hum ise track kar saken


# def _get_document_hash(docs) -> str:
#     """Build a stable hash from all chunk texts."""
#     h = hashlib.sha256()
#     for d in docs:
#         # page_content is safe; metadata differences won't affect the embedding text
#         h.update(d.page_content.encode("utf-8"))
#     return h.hexdigest()


# def _load_cache():
#     """Load pickle cache if present."""
#     if not os.path.exists(CACHE_FILE):
#         return None
#     try:
#         with open(CACHE_FILE, "rb") as f:
#             return pickle.load(f)
#     except Exception:
#         # if pickle format changed or file is corrupt, ignore
#         return None


# def _save_cache(meta: dict):
#     """Persist pickle cache."""
#     with open(CACHE_FILE, "wb") as f: # File open karta hai write-binary (wb) mode me.
#         pickle.dump(meta, f, protocol=pickle.HIGHEST_PROTOCOL) #use karke dictionary (meta) ko file me likh deta hai and Highest protocol use karta hai → fast + efficient save.


# def load_vectordb():
#     """Open an existing Chroma collection with the right embedding function."""
#     embedding = GoogleGenerativeAIEmbeddings(
#         google_api_key=API_KEY,
#         model=EMBEDDING_MODEL
#     )
#     return Chroma(
#         collection_name=COLLECTION_NAME,
#         persist_directory=PERSIST_DIR,
#         embedding_function=embedding,
#     )

# def store_embeddings(docs):
#     doc_hash = _get_document_hash(docs)
#     cache = _load_cache()
#     #Yeh function decide karta hai ki embeddings reuse karni hain ya nayi banani hain.


#     # quick reuse check     (abhi work nhi kar raha hai)
#     reuse_ok = (     
#         os.path.exists(PERSIST_DIR)
#         and cache is not None
#         and cache.get("schema") == CACHE_SCHEMA_VERSION
#         and cache.get("doc_hash") == doc_hash
#         and cache.get("embedding_model") == EMBEDDING_MODEL
#         and cache.get("collection") == COLLECTION_NAME
#         and cache.get("persist_dir") == PERSIST_DIR
#     )

#     if reuse_ok:
#         print("✅ Cache hit: Loading existing ChromaDB without re-embedding...")
#         return load_vectordb()

#     # else build fresh
#     print("⚡ Cache miss: Generating embeddings for new/changed document...")
#     embedding = GoogleGenerativeAIEmbeddings(
#         google_api_key=API_KEY,
#         model=EMBEDDING_MODEL
#     )
#     vectordb = Chroma.from_documents(
#         documents=docs,
#         embedding=embedding,
#         persist_directory=PERSIST_DIR,
#         collection_name=COLLECTION_NAME,
#     )

#     meta = {
#         "schema": CACHE_SCHEMA_VERSION,
#         "saved_at": datetime.utcnow().isoformat() + "Z",
#         "doc_hash": doc_hash,
#         "embedding_model": EMBEDDING_MODEL,
#         "collection": COLLECTION_NAME,
#         "persist_dir": PERSIST_DIR,
#     }
#     _save_cache(meta)
#     print("💾 Embeddings stored and cache.pkl updated.")
#     return vectordb




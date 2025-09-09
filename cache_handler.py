# cache_handler.py
import os
import json # iska main purpose ye hai ki hum apne cache metadata ko json file mein store kar saken 
import hashlib # ye bas ye dekhne ke liye hai ki document change hua hai ya nahi if yes to dubara embed karta hai
import shutil # Python ka built-in module jo file/folder operations ke liye use hota hai example: delete karna, copy karna, move karna, etc.

# This is the single source of truth for cache metadata
CACHE_MASTER_FILE = "cache_master.json"
VECTOR_DB_DIR = "./chroma_db"

def _generate_fingerprint(file_path: str, chunk_config: dict, model_name: str) -> str:
    """
    Generates a unique fingerprint based on file content and processing configuration.
    """
    file_hash = hashlib.sha256() #sha256 ek cryptographic hash function hai jo input data ko fixed-size string mein convert karta hai
    try:
        with open(file_path, "rb") as f: # ye file ko binary mode mein read kar raha hai
            while chunk := f.read(8192): 
                file_hash.update(chunk) # ye file ke har chunk ko read karke uska hash update kar raha hai
    except FileNotFoundError:
        return "file_not_found"

    config_string = f"{chunk_config['size']}-{chunk_config['overlap']}-{model_name}" 
    
    combined_hash = hashlib.sha256() # ye
    combined_hash.update(file_hash.hexdigest().encode('utf-8')) # ye file ko 
    combined_hash.update(config_string.encode('utf-8')) # 
    
    return combined_hash.hexdigest()

def is_cache_valid(pdf_path: str, chunk_size: int, chunk_overlap: int, embedding_model: str) -> bool:
    """
    Checks if a valid cache exists by comparing fingerprints.
    """
    chunk_config = {"size": chunk_size, "overlap": chunk_overlap}
    current_fingerprint = _generate_fingerprint(pdf_path, chunk_config, embedding_model)
    
    if not os.path.exists(CACHE_MASTER_FILE):
        return False

    with open(CACHE_MASTER_FILE, "r") as f:
        try:
            cache_data = json.load(f)
        except json.JSONDecodeError:
            return False # Corrupt JSON
            
    saved_fingerprint = cache_data.get("fingerprint")
    
    return saved_fingerprint == current_fingerprint and os.path.exists(VECTOR_DB_DIR)

def save_cache_metadata(pdf_path: str, chunk_size: int, chunk_overlap: int, embedding_model: str):
    """
    Saves the new metadata to the master cache file after a successful build.
    """
    chunk_config = {"size": chunk_size, "overlap": chunk_overlap}
    current_fingerprint = _generate_fingerprint(pdf_path, chunk_config, embedding_model)
    
    new_cache_data = {
        "fingerprint": current_fingerprint,
        "source_pdf": os.path.basename(pdf_path),
        "embedding_model": embedding_model,
        "chunk_config": chunk_config,
    }
    with open(CACHE_MASTER_FILE, "w") as f:
        json.dump(new_cache_data, f, indent=2)
    print(f"💾 Saved new cache metadata to: {CACHE_MASTER_FILE}")

def clear_db_and_cache_metadata():
    """
    Deletes the vector database and the master cache file for a full rebuild.
    """
    if os.path.exists(VECTOR_DB_DIR):
        print(f"🗑️ Deleting old database at: {VECTOR_DB_DIR}")
        shutil.rmtree(VECTOR_DB_DIR)
    if os.path.exists(CACHE_MASTER_FILE):
        print(f"🗑️ Deleting old cache metadata file: {CACHE_MASTER_FILE}")
        os.remove(CACHE_MASTER_FILE)


# import os
# import json
# import hashlib
# import shutil

# # This is the single source of truth for cache metadata
# CACHE_MASTER_FILE = "cache_master.json"
# VECTOR_DB_DIR = "./chroma_db"

# def _generate_fingerprint(file_path: str, chunk_config: dict, model_name: str) -> str:
#     """
#     Generates a unique fingerprint based on file content and processing configuration.
#     """
#     file_hash = hashlib.sha256()
#     try:
#         with open(file_path, "rb") as f:
#             while chunk := f.read(8192):
#                 file_hash.update(chunk)
#     except FileNotFoundError:
#         return "file_not_found"

#     config_string = f"{chunk_config['size']}-{chunk_config['overlap']}-{model_name}"
    
#     combined_hash = hashlib.sha256()
#     combined_hash.update(file_hash.hexdigest().encode('utf-8'))
#     combined_hash.update(config_string.encode('utf-8'))
    
#     return combined_hash.hexdigest()

# def is_cache_valid(pdf_path: str, chunk_size: int, chunk_overlap: int, embedding_model: str) -> bool:
#     """
#     Checks if a valid cache exists by comparing fingerprints.
#     """
#     chunk_config = {"size": chunk_size, "overlap": chunk_overlap}
#     current_fingerprint = _generate_fingerprint(pdf_path, chunk_config, embedding_model)
    
#     if not os.path.exists(CACHE_MASTER_FILE):
#         return False

#     with open(CACHE_MASTER_FILE, "r") as f:
#         try:
#             cache_data = json.load(f)
#         except json.JSONDecodeError:
#             return False # Corrupt JSON
            
#     saved_fingerprint = cache_data.get("fingerprint")
    
#     return saved_fingerprint == current_fingerprint and os.path.exists(VECTOR_DB_DIR)

# def save_cache_metadata(pdf_path: str, chunk_size: int, chunk_overlap: int, embedding_model: str):
#     """
#     Saves the new metadata to the master cache file after a successful build.
#     """
#     chunk_config = {"size": chunk_size, "overlap": chunk_overlap}
#     current_fingerprint = _generate_fingerprint(pdf_path, chunk_config, embedding_model)
    
#     new_cache_data = {
#         "fingerprint": current_fingerprint,
#         "source_pdf": os.path.basename(pdf_path),
#         "embedding_model": embedding_model,
#         "chunk_config": chunk_config,
#     }
#     with open(CACHE_MASTER_FILE, "w") as f:
#         json.dump(new_cache_data, f, indent=2)
#     print(f"💾 Saved new cache metadata to: {CACHE_MASTER_FILE}")

# def clear_db_and_cache_metadata():
#     """
#     Deletes the vector database and the master cache file for a full rebuild.
#     """
#     if os.path.exists(VECTOR_DB_DIR):
#         print(f"🗑️ Deleting old database at: {VECTOR_DB_DIR}")
#         shutil.rmtree(VECTOR_DB_DIR)
#     if os.path.exists(CACHE_MASTER_FILE):
#         print(f"🗑️ Deleting old cache metadata file: {CACHE_MASTER_FILE}")
#         os.remove(CACHE_MASTER_FILE)

# import os
# import pickle
# import shutil  # Python ka built-in module jo file/folder operations ke liye use hota hai example: delete karna, copy karna, move karna, etc.

# CACHE_FILE = "chunks_cache.pkl"
# CACHE_SCHEMA_VERSION = "v1"
# CHROMA_DIR = "chroma_db"

# def save_cache(chunks):
#     cache_obj = {
#         "schema": CACHE_SCHEMA_VERSION,
#         "chunks": chunks
#     }
#     with open(CACHE_FILE, "wb") as f:
#         pickle.dump(cache_obj, f)
#     print(f"✅ Saved cache to {CACHE_FILE}")


# def load_cache():
#     if not os.path.exists(CACHE_FILE):
#         return None
#     with open(CACHE_FILE, "rb") as f:
#         cache_obj = pickle.load(f)

#     # Old format (just a list)
#     if isinstance(cache_obj, list):
#         print("⚠️ Old cache format detected, ignoring cache.")
#         return None

#     # New format with schema
#     if cache_obj.get("schema") != CACHE_SCHEMA_VERSION:
#         print("⚠️ Cache schema mismatch, ignoring cache.")
#         return None

#     return cache_obj


# def clear_cache(mode="full"):
#     """
#     Clears cache and/or vector database.
#     mode:
#         "full" - delete both cache.pkl and chroma_db
#         "soft" - delete only chroma_db
#     """
#     if mode == "full" and os.path.exists(CACHE_FILE):
#         os.remove(CACHE_FILE)
#         print("🗑️ Deleted cache.pkl")

#     if os.path.exists(CHROMA_DIR):
#         shutil.rmtree(CHROMA_DIR)
#         print("🗑️ Deleted chroma_db directory")

#     print(f"✅ Cache clear ({mode} mode) complete.")



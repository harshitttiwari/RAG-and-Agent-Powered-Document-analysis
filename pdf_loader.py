# # pdf_loader.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_pdf(path: str, chunk_size: int, chunk_overlap: int):
    """
    Loads a PDF and splits it into chunks based on the provided settings.
    Handles cases where the file is not found.
    """
    try:
        print(f"📄 Loading and splitting PDF from: {path}")
        loader = PyPDFLoader(path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        split_docs = splitter.split_documents(docs)
        print(f"✅ PDF split into {len(split_docs)} chunks.")
        return split_docs
        
    except ValueError as e:
        # This catches the error from PyPDFLoader when the path is invalid.
        print(f"❌ Error: The file path '{path}' is not valid or the file could not be accessed.") 
        print(f"   (Underlying error: {e})") 
        return None
        
    except Exception as e:
        # A general catch-all for other unexpected errors.
        print(f"An unexpected error occurred: {e}")
        return None


# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter


# def load_and_split_pdf(path: str, chunk_size: int, chunk_overlap: int):
#     """
#     Loads a PDF and splits it into chunks based on the provided settings.
#     """
#     print(f"📄 Loading and splitting PDF: {path}")
#     loader = PyPDFLoader(path)
#     docs = loader.load()        
    
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap
#     )
#     return splitter.split_documents(docs)

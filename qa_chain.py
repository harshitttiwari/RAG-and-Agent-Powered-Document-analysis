# qa_chain.py
from langchain.chains import RetrievalQA 
from langchain.retrievers.multi_query import MultiQueryRetriever
from llm_config import llm
import logging 

logging.basicConfig() # 
logging.getLogger("langchain.retrieval.multi_query").setLevel(logging.INFO) 

def get_qa_chain(vectordb, k=12, chain_type="stuff"): 
    """
    Creates a advanced QA chain using a tuned MultiQueryRetriever.
    """
    # Create MultiQueryRetriever
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=vectordb.as_retriever(search_kwargs={'k': k}),
        llm=llm
    )

    # Use the new, more powerful retriever in the QA chain
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever_from_llm,
        return_source_documents=True
    )



# from langchain.chains import RetrievalQA
# from llm_config import llm

# def get_qa_chain(vectordb, k=4, chain_type="stuff"):
# # In qa_chain.py
#     """
#     Creates a more advanced and configurable RetrievalQA chain.

#     Args:
#         vectordb: The Chroma vector database instance.
#         k (int): The number of relevant documents to retrieve.
#         chain_type (str): The type of chain to use (e.g., "stuff", "map_reduce").

#     Returns:
#         A RetrievalQA chain that returns source documents.
#     """
#     retriever = vectordb.as_retriever(search_kwargs={'k': k})
    
#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type=chain_type,
#         retriever=retriever,
#         return_source_documents=True # iska main purpose ye hai ki hum apne answer ke sath source documents bhi le saken
#     )

 

# # from langchain.chains import RetrievalQA
# # from llm_config import llm

# # def get_qa_chain(vectordb):
# #     retriever = vectordb.as_retriever()
# #     return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

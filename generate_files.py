# import os
# # Use current working directory
# folder = os.getcwd()

# files_content = {
#     "app.py": '''from qa_chain import run_qa_chain

# if __name__ == "__main__":
#     query = input("Ask a question about the document: ")
#     result = run_qa_chain(query)
#     print("Answer:", result)
# ''',

#     "config.py": '''# Store Gemini or other API keys and constants here
# GEMINI_API_KEY = "your_gemini_api_key_here"

# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 200
# ''',

#     "llm_config.py": '''from langchain.llms import OpenAI
# from config import GEMINI_API_KEY

# def load_llm():
#     return OpenAI(openai_api_key=GEMINI_API_KEY)
# ''',

#     "vectordb.py": '''from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings
# import os

# def get_vectorstore():
#     persist_directory = "db"
#     embedding = OpenAIEmbeddings()
#     vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
#     return vectordb
# ''',

#     "pdf_loader.py": '''from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from config import CHUNK_SIZE, CHUNK_OVERLAP

# def load_and_split_pdf(file_path):
#     loader = PyPDFLoader(file_path)
#     documents = loader.load()
#     splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
#     return splitter.split_documents(documents)
# ''',

#     "qa_chain.py": '''from langchain.chains import RetrievalQA
# from llm_config import load_llm
# from vectordb import get_vectorstore

# def run_qa_chain(question):
#     llm = load_llm()
#     vectordb = get_vectorstore()
#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())
#     return qa.run(question)
# ''',

#     "auto_questioner.py": '''# This file generates follow-up or argument-style questions (dummy for now)

# def generate_follow_up(question):
#     return f"What do you mean by: {question}?"

# def generate_argument_style(question):
#     return f"Can you defend this idea: {question}?"
# ''',

#     "agent_tools.py": '''# This file is for adding tools like SerpAPI or Tavily search
# # Example: dummy tool function

# def web_search(query):
#     return f"Simulated web search result for '{query}'"
# ''',

#     "requirements.txt": '''langchain
# pypdf
# chromadb
# openai
# google-search-results
# tavily-python
# python-dotenv
# '''
# }

# # Write all files in the current directory
# for filename, content in files_content.items():
#     path = os.path.join(folder, filename)
#     with open(path, "w", encoding="utf-8") as f:
#         f.write(content)

# print("✅ All files generated successfully in:", folder)



# app.py
import argparse
import os   
from langchain.agents import Tool
from pdf_loader import load_and_split_pdf
from cache_handler import is_cache_valid, save_cache_metadata, clear_db_and_cache_metadata
from vectordb import create_vectordb_from_docs, load_existing_vectordb
from qa_chain import get_qa_chain
from agent_tools import initialize_router_agent
from auto_questioner import generate_follow_up, classify_intent, create_contextual_question
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, API_KEY

def main():
    parser = argparse.ArgumentParser(description="Professional Document Q&A App with Router Agent")
    parser.add_argument("--pdf", type=str, default="laws.pdf", help="Path to the PDF file to load.")
    parser.add_argument("--rebuild", action="store_true", help="Force a full rebuild of the database.")
    args = parser.parse_args()
    
    if not API_KEY:
        print("🔴 Error: API_KEY not found in config.py.")
        return 

    if args.rebuild:
        clear_db_and_cache_metadata()

    if is_cache_valid(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL):
        vectordb = load_existing_vectordb(EMBEDDING_MODEL)
    else:
        if not os.path.exists(args.pdf):
            print(f"🔴 Error: PDF file not found at '{args.pdf}'")
            return       
        print("⚡ Cache miss: Rebuilding database from scratch...")
         
        docs = load_and_split_pdf(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP)
        vectordb = create_vectordb_from_docs(docs, EMBEDDING_MODEL)
        save_cache_metadata(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL)

    qa_chain = get_qa_chain(vectordb)
    document_tool = Tool(
        name="Document QA System",
        func=qa_chain.invoke,
        description="Use this tool to answer questions about the loaded PDF document."
    )
    agent = initialize_router_agent(document_tool)

    # --- Main Conversational Loop ---
    print("\n✅ System ready. Ask any question.")
    
    # Initialize state for conversational memory
    last_follow_up_question = None
    
    while True: 
        user_question = input("\n🧑‍💻 Your Question (or type 'exit'):\n> ")
        if user_question.lower() == "exit":
            print("👋 Exiting. Bye.")
            break
        
        question_to_process = user_question
        
        # --- Intent Classification Step ---
        if last_follow_up_question:
            intent = classify_intent(user_question, last_follow_up_question)
            print(f"DEBUG: Classified intent as '{intent}'") # Optional: for debugging
            
            if intent == "answer_to_follow_up":
                question_to_process = create_contextual_question(user_question, last_follow_up_question)
                print(f"DEBUG: New contextual question is: '{question_to_process}'") # Optional: for debugging

        try:
            # The agent now processes the context-aware question
            response_dict = agent.invoke({"input": question_to_process})
            agent_answer = response_dict.get("output", "No answer found.").strip()
            print("\n🤖 Agent Answer:\n", agent_answer)
            
            intermediate_steps = response_dict.get("intermediate_steps", [])
            for action, result in intermediate_steps:
                if action.tool == "Document QA System":
                    source_docs = result.get("source_documents", [])
                    if source_docs:
                        print("\n--- Sources from Document ---")
                        for i, doc in enumerate(source_docs):
                            source_preview = doc.page_content[:150].replace("\n", " ") + "..."
                            print(f"[{i+1}] {source_preview}")
                        print("---------------------------")
            
            # Generate and save the new follow-up for the next turn
            follow_up = generate_follow_up(agent_answer, question_to_process)
            print("\n🤖 Follow-Up Question:\n", follow_up)
            last_follow_up_question = follow_up # Save to memory

        except Exception as e:
            print(f"🔴 An error occurred: {e}")
            last_follow_up_question = None # Reset memory on error

if __name__ == "__main__":
    main()



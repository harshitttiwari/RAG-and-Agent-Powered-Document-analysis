#app.py
import argparse 
import os
from langchain.agents import Tool
from pdf_loader import load_and_split_pdf
from cache_handler import is_cache_valid, save_cache_metadata, clear_db_and_cache_metadata
from vectordb import create_vectordb_from_docs, load_existing_vectordb
from qa_chain import get_qa_chain
from agent_tools import initialize_router_agent
from auto_questioner import generate_follow_up, classify_intent, create_contextual_question
from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    API_KEY
)

def main():
    parser = argparse.ArgumentParser(description="Professional Document Q&A App with Router Agent")
    # parser.add_argument("--pdf", type=str, default="laws.pdf", help="Path to the PDF file to load.")
    parser.add_argument("--pdf", type=str, default="UMNwriteup.pdf", help="Path to the PDF file to load.")
    parser.add_argument("--rebuild", action="store_true", help="Force a full rebuild of the database.")
    args = parser.parse_args()

    if not API_KEY or API_KEY == "hidden":
        print("🔴 Error: API_KEY not found or not set in config.py.")
        return
    
    docs = load_and_split_pdf(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP)
    if docs is None:
        # Error is handling 
        return

    if args.rebuild:
        clear_db_and_cache_metadata()

    if is_cache_valid(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL):
        vectordb = load_existing_vectordb(EMBEDDING_MODEL)
    else:
        print("⚡ Cache miss or rebuild forced: Rebuilding database from scratch...")
        vectordb = create_vectordb_from_docs(docs, EMBEDDING_MODEL)
        save_cache_metadata(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL)

    qa_chain = get_qa_chain(vectordb)

    def run_qa_and_print_sources(query: str) -> str:
        response = qa_chain.invoke(query)
        answer = response.get("result", "No answer found.")
        source_docs = response.get("source_documents", [])
        if source_docs:
            print("\n--- Sources from Document ---")
            for i, doc in enumerate(source_docs):
                source_preview = doc.page_content[:200].replace("\n", " ") + "..."
                page = doc.metadata.get('page', 'N/A')
                print(f"[{i+1}] Page {page}: {source_preview}")
            print("---------------------------")
        return answer
    
    # document_tool = Tool(
    #     name="Document QA System",
    #     func=run_qa_and_print_sources,
    #     description=f"""
    #     Use this tool as your primary and preferred source for answering questions about the provided document: '{args.pdf}'.
    #     This document contains the Supreme Court syllabus and opinion on the Google v. Oracle case,
    #     making it an authoritative source for topics like the Java SE API, copyright law, and the 'fair use' doctrine.
    #     """
    # )

    document_tool = Tool(
    name="Document QA System",
    func=run_qa_and_print_sources,
    # TAdv Des Work in All Scenarios   
    description=f"""
    This is your primary and most authoritative tool for answering questions about the document named '{os.path.basename(args.pdf)}'.
    You MUST prefer this tool over any other for questions that are directly about the content, people, events, or data within the document.
    If a question seems general but is related to the document's main subject matter, use this tool first to provide a specific, contextualized answer before attempting a general web search.
    """
    )

    agent = initialize_router_agent(document_tool)

    print("\n✅ System ready. Ask any question about the document or the web.")
    last_follow_up_question = None

    while True:
        try:
            user_question = input("\n 🧑‍💻 Your Question (or type 'exit'):\n> ")
            if user_question.lower() == "exit":
                break
            
            question_to_process = user_question
            
            if last_follow_up_question:
                intent = classify_intent(user_question, last_follow_up_question)
                if intent == "answer_to_follow_up":
                    question_to_process = create_contextual_question(user_question, last_follow_up_question)
                    print(f"\n🤖 Follow-Up Question:'{question_to_process}'")

            response_dict = agent.invoke({"input": question_to_process})
            agent_answer = response_dict.get("output", "No answer found.").strip()
            
            print("\n🤖 Agent Answer:\n", agent_answer)
            
            intermediate_steps = response_dict.get("intermediate_steps", [])
            
            if intermediate_steps and intermediate_steps[-1][0].tool == "Document QA System":
                follow_up = generate_follow_up(agent_answer, question_to_process)
                print("\n🤔 Follow-Up Question:\n", follow_up)
                last_follow_up_question = follow_up
            else:
                last_follow_up_question = None

        except Exception as e:
            print(f"🔴 An error occurred during agent execution: {e}")
            last_follow_up_question = None
        
        except KeyboardInterrupt:
             print("\n👋 Exiting due to user interruption. Bye.")
             break

if __name__ == "__main__":
    main()


# import argparse
# from langchain.agents import Tool
# from pdf_loader import load_and_split_pdf
# from cache_handler import is_cache_valid, save_cache_metadata, clear_db_and_cache_metadata
# from vectordb import create_vectordb_from_docs, load_existing_vectordb
# from qa_chain import get_qa_chain
# from agent_tools import initialize_router_agent
# from auto_questioner import generate_follow_up, classify_intent, create_contextual_question
# from config import (
#     CHUNK_SIZE, 
#     CHUNK_OVERLAP, 
#     EMBEDDING_MODEL, 
#     API_KEY
# )

# def main():
#     parser = argparse.ArgumentParser(description="Professional Document Q&A App with Router Agent")
#     parser.add_argument("--pdf", type=str, default="laws.pdf", help="Path to the PDF file to load.")
#     parser.add_argument("--rebuild", action="store_true", help="Force a full rebuild of the database.")
#     args = parser.parse_args()
    
#     if not API_KEY or API_KEY == "hidden":
#         print("🔴 Error: API_KEY not found or not set in config.py.")
#         return 

#     if args.rebuild:
#         clear_db_and_cache_metadata()

#     # Database setup
#     if is_cache_valid(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL):
#         vectordb = load_existing_vectordb(EMBEDDING_MODEL)
#     else:
#         docs = load_and_split_pdf(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP)
#         if docs is None:
#             return
#         print("⚡ Cache miss or rebuild forced: Rebuilding database from scratch...")
#         vectordb = create_vectordb_from_docs(docs, EMBEDDING_MODEL)
#         save_cache_metadata(args.pdf, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL)

#     qa_chain = get_qa_chain(vectordb)

#     # Wrapper function for the document tool
#     def run_qa_and_print_sources(query: str) -> str:
#         response = qa_chain.invoke(query)
#         answer = response.get("result", "No answer found.")
#         source_docs = response.get("source_documents", [])
#         if source_docs:
#             print("\n--- Sources from Document ---")
#             for i, doc in enumerate(source_docs):
#                 source_preview = doc.page_content[:200].replace("\n", " ") + "..."
#                 page = doc.metadata.get('page', 'N/A')
#                 print(f"[{i+1}] Page {page}: {source_preview}")
#             print("---------------------------")
#         return answer

#     # Tool Definition with assertive description
#     document_tool = Tool(
#         name="Document QA System",
#         func=run_qa_and_print_sources,
#         description=f"""
#         Use this tool as your primary and preferred source for answering questions about the provided document: '{args.pdf}'.
#         This document contains the Supreme Court syllabus and opinion on the Google v. Oracle case,
#         making it an authoritative source for topics like the Java SE API, copyright law, and the 'fair use' doctrine.
#         """
#     )
    
#     agent = initialize_router_agent(document_tool)

#     # --- Main Conversational Loop ---
#     print("\n✅ System ready. Ask any question about the document or the web.")
    
#     last_follow_up_question = None
    
#     while True: 
#         try:
#             user_question = input("\n🧑‍💻 Your Question (or type 'exit'):\n> ")
#             if user_question.lower() == "exit":
#                 break
            
#             question_to_process = user_question
            
#             if last_follow_up_question:
#                 intent = classify_intent(user_question, last_follow_up_question)
#                 if intent == "answer_to_follow_up":
#                     question_to_process = create_contextual_question(user_question, last_follow_up_question)
#                     print(f"🔄 Rephrased question: '{question_to_process}'")

#             response_dict = agent.invoke({"input": question_to_process})
#             agent_answer = response_dict.get("output", "No answer found.").strip()
#             print("\n🤖 Agent Answer:\n", agent_answer)
            
#             # This is the final, corrected logic for the follow-up question
#             intermediate_steps = response_dict.get("intermediate_steps", [])
#             if intermediate_steps and intermediate_steps[-1][0].tool == "Document QA System":
#                 follow_up = generate_follow_up(agent_answer, question_to_process)
#                 print("\n🤔 Follow-Up Question:\n", follow_up)
#                 last_follow_up_question = follow_up
#             else:
#                 last_follow_up_question = None

#         except Exception as e:
#             print(f"🔴 An error occurred during agent execution: {e}")
#             last_follow_up_question = None
        
#         except KeyboardInterrupt:
#              print("\n👋 Exiting due to user interruption. Bye.")
#              break

# if __name__ == "__main__":
#     main()




# # import argparse
# # from pdf_loader import load_and_split_pdf
# # from vectordb import store_embeddings
# # from qa_chain import get_qa_chain
# # from auto_questioner import generate_follow_up
# # from agent_tools import get_agent
# # from cache_handler import save_cache, load_cache, clear_cache


# # def main():
# #     parser = argparse.ArgumentParser(description="Document Q&A App with Smart Pickle Caching")

# #     parser.add_argument(
# #         "--rebuild", action="store_true",
# #         help="Full wipe (cache + DB)"
# #     )
# #     parser.add_argument(
# #         "--rebuild-soft", action="store_true",
# #         help="Soft wipe (DB only)"
# #     )
# #     parser.add_argument(
# #         "--pdf", type=str, default="Disaster_Ready.pdf",
# #         help="Path to the PDF file to load"
# #     )
   

# #     args = parser.parse_args()
# #     print(f"👉 Using PDF file: {args.pdf}")
# #     # Handle cache clearing
# #     if args.rebuild:
# #         clear_cache("full")
# #     elif args.rebuild_soft:
# #         clear_cache("soft")

# #     # Step 1: Load PDF chunks (from cache if available)
# #     cache_obj = load_cache()
# #     if cache_obj is not None:
# #         print("✅ Loaded chunks from cache.")
# #         chunks = cache_obj["chunks"]
# #     else:
# #         print(f"📄 Processing PDF: {args.pdf}")
# #         chunks = load_and_split_pdf(args.pdf)
# #         save_cache(chunks)


# #     # Step 2: Load or build embeddings
# #     vectordb = store_embeddings(chunks)

# #     # Step 3: Build QA chain
# #     qa_chain = get_qa_chain(vectordb)

# #     # Step 4: Initialize agent
# #     agent = get_agent()

# #     # Step 5: Main question-answer loop
# #     while True:
# #         user_question = input("\n🧑 Ask something about the document (or type 'exit'):\n ")
# #         if user_question.lower() == "exit":
# #             print("👋 Exiting. Bye.")
# #             break

# #         # 1) Ask RAG QA chain
# #         try:
# #             rag_answer = qa_chain.invoke(user_question)
# #             if not rag_answer:
# #                 result = qa_chain.invoke(user_question)
# #                 rag_answer = result.get("result") if isinstance(result, dict) else str(result)
# #         except Exception as e:
# #             print(f"⚠️ QA error: {e}")
# #             rag_answer = ""

# #         # Clean formatting
# #         rag_answer = rag_answer.strip().replace("\\n", "\n") if isinstance(rag_answer, str) else str(rag_answer)

# #         print("\n🤖 RAG Answer:\n", rag_answer)

# #         # 2) Optionally call agent for web search
# #         needs_web = any(tok in user_question.lower() for tok in [
# #             "current", "recent", "latest", "update", "search", "case law", "statute"
# #         ])
# #         if needs_web:
# #             print("\n🔎 Agent: doing web search / tool actions...")
# #             try:
# #                 agent_output = agent.run(user_question)
# #                 if isinstance(agent_output, dict):
# #                     print("\n🛠️ Agent output:\n", agent_output.get("output", agent_output))
# #                 else:
# #                     print("\n🛠️ Agent output:\n", agent_output)
# #             except Exception as e:
# #                 print("Agent error:", e)

# #         # 3) Generate follow-up question
# #         try:
# #             follow_up = generate_follow_up(rag_answer, user_question)
# #             if hasattr(follow_up, "content"):
# #                 follow_up_text = follow_up.content
# #             elif isinstance(follow_up, dict) and "result" in follow_up:
# #                 follow_up_text = follow_up["result"]
# #             else:
# #                 follow_up_text = str(follow_up)
# #             follow_up_text = follow_up_text.strip().replace("\\n", "\n")
# #         except Exception as e:
# #             follow_up_text = f"(Could not generate follow-up question: {e})"

# #         print("\n🤖 Follow-Up Question:\n", follow_up_text)


# # if __name__ == "__main__":
# #     main()

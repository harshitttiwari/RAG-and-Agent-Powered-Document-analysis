# config.py
API_KEY = "AIzaSyDfp54pCcWq-t8Wat-Y37nQ8ksgDwDNRk0"
SERPAPI_KEY = "1d9ff61c19161c59a7b1af0aded432957214a17e44cc35923853fe9b04de3513"  # Optional
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 300
EMBEDDING_MODEL = "models/embedding-001" 

# cd X:\document_analysis
# python app.py --pdf laws.pdf  
# python app.py --pdf Disaster_Ready.pdf        

            # intermediate_steps = response_dict.get("intermediate_steps", [])
            # for action, result in intermediate_steps:
            #     if action.tool == "Document QA System":
            #         source_docs = result.get("source_documents", [])
            #         if source_docs:
            #             print("\n--- Sources from Document ---")
            #             for i, doc in enumerate(source_docs):
            #                 source_preview = doc.page_content[:150].replace("\n", " ") + "..."
            #                 print(f"[{i+1}] {source_preview}")
            #             print("---------------------------")
            
            # # Generate and save the new follow-up for the next turn
            # follow_up = generate_follow_up(agent_answer, question_to_process)
            # print("\n🤖 Follow-Up Question:\n", follow_up)
            # last_follow_up_question = follow_up # Save to memory




#                 document_tool = Tool(
#     name="Document QA System",
#     func=qa_chain.invoke,
#     # This new description is far more specific and tells the agent what the document is about.
#     description=f"Authoritative source for answering questions about the provided document: '{args.pdf}'. This document contains the Supreme Court syllabus and opinion on the Google v. Oracle case regarding the Java SE API."
# )
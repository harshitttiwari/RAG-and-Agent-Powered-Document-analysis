# llm_config.py
from langchain_google_genai import ChatGoogleGenerativeAI
from config import API_KEY

llm = ChatGoogleGenerativeAI(
    # model="gemini-2.0-flash-lite",
    model="gemini-2.5-flash", # wE CAN CHANGE ACC TO OUR NEED 
    temperature=0.1,
    google_api_key=API_KEY
)


    # document_tool = Tool(
    #     name="Document QA System",
    #     func=run_qa_and_print_sources,
    #     description=f"""
    #     Use this tool as your primary and preferred source for answering questions about the provided document: '{args.pdf}'.
    #     This document contains the Supreme Court syllabus and opinion on the Google v. Oracle case,
    #     making it an authoritative source for topics like the Java SE API, copyright law, and the 'fair use' doctrine.
    #     """
    # )
    # In app.py, find and replace the document_tool creation with this:

    # In app.py, find and replace the document_tool creation with this:
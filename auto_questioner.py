# auto_questioner.py
from llm_config import llm

def generate_follow_up(summary: str, user_question: str) -> str:
    """Generates a follow-up question based on the context."""
    prompt = f"""
You are a helpful assistant. Based on this summary of a document:
\"\"\"{summary}\"\"\"

And the user's question:
\"\"\"{user_question}\"\"\"

Ask one insightful, relevant follow-up question that explores the topic further.
"""
    return llm.invoke(prompt).content.strip()

def classify_intent(user_input: str, last_follow_up: str) -> str:
    """
    Classifies the user's intent based on their input and the last follow-up question.
    """
    prompt = f"""
    Analyze the user's input in the context of the 'Last Follow-Up Question' that was asked.
    Your task is to classify the user's intent.

    Last Follow-Up Question: "{last_follow_up}"
    User Input: "{user_input}"

    Does the User Input seem like a direct response to the Last Follow-Up Question (e.g., 'yes', 'tell me more', 'explain that', 'why?'), or is it a completely new and unrelated question?

    Respond with ONLY one of the following two classifications:
    1. answer_to_follow_up
    2. new_question

    """
    response = llm.invoke(prompt).content.strip()
    
    if "answer_to_follow_up" in response:
        return "answer_to_follow_up"
    return "new_question"

def create_contextual_question(user_input: str, last_follow_up: str) -> str:
    """
    Creates a complete, standalone question by combining the user's short input
    with the context of the last follow-up question.

    This is useful when the user's reply is brief or ambiguous (e.g., "yes", "tell me more"),
    and you want to generate a full question that can be sent to a search or QA system.
    """
    prompt = f"""
    You are an expert at understanding conversation context.
    A user was asked the following question: "{last_follow_up}"
    The user responded with this short phrase: "{user_input}"

    Your task is to rephrase the user's short response into a complete, standalone question that can be sent to a search system.

    For example:
    - If the question was "Did you consider the legal implications?" and the user said "tell me more", you should generate: "Tell me more about the legal implications."
    - If the question was "Would you like a summary of Section 3?" and the user said "yes please", you should generate: "Please provide a summary of Section 3."

    Generate the complete, standalone question now.
    """
    return llm.invoke(prompt).content.strip()



# from llm_config import llm

# def generate_follow_up(summary, user_question):
#     prompt = f"""
# You are a helpful legal assistant. Based on this summary of a document:
# \"\"\"{summary}\"\"\"

# And the user's question:
# \"\"\"{user_question}\"\"\"

# Ask a follow-up question that explores or challenges the user's understanding. Your tone should be curious and slightly argumentative (in a helpful way).
# """
#     return llm.invoke(prompt).content
 
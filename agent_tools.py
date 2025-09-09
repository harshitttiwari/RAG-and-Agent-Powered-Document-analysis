# # agent_tools.py
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from config import SERPAPI_KEY
from llm_config import llm

def get_web_search_tools():
    """Returns a list of tools for web searching."""
    tools = []
    if SERPAPI_KEY and SERPAPI_KEY != "hidden":
        serp = SerpAPIWrapper(serpapi_api_key=SERPAPI_KEY)
        tools.append(
            Tool(
                name="SerpAPI",
                func=serp.run,
                description="A premium web search engine. Use this for questions about current events, or recent information."
            )
        )
    tools.append(
        Tool(
            name="DuckDuckGo",
            func=DuckDuckGoSearchRun().run,
            description="A lightweight web search engine. Use this for simple web searches."
        )
    )
    return tools

def initialize_router_agent(document_tool: Tool):
    """
    Initializes the main router agent with a toolbox.
    """
    tools = [document_tool] + get_web_search_tools()

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        # It tells the agent to return its steps.
        return_intermediate_steps=True 
    )
    print("\n✅ Router Agent initialized with the following tools:", [tool.name for tool in tools])
    return agent



# from langchain.agents import initialize_agent, AgentType, Tool
# from langchain_community.utilities import SerpAPIWrapper
# from langchain_community.tools import DuckDuckGoSearchRun
# from config import SERPAPI_KEY
# from llm_config import llm # The agent needs the LLM

# def get_web_search_tools():
#     """Returns a list of tools for web searching."""
#     tools = []
#     if SERPAPI_KEY:
#         serp = SerpAPIWrapper(serpapi_api_key=SERPAPI_KEY)
#         tools.append(
#             Tool(
#                 name="SerpAPI",
#                 func=serp.run,
#                 description="A web search engine. Use this for questions about current events, or recent information."
#             )
#         )
#     tools.append(
#         Tool(
#             name="DuckDuckGo",
#             func=DuckDuckGoSearchRun().run,
#             description="A lightweight web search engine. Use this for simple web searches."
#         )
#     )
#     return tools

# def initialize_router_agent(document_tool: Tool):
#     """
#     Initializes the main router agent with a toolbox containing the
#     document-specific tool and general web search tools.
#     """
#     # Combine the document-specific tool with the general web tools
#     tools = [document_tool]
#     web_tools = get_web_search_tools()
#     tools.extend(web_tools)

#     # Initialize the main Router Agent
#     agent = initialize_agent(
#         tools,
#         llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True
#     )
#     print("\n✅ Router Agent initialized with the following tools:", [tool.name for tool in tools])
#     return agent




# # from config import SERPAPI_KEY
# # from llm_config import llm
# # from langchain_community.utilities import SerpAPIWrapper
# # from langchain_community.tools import DuckDuckGoSearchRun
# # from langchain.agents import initialize_agent, Tool

# # def build_serpapi_tool(api_key: str):
# #     serp = SerpAPIWrapper(serpapi_api_key=api_key)
# #     return Tool(
# #         name="SerpAPI",
# #         func=serp.run,
# #         description="Search the web using SerpAPI and return top snippets."
# #     )

# # def build_duckduckgo_tool():
# #     ddg = DuckDuckGoSearchRun()
# #     return Tool(
# #         name="DuckDuckGo",
# #         func=ddg.run,
# #         description="Search the web using DuckDuckGo (lightweight)."
# #     )

# # def get_agent():
# #     tools = []
# #     if SERPAPI_KEY:
# #         tools.append(build_serpapi_tool(SERPAPI_KEY))
# #     tools.append(build_duckduckgo_tool())

# #     # initialize_agent is fine for langchain v0.3.27; agent param or agent_type may both work
# #     agent_executor = initialize_agent(
# #         tools,
# #         llm,
# #         agent="zero-shot-react-description",
# #         verbose=True
# #     )
# #     print("🔧 Agent initialized with tools:", [tool.name for tool in tools])
# #     return agent_executor


# # agent = get_agent()
# # print(agent)


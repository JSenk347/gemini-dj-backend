
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from .tools import search_spotify

def build_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") #initialize the gemini model
    tools = [search_spotify] #define the tools list
    return create_agent(llm, tools=tools) # create the agent and compile the graph

agent = build_agent()
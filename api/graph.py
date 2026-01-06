from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
#from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent #depricated yet stable. change to above line when needed
from langchain_core.prompts import ChatPromptTemplate #only needed since we are using stable version
#from langchain_core.output_parsers import StrOutputParser
from .tools import search_spotify
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an expert DJ and playlist curator. Your goal is to build the perfect playlist based on the user's request.

RULES FOR USING TOOLS:
1. NEVER just search once and dump the results. 
2. If a request has multiple parts (e.g., "Sad songs and 80s pop"), you MUST perform separate searches for each part and return a SINGLE playlist with results from each search.
3. After searching, READ the results and hand-pick only the songs that truly fit the vibe.
4. If a search returns irrelevant results, search again with a different query.
5. When you select songs for the final playlist, you MUST retain the Spotify URI for each song so we can save it later.
6. You must find a minimum of 10 songs unless the user asks for fewer.

Your final output should be a brief, friendly summary of the songs you chose and why.
""" #USE IN MODERN VERSION

# def generate_pet_name(animal_type: str) -> str:
#     llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
#     prompt_template_name = PromptTemplate( # defining a prompt template
#         input_variables=["animal_type"],
#         template="I have a {animal_type} and I want a cool name for it. suggest five cool names for my pet with no commentary"
#     )
#     output_parser = StrOutputParser()
#     chain = prompt_template_name | llm | output_parser

#     return chain.invoke({"animal_type": animal_type})

# if __name__ == "__main__":
#     print(generate_pet_name("dog"))

def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3 #play around with this val. -> 1 is TOTALLY random, -> 0 is NO randomness
        ) #initialize the gemini model
    tools = [search_spotify] #define the tools list

    # return create_agent(
    #     model=llm, 
    #     tools=tools,
    #     system_prompt=SYSTEM_PROMPT
    #     ) # create the agent and compile the graph
    return create_react_agent(
        model=llm,
        tools=tools,
        ) # create_react_agent is deprecated, yet stable. update to above line when needed

agent = build_agent()
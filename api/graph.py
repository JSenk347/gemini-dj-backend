
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
#from .tools import search_spotify
from dotenv import load_dotenv

load_dotenv()

def generate_pet_name(animal_type: str) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt_template_name = PromptTemplate( # defining a prompt template
        input_variables=["animal_type"],
        template="I have a {animal_type} and I want a cool name for it. suggest five cool names for my pet with no commentary"
    )
    output_parser = StrOutputParser()
    chain = prompt_template_name | llm | output_parser

    return chain.invoke({"animal_type": animal_type})

if __name__ == "__main__":
    print(generate_pet_name("dog"))

def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
        ) #initialize the gemini model
    tools = [search_spotify] #define the tools list
    return create_agent(llm, tools=tools) # create the agent and compile the graph

#agent = build_agent()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
#from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent #depricated yet stable. change to above line when needed
from langchain_core.prompts import ChatPromptTemplate #only needed since we are using stable version
#from langchain_core.output_parsers import StrOutputParser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from .tools import search_spotify

from .playlist import PlaylistSession
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are an expert DJ and musical tastemaker. Your goal is to curate a perfect, cohesive playlist using the tools provided.

You operate on a live playlist object. You do not need to "return" a list of songs at the end; your job is to modify the playlist state using your tools.

### YOUR TOOLKIT:
1. `add_song(query)`: Searches for and adds a specific track. Use this to establish a vibe or add user-requested songs.
2. `generate_recommendations()`: Adds 3 songs similar to the LAST song added. Use this to quickly expand the playlist with matching vibes.
3. `get_state()`: Returns the list of songs currently in the playlist.

### CURATION RULES:
1. **Start Strong:** Always begin by adding 1-2 specific "seed" tracks using `add_song` that perfectly match the user's requested genre or mood.
2. **Expand Smartly:** Once you have a good seed track, use `generate_recommendations` to find similar songs. Do not rely solely on `add_song` for every single track unless the user asks for specific titles.
3. **Maintain Flow:** If the user asks for a mix of genres (e.g., "Sad Jazz and 80s Pop"), switch between them. Add a Jazz song, get recommendations, then add an 80s Pop song, and get recommendations.
4. **Check Your Work:** Use `get_state` periodically to check the playlist length.
5. **Minimum Length:** Unless specified otherwise, aim for at least 10 songs.

### CRITICAL CONSTRAINTS:
- NEVER call `generate_recommendations` on an empty playlist. You MUST call `add_song` first.
- Do not output a JSON list of songs in your final text response. The system handles the data automatically.
- Your final text response should be a friendly commentary describing the vibe you created and highlighting a few key tracks.
"""

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

def build_agent(session_instance: PlaylistSession):
    """
    Creates an agent that is bound to a specific playlist session.
    """
    @tool
    def add_song(query: str):
        """
        Useful for when you need to search for a particular song and add it to the playlist.
        Input should be a search query such as "80's rock" or "Laufey".
        """
        return session_instance.search_and_add(query)
    
    @tool
    def add_similar_songs(genre: str = "", mood: str = ""):
        """
        Useful for when you want to add 3 more songs to the playlist that are similar to the
        song that was most recently added. You can also search for and add similar songs that have a 
        different genre or mood.
        """
        return session_instance.add_recommendations(genre, mood)

    @tool
    def check_playlist_status():
        """
        Useful to check what songs are currently in the playlist to ensure you aren't repeating artists
        or songs with the same title. Always check this before finalizing.
        """
        return session_instance.get_playlist_state()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3 #play around with this val. -> 1 is TOTALLY random, -> 0 is NO randomness
    ) #initialize the gemini model
    tools = [add_similar_songs, add_song, check_playlist_status] #define the tools list

    # return create_agent(
    #     model=llm, 
    #     tools=tools,
    #     system_prompt=SYSTEM_PROMPT
    #     ) # create the agent and compile the graph
    return create_react_agent(
        model=llm,
        tools=tools,
    ) # create_react_agent is deprecated, yet stable. update to above line when needed
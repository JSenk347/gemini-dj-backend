from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
#from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent #depricated yet stable. change to above line when needed
#from langchain_core.output_parsers import StrOutputParser
#from .tools import search_spotify

from .playlist import PlaylistSession
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are an expert DJ and musical tastemaker. Your goal is to curate a perfect, cohesive playlist using the tools provided.

You operate on a live playlist object. You do not need to "return" a list of songs at the end; your job is to modify the playlist state using your tools.

### YOUR TOOLKIT:
1. `add_song(query)`: Searches for and adds a specific track. Use this to establish a vibe or add user-requested songs.
2. `get_state()`: Returns the list of songs currently in the playlist.

### CURATION RULES:
1. **Use Your Knowledge:** Based on the user's input, use your knowledge of music as an expert DJ to determine what to search for. Eg. if someone asks for "top rap hits" from 2014, you should know that "Tuesday" by Fetty Wap was a top song, and then add it.
2. **Maintain Flow:** If the user asks for a mix of genres (e.g., "Sad Jazz and 80s Pop"), switch between them. Add a Jazz song, then add an 80s Pop song, then add a Jazz song, etc.
3. **Check Your Work:** Use `get_state` periodically to check the playlist length.
4. **Target Length:** The playlist must contain EXACTLY 10 songs — no more, no fewer. The system enforces a hard cap of 10; stop adding once the tools confirm the playlist is full.

### CRITICAL CONSTRAINTS:
- Do not output a JSON list of songs in your final text response. The system handles the data automatically.
- Your final text response should be a friendly commentary describing the vibe you created and highlighting a few key tracks.
"""

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
    def check_playlist_status():
        """
        Useful to check what songs are currently in the playlist to ensure you aren't repeating artists
        or songs with the same title. Always check this before finalizing.
        """
        return session_instance.get_playlist_state()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3 #play around with this val. -> 1 is TOTALLY random, -> 0 is NO randomness
    ) #initialize the gemini model
    tools = [add_song, check_playlist_status] #define the tools list

    # return create_agent(
    #     model=llm,
    #     tools=tools,
    #     system_prompt=SYSTEM_PROMPT
    #     ) # create the agent and compile the graph
    return create_react_agent(
        model=llm,
        tools=tools
    ) # create_react_agent is deprecated, yet stable. update to above line when needed

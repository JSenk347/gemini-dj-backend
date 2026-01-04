# this file defines the tools that the llm is able to use, such as searching for music
from langchain_core.tools import tool

@tool
def search_spotify(query: str):
    """Searches Spotify for music based on the user's query."""
    # Stage 1: Return dummy data
    return f"Mock results for: {query}"
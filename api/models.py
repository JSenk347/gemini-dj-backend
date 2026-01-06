# defines the data contracts, which are the formats of the requests that the frontend will send and receive to and from the backend
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    commentary: str 
    playlist: List[List[str]] = [] # = [] so that if no playlist exists, there is no crash

class SavePlaylistRequest(BaseModel):
    name: str
    user_id: str #the user's spotify id
    track_uris: List[str] # list of track uris as strings, sent by React
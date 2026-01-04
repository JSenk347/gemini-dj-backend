# defines the data contracts, which are the formats of the requests that the frontend will send and receive to and from the backend
from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str 
    # will need to add a playlist field later

class SavePlaylistRequest(BaseModel):
    name: str
    track_uris: List[str] # list of track uris as strings, sent by React
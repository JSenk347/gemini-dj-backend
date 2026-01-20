# defines the data contracts, which are the formats of the requests that the frontend will send and receive to and from the backend
from pydantic import BaseModel
from typing import List, Optional

class Track(BaseModel):
    track_uri: str
    track_name: str
    artist_name: str
    img_url: Optional[str] = None # Handle cases where images might be missing

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    commentary: str 
    playlist: List[Track] = [] # = [] so that if no playlist exists, there is no crash

class SavePlaylistRequest(BaseModel):
    name: str
    user_id: str
    auth_token: str
    track_uris: List[str] # list of track uris as strings, sent by React

class AuthURLRequest(BaseModel):
    redirect_uri: str # the URI for the spotify login window

class AccessTokenRequest(BaseModel):
    code: str # the code given by spotify upon user auth success
    redirect_uri: str

class UserDataRequest(BaseModel):
    auth_token: str
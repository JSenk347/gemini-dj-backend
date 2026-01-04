# defines the data contracts, which are the formats of the requests that the frontend will send and receive to and from the backend
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str 
    # will need to add a playlist field later
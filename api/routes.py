import json
import logging
#import spotipy
#from spotipy.oauth2 import SpotifyOAuth #Authenticates the USER
import os
from langchain_core.messages import ToolMessage
from fastapi import APIRouter, HTTPException
from .models import ChatRequest, ChatResponse, AuthURLRequest, AccessTokenRequest#, SavePlaylistRequest
from .graph import agent, SYSTEM_PROMPT
from .utils import get_spotify_oauth, extract_message

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    logger.info(f"Starting chat request for session: {request.session_id}")

    try:
        # pass input to the LangGraph agent
        result = await agent.ainvoke( # ainvoke is CRUCIAL as it is the asynchronous way to invoke the agent
            {"messages": [
                ("user", request.message),
                ("system", SYSTEM_PROMPT) # in future, will be removed and will add a system_prompt arg in build_agent
                ]},
            config={"configurable": {"thread_id": request.session_id}}
        )
    
        if not result.get("messages"):
            raise ValueError("Agent returned no messages.")

        last_message = result["messages"][-1]
        raw_content = last_message.content

        ai_message = extract_message(raw_content)

        # extract the playlist data by looking backwards through the messages for the most
        # recent ToolMessage
        extracted_playlist = []
        for msg in reversed(result["messages"]):
            if isinstance(msg, ToolMessage):
                try:
                    data = json.loads(msg.content)
                    if isinstance(data, list) and len(data) > 0:
                        extracted_playlist = data
                        break # we've found the latest results
                except:
                    continue # if the tool returned an error string, json.loads might fail. ignore it.
        print(ai_message)            
        return ChatResponse(commentary=ai_message, playlist=extracted_playlist)
    
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth_url")
async def serve_auth_url(payload: AuthURLRequest) -> object:
    sp_oauth = get_spotify_oauth(payload.redirect_uri)

    try:
        return {"auth_url": sp_oauth.get_authorize_url()}
    except Exception as e:
        logger.error(f"Error in auth_uri_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/token")
async def serve_token(payload: AccessTokenRequest):
    sp_oauth = get_spotify_oauth(payload.redirect_uri)

    try:
        #does not check if access token already exists to simplify logout->login
        return {"access_token" : sp_oauth.get_access_token(code=payload.code, as_dict=False, check_cache=False)} 
    except Exception as e:
        logger.error(f"Error in token_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/save-playlist")
# async def save_playlist(payload: SavePlaylistRequest) -> object:
#     """
#     Endpoint for the frontend to save the final playlist. Not used by LLM agent
    
#     :param payload: The data contract that describes a playlist, sent by the frontend.
#     :type payload: SavePlaylistRequest
#     """
#     try:
#         sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))
#         user_id = sp.current_user()["id"] # will replace with payload.user_id
#         # create empty playlist
#         playlist = sp.user_playlist_create(
#             user=user_id,
#             name=payload.name,
#             public=True,
#             description="Created by Gemini DJ"
#             )
#         # add the tracks to the playlist
#         if payload.track_uris:
#             sp.playlist_add_items(
#                 playlist_id=playlist["id"],
#                 items=payload.track_uris
#             )

#         return {
#             "status":"success",
#             "playlist_id":playlist["id"],
#             "url":playlist["external_urls"]["spotify"]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

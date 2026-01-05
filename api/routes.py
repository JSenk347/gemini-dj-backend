import json
import logging
from langchain_core.messages import ToolMessage
from fastapi import APIRouter, HTTPException
from .models import ChatRequest, ChatResponse, SavePlaylistRequest
from .tools import sp
from .graph import agent, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    logger.info(f"Starting chat request for session: {request.session_id}")

    try:
        # pass input to the LangGraph agent
        result = await agent.ainvoke(
            {"messages": [
                ("user", request.message),
                ("system", SYSTEM_PROMPT) # in future, will be removed and will add a system_prompt arg in build_agent
                ]},
            config={"configurable": {"thread_id": request.session_id}}
        )
    
        if not result.get("messages"):
            raise ValueError("Agent returned no messages.")

        # extract the AI's final commentary on the playlist
        ai_message = result["messages"][-1].content

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

        return ChatResponse(commentary=ai_message, playlist=extracted_playlist)
    
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save-playlist")
async def save_playlist(payload: SavePlaylistRequest) -> object:
    """
    Endpoint for the frontend to save the final playlist. Not used by LLM agent
    
    :param payload: The data contract that describes a playlist, sent by the frontend.
    :type payload: SavePlaylistRequest
    """
    try:
        user_id = sp.current_user()["id"]
        # create empty playlist
        playlist = sp.user_playlist_create(
            user=user_id,
            name=payload.name,
            public=True,
            description="Created by Gemini DJ"
            )
        # add the tracks to the playlist
        if payload.track_uris:
            sp.playlist_add_items(
                playlist_id=playlist["id"],
                items=payload.track_uris
            )

        return {
            "status":"success",
            "playlist_id":playlist["id"],
            "url":playlist["external_urls"]["spotify"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

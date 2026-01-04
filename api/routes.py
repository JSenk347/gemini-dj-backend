from fastapi import APIRouter
from .models import ChatRequest, ChatResponse
from .graph import agent

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # pass input to the LangGraph agent
    result = agent.invoke(
        {"messages": [("user", request.message)]},
        config={"configurable": {"thread_id": request.session_id}}
    )
    
    # extract the AI's final text response
    ai_message = result["messages"][-1].content
    return ChatResponse(response=ai_message)
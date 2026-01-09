from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from .routes import router

app = FastAPI(title="Gemini DJ API")

#CORS setup that allows the front-end to talk to the back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173", "https://jsenkcc-gemini-dj-frontend.hf.space'], 
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router=router)

# Opening huggingface URL in a browser will display this
@app.get('/')
def health_check():
    return {"status": "running", "service": "Gemini DJ API"}
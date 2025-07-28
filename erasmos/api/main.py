from . import routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Erasmos API",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,  # pyrefly: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    routes.document_router, prefix="/document", tags=["Document"])


@app.get("/", tags=["Root"])
def status():
    return {"status": "OK"}

def start():
    uvicorn.run(
        "erasmos.api.main:app", # Percorso all'oggetto app
        host="0.0.0.0",
        port=8000,
        reload=True # L'opzione --reload
    )

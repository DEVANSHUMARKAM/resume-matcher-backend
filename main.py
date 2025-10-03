# backend/main.py

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Import our new SearchEngine class
from ir_engine import SearchEngine

# FastAPI app initialization
app = FastAPI()
origins = ["http://localhost:3000",
           "https://resume-matcher-devanshu.onrender.com",
           ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Create a single, global instance of our search engine
search_engine = SearchEngine()

@app.on_event("startup")
def startup_event():
    """On startup, load and index the resumes."""
    search_engine.load_and_index()

# --- API Endpoints ---
# These endpoints are now very simple. They just call the methods on our engine.

@app.get("/")
def read_root():
    return {"message": "Hello from the Resume Matcher API!"}

@app.post("/search")
def search_resumes(query: str = Body(..., embed=True)):
    return search_engine.search(query)

@app.post("/refine-search")
def refine_search_endpoint(original_query: str = Body(...), relevant_docs: List[str] = Body(...)):
    return search_engine.refine_search(original_query, relevant_docs)

@app.post("/tolerant-search")
def tolerant_search_endpoint(query: str = Body(..., embed=True)):
    return search_engine.tolerant_search(query)
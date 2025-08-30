from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import daily_summery
import db

app = FastAPI()

# CORS settings: allow your frontend origin
origins = [
    "http://localhost:8080"  # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow frontend
    allow_credentials=True,
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all headers
)

class EntryRequest(BaseModel):
    text: str

@app.post("/entry")
def summarize_journals(req: EntryRequest):
    # get mood and focus area
    mood = daily_summery.classify_mood(req.text)
    focus_area = daily_summery.classify_focus_area(req.text)

    # save to db
    entry = db.add_daily_entry(req.text, mood, focus_area)

    return {"message": "Entry saved", "entry": entry}

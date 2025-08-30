import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import daily_summery
import db
from util import generate_weekly_summary_for_date

app = FastAPI()

class EntryRequest(BaseModel):
    text: str
    entry_date: Optional[str] = None  # Expecting "YYYY-MM-DD" format


@app.post("/entry")
def summarize_journals(req: EntryRequest):

    mood = daily_summery.classify_mood(req.text)
    focus_area = daily_summery.classify_focus_area(req.text)

    try:
        # parse date
        if req.entry_date:
            date_obj = datetime.strptime(req.entry_date, "%Y-%m-%d")

        else:
            date_obj = datetime.today()
            logging.info(date_obj)

        # weekly summary
        if date_obj.weekday() == 6:  # Sunday
            generate_weekly_summary_for_date(date_obj)
            logging.info("Sunday")
        else:
            prev_week_date = date_obj - timedelta(days=date_obj.weekday() + 1)
            generate_weekly_summary_for_date(prev_week_date)

    except Exception as e:
        import traceback
        print("Error generating weekly summary:")
        traceback.print_exc()


    # save to db
    entry = db.add_daily_entry(req.text, mood, focus_area)

    return {"message": "Entry saved", "entry": entry}


@app.get("/weekly_summary")
def get_weekly_summaries():
    summaries = db.get_weekly_summaries()
    return {"weekly_summaries": summaries}

@app.post("/weekly_summary")
def create_weekly_summary(date: Optional[str] = None):
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    else:
        date_obj = datetime.today()

    summary = generate_weekly_summary_for_date(date_obj)
    if summary:
        return {"message": "Weekly summary generated", "summary": summary}
    else:
        return {"message": "No entries for the week or summary already exists"}

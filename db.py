from tinydb import TinyDB, Query
from datetime import datetime

# Load databases
daily_db = TinyDB("daily_journals.json")
weekly_db = TinyDB("weekly_summaries.json")

# --- Daily Entries ---
def add_daily_entry(entry, mood, focus_area, date=None):
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    data = {
        "date": date,
        "entry": entry,
        "mood": mood,
        "focus_area": focus_area
    }
    daily_db.insert(data)
    return data

def get_daily_entries():
    return daily_db.all()

def get_daily_by_date(date):
    Journal = Query()
    return daily_db.search(Journal.date == date)

# --- Weekly Summaries ---
def add_weekly_summary(week_start, week_end, week_number, summary, mood, focus_area):
    data = {
        "week_start": week_start,
        "week_end": week_end,
        "week_number": week_number,
        "weekly_summary": summary,
        "weekly_mood": mood,
        "weekly_focus_area": focus_area
    }
    weekly_db.insert(data)
    return data

def get_weekly_summaries():
    return weekly_db.all()

def get_weekly_by_number(week_number):
    Summary = Query()
    return weekly_db.search(Summary.week_number == week_number)

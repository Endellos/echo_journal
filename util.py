from datetime import datetime

import db
from db import daily_db, weekly_db
from datetime import datetime, timedelta
import weekly_summery


def get_week_number_and_range(date=None):
    if date is None:
        date = datetime.today()
    week_number = date.isocalendar()[1]
    week_start = date - timedelta(days=date.weekday())  # Monday
    week_end = week_start + timedelta(days=6)  # Sunday
    return week_number, week_start.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d")
def generate_weekly_summary_for_date(date=None):
    if date is None:
        date = datetime.today()

    week_number = date.isocalendar()[1]
    week_start = (date - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
    week_end = (date - timedelta(days=date.weekday()) + timedelta(days=6)).strftime("%Y-%m-%d")

    # Check if summary already exists
    existing = weekly_db.search((db.Query().week_number == week_number))
    if existing:
        return existing[0]

    # Get entries for this week
    entries = daily_db.all()
    week_entries = [e for e in entries if week_start <= e["date"] <= week_end]
    if not week_entries:
        print("No entries for the week")
        return None
    print(week_entries)
    # Use the methods from the first module
    summary_text = weekly_summery.summarize_week(week_entries)
    weekly_mood = weekly_summery.classify_week_mood(summary_text)
    weekly_focus_info = weekly_summery.classify_week_focus_area(summary_text)


    # Store summary in weekly_db
    return db.add_weekly_summary(
        week_start=week_start,
        week_end=week_end,
        week_number=week_number,
        summary=summary_text,
        mood=weekly_mood,
        focus_area=weekly_focus_info
    )

def add_daily_entry_and_maybe_weekly(entry, mood, focus_area, date_str=None):
    # Add daily entry
    daily_entry = daily_db.add_daily_entry(entry, mood, focus_area, date=date_str)

    # Check if today is Sunday (weekday() = 6)
    date_obj = datetime.strptime(daily_entry["date"], "%Y-%m-%d")
    if date_obj.weekday() == 6:  # Sunday
        generate_weekly_summary_for_date(date_obj)
    else:
        # Check if previous week's summary exists
        prev_week_date = date_obj - timedelta(days=date_obj.weekday() + 1)  # last Sunday
        generate_weekly_summary_for_date(prev_week_date)

    return daily_entry

from dotenv import load_dotenv
import os
from openai import OpenAI

# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Example journal entries
import json

with open("input_weekly.json", "r", encoding="utf-8") as f:
    journals = json.load(f)

    # You are a journaling assistant. Summarize the following weekly journal entries
    # into a cohesive 1 paragraph narrative.
    # Highlight recurring events, important emotions, and overall tone. Try to focus on the positives.
# --- Weekly Summary Function ---
def summarize_week(entries):
    combined_text = "\n".join([f"{e['date']}: {e['text']}" for e in entries])
    prompt = f"""   
    Summarize in 3–5 sentences, capturing feelings, challenges, and highlights, so that reading it later clearly shows what the week was like emotionally. Focus on the positives. 
    Journals:
    {combined_text}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return resp.choices[0].message.content.strip()

# --- Week Classification Function ---
moods = ["curious", "persistent", "kind", "fair", "prudent", "grateful", "hopeful", "humorous", "adventurous", "reflective", "compassionate", "resilient"]
focus_areas = ["relationships", "career", "health", "personal growth", "creativity", "spirituality", "community"]


def classify_week_mood(summary):
    prompt = f"""
    Based on this weekly summary, classify the overall mood into one of these categories:
    {', '.join(moods)}.

    Weekly Summary:
    {summary}

    Respond with ONLY the category name.
    """
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    return resp.choices[0].message.content.strip().lower()

def classify_week_focus_area(summary):
    prompt = f"""
    Based on this weekly summary, classify the overall focus area into one of these categories:
    {', '.join(focus_areas)}.

    Weekly Summary:
    {summary}

    Respond with the category name and 1 sentence explanation.
    """
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    ,
    temperature=0.7
    )
    return resp.choices[0].message.content.strip().lower()

# --- Run the pipeline ---
weekly_summary = summarize_week(journals)
theme = classify_week_mood(weekly_summary)
focus_area = classify_week_focus_area(weekly_summary)

print("WEEKLY SUMMARY:\n", weekly_summary)
print("\nMood OF THE WEEK:", theme)
print("\nFocus Area OF THE WEEK:", focus_area)

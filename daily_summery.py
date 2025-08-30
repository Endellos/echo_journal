from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Example single-day entry
daily_journal = {
    "date": "2025-08-30",
    "text": "Tonight I went to a social gathering where I didn’t know many people. At first, I felt nervous and awkward, unsure how to start conversations. Slowly, I began chatting with a few people who shared similar interests, and it felt surprisingly easy to connect. I laughed a lot, exchanged stories, and even received a few invitations to future events. By the end of the evening, I felt energized and more confident socially, realizing that stepping out of my comfort zone can lead to meaningful connections. It was exhausting at times, but overall incredibly rewarding."
}


# --- Daily Summary Function ---
def summarize_day(entry):
    prompt = f"""
    You are a journaling assistant. Summarize the following journal entry 
    into 2-3 concise sentences capturing the main events, emotions, and tone. Focus on the feelings:

    Journal Entry:
    {entry['text']}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return resp.choices[0].message.content.strip()

moods = ["curious", "persistent", "kind", "fair", "prudent", "grateful", "hopeful", "humorous", "adventurous", "reflective", "compassionate", "resilient"]
focus_areas = ["relationships", "career", "health", "personal growth", "creativity", "spirituality", "community"]


def classify_mood(summary):
    prompt = f"""
    Based on this journal entry, classify the overall mood into one of these categories:
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

def classify_focus_area(summary):
    prompt = f"""
    Based on this journal entry, classify the overall focus area into one of these categories:
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


"""
MoodCanvas AI — Mood Tracker
Stores and retrieves mood history for visualization.
"""

import json
import os
from datetime import datetime


DATA_FILE = "mood_history.json"


def load_history() -> list:
    """Load mood history from JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_entry(entry: dict) -> None:
    """Save a new mood entry to history."""
    history = load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "mood": entry.get("mood", "Reflective"),
        "confidence": entry.get("confidence", 0),
        "polarity": entry.get("polarity", 0),
        "journal_preview": entry.get("journal_preview", "")[:100],
        "emoji": entry.get("emoji", "🤔")
    })
    
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_mood_stats(history: list) -> dict:
    """Calculate mood statistics from history."""
    if not history:
        return {
            "total_entries": 0,
            "most_common_mood": "N/A",
            "avg_polarity": 0,
            "mood_counts": {},
            "streak": 0
        }
    
    mood_counts = {}
    total_polarity = 0
    
    for entry in history:
        mood = entry.get("mood", "Reflective")
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
        total_polarity += entry.get("polarity", 0)
    
    most_common = max(mood_counts, key=mood_counts.get)
    
    return {
        "total_entries": len(history),
        "most_common_mood": most_common,
        "avg_polarity": round(total_polarity / len(history), 3),
        "mood_counts": mood_counts,
        "streak": len(history)  # simplified
    }


def clear_history() -> None:
    """Clear all mood history."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

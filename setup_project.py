"""
🎨 MoodCanvas AI — One-Click Project Setup
==========================================
Run this file ONCE and it will create ALL other project files automatically!

Usage:
    python setup_project.py

This creates:
    - requirements.txt
    - README.md
    - .env.example
    - .gitignore
"""

import os

print("🎨 MoodCanvas AI — Setting up project files...\n")

# ──────────────────────────────────────────────
# 1. requirements.txt
# ──────────────────────────────────────────────
with open("requirements.txt", "w") as f:
    f.write("""streamlit==1.41.0
textblob==0.18.0
plotly==5.24.0
openai==1.60.0
python-dotenv==1.0.1
Pillow==11.1.0
""")
print("✅ Created: requirements.txt")

# ──────────────────────────────────────────────
# 2. .env.example
# ──────────────────────────────────────────────
with open(".env.example", "w") as f:
    f.write("""# MoodCanvas AI — Environment Variables
# OpenAI API Key (optional — app works in demo mode without it)
# Get yours at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
""")
print("✅ Created: .env.example")

# ──────────────────────────────────────────────
# 3. .gitignore
# ──────────────────────────────────────────────
with open(".gitignore", "w") as f:
    f.write(""".env
__pycache__/
*.pyc
mood_history.json
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db
""")
print("✅ Created: .gitignore")

# ──────────────────────────────────────────────
# 4. README.md
# ──────────────────────────────────────────────
with open("README.md", "w") as f:
    f.write("""# 🎨 MoodCanvas AI — Turn Your Journal Into Art, Music & Wisdom

> **An AI-powered emotional wellness companion that transforms your daily journal entries into beautiful artwork, curated music, and personalized advice.**

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![AI](https://img.shields.io/badge/AI-Multimodal-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 What Makes This Unique?

Most AI projects do ONE thing. **MoodCanvas AI** is a **multimodal emotional intelligence system** that:

| Input | AI Processing | Output |
|-------|--------------|--------|
| 📝 Journal Text | NLP Sentiment Analysis | 😊 Mood Detection |
| 😊 Detected Mood | Generative AI | 🎨 AI-Generated Artwork |
| 😊 Detected Mood | Music Recommendation Engine | 🎵 Spotify Playlist |
| 😊 Detected Mood | LLM Wisdom Engine | 💡 Personalized Advice |
| 📅 Mood History | Time-Series Visualization | 📊 Mood Trend Dashboard |

**One input → Five AI outputs → Complete emotional experience**

---

## 🚀 Features

- ✍️ **Journal Entry** — Write how you're feeling in plain text
- 🧠 **AI Mood Detection** — Detects 8 emotions (Happy, Sad, Anxious, Calm, Angry, Excited, Grateful, Reflective)
- 🎨 **AI Art Generation** — Creates a unique artwork that visually represents your mood
- 🎵 **Music Matching** — Recommends songs/playlists that match your emotional state
- 💬 **AI Life Coach** — Gives thoughtful, personalized advice based on your mood
- 📊 **Mood Tracker** — Beautiful charts showing your emotional journey over time

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.9+ | Core Language |
| Streamlit | Web UI Framework |
| TextBlob / VADER | Sentiment Analysis |
| OpenAI API (GPT) | Advice Generation |
| OpenAI API (DALL-E) | Art Generation |
| Plotly | Mood Visualization |
| JSON | Local Data Storage |

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/MoodCanvas-AI.git
cd MoodCanvas-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys (Optional)
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

> 💡 **No API key?** The app works in **Demo Mode** with built-in mood art and advice!

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📸 How It Works

```
User Writes Journal
        |
   NLP Sentiment Analysis
        |
   +---------+---------+----------+
   |         |         |          |
🎨 Art   🎵 Music  💡 Advice  📊 Track
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new mood categories
- Improve the art generation prompts
- Add Spotify API integration
- Enhance the mood tracking dashboard

---

## 📄 License

MIT License — Free to use, modify, and share.

---

*Built with ❤️ and AI — Because your emotions deserve to be beautiful.*
""")
print("✅ Created: README.md")

print()
print("=" * 50)
print("🎉 ALL FILES CREATED SUCCESSFULLY!")
print("=" * 50)
print()
print("Your project now has these files:")
print()

all_files = [
    "app.py",
    "mood_engine.py", 
    "art_generator.py",
    "mood_tracker.py",
    "setup_project.py",
    "requirements.txt",
    "README.md",
    ".env.example",
    ".gitignore"
]

for f in all_files:
    exists = "✅" if os.path.exists(f) else "❌"
    print(f"  {exists} {f}")

print()
print("Next steps:")
print("  1. pip install -r requirements.txt")
print("  2. streamlit run app.py")
print("  3. Upload ALL files to GitHub")
print()
print("🎨 Happy MoodCanvas-ing! ✨")

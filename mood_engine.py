"""
MoodCanvas AI — Mood Detection Engine
Analyzes journal text to detect emotions using NLP.
"""

from textblob import TextBlob
import re


# ──────────────────────────────────────────────
# Emotion keyword dictionaries
# ──────────────────────────────────────────────

EMOTION_KEYWORDS = {
    "Happy": [
        "happy", "joy", "wonderful", "amazing", "great", "fantastic", "love",
        "excited", "blessed", "smile", "laugh", "cheerful", "delighted",
        "thrilled", "ecstatic", "glad", "pleased", "satisfied", "fun",
        "awesome", "brilliant", "celebrate", "winning", "proud", "success"
    ],
    "Sad": [
        "sad", "unhappy", "depressed", "down", "cry", "tears", "heartbreak",
        "lonely", "lost", "miss", "grief", "sorrow", "pain", "hurt",
        "disappointed", "gloomy", "miserable", "hopeless", "broken", "empty"
    ],
    "Anxious": [
        "anxious", "worried", "nervous", "stress", "stressed", "fear",
        "panic", "overthink", "restless", "uneasy", "tense", "dread",
        "overwhelmed", "pressure", "uncertain", "doubt", "insecure",
        "scared", "frightened", "apprehensive", "nightmare"
    ],
    "Calm": [
        "calm", "peaceful", "relaxed", "serene", "tranquil", "quiet",
        "gentle", "soothing", "mindful", "meditate", "breathe", "still",
        "content", "balanced", "harmony", "zen", "comfortable", "ease",
        "rested", "cozy"
    ],
    "Angry": [
        "angry", "furious", "mad", "rage", "annoyed", "frustrated",
        "irritated", "hate", "disgusted", "outraged", "resentful",
        "hostile", "bitter", "fed up", "aggravated", "infuriated",
        "livid", "enraged"
    ],
    "Excited": [
        "excited", "thrilled", "pumped", "eager", "enthusiastic",
        "can't wait", "looking forward", "anticipation", "adventure",
        "energized", "fired up", "buzzing", "hyped", "passionate",
        "motivated", "inspired", "ambitious"
    ],
    "Grateful": [
        "grateful", "thankful", "appreciate", "blessed", "fortunate",
        "lucky", "gratitude", "thanks", "cherish", "valued", "gift",
        "abundance", "recognition", "acknowledged", "humbled"
    ],
    "Reflective": [
        "think", "reflect", "wonder", "realize", "understand", "learn",
        "grow", "journey", "remember", "memories", "past", "future",
        "meaning", "purpose", "life", "perspective", "insight", "wisdom",
        "change", "evolve", "contemplate", "ponder"
    ]
}

# ──────────────────────────────────────────────
# Mood colors and emojis
# ──────────────────────────────────────────────

MOOD_CONFIG = {
    "Happy":      {"emoji": "😊", "color": "#FFD700", "gradient": ["#FFD700", "#FFA500"]},
    "Sad":        {"emoji": "😢", "color": "#4169E1", "gradient": ["#4169E1", "#191970"]},
    "Anxious":    {"emoji": "😰", "color": "#FF6347", "gradient": ["#FF6347", "#8B0000"]},
    "Calm":       {"emoji": "😌", "color": "#90EE90", "gradient": ["#90EE90", "#2E8B57"]},
    "Angry":      {"emoji": "😠", "color": "#DC143C", "gradient": ["#DC143C", "#8B0000"]},
    "Excited":    {"emoji": "🤩", "color": "#FF69B4", "gradient": ["#FF69B4", "#FF1493"]},
    "Grateful":   {"emoji": "🙏", "color": "#DDA0DD", "gradient": ["#DDA0DD", "#9370DB"]},
    "Reflective": {"emoji": "🤔", "color": "#87CEEB", "gradient": ["#87CEEB", "#4682B4"]},
}


def analyze_mood(text: str) -> dict:
    """
    Analyze journal text and return detected mood with confidence.
    
    Returns:
        dict with keys: mood, confidence, polarity, subjectivity, emoji, color, details
    """
    if not text or not text.strip():
        return {
            "mood": "Reflective",
            "confidence": 0.0,
            "polarity": 0.0,
            "subjectivity": 0.0,
            "emoji": "🤔",
            "color": "#87CEEB",
            "gradient": ["#87CEEB", "#4682B4"],
            "details": "Write something to see your mood analysis!"
        }
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # ── Step 1: TextBlob sentiment analysis ──
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity        # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    
    # ── Step 2: Keyword matching ──
    emotion_scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        matched_words = []
        for keyword in keywords:
            if keyword in text_lower:
                # Multi-word keywords get extra weight
                weight = len(keyword.split())
                count = text_lower.count(keyword)
                score += count * weight
                matched_words.append(keyword)
        emotion_scores[emotion] = {
            "score": score,
            "matched": matched_words
        }
    
    # ── Step 3: Combine sentiment + keywords ──
    # Boost scores based on polarity
    if polarity > 0.3:
        for mood in ["Happy", "Excited", "Grateful", "Calm"]:
            emotion_scores[mood]["score"] += polarity * 3
    elif polarity < -0.3:
        for mood in ["Sad", "Angry", "Anxious"]:
            emotion_scores[mood]["score"] += abs(polarity) * 3
    
    # ── Step 4: Determine dominant mood ──
    max_score = 0
    dominant_mood = "Reflective"  # default
    
    for emotion, data in emotion_scores.items():
        if data["score"] > max_score:
            max_score = data["score"]
            dominant_mood = emotion
    
    # ── Step 5: Calculate confidence ──
    total_score = sum(d["score"] for d in emotion_scores.values())
    if total_score > 0:
        confidence = round((max_score / total_score) * 100, 1)
    else:
        confidence = 50.0  # neutral/reflective default
    
    confidence = min(confidence, 99.0)
    
    config = MOOD_CONFIG[dominant_mood]
    
    # ── Step 6: Generate detail text ──
    matched = emotion_scores[dominant_mood]["matched"]
    if matched:
        detail_text = f"Detected keywords: {', '.join(matched[:5])}"
    else:
        detail_text = f"Based on overall sentiment (polarity: {polarity:.2f})"
    
    return {
        "mood": dominant_mood,
        "confidence": confidence,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "emoji": config["emoji"],
        "color": config["color"],
        "gradient": config["gradient"],
        "details": detail_text,
        "all_scores": {k: v["score"] for k, v in emotion_scores.items()}
    }


def get_mood_art_prompt(mood: str, journal_text: str) -> str:
    """
    Generate a DALL·E / Stable Diffusion prompt based on mood.
    """
    art_styles = {
        "Happy": "A vibrant, colorful abstract painting with warm golden sunlight, blooming flowers, and dancing butterflies. Impressionist style, joyful energy, bright yellows and oranges",
        "Sad": "A melancholic watercolor painting of rain falling on a quiet lake at twilight, muted blues and grays, soft reflections, ethereal and contemplative mood",
        "Anxious": "A surrealist painting with swirling storm clouds and tangled threads, deep reds and dark oranges, dynamic tension, abstract expressionist style",
        "Calm": "A serene Japanese zen garden at dawn, soft morning mist, gentle green tones, minimalist composition, peaceful watercolor style",
        "Angry": "A bold expressionist painting with sharp geometric shapes, intense crimson and black, powerful brushstrokes, raw energy, abstract",
        "Excited": "A dynamic pop-art explosion of colors, fireworks and confetti, electric pinks and neon blues, energetic composition, celebration",
        "Grateful": "A soft pastel painting of a sunrise over mountains with wildflowers, gentle purples and pinks, warm light, dreamy and hopeful atmosphere",
        "Reflective": "A contemplative painting of a person sitting by a window watching stars, deep blues and silver, moonlight, impressionist style, introspective"
    }
    
    base_prompt = art_styles.get(mood, art_styles["Reflective"])
    return f"{base_prompt}. Digital art, high quality, 4K, artistic, emotional"


def get_music_recommendations(mood: str) -> list:
    """
    Return curated music recommendations based on mood.
    """
    playlists = {
        "Happy": [
            {"song": "Happy", "artist": "Pharrell Williams", "genre": "Pop"},
            {"song": "Walking on Sunshine", "artist": "Katrina & The Waves", "genre": "Pop"},
            {"song": "Here Comes the Sun", "artist": "The Beatles", "genre": "Rock"},
            {"song": "Good as Hell", "artist": "Lizzo", "genre": "Pop"},
            {"song": "Don't Stop Me Now", "artist": "Queen", "genre": "Rock"},
        ],
        "Sad": [
            {"song": "Someone Like You", "artist": "Adele", "genre": "Pop"},
            {"song": "Hurt", "artist": "Johnny Cash", "genre": "Country"},
            {"song": "Fix You", "artist": "Coldplay", "genre": "Alternative"},
            {"song": "The Night We Met", "artist": "Lord Huron", "genre": "Indie"},
            {"song": "Skinny Love", "artist": "Bon Iver", "genre": "Indie Folk"},
        ],
        "Anxious": [
            {"song": "Weightless", "artist": "Marconi Union", "genre": "Ambient"},
            {"song": "Breathe Me", "artist": "Sia", "genre": "Pop"},
            {"song": "Strawberry Swing", "artist": "Coldplay", "genre": "Alternative"},
            {"song": "Orinoco Flow", "artist": "Enya", "genre": "New Age"},
            {"song": "Return to Innocence", "artist": "Enigma", "genre": "New Age"},
        ],
        "Calm": [
            {"song": "Clair de Lune", "artist": "Debussy", "genre": "Classical"},
            {"song": "Sunset Lover", "artist": "Petit Biscuit", "genre": "Electronic"},
            {"song": "Holocene", "artist": "Bon Iver", "genre": "Indie Folk"},
            {"song": "Gymnopédie No.1", "artist": "Erik Satie", "genre": "Classical"},
            {"song": "Re: Stacks", "artist": "Bon Iver", "genre": "Indie Folk"},
        ],
        "Angry": [
            {"song": "In the End", "artist": "Linkin Park", "genre": "Rock"},
            {"song": "Break Stuff", "artist": "Limp Bizkit", "genre": "Nu Metal"},
            {"song": "Killing in the Name", "artist": "Rage Against the Machine", "genre": "Rock"},
            {"song": "Fighter", "artist": "Christina Aguilera", "genre": "Pop"},
            {"song": "Stronger", "artist": "Kanye West", "genre": "Hip Hop"},
        ],
        "Excited": [
            {"song": "Uptown Funk", "artist": "Bruno Mars", "genre": "Pop"},
            {"song": "Can't Hold Us", "artist": "Macklemore", "genre": "Hip Hop"},
            {"song": "Titanium", "artist": "David Guetta ft. Sia", "genre": "EDM"},
            {"song": "Eye of the Tiger", "artist": "Survivor", "genre": "Rock"},
            {"song": "Levels", "artist": "Avicii", "genre": "EDM"},
        ],
        "Grateful": [
            {"song": "What a Wonderful World", "artist": "Louis Armstrong", "genre": "Jazz"},
            {"song": "Thank U", "artist": "Alanis Morissette", "genre": "Rock"},
            {"song": "Count on Me", "artist": "Bruno Mars", "genre": "Pop"},
            {"song": "Lean on Me", "artist": "Bill Withers", "genre": "Soul"},
            {"song": "Beautiful Day", "artist": "U2", "genre": "Rock"},
        ],
        "Reflective": [
            {"song": "The Sound of Silence", "artist": "Simon & Garfunkel", "genre": "Folk"},
            {"song": "Everybody's Changing", "artist": "Keane", "genre": "Alternative"},
            {"song": "Iris", "artist": "Goo Goo Dolls", "genre": "Rock"},
            {"song": "Time", "artist": "Pink Floyd", "genre": "Rock"},
            {"song": "Vienna", "artist": "Billy Joel", "genre": "Pop"},
        ],
    }
    
    return playlists.get(mood, playlists["Reflective"])


def get_ai_advice(mood: str, journal_text: str) -> str:
    """
    Generate personalized advice based on mood (demo mode — no API needed).
    """
    advice_bank = {
        "Happy": [
            "🌟 Your happiness is contagious! Take a moment to share this energy with someone who might need it today.",
            "📸 Capture this feeling — write down 3 specific things making you happy right now. Future-you will thank you on harder days.",
            "🎯 Happy moments are perfect for tackling that one thing you've been putting off. Ride this positive wave!"
        ],
        "Sad": [
            "💙 It's okay to feel this way. Sadness is not weakness — it's proof that you care deeply. Be gentle with yourself today.",
            "🌊 Like waves, emotions come and go. Try the 5-4-3-2-1 grounding technique: notice 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste.",
            "📞 Reach out to one person today — even a simple 'hi' can shift your energy. Connection heals."
        ],
        "Anxious": [
            "🫁 Try box breathing: Breathe in for 4 counts, hold for 4, exhale for 4, hold for 4. Repeat 3 times. Your nervous system will thank you.",
            "📝 Write down your worries, then ask: 'Will this matter in 5 years?' If not, take a deep breath and let it go.",
            "🚶 A 10-minute walk outside can reduce anxiety by up to 40%. Nature is free therapy — use it!"
        ],
        "Calm": [
            "🧘 Beautiful — you're in a state of balance. Use this clarity to set an intention for the week ahead.",
            "📖 Calm minds absorb knowledge best. This is the perfect time to read, learn, or explore something new.",
            "🌿 Protect this peace. Notice what brought you here and create more of it in your daily routine."
        ],
        "Angry": [
            "🔥 Your anger is valid, but don't let it drive the car. Take 10 deep breaths before responding to anything.",
            "💪 Channel this energy into something physical — exercise, cleaning, or even punching a pillow. Transform it!",
            "✍️ Write an unsent letter expressing everything you feel. Get it ALL out. Then decide what (if anything) to actually say."
        ],
        "Excited": [
            "🚀 Harness this energy! Write down 3 action steps for whatever is exciting you. Momentum is everything.",
            "🎯 Excitement is your compass pointing toward what matters. Pay attention to what lights you up!",
            "📣 Share your excitement with someone who'll celebrate with you. Joy multiplied is joy amplified!"
        ],
        "Grateful": [
            "💜 Gratitude rewires your brain for happiness. You're literally making yourself healthier right now!",
            "✉️ Send a thank-you message to someone who impacted your life. Unexpressed gratitude is a missed connection.",
            "📔 Start a gratitude chain — every day, add one new thing. Watch how it transforms your perspective over time."
        ],
        "Reflective": [
            "🔮 Reflection is where wisdom lives. Ask yourself: 'What did I learn today that I didn't know yesterday?'",
            "🌱 Growth happens in these quiet moments. Trust the process — you're evolving even when it doesn't feel like it.",
            "📝 Journal more deeply: What patterns do you notice in your life? What would you tell your past self?"
        ]
    }
    
    import random
    advices = advice_bank.get(mood, advice_bank["Reflective"])
    return random.choice(advices)

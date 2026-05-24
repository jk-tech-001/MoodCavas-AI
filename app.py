"""
🎨 MoodCanvas AI — Turn Your Journal Into Art, Music & Wisdom
Main Streamlit Application
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import base64

from mood_engine import analyze_mood, get_music_recommendations, get_ai_advice, MOOD_CONFIG
from art_generator import generate_mood_art_svg
from mood_tracker import load_history, save_entry, get_mood_stats, clear_history


# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="MoodCanvas AI 🎨",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    
    .mood-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    
    .mood-emoji {
        font-size: 4rem;
        margin-bottom: 10px;
    }
    
    .mood-label {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 10px 0;
    }
    
    .confidence-bar {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 8px;
        margin: 10px auto;
        width: 80%;
    }
    
    .music-item {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        border-left: 3px solid #1DB954;
    }
    
    .advice-box {
        background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(102,126,234,0.2);
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    div[data-testid="stTextArea"] textarea {
        font-size: 1.1rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎨 MoodCanvas AI")
    st.markdown("---")
    
    st.markdown("### How It Works")
    st.markdown("""
    1. ✍️ Write your journal entry
    2. 🧠 AI detects your mood
    3. 🎨 Get unique mood artwork
    4. 🎵 Discover matching music
    5. 💡 Receive AI advice
    6. 📊 Track your mood journey
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Your Stats")
    history = load_history()
    stats = get_mood_stats(history)
    
    st.metric("Total Entries", stats["total_entries"])
    if stats["total_entries"] > 0:
        st.metric("Most Common Mood", stats["most_common_mood"])
        avg_p = stats["avg_polarity"]
        sentiment_label = "Positive 😊" if avg_p > 0.1 else "Negative 😢" if avg_p < -0.1 else "Neutral 😐"
        st.metric("Avg Sentiment", sentiment_label)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear History", type="secondary"):
        clear_history()
        st.success("History cleared!")
        st.rerun()
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#666; font-size:0.8rem;'>"
        "Made with ❤️ by MoodCanvas AI<br>"
        "v1.0 — Multimodal Emotion AI"
        "</div>",
        unsafe_allow_html=True
    )


# ──────────────────────────────────────────────
# Main Content
# ──────────────────────────────────────────────

st.markdown('<h1 class="main-title">🎨 MoodCanvas AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Turn your journal into art, music & wisdom — powered by AI</p>', unsafe_allow_html=True)

# ── Journal Input ──
st.markdown('<div class="section-header">✍️ Your Journal Entry</div>', unsafe_allow_html=True)

journal_text = st.text_area(
    "Write freely about your day, thoughts, or feelings...",
    height=180,
    placeholder="Today I woke up feeling... The best part of my day was... I'm thinking about... I'm grateful for...",
    label_visibility="collapsed"
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
with col_btn1:
    analyze_btn = st.button("🧠 Analyze My Mood", type="primary", use_container_width=True)
with col_btn2:
    example_btn = st.button("📝 Try Example", use_container_width=True)

# ── Example text ──
if example_btn:
    st.session_state["example_text"] = (
        "Today was a really good day! I had a wonderful morning walk in the park, "
        "the sun was shining and the birds were singing. I felt so grateful for the little things. "
        "Had coffee with an old friend and we laughed about old memories. "
        "Sometimes life is just beautiful when you slow down and appreciate the moment."
    )
    st.rerun()

if "example_text" in st.session_state:
    journal_text = st.session_state.pop("example_text")
    st.info(f"📝 Example loaded: *\"{journal_text[:80]}...\"*")

# ──────────────────────────────────────────────
# Analysis Results
# ──────────────────────────────────────────────
if analyze_btn and journal_text.strip():
    
    # Analyze mood
    result = analyze_mood(journal_text)
    mood = result["mood"]
    emoji = result["emoji"]
    confidence = result["confidence"]
    color = result["color"]
    
    # Save to history
    save_entry({
        "mood": mood,
        "confidence": confidence,
        "polarity": result["polarity"],
        "journal_preview": journal_text,
        "emoji": emoji
    })
    
    st.markdown("---")
    
    # ── Row 1: Mood Detection + Art ──
    col_mood, col_art = st.columns([1, 2])
    
    with col_mood:
        st.markdown(f'<div class="section-header">🧠 Detected Mood</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {result['gradient'][0]}22, {result['gradient'][1]}22);
            border: 2px solid {color}44;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        ">
            <div style="font-size: 4rem;">{emoji}</div>
            <div style="font-size: 2rem; font-weight: 700; color: {color}; margin: 10px 0;">{mood}</div>
            <div style="color: #aaa; margin-bottom: 15px;">Confidence: {confidence}%</div>
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                height: 10px;
                width: 80%;
                margin: 0 auto;
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, {result['gradient'][0]}, {result['gradient'][1]});
                    height: 100%;
                    width: {confidence}%;
                    border-radius: 10px;
                "></div>
            </div>
            <div style="color: #888; font-size: 0.85rem; margin-top: 15px;">
                Polarity: {result['polarity']} | Subjectivity: {result['subjectivity']}
            </div>
            <div style="color: #999; font-size: 0.8rem; margin-top: 8px;">
                {result['details']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Emotion breakdown mini-chart
        if "all_scores" in result:
            scores = result["all_scores"]
            non_zero = {k: v for k, v in scores.items() if v > 0}
            if non_zero:
                st.markdown("<br>", unsafe_allow_html=True)
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(non_zero.keys()),
                    values=list(non_zero.values()),
                    hole=0.5,
                    marker_colors=[MOOD_CONFIG[m]["color"] for m in non_zero.keys()],
                    textinfo='label+percent',
                    textfont_size=11,
                )])
                fig_pie.update_layout(
                    title="Emotion Breakdown",
                    showlegend=False,
                    height=280,
                    margin=dict(t=40, b=10, l=10, r=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ccc')
                )
                st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_art:
        st.markdown(f'<div class="section-header">🎨 Your Mood Artwork</div>', unsafe_allow_html=True)
        
        # Generate SVG art
        svg_art = generate_mood_art_svg(mood, journal_text, width=700, height=420)
        
        st.markdown(f"""
        <div style="
            background: #111;
            border-radius: 16px;
            padding: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            border: 1px solid {color}33;
        ">
            {svg_art}
        </div>
        <div style="text-align: center; color: #666; font-size: 0.85rem; margin-top: 8px;">
            🖼️ Procedurally generated from your journal — each entry creates unique art!
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Row 2: Music + Advice ──
    col_music, col_advice = st.columns(2)
    
    with col_music:
        st.markdown(f'<div class="section-header">🎵 Music For Your Mood</div>', unsafe_allow_html=True)
        
        songs = get_music_recommendations(mood)
        
        for i, song in enumerate(songs):
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.03);
                border-radius: 12px;
                padding: 14px 18px;
                margin: 8px 0;
                border-left: 3px solid {color};
                display: flex;
                align-items: center;
            ">
                <span style="font-size: 1.4rem; margin-right: 12px;">{'🎵' if i % 2 == 0 else '🎶'}</span>
                <div>
                    <div style="font-weight: 600; font-size: 1rem;">{song['song']}</div>
                    <div style="color: #888; font-size: 0.85rem;">{song['artist']} · {song['genre']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 15px;">
            <span style="color: #1DB954; font-size: 0.9rem;">
                🎧 Search these on Spotify for the perfect {mood.lower()} playlist
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_advice:
        st.markdown(f'<div class="section-header">💡 AI Wisdom For You</div>', unsafe_allow_html=True)
        
        advice = get_ai_advice(mood, journal_text)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {result['gradient'][0]}15, {result['gradient'][1]}15);
            border: 1px solid {color}33;
            border-radius: 16px;
            padding: 28px;
            font-size: 1.15rem;
            line-height: 1.8;
            min-height: 120px;
        ">
            {advice}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick mood tips
        tips = {
            "Happy": "💛 Pro tip: Write down 3 things making you happy right now. Revisit on tough days!",
            "Sad": "💙 Remember: It's okay to not be okay. Every storm runs out of rain.",
            "Anxious": "🧡 Try this: Name 5 things you can see, 4 you can touch, 3 you can hear.",
            "Calm": "💚 Beautiful state! Practice gratitude to make this feeling last longer.",
            "Angry": "❤️ Channel it: Transform anger into motivation for positive change.",
            "Excited": "💗 Ride the wave! Use this energy to start something you've been putting off.",
            "Grateful": "💜 Gratitude is a superpower. Share it with someone today!",
            "Reflective": "💎 Reflection = growth. Keep journaling — patterns will reveal themselves."
        }
        
        st.info(tips.get(mood, "Keep journaling! Every entry reveals something new."))


# ──────────────────────────────────────────────
# Mood History Dashboard
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">📊 Your Mood Journey</div>', unsafe_allow_html=True)

history = load_history()

if history and len(history) >= 1:
    
    # ── Stats Row ──
    stat1, stat2, stat3, stat4 = st.columns(4)
    stats = get_mood_stats(history)
    
    with stat1:
        st.metric("📝 Total Entries", stats["total_entries"])
    with stat2:
        st.metric("🏆 Top Mood", f"{MOOD_CONFIG.get(stats['most_common_mood'], {}).get('emoji', '🤔')} {stats['most_common_mood']}")
    with stat3:
        avg_p = stats['avg_polarity']
        st.metric("📈 Avg Sentiment", f"{avg_p:+.2f}")
    with stat4:
        unique_moods = len(stats["mood_counts"])
        st.metric("🌈 Mood Range", f"{unique_moods} moods")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Mood timeline
        dates = [e.get("date", "N/A") for e in history]
        moods = [e.get("mood", "Reflective") for e in history]
        mood_to_num = {"Happy": 4, "Excited": 4, "Grateful": 3, "Calm": 3, 
                       "Reflective": 2, "Anxious": 1, "Sad": 0, "Angry": 0}
        mood_nums = [mood_to_num.get(m, 2) for m in moods]
        colors_list = [MOOD_CONFIG.get(m, {}).get("color", "#888") for m in moods]
        emojis = [MOOD_CONFIG.get(m, {}).get("emoji", "🤔") for m in moods]
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=list(range(len(history))),
            y=mood_nums,
            mode='lines+markers+text',
            text=emojis,
            textposition="top center",
            line=dict(color='#667eea', width=2),
            marker=dict(size=12, color=colors_list, line=dict(width=2, color='white')),
            hovertext=[f"{m} ({d})" for m, d in zip(moods, dates)],
            hoverinfo='text'
        ))
        fig_timeline.update_layout(
            title="📈 Mood Over Time",
            xaxis_title="Entry #",
            yaxis=dict(
                tickvals=[0, 1, 2, 3, 4],
                ticktext=["Low 😢", "Uneasy 😰", "Neutral 🤔", "Good 😌", "Great 😊"]
            ),
            height=350,
            margin=dict(t=50, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ccc')
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col_chart2:
        # Mood distribution
        mood_counts = stats["mood_counts"]
        
        fig_bar = go.Figure(data=[go.Bar(
            x=list(mood_counts.keys()),
            y=list(mood_counts.values()),
            marker_color=[MOOD_CONFIG.get(m, {}).get("color", "#888") for m in mood_counts.keys()],
            text=[MOOD_CONFIG.get(m, {}).get("emoji", "🤔") for m in mood_counts.keys()],
            textposition='outside',
        )])
        fig_bar.update_layout(
            title="🎯 Mood Distribution",
            xaxis_title="Mood",
            yaxis_title="Count",
            height=350,
            margin=dict(t=50, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ccc')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # ── Recent entries ──
    with st.expander("📋 Recent Journal Entries"):
        for entry in reversed(history[-10:]):
            mood_e = entry.get("emoji", "🤔")
            mood_n = entry.get("mood", "?")
            date = entry.get("date", "N/A")
            time = entry.get("time", "")
            preview = entry.get("journal_preview", "")
            conf = entry.get("confidence", 0)
            st.markdown(f"**{mood_e} {mood_n}** — {date} {time} (confidence: {conf}%)")
            if preview:
                st.caption(f"*\"{preview}...\"*")
            st.markdown("---")

else:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px;
        color: #666;
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        border: 1px dashed #333;
    ">
        <div style="font-size: 3rem; margin-bottom: 10px;">📝</div>
        <div style="font-size: 1.2rem;">No entries yet!</div>
        <div style="font-size: 0.9rem; margin-top: 5px;">Write your first journal entry above to start tracking your mood journey.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ──
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #444; font-size: 0.8rem; padding: 20px;">
    🎨 MoodCanvas AI v1.0 — Built with Python, Streamlit, TextBlob, Plotly & Generative AI<br>
    Transform your emotions into art, music & wisdom ✨
</div>
""", unsafe_allow_html=True)

"""
MoodCanvas AI — Art Generator
Creates beautiful mood-based artwork using either:
1. OpenAI DALL·E API (if API key available)
2. Procedural SVG art generation (demo mode — no API needed!)
"""

import math
import random
import hashlib


# ──────────────────────────────────────────────
# Mood color palettes for procedural art
# ──────────────────────────────────────────────

MOOD_PALETTES = {
    "Happy": {
        "bg": "#FFF8E7",
        "colors": ["#FFD700", "#FFA500", "#FF6347", "#FFB6C1", "#FFDAB9", "#F0E68C"],
        "shapes": "circles",
        "energy": "high"
    },
    "Sad": {
        "bg": "#1a1a2e",
        "colors": ["#4169E1", "#6495ED", "#87CEEB", "#B0C4DE", "#483D8B", "#2F4F4F"],
        "shapes": "drops",
        "energy": "low"
    },
    "Anxious": {
        "bg": "#2d1b2e",
        "colors": ["#FF6347", "#DC143C", "#FF4500", "#8B0000", "#CD853F", "#D2691E"],
        "shapes": "spirals",
        "energy": "chaotic"
    },
    "Calm": {
        "bg": "#f0f7f0",
        "colors": ["#90EE90", "#3CB371", "#2E8B57", "#98FB98", "#8FBC8F", "#66CDAA"],
        "shapes": "waves",
        "energy": "low"
    },
    "Angry": {
        "bg": "#1a0a0a",
        "colors": ["#DC143C", "#FF0000", "#8B0000", "#FF4500", "#B22222", "#CD5C5C"],
        "shapes": "shards",
        "energy": "high"
    },
    "Excited": {
        "bg": "#1a0a2e",
        "colors": ["#FF69B4", "#FF1493", "#DA70D6", "#FF00FF", "#FFD700", "#00FFFF"],
        "shapes": "stars",
        "energy": "high"
    },
    "Grateful": {
        "bg": "#f5f0ff",
        "colors": ["#DDA0DD", "#DA70D6", "#BA55D3", "#9370DB", "#FFB6C1", "#FFC0CB"],
        "shapes": "flowers",
        "energy": "medium"
    },
    "Reflective": {
        "bg": "#0a1628",
        "colors": ["#87CEEB", "#4682B4", "#5F9EA0", "#708090", "#B0C4DE", "#ADD8E6"],
        "shapes": "ripples",
        "energy": "low"
    }
}


def _seed_from_text(text: str) -> int:
    """Create a deterministic seed from text so same journal = same art."""
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


def generate_mood_art_svg(mood: str, journal_text: str = "", width: int = 600, height: int = 400) -> str:
    """
    Generate beautiful procedural SVG art based on mood.
    No API key needed — pure algorithmic art!
    
    Returns: SVG string
    """
    seed = _seed_from_text(journal_text or mood)
    rng = random.Random(seed)
    
    palette = MOOD_PALETTES.get(mood, MOOD_PALETTES["Reflective"])
    bg = palette["bg"]
    colors = palette["colors"]
    shape_type = palette["shapes"]
    energy = palette["energy"]
    
    elements = []
    
    # ── Background gradient ──
    grad_id = f"bg_grad_{seed % 1000}"
    c1 = colors[0]
    c2 = colors[-1]
    elements.append(f'''
    <defs>
        <radialGradient id="{grad_id}" cx="50%" cy="50%" r="70%">
            <stop offset="0%" style="stop-color:{bg};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{c2};stop-opacity:0.3" />
        </radialGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="soft">
            <feGaussianBlur stdDeviation="1.5"/>
        </filter>
    </defs>
    <rect width="{width}" height="{height}" fill="url(#{grad_id})"/>
    ''')
    
    num_shapes = {"high": 40, "medium": 25, "low": 15, "chaotic": 50}.get(energy, 25)
    
    # ── Generate shapes based on mood ──
    
    if shape_type == "circles":
        # Happy — floating, overlapping colorful circles
        for i in range(num_shapes):
            x = rng.randint(0, width)
            y = rng.randint(0, height)
            r = rng.randint(10, 80)
            color = rng.choice(colors)
            opacity = rng.uniform(0.2, 0.6)
            elements.append(
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{opacity}" filter="url(#soft)"/>'
            )
    
    elif shape_type == "drops":
        # Sad — falling teardrops / rain
        for i in range(num_shapes):
            x = rng.randint(0, width)
            y = rng.randint(0, height)
            size = rng.randint(3, 15)
            color = rng.choice(colors)
            opacity = rng.uniform(0.3, 0.7)
            # Teardrop shape using path
            elements.append(
                f'<ellipse cx="{x}" cy="{y}" rx="{size}" ry="{size*2}" fill="{color}" opacity="{opacity}" filter="url(#soft)"/>'
            )
        # Add some horizontal lines like rain streaks
        for i in range(8):
            x1 = rng.randint(0, width)
            y1 = rng.randint(0, height)
            length = rng.randint(20, 80)
            color = rng.choice(colors)
            elements.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x1+5}" y2="{y1+length}" stroke="{color}" stroke-width="1" opacity="0.3"/>'
            )
    
    elif shape_type == "spirals":
        # Anxious — chaotic spirals and tangled lines
        for i in range(num_shapes // 3):
            cx = rng.randint(50, width - 50)
            cy = rng.randint(50, height - 50)
            color = rng.choice(colors)
            path_d = f"M {cx} {cy} "
            for j in range(30):
                angle = j * 0.5
                r = j * 2
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                path_d += f"L {px:.1f} {py:.1f} "
            elements.append(
                f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.5" filter="url(#glow)"/>'
            )
    
    elif shape_type == "waves":
        # Calm — gentle sine waves
        for i in range(12):
            y_base = 30 + i * 30
            color = rng.choice(colors)
            amplitude = rng.uniform(8, 25)
            freq = rng.uniform(0.01, 0.03)
            phase = rng.uniform(0, 6.28)
            path_d = f"M 0 {y_base} "
            for x in range(0, width + 5, 5):
                y = y_base + amplitude * math.sin(freq * x + phase)
                path_d += f"L {x} {y:.1f} "
            elements.append(
                f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="2" opacity="0.4"/>'
            )
    
    elif shape_type == "shards":
        # Angry — sharp geometric shards
        for i in range(num_shapes):
            x = rng.randint(0, width)
            y = rng.randint(0, height)
            size = rng.randint(15, 60)
            color = rng.choice(colors)
            opacity = rng.uniform(0.3, 0.7)
            # Random triangle
            points = []
            for _ in range(3):
                px = x + rng.randint(-size, size)
                py = y + rng.randint(-size, size)
                points.append(f"{px},{py}")
            elements.append(
                f'<polygon points="{" ".join(points)}" fill="{color}" opacity="{opacity}"/>'
            )
    
    elif shape_type == "stars":
        # Excited — star bursts and sparkles
        for i in range(num_shapes):
            cx = rng.randint(20, width - 20)
            cy = rng.randint(20, height - 20)
            size = rng.randint(5, 30)
            color = rng.choice(colors)
            opacity = rng.uniform(0.4, 0.9)
            # 4-pointed star
            points = []
            for j in range(8):
                angle = j * math.pi / 4
                r = size if j % 2 == 0 else size * 0.4
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                points.append(f"{px:.1f},{py:.1f}")
            elements.append(
                f'<polygon points="{" ".join(points)}" fill="{color}" opacity="{opacity}" filter="url(#glow)"/>'
            )
    
    elif shape_type == "flowers":
        # Grateful — soft flower-like shapes
        for i in range(num_shapes // 2):
            cx = rng.randint(40, width - 40)
            cy = rng.randint(40, height - 40)
            size = rng.randint(10, 35)
            color = rng.choice(colors)
            opacity = rng.uniform(0.3, 0.6)
            # Petals using circles around center
            for j in range(6):
                angle = j * math.pi / 3
                px = cx + size * math.cos(angle)
                py = cy + size * math.sin(angle)
                elements.append(
                    f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{size*0.6}" fill="{color}" opacity="{opacity}" filter="url(#soft)"/>'
                )
            elements.append(
                f'<circle cx="{cx}" cy="{cy}" r="{size*0.35}" fill="{colors[0]}" opacity="{opacity+0.1}"/>'
            )
    
    elif shape_type == "ripples":
        # Reflective — concentric ripples
        num_centers = rng.randint(3, 6)
        for i in range(num_centers):
            cx = rng.randint(50, width - 50)
            cy = rng.randint(50, height - 50)
            color = rng.choice(colors)
            for j in range(1, 8):
                r = j * rng.randint(15, 30)
                opacity = max(0.1, 0.5 - j * 0.06)
                elements.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="1.5" opacity="{opacity}"/>'
                )
    
    # ── Assemble SVG ──
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    {"".join(elements)}
    <text x="{width//2}" y="{height - 15}" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{colors[0]}" opacity="0.5">MoodCanvas AI — {mood}</text>
</svg>'''
    
    return svg


def generate_mood_art_with_api(mood: str, journal_text: str, api_key: str) -> str:
    """
    Generate art using OpenAI DALL·E API.
    Returns: URL of generated image
    """
    try:
        from openai import OpenAI
        from mood_engine import get_mood_art_prompt
        
        client = OpenAI(api_key=api_key)
        prompt = get_mood_art_prompt(mood, journal_text)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        return response.data[0].url
    except Exception as e:
        return None

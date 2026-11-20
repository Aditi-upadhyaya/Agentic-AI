"""
generate_promo.py
-----------------
Generates a 35-second high-definition (1280x720, 24fps) animated promo video
for ANANTA INFOTECH featuring the real-world Agentic AI case study
(Student Inquiry -> Gemini LLM -> FastMCP -> Private Database -> Grounded Delivery)
and displays trainer contact details at the end.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "agentic_ai_promo.mp4")

WIDTH = 1280
HEIGHT = 720
FPS = 24
DURATION = 35  # Exactly 35.0 seconds
TOTAL_FRAMES = FPS * DURATION

def get_fonts():
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf",  # Segoe UI Bold
        "C:\\Windows\\Fonts\\arialbd.ttf",   # Arial Bold
        "C:\\Windows\\Fonts\\calibrib.ttf"   # Calibri Bold
    ]
    font_reg_paths = [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    
    bold_path = next((p for p in font_paths if os.path.exists(p)), None)
    reg_path = next((p for p in font_reg_paths if os.path.exists(p)), None)

    if bold_path:
        title_font = ImageFont.truetype(bold_path, 34)
        subtitle_font = ImageFont.truetype(bold_path, 22)
        card_font = ImageFont.truetype(bold_path, 19)
        caption_font = ImageFont.truetype(bold_path, 26)
        small_font = ImageFont.truetype(reg_path or bold_path, 16)
        contact_font = ImageFont.truetype(bold_path, 21)
    else:
        title_font = subtitle_font = card_font = caption_font = small_font = contact_font = ImageFont.load_default()

    return title_font, subtitle_font, card_font, caption_font, small_font, contact_font

title_font, subtitle_font, card_font, caption_font, small_font, contact_font = get_fonts()


def draw_card(draw, box, radius=14, fill=(20, 26, 45), outline=(59, 130, 246), width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def render_stations(draw, active_index, pulse_t):
    """Renders the 4 horizontal architectural stations across the screen"""
    stations = [
        {"title": "1. WEB PORTAL", "sub": "anantainfotech.co.in", "icon": "🌐", "accent": (59, 130, 246)},
        {"title": "2. ANANTA AGENT", "sub": "Internal Orchestrator", "icon": "⚙️", "accent": (168, 85, 247)},
        {"title": "3. GEMINI LLM", "sub": "Autonomous Brain", "icon": "🧠", "accent": (236, 72, 153)},
        {"title": "4. PRIVATE VAULT", "sub": "FastMCP + Database", "icon": "📁", "accent": (16, 185, 129)}
    ]

    card_w = 230
    card_h = 100
    gap = 70
    start_x = (WIDTH - (4 * card_w + 3 * gap)) // 2
    y = 150

    coords = []
    for i, s in enumerate(stations):
        x = start_x + i * (card_w + gap)
        coords.append((x, y, card_w, card_h))
        is_active = (i == active_index)
        border_col = s["accent"] if is_active else (55, 65, 81)
        fill_col = (25, 33, 58) if is_active else (15, 20, 32)
        glow = int(3 * math.sin(pulse_t * 8)) if is_active else 0

        draw_card(draw, (x, y, x + card_w, y + card_h), fill=fill_col, outline=border_col, width=3 + glow if is_active else 1)
        draw.text((x + card_w//2, y + 32), f"{s['icon']} {s['title']}", font=card_font, fill=s["accent"] if is_active else (156, 163, 175), anchor="mm")
        draw.text((x + card_w//2, y + 68), s["sub"], font=small_font, fill=(255, 255, 255) if is_active else (107, 114, 128), anchor="mm")

        # Connection line with animated traveling particle
        if i < 3:
            line_start_x = x + card_w
            line_end_x = line_start_x + gap
            line_y = y + card_h // 2
            draw.line([(line_start_x, line_y), (line_end_x, line_y)], fill=(55, 65, 81), width=2)
            
            # Pulse traveling forward
            if active_index == i:
                p_progress = (pulse_t % 1.0)
                px = line_start_x + int(p_progress * gap)
                draw.ellipse([(px - 6, line_y - 6), (px + 6, line_y + 6)], fill=s["accent"])

    return coords


def render_act_1(draw, t, act_t):
    """Act 1 (00:00 - 00:08): Student Inquiry at Ananta Infotech"""
    draw.text((WIDTH//2, 55), "ANANTA INFOTECH: AGENTIC AI CASE STUDY", font=title_font, fill=(255, 255, 255), anchor="mm")
    draw.text((WIDTH//2, 95), "Step 1: Student visits anantainfotech.co.in & submits an inquiry", font=subtitle_font, fill=(96, 165, 250), anchor="mm")

    render_stations(draw, active_index=0, pulse_t=act_t)

    # Big Interactive Web Inquiry Card
    draw_card(draw, (220, 280, 1060, 480), fill=(17, 24, 39), outline=(59, 130, 246), width=3)
    draw.text((WIDTH//2, 320), "🌐 ANANTA INFOTECH STUDENT INQUIRY PORTAL", font=card_font, fill=(96, 165, 250), anchor="mm")

    # Inquiry input box with typed text
    draw_card(draw, (280, 355, 1000, 420), fill=(31, 41, 55), outline=(52, 211, 153), width=2)
    draw.text((WIDTH//2, 388), '💬 "Please give me the Java intermediate syllabus"', font=card_font, fill=(255, 255, 255), anchor="mm")

    draw.text((WIDTH//2, 450), "➡️ Query captured! Forwarding to Ananta Internal AI Agent...", font=small_font, fill=(52, 211, 153), anchor="mm")


def render_act_2(draw, t, act_t):
    """Act 2 (00:08 - 00:17): Gemini Reasoning & FastMCP Tool Call"""
    draw.text((WIDTH//2, 55), "AUTONOMOUS REASONING & PROTOCOL CALL", font=title_font, fill=(192, 132, 252), anchor="mm")
    draw.text((WIDTH//2, 95), "Step 2: Google Gemini extracts intent & fires an MCP tool call", font=subtitle_font, fill=(209, 213, 219), anchor="mm")

    render_stations(draw, active_index=2, pulse_t=act_t)

    # Two detail cards: Left = Gemini Intent, Right = FastMCP Tool Call
    draw_card(draw, (140, 280, 610, 485), fill=(17, 24, 39), outline=(236, 72, 153), width=2)
    draw.text((375, 315), "🧠 GEMINI INTENT ANALYSIS", font=card_font, fill=(244, 114, 182), anchor="mm")
    draw.text((375, 360), 'User Request: "Java Intermediate"', font=small_font, fill=(255, 255, 255), anchor="mm")
    draw.text((375, 395), "Extracted Course: 'java'", font=small_font, fill=(52, 211, 153), anchor="mm")
    draw.text((375, 430), "Extracted Level: 'intermediate'", font=small_font, fill=(52, 211, 153), anchor="mm")
    draw.text((375, 460), "Decision: Invoke FastMCP Tool!", font=small_font, fill=(251, 191, 36), anchor="mm")

    draw_card(draw, (670, 280, 1140, 485), fill=(17, 24, 39), outline=(16, 185, 129), width=2)
    draw.text((905, 315), "🔌 FASTMCP TOOL EXECUTION", font=card_font, fill=(52, 211, 153), anchor="mm")
    draw.text((905, 360), "Protocol: Model Context Protocol", font=small_font, fill=(156, 163, 175), anchor="mm")
    draw.text((905, 400), "call: get_syllabus(", font=card_font, fill=(255, 255, 255), anchor="mm")
    draw.text((905, 430), "  course='java', level='intermediate'", font=card_font, fill=(52, 211, 153), anchor="mm")
    draw.text((905, 460), ") -> Calling Ananta Private Database...", font=small_font, fill=(156, 163, 175), anchor="mm")


def render_act_3(draw, t, act_t):
    """Act 3 (00:17 - 00:26): Secure Database Fetch & Grounded Delivery"""
    draw.text((WIDTH//2, 55), "GROUNDED TRUTH & ZERO HALLUCINATION", font=title_font, fill=(52, 211, 153), anchor="mm")
    draw.text((WIDTH//2, 95), "Step 3: Verified JSON retrieved & delivered live to student", font=subtitle_font, fill=(209, 213, 219), anchor="mm")

    render_stations(draw, active_index=3, pulse_t=act_t)

    # Result Card: Grounded Curriculum Delivered to User
    draw_card(draw, (180, 275, 1100, 485), fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((WIDTH//2, 305), "✅ ANANTA INFOTECH VERIFIED JAVA SYLLABUS DELIVERED", font=card_font, fill=(52, 211, 153), anchor="mm")

    # Module details
    draw_card(draw, (220, 335, 620, 450), fill=(24, 33, 56), outline=(59, 130, 246), width=1)
    draw.text((420, 365), "Module 1: Flowing Streams", font=card_font, fill=(255, 255, 255), anchor="mm")
    draw.text((420, 400), "• Lambdas & Functional Interfaces", font=small_font, fill=(156, 163, 175), anchor="mm")
    draw.text((420, 425), "• High-performance data pipelines", font=small_font, fill=(52, 211, 153), anchor="mm")

    draw_card(draw, (660, 335, 1060, 450), fill=(24, 33, 56), outline=(59, 130, 246), width=1)
    draw.text((860, 365), "Module 2: Project Loom & Threads", font=card_font, fill=(255, 255, 255), anchor="mm")
    draw.text((860, 400), "• Virtual Threads & Concurrency", font=small_font, fill=(156, 163, 175), anchor="mm")
    draw.text((860, 425), "• Millions of lightweight tasks", font=small_font, fill=(52, 211, 153), anchor="mm")

    draw.text((WIDTH//2, 468), "✨ 100% Grounded in Private Database • Zero Hallucination • Built with FastMCP", font=small_font, fill=(251, 191, 36), anchor="mm")


def render_act_4(draw, t, act_t):
    """Act 4 (00:26 - 00:35): Masterclass Pitch & Contact Information"""
    draw.text((WIDTH//2, 45), "ANANTA INFOTECH", font=title_font, fill=(251, 191, 36), anchor="mm")
    draw.text((WIDTH//2, 85), "HANDS-ON AGENTIC AI & MODEL CONTEXT PROTOCOL (MCP) MASTERCLASS", font=subtitle_font, fill=(255, 255, 255), anchor="mm")

    # Main Executive Contact Card
    draw_card(draw, (140, 120, 1140, 485), radius=20, fill=(17, 24, 39), outline=(59, 130, 246), width=3)

    # 3 Feature Pills
    pills = [
        "⚡ FastMCP Tool Protocols",
        "🤖 Autonomous Gemini & Claude Tool Calling",
        "🚀 Full-Stack AI Architecture"
    ]
    for i, p in enumerate(pills):
        px = 180 + i * 325
        draw_card(draw, (px, 140, px + 300, 185), radius=10, fill=(30, 41, 59), outline=(75, 85, 99), width=1)
        draw.text((px + 150, 162), p, font=small_font, fill=(52, 211, 153), anchor="mm")

    # Trainer Details Box
    draw.text((WIDTH//2, 220), "👨‍🏫 INSTRUCTOR & CORPORATE TRAINER: MANOJ UPADHYAYA", font=card_font, fill=(255, 255, 255), anchor="mm")
    draw.line([(340, 240), (940, 240)], fill=(75, 85, 99), width=1)

    # Contact Details (Prominently Displayed)
    draw_card(draw, (200, 255, 1080, 410), radius=14, fill=(10, 15, 29), outline=(16, 185, 129), width=2)

    # 1. Mobile & WhatsApp
    draw.text((240, 285), "📱 Mobile & WhatsApp:", font=contact_font, fill=(156, 163, 175))
    draw.text((520, 285), "+91 9850597704", font=contact_font, fill=(52, 211, 153))

    # 2. Emails
    draw.text((240, 325), "✉️ Email Addresses:", font=contact_font, fill=(156, 163, 175))
    draw.text((520, 325), "manoj@anantainfotech.co.in  |  manojl.upadhyaya@gmail.com", font=small_font, fill=(255, 255, 255))

    # 3. Website
    draw.text((240, 365), "🌐 Official Website:", font=contact_font, fill=(156, 163, 175))
    draw.text((520, 365), "anantainfotech.co.in", font=contact_font, fill=(96, 165, 250))

    # Pulsing CTA Button
    pulse = int(3 * math.sin(act_t * 8))
    draw_card(draw, (360, 425, 920, 475), radius=12, fill=(30, 64, 175), outline=(96, 165, 250), width=2 + pulse)
    draw.text((WIDTH//2, 450), "👉 ENROLL IN THE MASTERCLASS TODAY • LIMITED SEATS", font=card_font, fill=(255, 255, 255), anchor="mm")


def render_caption_bar(draw, caption_text, act_label, t):
    """High-contrast bottom caption bar for OBS recording"""
    draw.rectangle([0, HEIGHT - 130, WIDTH, HEIGHT], fill=(8, 12, 22))
    draw.line([(0, HEIGHT - 130), (WIDTH, HEIGHT - 130)], fill=(37, 99, 235), width=2)

    mins = int(t) // 60
    secs = int(t) % 60
    time_str = f"{mins:02d}:{secs:02d} / 00:35"
    draw.text((40, HEIGHT - 105), f"🎙️ {act_label.upper()}  •  {time_str}", font=small_font, fill=(96, 165, 250))
    draw.text((WIDTH//2, HEIGHT - 55), f'"{caption_text}"', font=caption_font, fill=(255, 255, 255), anchor="mm")


def get_current_caption(t):
    """Synchronized captions matching the 35s timeline"""
    if t < 4.0:
        return "A student visits Ananta Infotech asking for the Java Intermediate syllabus.", "Act 1: Website Inquiry"
    elif t < 8.0:
        return "Our AI agent instantly captures the natural language inquiry.", "Act 1: Website Inquiry"
    elif t < 12.5:
        return "The agent contacts Google Gemini, which analyzes user intent autonomously.", "Act 2: Gemini & FastMCP"
    elif t < 17.0:
        return "Gemini issues an autonomous tool call via Model Context Protocol.", "Act 2: Gemini & FastMCP"
    elif t < 21.5:
        return "FastMCP queries Ananta's private database vault and retrieves verified JSON.", "Act 3: Grounded Truth"
    elif t < 26.0:
        return "Delivering a grounded, verified curriculum with zero hallucination!", "Act 3: Grounded Truth"
    elif t < 30.5:
        return "Learn how to architect and build real Agentic AI systems like this.", "Act 4: Ananta Infotech Training"
    else:
        return "Contact Manoj Upadhyaya at Ananta Infotech (+91 9850597704) today!", "Act 4: Ananta Infotech Training"


def main():
    print(f"Generating 35-second Ananta Infotech video: {WIDTH}x{HEIGHT} @ {FPS}fps ({TOTAL_FRAMES} frames)...")
    writer = imageio.get_writer(OUTPUT_FILE, fps=FPS, codec="libx264", quality=8)

    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS

        # Dark theme canvas
        img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 14, 26))
        draw = ImageDraw.Draw(img)

        # Render corresponding Act based on timestamp
        if t < 8.0:
            render_act_1(draw, t, t)
        elif t < 17.0:
            render_act_2(draw, t, t - 8.0)
        elif t < 26.0:
            render_act_3(draw, t, t - 17.0)
        else:
            render_act_4(draw, t, t - 26.0)

        # Bottom Caption Bar
        caption, act_label = get_current_caption(t)
        render_caption_bar(draw, caption, act_label, t)

        # Write frame to video
        frame_np = np.array(img)
        writer.append_data(frame_np)

        if frame_idx % (FPS * 5) == 0:
            print(f"Render progress: {int(t)}s / {DURATION}s ({int(frame_idx/TOTAL_FRAMES*100)}%)...")

    writer.close()
    print(f"\n✅ Video successfully rendered and saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()

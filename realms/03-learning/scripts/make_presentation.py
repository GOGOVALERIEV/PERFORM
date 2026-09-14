"""
Universal Presentation Builder — python-pptx
=============================================
Claude uses this to build ANY presentation George asks for.

HOW CLAUDE USES THIS:
1. George says: "Make me a presentation about X"
2. Claude researches the topic + finds image URLs
3. Claude edits the TOPIC, SLIDES, and IMAGES sections below
4. Claude runs: python scripts/make_presentation.py
5. PPTX appears on Desktop

DESIGN: Dark theme, real photos, clean text, no overflow issues.
"""
import sys
import os
import io
import time
import requests
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Fix encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# === PATHS ===
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
IMG_DIR = os.path.join(OUTPUT_DIR, "presentation_images")
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
os.makedirs(IMG_DIR, exist_ok=True)

# === COLORS ===
BG_DARK = RGBColor(0x0F, 0x0E, 0x17)
BG_CARD = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT = RGBColor(0x6C, 0x63, 0xFF)
ACCENT2 = RGBColor(0xFF, 0x65, 0x84)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xCC, 0xCC, 0xCC)
MUTED = RGBColor(0xA7, 0xA9, 0xBE)
GOLD = RGBColor(0xFF, 0xD7, 0x00)

# ================================================================
# EDIT THIS SECTION FOR EACH PRESENTATION
# ================================================================

TITLE = "Изкуствен Интелект в Образованието"
SUBTITLE = "Как AI променя начина, по който учим"
AUTHOR = ""
FILENAME = "AI-Education.pptx"

# Each slide: (type, title, content, image_url_or_None)
# Types: "title", "bullets", "two_column", "image_right", "image_left", "stats", "conclusion"
SLIDES = [
    ("title", TITLE, SUBTITLE, "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&q=80"),

    ("bullets", "Какво е AI в образованието?", [
        "AI използва машинно обучение за персонализиране на учебния процес",
        "Автоматично оценяване и мигновена обратна връзка",
        "AI асистенти като ChatGPT и Claude помагат с обяснения",
        "Генериране на презентации, резюмета и тестове",
        "Анализ на данни за проследяване на напредъка",
    ], "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&q=80"),

    ("stats", "Ключова Статистика", [
        ("86%", "от учениците използват AI за домашни"),
        ("$20B+", "глобален пазар на AI в образованието"),
        ("47%", "по-бързо учене с AI персонализация"),
        ("3.5x", "ръст на EdTech от 2020 г."),
    ], None),

    ("image_right", "AI Инструменти за Ученици", [
        "ChatGPT / Claude — обяснения и помощ с есета",
        "Google NotebookLM — анализ на документи",
        "Gamma.app — AI презентации безплатно",
        "Anki + AI — автоматични флашкарти",
        "Zotero + GPT — AI резюмира научни статии",
    ], "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=800&q=80"),

    ("image_left", "AI Инструменти за Учители", [
        "Автоматично оценяване на домашни и тестове",
        "Генериране на въпроси от учебен материал",
        "Персонализирани учебни планове за всеки ученик",
        "Транскрипция и резюме на видео лекции",
        "24/7 чатбот помощник за студенти",
    ], "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&q=80"),

    ("two_column", "Предимства и Рискове", {
        "left_title": "Предимства",
        "left_items": [
            "Персонализирано темпо за всеки",
            "Мигновена обратна връзка",
            "24/7 достъпност за учене",
            "Намалена административна работа",
        ],
        "right_title": "Рискове",
        "right_items": [
            "Академична нечестност (копиране)",
            "Зависимост от технологиите",
            "Неточности в AI отговорите",
            "Неравен достъп за бедни ученици",
        ],
    }, None),

    ("bullets", "Бъдещето на AI в Образованието", [
        "AI учители-асистенти във всяка класна стая до 2030 г.",
        "VR + AI — виртуални лаборатории и екскурзии",
        "Реално време превод — учене на всеки език",
        "Емоционален AI — разпознаване кога ученикът е объркан",
        "Автоматично генериране на персонализирани учебници",
    ], "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=800&q=80"),

    ("conclusion", "Заключение", [
        "AI не заменя ученето — прави го по-достъпно и по-интересно",
        "Технологията вече е настояще, не бъдеще",
        "Учителите, които използват AI, ще заменят тези, които не го правят",
    ], None),
]

# ================================================================
# PRESENTATION BUILDER (Don't edit below unless fixing bugs)
# ================================================================

def download_image(url, name):
    """Download and resize image."""
    filepath = os.path.join(IMG_DIR, f"{name}.jpg")
    if os.path.exists(filepath):
        print(f"  [cache] {name}")
        return filepath

    print(f"  [download] {name}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; educational project; contact: test@example.com)"}
    for attempt in range(4):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 429:
                wait = 5 * (attempt + 1)
                print(f"    [retry] rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            break
        except Exception as e:
            if attempt == 3:
                print(f"  [FAIL] {name}: {e}")
                return None
            time.sleep(3)

    try:
        img = Image.open(io.BytesIO(resp.content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
        img.save(filepath, "JPEG", quality=85)
        print(f"  [saved] {name} ({img.width}x{img.height})")
        return filepath
    except Exception as e:
        print(f"  [FAIL] processing {name}: {e}")
        return None


def set_bg(slide, color=BG_DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_bg_image(slide, img_path, prs):
    if not img_path:
        return
    pic = slide.shapes.add_picture(img_path, 0, 0, prs.slide_width, prs.slide_height)
    sp = pic._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)


def add_overlay(slide, prs, alpha="55000"):
    from lxml import etree
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    shape.line.fill.background()
    sp = shape._element
    nsmap = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    spPr = sp.find(".//a:spPr", nsmap)
    if spPr is not None:
        for old in spPr.findall("a:solidFill", nsmap) + spPr.findall("a:noFill", nsmap):
            spPr.remove(old)
        sf = etree.SubElement(spPr, f"{{{nsmap['a']}}}solidFill")
        clr = etree.SubElement(sf, f"{{{nsmap['a']}}}srgbClr", val="0F0E17")
        etree.SubElement(clr, f"{{{nsmap['a']}}}alpha", val=alpha)


def add_text(slide, left, top, width, height, text, size=18, color=WHITE,
             bold=False, align=PP_ALIGN.LEFT, font="Calibri"):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = str(text)
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font
    p.alignment = align
    return box


def add_bullets(slide, items, left, top, width, size=15, color=LIGHT):
    box = slide.shapes.add_textbox(left, top, width, Inches(3.5))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"  {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(8)
    return box


def add_card(slide, left, top, width, height, color=BG_CARD):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_accent_line(slide, left, top, width):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()


# === SLIDE BUILDERS ===

def build_title(prs, title, subtitle, img_path):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    if img_path:
        add_bg_image(slide, img_path, prs)
        add_overlay(slide, prs)
    else:
        set_bg(slide)
    add_text(slide, Inches(0.8), Inches(1.5), Inches(8.4), Inches(1.5),
             title, size=44, bold=True, align=PP_ALIGN.CENTER)
    add_accent_line(slide, Inches(3.5), Inches(3.2), Inches(3))
    if subtitle:
        add_text(slide, Inches(0.8), Inches(3.5), Inches(8.4), Inches(1),
                 subtitle, size=20, color=LIGHT, align=PP_ALIGN.CENTER)


def build_bullets(prs, title, items, img_path):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    if img_path:
        add_bg_image(slide, img_path, prs)
        add_overlay(slide, prs, "70000")
    else:
        set_bg(slide)
    add_text(slide, Inches(0.6), Inches(0.3), Inches(8.8), Inches(0.7),
             title, size=28, color=ACCENT, bold=True)
    add_accent_line(slide, Inches(0.6), Inches(1.0), Inches(2))
    add_bullets(slide, items, Inches(0.6), Inches(1.2), Inches(8.8))


def build_image_right(prs, title, items, img_path):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_text(slide, Inches(0.6), Inches(0.3), Inches(8.8), Inches(0.7),
             title, size=28, color=ACCENT, bold=True)
    add_accent_line(slide, Inches(0.6), Inches(1.0), Inches(2))
    add_bullets(slide, items, Inches(0.5), Inches(1.2), Inches(5))
    if img_path:
        try:
            slide.shapes.add_picture(img_path, Inches(6), Inches(1.3), Inches(3.5), Inches(3.5))
        except Exception:
            pass


def build_image_left(prs, title, items, img_path):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_text(slide, Inches(0.6), Inches(0.3), Inches(8.8), Inches(0.7),
             title, size=28, color=ACCENT, bold=True)
    add_accent_line(slide, Inches(0.6), Inches(1.0), Inches(2))
    if img_path:
        try:
            slide.shapes.add_picture(img_path, Inches(0.5), Inches(1.3), Inches(3.5), Inches(3.5))
        except Exception:
            pass
    add_bullets(slide, items, Inches(4.5), Inches(1.2), Inches(5.2))


def build_stats(prs, title, stats, _):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_text(slide, Inches(0.6), Inches(0.3), Inches(8.8), Inches(0.7),
             title, size=28, color=ACCENT, bold=True)
    add_accent_line(slide, Inches(0.6), Inches(1.0), Inches(2))

    cols = min(len(stats), 4)
    card_w = Inches(2.1)
    gap = Inches(0.25)
    total_w = cols * card_w + (cols - 1) * gap
    start_x = (prs.slide_width - total_w) / 2

    for i, (num, label) in enumerate(stats):
        row = i // 4
        col = i % 4
        x = start_x + col * (card_w + gap)
        y = Inches(1.5) + row * Inches(2.2)
        add_card(slide, x, y, card_w, Inches(1.9))
        add_text(slide, x, y + Inches(0.2), card_w, Inches(0.8),
                 str(num), size=32, color=ACCENT2, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, x + Inches(0.1), y + Inches(1.0), card_w - Inches(0.2), Inches(0.8),
                 str(label), size=11, color=LIGHT, align=PP_ALIGN.CENTER)


def build_two_column(prs, title, data, _):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_text(slide, Inches(0.6), Inches(0.3), Inches(8.8), Inches(0.7),
             title, size=28, color=ACCENT, bold=True)
    add_accent_line(slide, Inches(0.6), Inches(1.0), Inches(2))

    # Left column
    add_card(slide, Inches(0.4), Inches(1.3), Inches(4.5), Inches(3.8), RGBColor(0x1A, 0x2E, 0x1A))
    add_text(slide, Inches(0.6), Inches(1.4), Inches(4.1), Inches(0.5),
             data["left_title"], size=18, color=RGBColor(0x4C, 0xAF, 0x50), bold=True)
    add_bullets(slide, data["left_items"], Inches(0.6), Inches(1.9), Inches(4.1), size=13)

    # Right column
    add_card(slide, Inches(5.1), Inches(1.3), Inches(4.5), Inches(3.8), RGBColor(0x2E, 0x1A, 0x1A))
    add_text(slide, Inches(5.3), Inches(1.4), Inches(4.1), Inches(0.5),
             data["right_title"], size=18, color=ACCENT2, bold=True)
    add_bullets(slide, data["right_items"], Inches(5.3), Inches(1.9), Inches(4.1), size=13)


def build_conclusion(prs, title, items, _):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.8), Inches(8.4), Inches(1),
             title, size=36, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
    add_accent_line(slide, Inches(3.5), Inches(1.7), Inches(3))

    for i, item in enumerate(items):
        y = Inches(2.2) + i * Inches(0.9)
        add_card(slide, Inches(1), y, Inches(8), Inches(0.7))
        add_text(slide, Inches(1.3), y + Inches(0.1), Inches(7.4), Inches(0.5),
                 item, size=15, color=WHITE, align=PP_ALIGN.CENTER)

    add_text(slide, Inches(0.5), Inches(4.8), Inches(9), Inches(0.5),
             "Благодаря за вниманието!", size=22, color=GOLD,
             bold=True, align=PP_ALIGN.CENTER)


BUILDERS = {
    "title": build_title,
    "bullets": build_bullets,
    "image_right": build_image_right,
    "image_left": build_image_left,
    "stats": build_stats,
    "two_column": build_two_column,
    "conclusion": build_conclusion,
}


def main():
    print("=" * 50)
    print(f"  PRESENTATION: {TITLE}")
    print("=" * 50)

    # Download images
    print("\nDownloading images...")
    images = {}
    for i, (stype, stitle, content, img_url) in enumerate(SLIDES):
        if img_url:
            img_path = download_image(img_url, f"slide_{i}")
            images[i] = img_path
            time.sleep(2)
        else:
            images[i] = None

    # Build presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    print("\nBuilding slides...")
    for i, (stype, stitle, content, img_url) in enumerate(SLIDES):
        builder = BUILDERS.get(stype, build_bullets)
        builder(prs, stitle, content, images.get(i))
        print(f"  [{i+1}/{len(SLIDES)}] {stitle}")

    # Save
    output_path = os.path.join(DESKTOP, FILENAME)
    prs.save(output_path)
    print(f"\nDone! Saved to: {output_path}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()

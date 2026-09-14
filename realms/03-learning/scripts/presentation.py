"""
Prezentacia: Prirodni bedstvia
Generates a PowerPoint file with real photos and info in Bulgarian.
"""

import sys
import os
import io

# Fix console encoding for Bulgarian text on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# === CONFIG ===
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
IMG_DIR = os.path.join(OUTPUT_DIR, "disaster_images")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Природни_бедствия.pptx")

os.makedirs(IMG_DIR, exist_ok=True)

# === COLORS ===
DARK_BG = RGBColor(0x1B, 0x1B, 0x2F)       # тъмно синьо-черно
ACCENT = RGBColor(0xE8, 0x4D, 0x4D)         # червено за акцент
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
YELLOW = RGBColor(0xFF, 0xD7, 0x00)
DARK_OVERLAY = RGBColor(0x10, 0x10, 0x20)

# === IMAGE URLS ===
IMAGES = {
    "title": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Hatay_in_the_2023_Gaziantep-Kahramanmara%C5%9F_earthquakes_01.jpg",
    "earthquake": "https://upload.wikimedia.org/wikipedia/commons/6/6c/City_of_Antakya_after_7.8_magnitude_earthquake_in_T%C3%BCrkiye.jpg",
    "before": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Hatay_Antakya_Turkey_2013_View.jpg",
    "after": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Aerial_View_of_Antakya_after_the_7.8_magnitude_earthquake_that_occurred_in_Turkey_2.jpg",
    "tsunami": "https://upload.wikimedia.org/wikipedia/commons/2/2d/2004-tsunami.jpg",
    "flood": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Devastating_floods_in_Pakistan.jpg",
    "volcano": "https://upload.wikimedia.org/wikipedia/commons/d/d1/MSH80_eruption_mount_st_helens_05-18-80-dramatic-edit.jpg",
    "hurricane": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Hurricane_Katrina_August_28_2005_NASA.jpg",
}


def download_image(name, url, max_width=1920):
    """Download and resize image to keep file size reasonable."""
    import time
    filepath = os.path.join(IMG_DIR, f"{name}.jpg")
    if os.path.exists(filepath):
        print(f"  [cache] {name}")
        return filepath

    print(f"  [download] {name}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; educational project; contact: test@example.com)"}
    # Retry with delay to avoid 429
    for attempt in range(3):
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 429:
            wait = 3 * (attempt + 1)
            print(f"    [retry] waiting {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        break
    else:
        resp.raise_for_status()

    img = Image.open(io.BytesIO(resp.content))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    img.save(filepath, "JPEG", quality=85)
    print(f"  [saved] {name} ({img.width}x{img.height})")
    return filepath


def download_all():
    """Download all images."""
    import time
    print("Сваляне на снимки...")
    paths = {}
    for name, url in IMAGES.items():
        try:
            paths[name] = download_image(name, url)
            time.sleep(1.5)  # polite delay between requests
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")
            paths[name] = None
    return paths


def set_slide_bg(slide, color):
    """Set solid color background for a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_bg_image(slide, img_path, prs):
    """Add a background image that covers the full slide."""
    if not img_path:
        return
    slide_w = prs.slide_width
    slide_h = prs.slide_height
    pic = slide.shapes.add_picture(img_path, 0, 0, slide_w, slide_h)
    # Send to back
    sp = pic._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)


def add_overlay(slide, prs):
    """Add a dark semi-transparent overlay rectangle via XML manipulation."""
    from lxml import etree
    slide_w = prs.slide_width
    slide_h = prs.slide_height
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, slide_w, slide_h)
    shape.line.fill.background()
    # Manipulate XML directly for alpha transparency
    sp = shape._element
    nsmap = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    spPr = sp.find(".//a:spPr", nsmap)
    if spPr is not None:
        # Remove existing fill
        for old_fill in spPr.findall("a:solidFill", nsmap):
            spPr.remove(old_fill)
        for old_fill in spPr.findall("a:noFill", nsmap):
            spPr.remove(old_fill)
        # Add solid fill with alpha
        solidFill = etree.SubElement(spPr, f"{{{nsmap['a']}}}solidFill")
        srgbClr = etree.SubElement(solidFill, f"{{{nsmap['a']}}}srgbClr", val="000000")
        etree.SubElement(srgbClr, f"{{{nsmap['a']}}}alpha", val="40000")


def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    """Add a text box with specified properties."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_slide_content(slide, bullets, start_top, left, width, font_size=16, color=WHITE):
    """Add bullet points to a slide."""
    txBox = slide.shapes.add_textbox(left, start_top, width, Inches(4))
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"● {bullet}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(8)
    return txBox


# ============================================================
# SLIDE BUILDERS
# ============================================================

def slide_title(prs, img):
    """Слайд 1: Заглавие"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    add_bg_image(slide, img, prs)
    add_overlay(slide, prs)

    # Title
    add_textbox(slide, Inches(0.8), Inches(1.8), Inches(8.4), Inches(1.5),
                "ПРИРОДНИ БЕДСТВИЯ", font_size=48, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Subtitle
    add_textbox(slide, Inches(0.8), Inches(3.3), Inches(8.4), Inches(1),
                "Сила на природата, която променя света", font_size=22,
                color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    # Bottom line
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    Inches(3.5), Inches(4.5), Inches(3), Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()


def slide_contents(prs):
    """Слайд 2: Съдържание"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8),
                "СЪДЪРЖАНИЕ", font_size=36, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    items = [
        "1.  Какво представляват природните бедствия?",
        "2.  Земетресения",
        "3.  Преди и след: Антакия, Турция (2023)",
        "4.  Цунами",
        "5.  Наводнения",
        "6.  Вулканични изригвания",
        "7.  Урагани",
        "8.  Как да се предпазим?",
        "9.  Заключение",
    ]

    txBox = slide.shapes.add_textbox(Inches(2), Inches(1.2), Inches(6), Inches(4.2))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"
        p.space_after = Pt(6)


def slide_what_are(prs):
    """Слайд 3: Какво са природните бедствия?"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.8),
                "КАКВО ПРЕДСТАВЛЯВАТ ПРИРОДНИТЕ БЕДСТВИЯ?",
                font_size=30, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

    definition = (
        "Природните бедствия са екстремни природни явления, които причиняват "
        "значителни разрушения, човешки жертви и икономически загуби. Те се "
        "предизвикват от геоложки, метеорологични или хидроложки процеси."
    )
    add_textbox(slide, Inches(0.8), Inches(1.5), Inches(8.4), Inches(1.2),
                definition, font_size=17, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    # Stats
    stats = [
        ("🌍", "Средно 400+ природни бедствия годишно по света"),
        ("👥", "Около 60 000 жертви годишно средно за последните 20 години"),
        ("💰", "Над $200 милиарда щети годишно"),
        ("📈", "Честотата на бедствията се увеличава заради климатичните промени"),
    ]

    for i, (icon, text) in enumerate(stats):
        y = Inches(2.9) + Inches(0.65) * i
        # Box background
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                      Inches(1.2), y, Inches(7.6), Inches(0.55))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0x25, 0x25, 0x40)
        box.line.fill.background()

        add_textbox(slide, Inches(1.5), y + Pt(6), Inches(7), Inches(0.5),
                    f"{icon}  {text}", font_size=15, color=WHITE)


def slide_earthquake(prs, img):
    """Слайд 4: Земетресения"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(8.4), Inches(0.7),
                "ЗЕМЕТРЕСЕНИЯ", font_size=34, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Image on the right
    if img:
        pic = slide.shapes.add_picture(img, Inches(5.2), Inches(1.3), Inches(4.5), Inches(3))

    # Text on the left
    bullets = [
        "Причиняват се от движение на тектонски плочи",
        "Измерват се по скалата на Рихтер (1-10)",
        "Земетресението в Турция и Сирия (2023):\n    магнитуд 7.8, над 59 000 жертви",
        "Най-силното регистрирано: Чили 1960 — 9.5 по Рихтер",
        "Могат да предизвикат цунами, свлачища и пожари",
        "България е в сеизмично активна зона — Балканите",
    ]
    add_bullet_slide_content(slide, bullets, Inches(1.3), Inches(0.5), Inches(4.5),
                             font_size=14, color=WHITE)


def slide_before_after(prs, img_before, img_after):
    """Слайд 5: Преди и след — Антакия"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.3), Inches(0.2), Inches(9.4), Inches(0.7),
                "ПРЕДИ И СЛЕД: АНТАКИЯ, ТУРЦИЯ — ЗЕМЕТРЕСЕНИЕ 2023",
                font_size=26, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

    # Before image
    if img_before:
        slide.shapes.add_picture(img_before, Inches(0.3), Inches(1.3), Inches(4.6), Inches(3.2))
    add_textbox(slide, Inches(0.3), Inches(4.55), Inches(4.6), Inches(0.4),
                "ПРЕДИ — Антакия, 2013 г.", font_size=16, color=YELLOW,
                bold=True, alignment=PP_ALIGN.CENTER)

    # After image
    if img_after:
        slide.shapes.add_picture(img_after, Inches(5.1), Inches(1.3), Inches(4.6), Inches(3.2))
    add_textbox(slide, Inches(5.1), Inches(4.55), Inches(4.6), Inches(0.4),
                "СЛЕД — Антакия, февруари 2023 г.", font_size=16, color=ACCENT,
                bold=True, alignment=PP_ALIGN.CENTER)

    # Bottom note
    add_textbox(slide, Inches(0.5), Inches(5.1), Inches(9), Inches(0.5),
                "Земетресението от 6 февруари 2023 г. с магнитуд 7.8 унищожи над 300 000 сгради в Турция и Сирия.",
                font_size=13, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)


def slide_tsunami(prs, img):
    """Слайд 6: Цунами"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(8.4), Inches(0.7),
                "ЦУНАМИ", font_size=34, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Image on the left
    if img:
        slide.shapes.add_picture(img, Inches(0.3), Inches(1.3), Inches(4.5), Inches(3.2))

    # Text on the right
    bullets = [
        "Гигантски вълни, предизвикани от подводни земетресения",
        "Могат да достигнат височина над 30 метра",
        "Цунами в Индийския океан (2004):\n    загинали над 230 000 души в 14 държави",
        "Цунами в Япония (2011):\n    предизвика ядрена авария във Фукушима",
        "Скоростта на вълните може да надмине 800 км/ч",
        "Системите за ранно предупреждение спасяват хиляди животи",
    ]
    add_bullet_slide_content(slide, bullets, Inches(1.3), Inches(5), Inches(4.8),
                             font_size=14, color=WHITE)


def slide_floods(prs, img):
    """Слайд 7: Наводнения"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(8.4), Inches(0.7),
                "НАВОДНЕНИЯ", font_size=34, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    if img:
        slide.shapes.add_picture(img, Inches(5.2), Inches(1.3), Inches(4.5), Inches(3))

    bullets = [
        "Най-честото природно бедствие в света",
        "Причини: проливни дъждове, топене на лед, скъсване на язовири",
        "Наводненията в Пакистан (2022):\n    1/3 от страната под вода, 1700+ жертви",
        "В България: тежки наводнения през 2014 г. в Мизия и Враца",
        "Годишно засягат над 250 милиона души по света",
        "Климатичните промени увеличават риска значително",
    ]
    add_bullet_slide_content(slide, bullets, Inches(1.3), Inches(0.5), Inches(4.5),
                             font_size=14, color=WHITE)


def slide_volcano(prs, img):
    """Слайд 8: Вулканични изригвания"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg_image(slide, img, prs)
    add_overlay(slide, prs)

    add_textbox(slide, Inches(0.5), Inches(0.3), Inches(9), Inches(0.7),
                "ВУЛКАНИЧНИ ИЗРИГВАНИЯ", font_size=34, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    bullets = [
        "Около 1 500 активни вулкана по света, ~50 изригват годишно",
        "Изхвърлят лава, пепел, токсични газове и пирокластични потоци",
        "Връх Сейнт Хелънс, САЩ (1980): изригването унищожи 600 км² гора",
        "Везувий (79 г.): погреба градовете Помпей и Херкулан",
        "Вулканичната пепел може да спре самолетния трафик за седмици",
        "Супервулканите могат да причинят глобална вулканична зима",
    ]
    add_bullet_slide_content(slide, bullets, Inches(1.5), Inches(0.5), Inches(9),
                             font_size=16, color=WHITE)

    # Image credit
    add_textbox(slide, Inches(0.5), Inches(5.2), Inches(9), Inches(0.3),
                "Снимка: Изригване на вулкана Сейнт Хелънс, 18 май 1980 г. (USGS)",
                font_size=10, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)


def slide_hurricane(prs, img):
    """Слайд 9: Урагани"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(8.4), Inches(0.7),
                "УРАГАНИ И ЦИКЛОНИ", font_size=34, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    if img:
        slide.shapes.add_picture(img, Inches(0.3), Inches(1.3), Inches(4.2), Inches(3.5))

    bullets = [
        "Мощни въртящи се бури с ветрове над 119 км/ч",
        "Категоризират се от 1 до 5 по скалата Сафир-Симпсън",
        "Ураганът Катрина (2005): над 1800 жертви,\n    $125 милиарда щети в САЩ",
        "Тайфунът Хайян (2013): ветрове до 315 км/ч,\n    над 6 000 жертви във Филипините",
        "Сезонът на ураганите: юни–ноември (Атлантика)",
        "Затопляне на океаните = по-силни бури",
    ]
    add_bullet_slide_content(slide, bullets, Inches(1.3), Inches(4.8), Inches(5),
                             font_size=14, color=WHITE)

    add_textbox(slide, Inches(0.3), Inches(4.9), Inches(4.2), Inches(0.3),
                "Ураганът Катрина от сателит (NASA, 2005)",
                font_size=10, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)


def slide_protection(prs):
    """Слайд 10: Как да се предпазим?"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(8.4), Inches(0.7),
                "КАК ДА СЕ ПРЕДПАЗИМ?", font_size=34, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    left_items = [
        ("🏠  Подготовка у дома", [
            "Аварийна раница с вода, храна, аптечка",
            "Фенерче, радио на батерии, документи",
            "Познавайте пътищата за евакуация",
        ]),
        ("📱  Информираност", [
            "Следете предупрежденията от метеослужбите",
            "Инсталирайте приложения за бедствия",
            "Научете сигналите за тревога",
        ]),
    ]
    right_items = [
        ("🤝  По време на бедствие", [
            "Земетресение: паднете, покрийте се, дръжте се",
            "Наводнение: качете се на високо, НЕ пресичайте вода",
            "Ураган: затворете се вътре, далеч от прозорци",
        ]),
        ("🌍  За обществото", [
            "Инвестиране в ранно предупреждение",
            "Устойчиво строителство",
            "Международна координация и помощ",
        ]),
    ]

    y_start = Inches(1.3)
    for col_items, x_start in [(left_items, Inches(0.3)), (right_items, Inches(5.1))]:
        y = y_start
        for title, points in col_items:
            # Title box
            box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                          x_start, y, Inches(4.6), Inches(0.45))
            box.fill.solid()
            box.fill.fore_color.rgb = RGBColor(0x30, 0x30, 0x55)
            box.line.fill.background()
            add_textbox(slide, x_start + Inches(0.1), y + Pt(3),
                        Inches(4.4), Inches(0.4),
                        title, font_size=15, color=YELLOW, bold=True)
            y += Inches(0.55)

            for pt in points:
                add_textbox(slide, x_start + Inches(0.2), y,
                            Inches(4.3), Inches(0.35),
                            f"▸ {pt}", font_size=12, color=WHITE)
                y += Inches(0.32)
            y += Inches(0.15)


def slide_conclusion(prs):
    """Слайд 11: Заключение"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.8), Inches(8.4), Inches(0.8),
                "ЗАКЛЮЧЕНИЕ", font_size=40, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Decorative line
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    Inches(3.5), Inches(1.7), Inches(3), Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()

    conclusion_text = (
        "Природните бедствия са неизбежна част от живота на нашата планета.\n\n"
        "Не можем да ги спрем, но можем да се подготвим.\n\n"
        "Знанието, технологиите и международното сътрудничество\n"
        "са нашите най-силни оръжия срещу силата на природата.\n\n"
        "Всеки от нас може да направи разликата —\n"
        "като се информира, подготви и помогне."
    )

    add_textbox(slide, Inches(1), Inches(1.9), Inches(8), Inches(2.8),
                conclusion_text, font_size=18, color=WHITE,
                alignment=PP_ALIGN.CENTER)

    # Bottom — moved up to avoid overlap
    add_textbox(slide, Inches(0.5), Inches(4.7), Inches(9), Inches(0.5),
                "Благодаря за вниманието!", font_size=26, color=YELLOW,
                bold=True, alignment=PP_ALIGN.CENTER)


def slide_sources(prs):
    """Слайд 12: Източници"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, DARK_BG)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.7),
                "ИЗТОЧНИЦИ", font_size=30, color=ACCENT, bold=True,
                alignment=PP_ALIGN.CENTER)

    sources = [
        "Снимки: Wikimedia Commons (Public Domain / CC BY 2.0)",
        "USGS — Геоложка служба на САЩ (earthquake.usgs.gov)",
        "NASA — Национална агенция по аеронавтика и изследване на космоса",
        "NOAA — Национална служба за океана и атмосферата",
        "EM-DAT — Международна база данни за бедствия (emdat.be)",
        "Voice of America — снимки от земетресението в Турция 2023",
        "Copernicus Sentinel — сателитни снимки от наводненията в Пакистан 2022",
        "Световна метеорологична организация (WMO)",
    ]

    txBox = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(4.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, src in enumerate(sources):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {src}"
        p.font.size = Pt(14)
        p.font.color.rgb = LIGHT_GRAY
        p.font.name = "Calibri"
        p.space_after = Pt(8)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 50)
    print("  ПРЕЗЕНТАЦИЯ: ПРИРОДНИ БЕДСТВИЯ")
    print("=" * 50)

    # Download images
    imgs = download_all()

    # Create presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    print("\nСъздаване на слайдове...")

    slide_title(prs, imgs.get("title"))
    print("  [1/11] Заглавие")

    slide_contents(prs)
    print("  [2/11] Съдържание")

    slide_what_are(prs)
    print("  [3/11] Какво са природните бедствия")

    slide_earthquake(prs, imgs.get("earthquake"))
    print("  [4/11] Земетресения")

    slide_before_after(prs, imgs.get("before"), imgs.get("after"))
    print("  [5/11] Преди и след")

    slide_tsunami(prs, imgs.get("tsunami"))
    print("  [6/11] Цунами")

    slide_floods(prs, imgs.get("flood"))
    print("  [7/11] Наводнения")

    slide_volcano(prs, imgs.get("volcano"))
    print("  [8/11] Вулканични изригвания")

    slide_hurricane(prs, imgs.get("hurricane"))
    print("  [9/11] Урагани")

    slide_protection(prs)
    print("  [10/11] Как да се предпазим")

    slide_conclusion(prs)
    print("  [11/11] Заключение")

    # Bonus: sources
    slide_sources(prs)
    print("  [bonus] Източници")

    # Save
    prs.save(OUTPUT_FILE)
    print(f"\n✅ Презентацията е запазена: {OUTPUT_FILE}")
    print(f"   Общо слайдове: {len(prs.slides)}")


if __name__ == "__main__":
    main()

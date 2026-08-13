import os
from PIL import Image, ImageDraw
from fpdf import FPDF

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "assets", "hero.png")
OUT = os.path.join(BASE, "assets", "resume.pdf")
TMP = os.path.join(BASE, "assets", "_avatar.png")

GOLD = (244, 145, 63)          # site --gold
GOLD_LIGHT = (255, 178, 92)    # lighter gold
CARD = (22, 22, 22)            # sidebar card
BG = (10, 10, 10)              # site --bg
WHITE = (255, 255, 255)
GRAY = (163, 163, 163)
GRAY_DARK = (107, 107, 107)

SIDEBAR_W = 72  # mm


def make_avatar():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    im = im.resize((800, 800), Image.LANCZOS)
    mask = Image.new("L", (800, 800), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 800, 800), fill=255)
    out = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    out.save(TMP)
    return TMP


class Resume(FPDF):
    def sidebar_section(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*GOLD)
        self.cell(SIDEBAR_W - 28, 6, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.6)
        self.line(14, self.get_y() + 0.5, 14 + SIDEBAR_W - 28, self.get_y() + 0.5)
        self.ln(5)

    def main_section(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*GOLD)
        self.cell(0, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(5)


def build():
    avatar = make_avatar()
    pdf = Resume(format="A4")
    pdf.set_left_margin(SIDEBAR_W + 20)
    pdf.set_right_margin(20)
    pdf.set_top_margin(20)
    pdf.set_auto_page_break(False)
    pdf.add_page()

    # ---------- SIDEBAR ----------
    pdf.set_fill_color(*CARD)
    pdf.rect(0, 0, SIDEBAR_W, pdf.h, "F")
    pdf.set_fill_color(*GOLD)
    pdf.rect(0, 0, SIDEBAR_W, 8, "F")

    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.2)
    pdf.ellipse(SIDEBAR_W / 2 - 24, 16, 48, 48, "D")
    pdf.image(avatar, x=SIDEBAR_W / 2 - 21, y=19, w=42)
    pdf.ln(58)

    pdf.set_x(14)
    pdf.sidebar_section("Contact")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*WHITE)
    contacts = [
        ("Email", "merjohnpagente2004@gmail.com"),
        ("GitHub", "MerjohnPagente"),
        ("Facebook", "Merjohn Pagente"),
    ]
    for label, value in contacts:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*GOLD)
        pdf.set_x(14)
        pdf.cell(SIDEBAR_W - 28, 4.5, label.upper())
        pdf.ln(4.5)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*WHITE)
        pdf.set_x(14)
        pdf.multi_cell(SIDEBAR_W - 28, 4.6, value)
        pdf.set_x(14)
        pdf.ln(2)
    pdf.set_x(14)
    pdf.ln(3)

    pdf.set_x(14)
    pdf.sidebar_section("Skills")
    skills = [
        ("HTML5", 90),
        ("CSS3", 85),
        ("JavaScript", 75),
        ("Responsive Design", 88),
        ("Git & GitHub", 70),
        ("Web APIs", 72),
        ("C#", 70),
        ("Python", 75),
    ]
    for name, pct in skills:
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*WHITE)
        pdf.set_x(14)
        pdf.cell(SIDEBAR_W - 28, 4.5, name)
        pdf.ln(4.5)
        pdf.set_x(14)
        pdf.set_fill_color(50, 50, 50)
        pdf.rect(14, pdf.get_y() + 0.3, SIDEBAR_W - 28, 2.2, "F")
        pdf.set_fill_color(*GOLD)
        pdf.rect(14, pdf.get_y() + 0.3, (SIDEBAR_W - 28) * pct / 100, 2.2, "F")
        pdf.ln(2.5)
        pdf.ln(1.5)
    pdf.set_x(14)
    pdf.ln(2)

    pdf.set_x(14)
    pdf.sidebar_section("Hobbies")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*WHITE)
    pdf.set_x(14)
    pdf.multi_cell(SIDEBAR_W - 28, 4.6, "Gaming\nExploring Open Worlds")

    # ---------- MAIN ----------
    pdf.set_fill_color(*BG)
    pdf.rect(SIDEBAR_W, 0, pdf.w - SIDEBAR_W, pdf.h, "F")

    pdf.set_xy(pdf.l_margin, 22)
    pdf.set_font("Helvetica", "B", 27)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 13, "MERJOHN PAGENTE")

    pdf.set_xy(pdf.l_margin, 37)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 7, "Web Developer & Designer")

    pdf.set_xy(pdf.l_margin, 46)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "BSCS Student at Tangub City Global College  |  Front-End Focused")

    pdf.set_xy(pdf.l_margin, 64)
    pdf.main_section("Profile")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 5.6,
        "A web developer and designer with a passion for creating clean, modern, and "
        "functional websites and web applications. I specialize in front-end development, "
        "crafting responsive and interactive user interfaces using HTML, CSS, and "
        "JavaScript. When I'm not coding, gaming fuels my creativity and "
        "problem-solving skills.")
    pdf.ln(3)

    pdf.main_section("Education")
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 6, "BSCS - Bachelor of Science in Computer Science")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "Tangub City Global College")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 5.4,
        "Focused on web development, programming fundamentals, and software engineering "
        "practices.")
    pdf.ln(3)

    pdf.main_section("What I Bring")
    items = [
        ("Front-end development", "Semantic markup, animations, clean interactive interfaces."),
        ("Responsive design", "Mobile-first, adaptive layouts that scale on any screen."),
        ("Web apps & APIs", "Dynamic functionality, REST integration, async workflows."),
        ("Version control", "Git branching, collaboration, and deployment."),
    ]
    for left, right in items:
        pdf.set_x(pdf.l_margin + 4)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*WHITE)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 8, 5.5, left)
        pdf.ln(5.5)
        pdf.set_x(pdf.l_margin + 4)
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*GRAY)
        pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 8, 5, right)
        pdf.ln(3.5)
    pdf.ln(3)

    pdf.main_section("Languages & More")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 5.5, "Cebuano  |  Filipino  |  English")
    pdf.ln(8)

    pdf.set_fill_color(*GOLD)
    pdf.rect(0, pdf.h - 8, pdf.w, 8, "F")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*BG)
    pdf.set_xy(0, pdf.h - 6.5)
    pdf.cell(pdf.w / 2, 4, "  Merjohn Pagente - Web Developer", align="L")
    pdf.cell(pdf.w / 2, 4, "merjohnpagente2004@gmail.com", align="R")

    pdf.output(OUT)
    os.remove(TMP)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()

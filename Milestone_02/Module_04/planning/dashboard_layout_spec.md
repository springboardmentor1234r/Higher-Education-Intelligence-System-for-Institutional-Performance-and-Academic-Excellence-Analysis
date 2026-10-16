import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors

# ============================================================
# EDUVISION_DV — MODULE 4 VISUAL PROTOTYPE
# Updated to match the storyboard:
# 4 dashboards × 4 worksheet views
# ============================================================

DATA_FILE = "/mnt/data/university_final_dataset.xlsx"
OUTPUT_DIR = Path("/mnt/data")
PDF_FILE = OUTPUT_DIR / "eduvision_storyboard_aligned_prototype.pdf"

# -----------------------------
# 1. Load final dataset
# -----------------------------
df = pd.read_excel(DATA_FILE)

# Convert text/numeric fields safely
def to_num(series):
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="coerce"
    )

df["Students Numeric"] = to_num(df["No of student"])
df["International Students Numeric"] = to_num(df["International Student"])
df["Students per Staff Numeric"] = to_num(df["No of student per staff"])
df["University Rank Numeric"] = to_num(df["University Rank"])

# Existing score fields
df["Global Ranking Score"] = to_num(df["Global Ranking Score"])
df["Overall Score"] = to_num(df["OverAll Score"])
df["Research Score"] = to_num(df["Research Score"])
df["Citations Score"] = to_num(df["Citations Score"])
df["Teaching Score"] = to_num(df["Teaching Score"])
df["International Outlook Score"] = to_num(df["International Outlook Score"])
df["Industry Income Score"] = to_num(df["Industry Income Score"])

# IMPORTANT:
# Do not use these constant fields for meaningful comparison:
# Research Impact Score = 50
# Faculty-to-Student Ratio = 15
# International Student Percentage = 10
# Academic Reputation Score = 50
# Research Productivity Index = 42

# -----------------------------
# 2. Chart creation helpers
# -----------------------------
def save_bar(series, title, xlabel, filename, topn=10):
    s = series.dropna().sort_values(ascending=False).head(topn)
    if s.empty:
        return None

    fig, ax = plt.subplots(figsize=(6.0, 2.7))
    s = s.sort_values()
    ax.barh([str(i)[:30] for i in s.index], s.values)
    ax.set_title(title, loc="left", fontsize=11)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", alpha=0.20)
    fig.tight_layout()

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return path


def save_scatter(x, y, title, xlabel, ylabel, filename):
    tmp = pd.DataFrame({"x": x, "y": y}).dropna()

    if len(tmp) > 600:
        tmp = tmp.sample(600, random_state=42)

    fig, ax = plt.subplots(figsize=(6.0, 2.7))
    ax.scatter(tmp["x"], tmp["y"], s=12, alpha=0.55)
    ax.set_title(title, loc="left", fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.20)
    fig.tight_layout()

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return path


def save_grouped_bar(group1, group2, title, label1, label2, filename):
    tmp = pd.DataFrame({
        label1: group1,
        label2: group2
    }).dropna().head(10)

    fig, ax = plt.subplots(figsize=(6.0, 2.7))
    x = range(len(tmp))
    width = 0.38

    ax.bar([i - width / 2 for i in x], tmp[label1], width, label=label1)
    ax.bar([i + width / 2 for i in x], tmp[label2], width, label=label2)

    ax.set_title(title, loc="left", fontsize=11)
    ax.set_xticks(list(x))
    ax.set_xticklabels([str(i)[:16] for i in tmp.index], rotation=35)
    ax.legend(fontsize=7)
    ax.grid(axis="y", alpha=0.20)
    fig.tight_layout()

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return path


# -----------------------------
# 3. Create storyboard views
# -----------------------------

# UNIVERSITY OVERVIEW
ov01 = save_bar(
    df.groupby("Name of University")["Global Ranking Score"].max(),
    "Top Universities by Global Ranking Score",
    "Global Ranking Score",
    "ov01_top_universities.png",
    topn=10
)

ov03 = save_scatter(
    df["University Rank Numeric"],
    df["Overall Score"],
    "Rank vs Overall Score",
    "University Rank",
    "Overall Score",
    "ov03_rank_vs_overall.png"
)

ov04 = save_bar(
    df.groupby("Name of University")["Research Score"].max(),
    "Research Performance",
    "Research Score",
    "ov04_research_performance.png",
    topn=10
)

# RESEARCH ANALYTICS
ra01 = save_bar(
    df.groupby("Name of University")["Research Score"].max(),
    "Top Research Universities",
    "Research Score",
    "ra01_top_research.png",
    topn=10
)

ra02 = save_scatter(
    df["Research Score"],
    df["Citations Score"],
    "Research vs Citations",
    "Research Score",
    "Citations Score",
    "ra02_research_vs_citations.png"
)

ra03 = save_bar(
    df.groupby("Location")["Research Score"].mean(),
    "Research Performance by Country",
    "Average Research Score",
    "ra03_research_by_country.png",
    topn=10
)

# STUDENT ANALYTICS
sa01 = save_bar(
    df.groupby("Name of University")["Students Numeric"].max(),
    "Student Population",
    "Number of Students",
    "sa01_student_population.png",
    topn=10
)

sa03 = save_scatter(
    df["University Rank Numeric"],
    df["Students Numeric"],
    "Students vs Rank",
    "University Rank",
    "Number of Students",
    "sa03_students_vs_rank.png"
)

sa04 = save_bar(
    df.groupby("Name of University")["Students per Staff Numeric"].mean(),
    "Students per Staff",
    "Students per Staff",
    "sa04_students_per_staff.png",
    topn=10
)

# COUNTRY COMPARISON
cc01 = save_bar(
    df.groupby("Location")["Overall Score"].mean(),
    "Country Performance Ranking",
    "Average Overall Score",
    "cc01_country_ranking.png",
    topn=10
)

# -----------------------------
# 4. Create PDF prototype
# -----------------------------
W, H = landscape(A4)
c = canvas.Canvas(str(PDF_FILE), pagesize=(W, H))

def header(title, active):
    c.setFillColor(colors.HexColor("#0B3A63"))
    c.rect(0, H - 55, W, 55, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(25, H - 34, "EduVision")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(125, H - 33, title)

    tabs = ["OVERVIEW", "RESEARCH", "STUDENT", "COUNTRY"]
    x = W - 330

    for tab in tabs:
        fill = (
            colors.HexColor("#2E78B7")
            if tab == active
            else colors.HexColor("#0B3A63")
        )
        c.setFillColor(fill)
        c.roundRect(x, H - 46, 70, 20, 3, fill=1, stroke=0)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(x + 35, H - 39, tab)
        x += 75


def filters(items):
    y = H - 78
    x = 25

    for item in items:
        c.setFillColor(colors.HexColor("#F4F7FA"))
        c.roundRect(x, y - 15, 130, 23, 3, fill=1, stroke=1)

        c.setFillColor(colors.HexColor("#3D4B52"))
        c.setFont("Helvetica", 7)
        c.drawString(x + 6, y - 1, item)

        c.setFont("Helvetica-Bold", 7)
        c.drawRightString(x + 122, y - 1, "All ▾")
        x += 140


def card(x, y, w, h, title, image=None, note=None):
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    c.setFillColor(colors.HexColor("#123E5A"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x + 8, y + h - 15, title)

    if image and Path(image).exists():
        c.drawImage(
            str(image),
            x + 5,
            y + 7,
            width=w - 10,
            height=h - 28,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto"
        )

    if note:
        c.setFillColor(colors.HexColor("#5E6A70"))
        c.setFont("Helvetica", 6.5)
        c.drawString(x + 8, y + 7, note)


def footer():
    c.setFillColor(colors.HexColor("#667780"))
    c.setFont("Helvetica", 7)
    c.drawString(
        25,
        18,
        "EduVision_DV • Module 4 Visual Prototype • Final Dataset"
    )
    c.drawRightString(
        W - 25,
        18,
        "Prototype reference for Tableau build"
    )


# Common 2×2 layout
margin = 25
gap = 12
cw = (W - 2 * margin - gap) / 2
ch = 190
y_top = 100 + ch + gap
y_bottom = 100

# -----------------------------
# Dashboard 1
# -----------------------------
header("University Overview", "OVERVIEW")
filters(["Location", "University", "Rank Category"])

card(
    margin, y_top, cw, ch,
    "TOP UNIVERSITIES",
    ov01,
    "Top 10 • Global Ranking Score • descending"
)

card(
    margin + cw + gap, y_top, cw, ch,
    "GLOBAL UNIVERSITY DISTRIBUTION",
    None,
    "World map • Location on Detail • record count on Size + Color"
)

card(
    margin, y_bottom, cw, ch,
    "RANK VS OVERALL SCORE",
    ov03,
    "University Rank × Overall Score • University Detail"
)

card(
    margin + cw + gap, y_bottom, cw, ch,
    "RESEARCH PERFORMANCE",
    ov04,
    "University × Research Score • Top N / selection"
)

footer()
c.showPage()

# -----------------------------
# Dashboard 2
# -----------------------------
header("Research Analytics", "RESEARCH")
filters(["Location", "University"])

card(
    margin, y_top, cw, ch,
    "TOP RESEARCH UNIVERSITIES",
    ra01,
    "Research Score • Top N"
)

card(
    margin + cw + gap, y_top, cw, ch,
    "RESEARCH VS CITATIONS",
    ra02,
    "Research Score × Citations Score • University Detail"
)

card(
    margin, y_bottom, cw, ch,
    "RESEARCH BY COUNTRY",
    ra03,
    "Location × Average Research Score"
)

card(
    margin + cw + gap, y_bottom, cw, ch,
    "RESEARCH PERFORMANCE COMPARISON",
    None,
    "Research Score + Citations Score • University / Location"
)

footer()
c.showPage()

# -----------------------------
# Dashboard 3
# -----------------------------
header("Student Analytics", "STUDENT")
filters(["Location", "University"])

card(
    margin, y_top, cw, ch,
    "STUDENT POPULATION",
    sa01,
    "Numeric student population • Top N / selection"
)

card(
    margin + cw + gap, y_top, cw, ch,
    "INTERNATIONAL STUDENTS",
    None,
    "International Student field • percentage / comparison"
)

card(
    margin, y_bottom, cw, ch,
    "STUDENTS VS RANK",
    sa03,
    "University Rank × Student Population"
)

card(
    margin + cw + gap, y_bottom, cw, ch,
    "STUDENTS PER STAFF",
    sa04,
    "Students per Staff • University / Location"
)

footer()
c.showPage()

# -----------------------------
# Dashboard 4
# -----------------------------
header("Country Comparison", "COUNTRY")
filters(["Country A", "Country B", "Location"])

card(
    margin, y_top, cw, ch,
    "COUNTRY RANKING",
    cc01,
    "Location × Average Overall Score"
)

card(
    margin + cw + gap, y_top, cw, ch,
    "OVERALL PERFORMANCE",
    None,
    "Country A vs Country B • Average Overall Score"
)

card(
    margin, y_bottom, cw, ch,
    "RESEARCH BY COUNTRY",
    None,
    "Country A vs Country B • Average Research Score"
)

card(
    margin + cw + gap, y_bottom, cw, ch,
    "INTERNATIONAL OUTLOOK",
    None,
    "Country A vs Country B • Average International Outlook"
)

footer()
c.showPage()

# -----------------------------
# Final implementation page
# -----------------------------
header("Tableau Prototype Build Map", "")

c.setFillColor(colors.HexColor("#123E5A"))
c.setFont("Helvetica-Bold", 15)
c.drawString(25, H - 85, "Storyboard → Tableau prototype")

steps = [
    ("1", "Build worksheets", "Create the 16 worksheets shown in the storyboard."),
    ("2", "Assemble dashboards", "Place the worksheets into four 2×2 tiled dashboards."),
    ("3", "Add filters", "Location, University and Rank Category / Country selectors."),
    ("4", "Add actions", "University and Location selection filter related views."),
    ("5", "Add navigation", "Overview → Research → Student → Country."),
    ("6", "Test and save", "Verify interactions, then save as eduvision_prototype.twbx."),
]

yy = H - 120
for number, title, description in steps:
    c.setFillColor(colors.HexColor("#EAF3F8"))
    c.roundRect(30, yy - 10, 790, 42, 6, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#2E78B7"))
    c.circle(50, yy + 10, 12, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(50, yy + 7, number)

    c.setFillColor(colors.HexColor("#123E5A"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(72, yy + 10, title)

    c.setFillColor(colors.HexColor("#46555D"))
    c.setFont("Helvetica", 7.5)
    c.drawString(190, yy + 10, description)

    yy -= 48

c.setFillColor(colors.HexColor("#FFF5E6"))
c.roundRect(30, 62, 790, 65, 8, fill=1, stroke=0)

c.setFillColor(colors.HexColor("#7A4E00"))
c.setFont("Helvetica-Bold", 8)
c.drawString(43, 108, "DATA-SAFE DESIGN RULE")

c.setFont("Helvetica", 7)
c.drawString(
    43, 94,
    "The prototype uses variable fields from the final dataset and does not invent 2024/2025 data."
)
c.drawString(
    43, 81,
    "Constant derived fields are not used as meaningful comparative measures."
)
c.drawString(
    43, 68,
    "Country comparisons can use the available university KPI fields; external World Bank data requires a separate join."
)

footer()
c.save()

print("Created:", PDF_FILE)

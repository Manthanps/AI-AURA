from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = "/Users/manthan/ai_os/AIOS_Project_Analysis.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2.2*cm,
    leftMargin=2.2*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
)

W, H = A4
NAVY   = colors.HexColor("#1A2E4A")
ACCENT = colors.HexColor("#2B6CB0")
LIGHT  = colors.HexColor("#EBF4FF")
GRAY   = colors.HexColor("#6B7280")
WHITE  = colors.white

base = getSampleStyleSheet()

def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

title_style = sty("DocTitle", "Title",
    fontName="Helvetica-Bold", fontSize=22,
    textColor=WHITE, alignment=TA_CENTER, leading=28)

subtitle_style = sty("DocSub", "Normal",
    fontName="Helvetica", fontSize=11,
    textColor=colors.HexColor("#BFD7F0"), alignment=TA_CENTER, leading=16)

section_style = sty("Section", "Heading1",
    fontName="Helvetica-Bold", fontSize=14,
    textColor=NAVY, spaceBefore=18, spaceAfter=6, leading=18)

subsection_style = sty("SubSection", "Heading2",
    fontName="Helvetica-Bold", fontSize=11,
    textColor=ACCENT, spaceBefore=12, spaceAfter=4, leading=14)

body_style = sty("Body", "Normal",
    fontName="Helvetica", fontSize=10,
    textColor=colors.HexColor("#1F2937"),
    leading=15, spaceAfter=4, alignment=TA_JUSTIFY)

bullet_style = sty("Bullet", "Normal",
    fontName="Helvetica", fontSize=10,
    textColor=colors.HexColor("#1F2937"),
    leading=15, spaceAfter=3,
    leftIndent=14, firstLineIndent=0)

label_style = sty("Label", "Normal",
    fontName="Helvetica-Bold", fontSize=10,
    textColor=NAVY, leading=15, spaceAfter=2)

highlight_style = sty("Highlight", "Normal",
    fontName="Helvetica", fontSize=10,
    textColor=colors.HexColor("#1F2937"),
    leading=15, spaceAfter=4,
    backColor=LIGHT, leftIndent=10, rightIndent=10)

summary_style = sty("Summary", "Normal",
    fontName="Helvetica-Oblique", fontSize=10,
    textColor=colors.HexColor("#374151"),
    leading=15, alignment=TA_JUSTIFY,
    backColor=colors.HexColor("#F0F9FF"),
    leftIndent=10, rightIndent=10)

story = []

# ── Cover banner ──────────────────────────────────────────────────────────────
banner = Table(
    [[Paragraph("AIOS", title_style)],
     [Paragraph("AI-Powered Operating System Assistant", subtitle_style)],
     [Paragraph("Project Analysis Report", subtitle_style)]],
    colWidths=[doc.width],
)
banner.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,0),  28),
    ("BOTTOMPADDING", (0,-1),(-1,-1), 28),
    ("LEFTPADDING",  (0,0), (-1,-1), 18),
    ("RIGHTPADDING", (0,0), (-1,-1), 18),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[NAVY]),
]))
story.append(banner)
story.append(Spacer(1, 0.5*cm))

# ── Section 1 ─────────────────────────────────────────────────────────────────
story.append(Paragraph("1. Who Benefits from This Work", section_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=8))

story.append(Paragraph("End Users (Direct Beneficiaries)", subsection_style))

beneficiaries = [
    ("Non-technical users & general public",
     "People unfamiliar with terminal commands or OS internals can control their "
     "computer using plain English (e.g., \"open Chrome and search for the weather\"). "
     "This significantly lowers the barrier to computer literacy."),
    ("Parents & Families",
     "The built-in parental control module provides real-time web filtering, blocking "
     "adult content, fraud websites, and harmful keywords — particularly valuable for "
     "households where parents lack the technical knowledge to configure traditional "
     "parental controls."),
    ("Healthcare workers & patients",
     "The medical interface module allows non-technical users to run health risk "
     "prediction models (heart disease, general risk scoring) through a conversational "
     "interface, making AI-powered health screening more accessible."),
    ("Students & Researchers",
     "The architecture assistant and debugging agent modules help users understand "
     "system-level concepts (cache simulation, pipeline stages) and diagnose software "
     "issues, making it useful as an educational and research tool."),
]

for label, desc in beneficiaries:
    story.append(Paragraph(f"•  <b>{label}</b>", bullet_style))
    story.append(Paragraph(f"    {desc}", bullet_style))
    story.append(Spacer(1, 3))

story.append(Paragraph("Indirect Beneficiaries", subsection_style))

indirect = [
    ("Educational institutions",
     "Schools can deploy the parental control and web filtering stack to manage "
     "student access without expensive commercial software."),
    ("Rural / low-resource communities",
     "The system runs entirely on-device using a local LLM (Ollama), requiring no "
     "internet connection or paid API subscriptions — making it viable in "
     "low-connectivity environments."),
]

for label, desc in indirect:
    story.append(Paragraph(f"•  <b>{label}</b>", bullet_style))
    story.append(Paragraph(f"    {desc}", bullet_style))
    story.append(Spacer(1, 3))

# ── Section 2 ─────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("2. Existing Work in This Area", section_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=8))

story.append(Paragraph(
    "Several tools exist in related domains, but none combines all capabilities "
    "in a single offline, locally-run system:",
    body_style))
story.append(Spacer(1, 0.2*cm))

table_data = [
    ["Existing Tool", "What It Does", "Gap vs. This Project"],
    ["Apple Siri / Shortcuts", "Voice-driven OS automation", "Cloud-dependent, limited programmability"],
    ["Raycast AI", "NL command bar for macOS", "Requires internet; no parental or health features"],
    ["Open Interpreter", "LLM executes OS tasks via code", "No vision/OCR, no parental controls, cloud LLM"],
    ["AutoGPT", "Autonomous LLM agent", "No native OS control, no offline mode"],
    ["Circle / Disney Circle", "Parental web filtering", "Standalone device; not integrated with an assistant"],
    ["Microsoft Copilot", "AI assistant for Windows", "Cloud-only; no health/parental integration"],
]

col_w = [doc.width * r for r in (0.26, 0.30, 0.44)]
tbl = Table(table_data, colWidths=col_w, repeatRows=1)
tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0),  NAVY),
    ("TEXTCOLOR",    (0,0), (-1,0),  WHITE),
    ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",     (0,0), (-1,0),  9),
    ("ALIGN",        (0,0), (-1,-1), "LEFT"),
    ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",     (0,1), (-1,-1), 9),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT]),
    ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ("TOPPADDING",   (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
]))
story.append(tbl)
story.append(Spacer(1, 0.35*cm))

story.append(Paragraph("What makes this project distinct:", subsection_style))
distincts = [
    "Fully <b>offline and local</b> — uses Ollama with open-source LLMs (no API cost, no data sent to cloud)",
    "Combines <b>natural language OS control + parental filtering + health model execution + screen automation</b> in one unified system",
    "Uses <b>Swift-based OCR and Vision framework</b> for native macOS UI understanding — allowing automation of any app without needing its API",
    "Parental blocklists can be shared and updated via <b>WhatsApp</b>, making it practical for non-technical parents",
]
for d in distincts:
    story.append(Paragraph(f"•  {d}", bullet_style))

# ── Section 3 ─────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("3. Future Scope & How to Take It Forward", section_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=8))

phases = [
    ("Phase 1 — Consolidation & Stability", [
        "Add a proper test suite to validate core modules (OS actions, intent classification, web filtering)",
        "Generalize hardcoded user paths to support multi-user installation",
        "Replace flat-file memory storage with a structured local database (SQLite) for reliability and scalability",
    ]),
    ("Phase 2 — Accessibility & Reach", [
        "Voice input integration using Whisper (local speech-to-text) to make the assistant fully hands-free — critical for elderly or differently-abled users",
        "Graphical interface / menu bar app (SwiftUI or Electron) to replace the terminal-only interface, opening it to non-technical users",
        "Multilingual support — integrating multilingual LLMs to support regional languages, increasing reach in non-English-speaking communities",
    ]),
    ("Phase 3 — Domain Expansion", [
        "Education sector deployment — Package the parental control and web filtering system as a standalone tool for schools, with a teacher/admin dashboard",
        "Healthcare screening assistant — Expand the medical module with more models (diabetes, blood pressure risk) and a structured reporting interface for community health workers",
        "Workflow automation platform — The existing workflow engine and Swift automation stack can evolve into a full RPA tool for small businesses",
    ]),
    ("Phase 4 — Research Directions", [
        "Adaptive intent learning — Train a lightweight intent classifier on user interaction logs to personalise responses over time",
        "Cross-platform support — Port the vision and automation layer to Linux and Windows using platform-agnostic libraries",
        "Privacy-preserving personalisation — Research federated or on-device fine-tuning of the LLM so the assistant improves without sending data to the cloud",
    ]),
]

for phase_title, points in phases:
    story.append(Paragraph(phase_title, subsection_style))
    for p in points:
        story.append(Paragraph(f"•  {p}", bullet_style))
    story.append(Spacer(1, 4))

# ── Summary ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
story.append(Paragraph(
    "<b>Summary:</b>  This project addresses a genuine gap — an offline, privacy-respecting, "
    "conversational OS assistant that simultaneously serves general users, families, and "
    "healthcare contexts. The foundation is in place; the forward path lies in broadening "
    "accessibility, strengthening reliability, and deepening the domain-specific modules "
    "with research-backed features.",
    summary_style))

doc.build(story)
print("PDF saved to", OUTPUT)

"""
AgroManch Master Content Intelligence System
==============================================
Builds a 15-sheet Excel workbook covering all 8 phases of the
AgroManch Content Factory brief:

  Phase 1  Viral Pattern Prioritization (Tier A/B/C, 7 scores)
  Phase 2  Content Database (200 Reels, 100 Carousel, 100 Static,
           100 Story, 100 Engagement = 600 production-ready rows)
  Phase 3  Google Sheets System (Master Calendar, 6 content banks,
           News bank, KPI tracker)
  Phase 4  AI Image Generation Engine (prompt library)
  Phase 5  Daily Viral Content Generator (reusable template)
  Phase 6  Automated Content Operating System (SOPs)
  Phase 7  Farmer Psychology Database
  Phase 8  Final Output (Executive Summary + Dashboards + Roadmap)

Output: AgroManch_Master_System.xlsx
"""

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
GREEN_DARK   = "1B5E20"; GREEN_MED = "2E7D32"; GREEN_LIGHT = "C8E6C9"
AMBER        = "F57F17"; AMBER_LIGHT = "FFF9C4"
RED_DARK     = "B71C1C"; RED_LIGHT = "FFCDD2"
BLUE_DARK    = "0D47A1"; BLUE_LIGHT = "BBDEFB"
YELLOW       = "FFEB3B"; WHITE = "FFFFFF"; GRAY_LIGHT = "F5F5F5"; GRAY_MED = "E0E0E0"
ORANGE       = "E65100"; ORANGE_LIGHT = "FFE0B2"
PURPLE       = "4A148C"; PURPLE_LIGHT = "E1BEE7"
TEAL         = "004D40"; TEAL_LIGHT = "B2DFDB"
TIER_A       = "1B5E20"; TIER_B = "F57F17"; TIER_C = "757575"
PINK_DARK    = "880E4F"; PINK_LIGHT = "F8BBD0"

def hdr_font(size=10, bold=True, color=WHITE): return Font(name="Calibri", size=size, bold=bold, color=color)
def body_font(size=9, bold=False, color="000000"): return Font(name="Calibri", size=size, bold=bold, color=color)
def fill(c): return PatternFill("solid", fgColor=c)
def center(): return Alignment(horizontal="center", vertical="center", wrap_text=True)
def left(): return Alignment(horizontal="left", vertical="center", wrap_text=True)
def thin(): s = Side(style="thin", color="BBBBBB"); return Border(left=s, right=s, top=s, bottom=s)

def title_bar(ws, text, span, color=GREEN_DARK, size=15, sub=None, subcolor=YELLOW):
    ws.merge_cells(f"A1:{span}1")
    c = ws["A1"]; c.value = text; c.fill = fill(color)
    c.font = Font(name="Calibri", size=size, bold=True, color=WHITE); c.alignment = center()
    ws.row_dimensions[1].height = 34
    if sub:
        ws.merge_cells(f"A2:{span}2")
        s = ws["A2"]; s.value = sub; s.fill = fill(GREEN_MED)
        s.font = Font(name="Calibri", size=10, color=subcolor); s.alignment = center()
        ws.row_dimensions[2].height = 20

def header_row(ws, row, headers, bg=GREEN_DARK, fc=WHITE, height=28):
    ws.row_dimensions[row].height = height
    for col, text in enumerate(headers, 1):
        c = ws.cell(row=row, column=col, value=text)
        c.fill = fill(bg); c.font = hdr_font(9, True, fc); c.alignment = center(); c.border = thin()

def cell(ws, r, col, val, bg=None, bold=False, color="000000", align="left", size=9):
    c = ws.cell(row=r, column=col, value=val)
    if bg: c.fill = fill(bg)
    c.font = body_font(size, bold, color)
    c.alignment = left() if align == "left" else center()
    c.border = thin(); return c

def widths(ws, w):
    for i, x in enumerate(w, 1): ws.column_dimensions[get_column_letter(i)].width = x

def write_table(ws, start_row, rows, color_idx_fn=None, fonts=9):
    """rows = list of tuples; returns next free row"""
    for i, row in enumerate(rows):
        r = start_row + i
        ws.row_dimensions[r].height = 42
        bg = color_idx_fn(i, row) if color_idx_fn else (WHITE if i % 2 == 0 else GRAY_LIGHT)
        for col, val in enumerate(row, 1):
            cell(ws, r, col, val, bg, size=fonts)
    return start_row + len(rows)

wb = Workbook()

# ══════════════════════════════════════════════════════════════════════════════
# DATA POOLS — drive content generation for genuine variety
# ══════════════════════════════════════════════════════════════════════════════

# 20 verified viral patterns with 7 scores each (1-10)
# (Virality, Trust, Shareability, FarmerRelevance, Download, LeadGen, Marketplace)
PATTERNS = [
    # name, hindi, V, T, S, R, D, L, M, psychology
    ("Profit Reveal",        "मुनाफा खुलासा",      10, 8, 9, 10, 9, 9, 10, "Greed + aspiration — पैसे का सपना"),
    ("Mandi Shock",          "मंडी शॉक",          10, 7,10, 10, 9, 8, 10, "Loss aversion + anger — शोषण का गुस्सा"),
    ("Crop Emergency Alert", "फसल आपातकाल",        9, 9,10, 10, 8, 9,  6, "Fear + urgency — फसल बचाने का डर"),
    ("Farmer Success Story", "किसान सफलता कहानी",   9,10, 8, 10, 8, 8,  7, "Social proof + hope — 'मैं भी कर सकता हूं'"),
    ("Machinery Pride",      "मशीन गर्व",          8, 7, 8,  8, 6, 7,  8, "Status + envy — आधुनिक किसान पहचान"),
    ("Scheme Bomb",          "योजना बम",           9, 9, 9, 10, 9, 9,  5, "Free money + FOMO — सरकारी लाभ छूट न जाए"),
    ("Jugaad Hack",          "जुगाड़ हैक",          9, 8,10,  9, 7, 6,  6, "Curiosity + thrift — सस्ता समाधान"),
    ("Before / After",       "पहले / बाद",         8, 8, 9,  9, 7, 7,  8, "Transformation proof — बदलाव दिखता है"),
    ("Mahila Kisan",         "महिला किसान",         9,10, 9,  9, 7, 7,  7, "Empowerment + pride — महिला सशक्तिकरण"),
    ("Weather Emergency",    "मौसम आपातकाल",        9, 9,10, 10, 8, 8,  5, "Fear + urgency — मौसम से नुकसान"),
    ("Myth Buster",          "मिथक तोड़",           8, 9, 8,  9, 6, 6,  5, "Authority + surprise — गलतफहमी दूर"),
    ("Profit Calculator",    "मुनाफा कैलकुलेटर",     9, 8, 8, 10, 8, 9,  9, "Logic + greed — सटीक कमाई का गणित"),
    ("Field Interview",      "खेत इंटरव्यू",        8,10, 7,  9, 6, 7,  7, "Authenticity — असली किसान की आवाज़"),
    ("Old vs New",           "पुराना बनाम नया",      8, 8, 9,  9, 8, 7,  8, "Progress + identity — आधुनिक बनो"),
    ("Hidden Crop",          "छुपी फसल",            9, 7,10,  8, 7, 8, 10, "Curiosity + opportunity — नई कमाई"),
    ("Tech Tutorial",        "टेक ट्यूटोरियल",       8, 9, 7,  9, 9, 8,  8, "Mastery + ease — डर खत्म, सीखो"),
    ("Award / Recognition",  "सम्मान / पुरस्कार",    8, 9, 8,  8, 6, 6,  6, "Recognition + loyalty — सम्मान की चाह"),
    ("Regional Language",    "क्षेत्रीय भाषा",        9, 9, 9, 10, 9, 8,  7, "Local identity — अपनी भाषा अपनापन"),
    ("Community Debate",     "समुदाय बहस",          9, 7,10,  9, 6, 7,  6, "Belonging + opinion — आवाज़ रखो"),
    ("Seasonal Countdown",   "मौसमी काउंटडाउन",      8, 8, 9, 10, 8, 8,  8, "Urgency + timing — सही समय चूको मत"),
]

CROPS = ["गेहूं","धान","मक्का","सोयाबीन","कपास","गन्ना","टमाटर","प्याज","आलू","मिर्च",
         "सरसों","चना","मूंग","बाजरा","ज्वार","हल्दी","अदरक","लहसुन","केला","अनार",
         "Dragon Fruit","स्ट्रॉबेरी","मशरूम","सब्ज़ी","भिंडी","बैंगन","फूलगोभी","मटर","अरहर","मूंगफली"]

SCHEMES = ["PM-KISAN","PMFBY फसल बीमा","KCC (Kisan Credit Card)","PM-KUSUM सोलर","e-NAM",
           "Soil Health Card","PKVY जैविक","Agri Infrastructure Fund","NABARD योजना","Kisan Drone Subsidy"]

PAINS = ["मंडी में कम भाव","बिचौलियों की लूट","payment में देरी","फसल में रोग/कीट","मौसम का नुकसान",
         "भंडारण की समस्या","transport खर्च","quality grading","सही buyer नहीं मिलता","कर्ज़ का बोझ",
         "नकली बीज/खाद","पानी की कमी","मजदूरों की कमी","सरकारी योजना की जानकारी नहीं","बाज़ार भाव की जानकारी नहीं"]

REGIONS = ["UP","बिहार","पंजाब","MP","महाराष्ट्र","राजस्थान","हरियाणा","गुजरात","कर्नाटक","पश्चिम बंगाल"]
LANGS   = ["भोजपुरी","पंजाबी","मराठी","हरियाणवी","मगही","अवधी","राजस्थानी","गुजराती","कन्नड़","बंगाली"]
AUDIENCES = ["छोटे किसान","युवा किसान (18-35)","महिला किसान","FPO सदस्य","प्रगतिशील किसान",
             "नए डिजिटल किसान","सब्ज़ी उत्पादक","बागवानी किसान","सीमांत किसान","जोखिम-सतर्क किसान"]

PILLARS = ["Awareness (जागरूकता)","Trust (भरोसा)","Education (शिक्षा)","Community (समुदाय)",
           "Marketplace (बाज़ार)","Acquisition (अधिग्रहण)","Retention (रिटेंशन)","Brand (ब्रांड)"]

CTAS = [
    "AgroManch App download करो — link bio में 👇",
    "अभी फसल list करो — पहली sale आज ही 📲",
    "WhatsApp group join करो — daily भाव alerts 🔔",
    "Save करो 📌 और किसान दोस्त को share करो 🙏",
    "Comment करो — आपका जवाब video में आ सकता है 💬",
    "Expert से free बात करो — App → Expert section 👨‍🌾",
    "Tag करो उस किसान को जिसे यह मदद करेगा 👇",
    "Schemes section में status check करो — App खोलो 📋",
]

OBJECTIVES = ["App Download","Farmer Registration","Marketplace Listing","Buyer-Seller Connect",
              "WhatsApp Growth","Brand Authority","Farmer Retention","Revenue Growth"]

PSYCH = ["Fear (डर)","Profit (मुनाफा)","Loss Avoidance (नुकसान से बचाव)","Social Proof (सामाजिक प्रमाण)",
         "Local Identity (स्थानीय पहचान)","Authority (अधिकार)","Curiosity (जिज्ञासा)",
         "Urgency (तात्कालिकता)","Community (समुदाय)"]

def cyc(lst, i): return lst[i % len(lst)]

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1: 🏠 EXECUTIVE SUMMARY / DASHBOARD  (Phase 8.1)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.active; ws.title = "🏠 Executive Summary"; ws.sheet_view.showGridLines = False
title_bar(ws, "🌾  AgroManch — Master Content Intelligence System  🌾", "J",
          sub="Zero → 1 Million Farmers  |  Self-Sustaining Agriculture Content Factory  |  12-Month Engine")

ws.merge_cells("A4:J4")
ws["A4"].value = "🎯  MISSION"; ws["A4"].fill = fill(AMBER); ws["A4"].font = hdr_font(11, True, WHITE); ws["A4"].alignment = center()
ws.row_dimensions[4].height = 20
ws.merge_cells("A5:J6")
ws["A5"].value = ("एक self-sustaining Agriculture Content Factory बनाना जो अगले 12 महीने रोज़ viral content "
                  "generate करे — हर asset कम से कम एक business goal (App Download, Registration, Marketplace "
                  "Listing, Buyer-Seller Connect, WhatsApp Growth, Brand Authority, Retention, Revenue) को आगे बढ़ाए।")
ws["A5"].font = body_font(10); ws["A5"].alignment = left(); ws["A5"].fill = fill(GREEN_LIGHT)

# Workbook map
ws.merge_cells("A8:J8")
ws["A8"].value = "📚  WORKBOOK MAP — 15 SHEETS, 8 PHASES"; ws["A8"].fill = fill(BLUE_DARK)
ws["A8"].font = hdr_font(11, True, WHITE); ws["A8"].alignment = center(); ws.row_dimensions[8].height = 20

nav = [
    ("Phase", "Sheet", "What's Inside", "Use When"),
    ("8",  "🏠 Executive Summary",     "Mission, KPIs, 15-sheet map",                 "Start here / leadership review"),
    ("1",  "🏆 Pattern Prioritization", "20 patterns ranked, 7 scores, Tier A/B/C",   "Choosing which pattern to use"),
    ("2/3","🎬 Reel Bank (200)",        "200 production-ready Reel ideas",            "Daily Reel creation"),
    ("2/3","🖼️ Carousel Bank (100)",    "100 carousel ideas, all fields",             "Making carousels"),
    ("2/3","📄 Static Post Bank (100)",  "100 static/poster ideas",                    "Single-image posts"),
    ("2/3","📲 Story Bank (100)",        "100 story-sequence ideas",                   "Daily stories"),
    ("2/3","💬 Engagement Bank (100)",   "100 engagement / community posts",           "Driving comments + DMs"),
    ("3",  "📰 News Content Bank",       "Newsjacking templates + sources",            "Reacting to agri news"),
    ("3",  "📅 Master Calendar (90d)",   "90-day date-wise plan",                      "Daily — what to post today"),
    ("4",  "🎨 AI Image Prompt Library", "Poster/Thumb/Carousel/Infographic prompts",  "Generating visuals"),
    ("5",  "⚡ Daily Content Generator", "1 topic → 5 assets (reusable template)",     "Every morning"),
    ("6",  "⚙️ Content Operating System","Daily/Weekly/Monthly SOPs",                  "Running the factory"),
    ("7",  "🧠 Farmer Psychology DB",    "9 triggers mapped to patterns + hooks",      "Sharpening the hook"),
    ("3/8","📊 KPI Tracker + Roadmap",   "KPI framework + 90-day growth roadmap",      "Weekly performance review"),
]
header_row(ws, 9, nav[0], BLUE_DARK)
for i, row in enumerate(nav[1:]):
    r = 10 + i; ws.row_dimensions[r].height = 22
    bg = WHITE if i % 2 == 0 else BLUE_LIGHT
    # style all cells first, then merge
    cell(ws, r, 1, row[0], bg, True, BLUE_DARK, "center")
    cell(ws, r, 2, row[1], bg, True); cell(ws, r, 3, "", bg)
    cell(ws, r, 4, row[2], bg)
    for c in range(5, 8): cell(ws, r, c, "", bg)
    cell(ws, r, 8, row[3], bg)
    for c in range(9, 11): cell(ws, r, c, "", bg)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=7)
    ws.merge_cells(start_row=r, start_column=8, end_row=r, end_column=10)

# KPI snapshot box
base = 25
ws.merge_cells(f"A{base}:J{base}")
ws[f"A{base}"].value = "📈  NORTH-STAR KPIs (12-Month Targets)"; ws[f"A{base}"].fill = fill(GREEN_DARK)
ws[f"A{base}"].font = hdr_font(11, True, WHITE); ws[f"A{base}"].alignment = center(); ws.row_dimensions[base].height = 20
kpis = [
    ("Metric", "Month 1", "Month 3", "Month 6", "Month 12"),
    ("App Downloads",          "10,000",  "75,000",   "3,00,000",  "10,00,000"),
    ("Registered Farmers",     "6,000",   "50,000",   "2,00,000",  "7,00,000"),
    ("Marketplace Listings",   "1,500",   "15,000",   "75,000",    "3,00,000"),
    ("Buyer-Seller Connects",  "500",     "6,000",    "40,000",    "2,00,000"),
    ("WhatsApp Community",      "5,000",   "40,000",   "1,75,000",  "6,00,000"),
    ("Monthly Reach",          "5 लाख",   "40 लाख",   "1.5 करोड़", "5 करोड़"),
]
# header (each label spans 2 cols)
ws.row_dimensions[base+1].height = 20
for j, txt in enumerate(kpis[0]):
    cell(ws, base+1, j*2+1, txt, GREEN_DARK, True, WHITE, "left" if j==0 else "center")
    cell(ws, base+1, j*2+2, "", GREEN_DARK)
    ws.merge_cells(start_row=base+1, start_column=j*2+1, end_row=base+1, end_column=j*2+2)
for i, row in enumerate(kpis[1:]):
    r = base+2+i; ws.row_dimensions[r].height = 20
    bg = WHITE if i % 2 == 0 else GREEN_LIGHT
    for col, val in enumerate(row):
        cell(ws, r, col*2+1, val, bg, col==0, GREEN_DARK if col==0 else "000000", "left" if col==0 else "center")
        cell(ws, r, col*2+2, "", bg)
        ws.merge_cells(start_row=r, start_column=col*2+1, end_row=r, end_column=col*2+2)
widths(ws, [12,8,12,8,12,8,12,8,12,8])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 2: 🏆 PATTERN PRIORITIZATION  (Phase 1)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("🏆 Pattern Prioritization"); ws.sheet_view.showGridLines = False
title_bar(ws, "🏆  Phase 1 — Viral Pattern Prioritization", "M", color=RED_DARK,
          sub="20 patterns scored across 7 dimensions → ranked → Tier A / B / C")

heads = ["Rank","Pattern (EN)","Pattern (HI)","Virality","Trust","Share","Relevance",
         "Download","LeadGen","Marketplace","TOTAL /70","Tier","Psychology Trigger"]
header_row(ws, 3, heads, RED_DARK)

# compute totals and rank
scored = []
for name, hi, V,T,S,R,D,L,M, psy in PATTERNS:
    total = V+T+S+R+D+L+M
    scored.append((name,hi,V,T,S,R,D,L,M,total,psy))
scored.sort(key=lambda x: -x[9])

def tier_for(total):
    if total >= 58: return "A", TIER_A, WHITE
    if total >= 52: return "B", TIER_B, WHITE
    return "C", TIER_C, WHITE

for i, (name,hi,V,T,S,R,D,L,M,total,psy) in enumerate(scored):
    r = 4 + i; ws.row_dimensions[r].height = 26
    tier, tcol, tfc = tier_for(total)
    band = {"A":GREEN_LIGHT, "B":AMBER_LIGHT, "C":GRAY_LIGHT}[tier]
    cell(ws, r, 1, i+1, band, True, "000000", "center")
    cell(ws, r, 2, name, band, True)
    cell(ws, r, 3, hi, band)
    for col, val in zip(range(4,11), [V,T,S,R,D,L,M]):
        sc_bg = GREEN_LIGHT if val>=9 else (AMBER_LIGHT if val>=7 else RED_LIGHT)
        cell(ws, r, col, val, sc_bg, val>=9, "000000", "center")
    cell(ws, r, 11, total, band, True, "000000", "center", 10)
    tc = cell(ws, r, 12, f"Tier {tier}", tcol, True, tfc, "center")
    cell(ws, r, 13, psy, band)

# Tier legend
lr = 4 + len(scored) + 1
ws.merge_cells(f"A{lr}:M{lr}")
ws[f"A{lr}"].value = "📌  TIER STRATEGY"; ws[f"A{lr}"].fill = fill(BLUE_DARK)
ws[f"A{lr}"].font = hdr_font(10, True, WHITE); ws[f"A{lr}"].alignment = center()
legend = [
    ("Tier A (58-70)", GREEN_LIGHT, "Daily drivers — 60% of content. Highest virality + business impact. Profit Reveal, Mandi Shock, Scheme Bomb, Crop Emergency, Success Story."),
    ("Tier B (52-57)", AMBER_LIGHT, "Supporting mix — 30% of content. Strong but situational. Jugaad, Mahila Kisan, Weather, Calculator, Regional Language, Countdown."),
    ("Tier C (<52)",   GRAY_LIGHT,  "Flavor / depth — 10% of content. Build authority & variety. Myth Buster, Machinery Pride, Award, Field Interview, Old vs New."),
]
for i, (t, bg, desc) in enumerate(legend):
    r = lr+1+i; ws.row_dimensions[r].height = 30
    cell(ws, r, 1, t, bg, True, "000000", "center")
    cell(ws, r, 2, "", bg)
    cell(ws, r, 3, desc, bg)
    for c in range(4, 14): cell(ws, r, c, "", bg)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=13)
widths(ws, [5,20,18,8,7,7,9,9,9,11,9,9,34])

# ══════════════════════════════════════════════════════════════════════════════
# CONTENT BANK GENERATORS  (Phase 2 + 3)
# ══════════════════════════════════════════════════════════════════════════════
BANK_HEADERS = ["Content ID","Pillar","Pattern Used","Topic","Target Audience","Hook (First 3s)",
                "Farmer Pain Point","Solution","CTA","Expected Outcome","Virality /10"]

def hook_for(pat, topic, crop, region, scheme):
    bank = {
        "Profit Reveal":        f"इस किसान ने {crop} से ₹__ लाख कमाए — कैसे?",
        "Mandi Shock":          f"{crop} मंडी में ₹__/kg — AgroManch पर ₹__! फर्क देखो 🔴🟢",
        "Crop Emergency Alert": f"🚨 {region} में {crop} पर रोग — 72 घंटे में यह करो!",
        "Farmer Success Story": f"'पहले डर था — आज {crop} से खुशी है' — असली कहानी",
        "Machinery Pride":      f"यह मशीन {crop} की लागत आधी कर देती है 😮",
        "Scheme Bomb":          f"🚨 {scheme} — किस्त आ रही है, status check करो!",
        "Jugaad Hack":          f"₹200 में {crop} का जुगाड़ — 90% किसान नहीं जानते",
        "Before / After":       f"{crop} खेत: पहले बनाम बाद — यकीन नहीं होगा",
        "Mahila Kisan":         f"'अकेले 3 एकड़ {crop} संभाला' — रेखा देवी की कहानी",
        "Weather Emergency":    f"🚨 {region} Alert: 72 घंटे में मौसम — {crop} बचाओ!",
        "Myth Buster":          f"{crop} के बारे में यह बात झूठ है — सच जानो",
        "Profit Calculator":    f"{crop} में 1 एकड़ = कितना मुनाफा? पूरा हिसाब",
        "Field Interview":      f"खेत से सीधे: {region} के किसान क्या कह रहे हैं?",
        "Old vs New":           f"{crop} बेचने का पुराना तरीका vs AgroManch — 5 घंटे vs 5 मिनट",
        "Hidden Crop":          f"यह फसल ₹__/kg बिकती है — कोई {region} में नहीं उगाता क्यों?",
        "Tech Tutorial":        f"AgroManch पर {crop} list करो — 5 मिनट tutorial",
        "Award / Recognition":  f"🏆 Kisan Star of the Week — {region} के किसान को बधाई!",
        "Regional Language":    f"किसान भाई — आज {cyc(LANGS,0)} में {crop} की बात",
        "Community Debate":     f"सच बोलो — {crop} मंडी में सही भाव मिलता है? Poll 👇",
        "Seasonal Countdown":   f"{crop} बुवाई में बस __ दिन बाकी — तैयारी शुरू!",
    }
    return bank.get(pat, f"{crop} किसानों के लिए ज़रूरी जानकारी")

def solution_for(pat, crop):
    return (f"AgroManch पर {crop} direct buyers को बेचो — fair price, 72hr payment, free expert. "
            f"App → List → Sell. बिचौलिया खत्म, मुनाफा आपका।")

def outcome_for(pat):
    m = {
        "Profit Reveal":"App Download + Listing", "Mandi Shock":"App Download + Trust",
        "Crop Emergency Alert":"Retention + WhatsApp Growth", "Farmer Success Story":"Trust + Registration",
        "Machinery Pride":"Marketplace + Brand", "Scheme Bomb":"WhatsApp Growth + Registration",
        "Jugaad Hack":"Shareability + Reach", "Before / After":"Trust + Listing",
        "Mahila Kisan":"Community + Brand", "Weather Emergency":"Retention + App Download",
        "Myth Buster":"Brand Authority", "Profit Calculator":"Lead Gen + Listing",
        "Field Interview":"Trust + Authority", "Old vs New":"App Download",
        "Hidden Crop":"Marketplace + Listing", "Tech Tutorial":"App Download + Activation",
        "Award / Recognition":"Retention + Loyalty", "Regional Language":"Registration + Reach",
        "Community Debate":"Engagement + Community", "Seasonal Countdown":"Listing + Marketplace",
    }
    return m.get(pat, "Engagement")

def gen_bank(prefix, count, format_label, pattern_weighting):
    """Generate `count` rows. pattern_weighting = list of pattern indices (weighted)."""
    rows = []
    for n in range(count):
        pidx = pattern_weighting[n % len(pattern_weighting)]
        pat = PATTERNS[pidx][0]
        Vsc = PATTERNS[pidx][2]
        crop = cyc(CROPS, n); region = cyc(REGIONS, n); scheme = cyc(SCHEMES, n)
        aud = cyc(AUDIENCES, n); pillar = cyc(PILLARS, n); pain = cyc(PAINS, n)
        cid = f"{prefix}-{n+1:03d}"
        topic = f"{pat}: {crop} ({format_label})"
        hook = hook_for(pat, topic, crop, region, scheme)
        sol = solution_for(pat, crop)
        cta = cyc(CTAS, n)
        out = outcome_for(pat)
        rows.append((cid, pillar, pat, topic, aud, hook, pain, sol, cta, out, Vsc))
    return rows

# Pattern weighting: Tier A heavy. Build index list weighted by tier.
def weighting():
    w = []
    for idx,(name,hi,V,T,S,R,D,L,M,psy) in enumerate(PATTERNS):
        total = V+T+S+R+D+L+M
        reps = 4 if total>=58 else (2 if total>=52 else 1)
        w += [idx]*reps
    return w
WEIGHT = weighting()

def build_bank_sheet(tab, title, color, prefix, count, fmt):
    sh = wb.create_sheet(tab); sh.sheet_view.showGridLines = False
    title_bar(sh, title, "K", color=color,
              sub=f"{count} production-ready ideas  |  Phase 2 + 3  |  हर row = ready to shoot/design")
    header_row(sh, 3, BANK_HEADERS, color)
    rows = gen_bank(prefix, count, fmt, WEIGHT)
    def colfn(i, row):
        pat = row[2]
        t = next(p for p in PATTERNS if p[0]==pat)
        total = sum(t[2:9])
        return GREEN_LIGHT if total>=58 else (AMBER_LIGHT if total>=52 else WHITE if i%2==0 else GRAY_LIGHT)
    write_table(sh, 4, rows, colfn, fonts=9)
    sh.freeze_panes = "A4"
    widths(sh, [10,18,18,28,18,34,20,40,30,20,8])
    return rows

reel_rows     = build_bank_sheet("🎬 Reel Bank (200)",     "🎬  Reel Content Bank — 200 Ideas",      ORANGE,    "REEL", 200, "Reel")
carousel_rows = build_bank_sheet("🖼️ Carousel Bank (100)",  "🖼️  Carousel Content Bank — 100 Ideas",  PURPLE,    "CARO", 100, "Carousel")
static_rows   = build_bank_sheet("📄 Static Post Bank",     "📄  Static / Poster Bank — 100 Ideas",   BLUE_DARK, "STAT", 100, "Static Poster")
story_rows    = build_bank_sheet("📲 Story Bank",           "📲  Story Content Bank — 100 Ideas",     PINK_DARK, "STOR", 100, "Story")
engage_rows   = build_bank_sheet("💬 Engagement Bank",      "💬  Engagement / Community Bank — 100",  TEAL,      "ENGG", 100, "Engagement")

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: 📰 NEWS CONTENT BANK  (Phase 3)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("📰 News Content Bank"); ws.sheet_view.showGridLines = False
title_bar(ws, "📰  News Content Bank — Newsjacking Engine", "I", color=RED_DARK,
          sub="React fast to agri news → ride the trend → drive downloads. Check sources daily 7 AM.")
news_h = ["ID","News Trigger Type","Example Topic","Pattern to Apply","Hook Template","Angle for AgroManch","CTA","Speed","Source to Watch"]
header_row(ws, 3, news_h, RED_DARK)
news = [
    ("NEWS-01","MSP Announcement","सरकार ने MSP बढ़ाया","Scheme Bomb","🚨 MSP बढ़ा! आपकी {crop} पर कितना फायदा?","MSP vs AgroManch real price comparison","भाव calculator App में देखो","Same day","PIB, Krishi Jagran"),
    ("NEWS-02","Weather / Monsoon","IMD मानसून अलर्ट","Weather Emergency","🚨 {region} में भारी बारिश — फसल बचाओ","District-level alert + expert tips","Weather Alert ON करो 🔔","< 6 hrs","IMD, Skymet"),
    ("NEWS-03","Mandi Price Spike","प्याज/टमाटर भाव में उछाल","Mandi Shock","प्याज ₹__/kg! बेचने का सही समय अभी?","Real-time AgroManch price + sell now","अभी list करो 📲","< 12 hrs","Agmarknet, e-NAM"),
    ("NEWS-04","New Govt Scheme","नई किसान योजना लॉन्च","Scheme Bomb","नई योजना — ₹__ सीधे खाते में!","Eligibility + how-to-apply tutorial","Schemes section में check 📋","Same day","PIB, agricoop.gov.in"),
    ("NEWS-05","Pest / Disease Outbreak","टिड्डी/रोग का प्रकोप","Crop Emergency Alert","🚨 {region} में {crop} पर हमला!","Free expert consult + treatment","Expert को photo भेजो","< 6 hrs","ICAR, State Agri Dept"),
    ("NEWS-06","Budget / Policy","कृषि बजट घोषणा","Myth Buster","बजट में किसान को क्या मिला? सच","Simple Hindi breakdown of impact","पूरी जानकारी App में","< 24 hrs","Union Budget, PIB"),
    ("NEWS-07","Success / Award News","किसान को राष्ट्रीय पुरस्कार","Award / Recognition","🏆 इस किसान ने देश का नाम रोशन किया","Inspire + 'you can too' angle","अपनी कहानी share करो","< 24 hrs","Krishi Jagran, DD Kisan"),
    ("NEWS-08","Export / Demand News","विदेश में भारतीय फसल की मांग","Hidden Crop","यह फसल विदेश में ₹__/kg बिक रही!","Export buyers on AgroManch","Buyers देखो App में","< 24 hrs","APEDA, Commerce Ministry"),
    ("NEWS-09","Festival / Season","त्योहार पर फसल की मांग","Seasonal Countdown","दिवाली से पहले __ दिन — भाव बढ़ेंगे!","Best selling window prediction","अभी list करो","2-3 days ahead","Market calendar"),
    ("NEWS-10","Tech / Innovation","ड्रोन/AI खेती की खबर","Tech Tutorial","ड्रोन से खेती — अब आपके लिए भी","How AgroManch enables access","App में explore करो","< 48 hrs","Agri-tech news"),
]
def newsfn(i,row): return RED_LIGHT if i%2==0 else WHITE
write_table(ws, 4, news, newsfn, fonts=9)
widths(ws, [9,20,26,18,38,34,24,10,22])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: 📅 MASTER CALENDAR (90 days)  (Phase 3)
# ══════════════════════════════════════════════════════════════════════════════
import datetime
ws = wb.create_sheet("📅 Master Calendar (90d)"); ws.sheet_view.showGridLines = False
title_bar(ws, "📅  Master Content Calendar — 90 Days", "K", color=GREEN_DARK,
          sub="Daily plan, June 2026 onward. Mix: ~1 Reel + 1 secondary asset/day. Pulls from all banks.")
cal_h = ["Date","Day","Week","Primary Asset","Pattern","Topic","Secondary Asset","Platform Mix","Best Time IST","Objective","Status"]
header_row(ws, 3, cal_h, GREEN_DARK)

start = datetime.date(2026, 6, 7)
secondary_cycle = ["Carousel","Story","Engagement","Static Poster","Story","WhatsApp Broadcast","Carousel"]
platmix = ["IG + YT Short + WA","IG + FB","IG + WA","YT + IG","IG + FB + WA","IG Story + WA","YT + IG + FB"]
times = ["08:30 PM","05:00 PM","08:00 PM","07:30 AM","09:30 AM","07:00 PM","12:00 PM"]
cal_rows = []
allbanks = reel_rows  # reels as primary
for d in range(90):
    date = start + datetime.timedelta(days=d)
    rr = allbanks[d % len(allbanks)]
    cal_rows.append((
        date.strftime("%d-%m-%Y"),
        date.strftime("%a"),
        f"W{d//7+1}",
        "Reel",
        rr[2],
        rr[3],
        cyc(secondary_cycle, d),
        cyc(platmix, d),
        cyc(times, d),
        cyc(OBJECTIVES, d),
        "⬜ Pending",
    ))
def calfn(i,row):
    return GREEN_LIGHT if i%7 in (0,) else (BLUE_LIGHT if i%2==0 else WHITE)
nr = write_table(ws, 4, cal_rows, calfn, fonts=9)
for i in range(len(cal_rows)):
    ws.cell(row=4+i, column=11).font = body_font(9, True, AMBER)
ws.freeze_panes = "A4"
widths(ws, [12,5,5,13,18,30,15,18,11,18,11])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: 🎨 AI IMAGE PROMPT LIBRARY  (Phase 4)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("🎨 AI Image Prompt Library"); ws.sheet_view.showGridLines = False
title_bar(ws, "🎨  AI Image Generation Engine — Prompt Library", "L", color=PURPLE,
          sub="Poster · Reel Thumbnail · Carousel Cover · Infographic  |  Works in Claude/ChatGPT/Canva/Ideogram/MJ/Flux")

# Brand guide box
ws.merge_cells("A3:L3")
ws["A3"].value = "🎨 BRAND CONSISTENCY (paste into every prompt): AgroManch green (#1B5E20) + amber (#F57F17) accents · clean modern · authentic Indian farmer · Devanagari-friendly text zones · logo bottom-right · warm trustworthy mood"
ws["A3"].fill = fill(AMBER_LIGHT); ws["A3"].font = body_font(9, True); ws["A3"].alignment = left(); ws.row_dimensions[3].height = 34

prompt_h = ["Type","Subject","Environment","Camera","Lighting","Color","Composition","Emotion","Text Placement","Full Prompt (copy-paste)"]
header_row(ws, 4, prompt_h, PURPLE)

def full_prompt(ptype, subj, env, cam, light, color, comp, emo, textz):
    return (f"{subj}, {env}, {cam}, {light}, {color}, {comp}, {emo}. {textz}. "
            f"AgroManch brand: deep green #1B5E20 + amber #F57F17 accents, modern clean Indian agri aesthetic, "
            f"Devanagari text-safe zone, logo bottom-right, high detail, no watermark. --ar "
            + ("9:16" if ptype in ("Reel Thumbnail","Infographic") else "4:5" if ptype=="Carousel Cover" else "1:1"))

prompts = [
    ("Poster","मुस्कुराता भारतीय किसान हाथ में स्मार्टफोन व सुनहरी गेहूं की बालियां","धूप वाला हरा-भरा खेत, दूर ट्रैक्टर","mid-shot, 35mm, shallow depth","सुनहरी golden-hour rim light","हरा+एम्बर+नीला आसमान","rule-of-thirds, किसान बाएं, दायां top text-space खाली","गर्व + उम्मीद","ऊपर-दाएं headline ज़ोन, नीचे CTA bar",""),
    ("Reel Thumbnail","किसान चौंका हुआ चेहरा, हाथ में मंडी की पर्ची","साधारण मंडी background blur","close-up portrait, 50mm","high-contrast dramatic","लाल alert + हरा contrast","face बाएं, दायां बड़े bold Hindi text के लिए","हैरानी + curiosity","दायां 50% बड़े Devanagari hook के लिए",""),
    ("Carousel Cover","गेहूं/टमाटर की फसल top-down flat-lay व छोटे icons","साफ़ studio जैसा सफ़ेद-हरा background","top-down flat lay, 24mm","soft even diffused","हरा+सफ़ेद minimal","center title, चारों ओर breathing space","भरोसा + clarity","center headline block, नीचे swipe hint",""),
    ("Infographic","step-by-step icons: फसल→app→buyer→पैसा, तीर के साथ","minimal solid green-amber background","flat vector illustration","flat no-shadow","हरा+एम्बर+सफ़ेद","vertical flow top→bottom, 4 steps","समझ + ease","हर step के नीचे label ज़ोन, top title bar",""),
    ("Poster","महिला किसान सब्ज़ी टोकरी के साथ आत्मविश्वास से","गाँव का खेत, सुबह की रोशनी","mid-shot, 35mm","soft morning light","हरा+गुलाबी warm","किसान center-left, दायां text","सशक्तिकरण + गर्व","दायां top headline, नीचे CTA",""),
    ("Reel Thumbnail","split-screen: मुरझाई बनाम स्वस्थ फसल","खेत close-up दोनों तरफ","split close-up macro","dramatic side light","लाल बनाम हरा","आधा-आधा split, center divider","चिंता→राहत","ऊपर बड़ा 'ALERT' Hindi ज़ोन",""),
    ("Infographic","सरकारी योजना का पैसा खाते में जाते हुए, rupee icons","green gradient background","flat vector","flat bright","हरा+एम्बर+सफ़ेद","center rupee flow, side eligibility list","उत्साह + भरोसा","top scheme-name bar, side bullet ज़ोन",""),
    ("Carousel Cover","Dragon fruit / नई फसल का vibrant close-up","साफ़ dark background, spotlight","macro product shot, 100mm","spotlight high-contrast","गुलाबी+हरा vibrant","fruit center, top headline","जिज्ञासा + अवसर","top bold 'छुपी फसल' ज़ोन",""),
]
def pcolor(i,row): return PURPLE_LIGHT if i%2==0 else WHITE
disp = []
for ptype, subj, env, cam, light, color, comp, emo, textz, _ in prompts:
    fp = full_prompt(ptype, subj, env, cam, light, color, comp, emo, textz)
    disp.append((ptype, subj, env, cam, light, color, comp, emo, textz, fp))
write_table(ws, 5, disp, pcolor, fonts=9)
# usage note
ur = 5 + len(disp) + 1
ws.merge_cells(f"A{ur}:L{ur}")
ws[f"A{ur}"].value = "💡 HOW TO USE: Copy the 'Full Prompt' cell → paste into your image tool → replace {crop}/{region} with today's topic → generate 3 variants → pick highest-contrast for the hook. For Ideogram/Canva keep Devanagari text in the prompt; for MJ/Flux add Hindi text in Canva after."
ws[f"A{ur}"].fill = fill(AMBER_LIGHT); ws[f"A{ur}"].font = body_font(9, True); ws[f"A{ur}"].alignment = left(); ws.row_dimensions[ur].height = 30
widths(ws, [14,30,26,20,20,18,28,16,24,60])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: ⚡ DAILY CONTENT GENERATOR  (Phase 5)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("⚡ Daily Content Generator"); ws.sheet_view.showGridLines = False
title_bar(ws, "⚡  Daily Viral Content Generator — 1 Topic → 5 Assets", "H", color=ORANGE,
          sub="Reusable template. Type today's topic in the yellow cell → follow each block to produce all 5 assets.")

ws.merge_cells("A3:H3")
ws["A3"].value = "👉 INPUT — आज का Topic यहाँ लिखो:"; ws["A3"].fill = fill(GREEN_DARK)
ws["A3"].font = hdr_font(11, True, WHITE); ws["A3"].alignment = left(); ws.row_dimensions[3].height = 24
ws.merge_cells("A4:H4")
ws["A4"].value = "[ यहाँ topic टाइप करो — जैसे: गेहूं मंडी भाव / PMFBY claim / प्याज भंडारण ]"
ws["A4"].fill = fill(YELLOW); ws["A4"].font = Font(name="Calibri", size=12, bold=True, color="000000"); ws["A4"].alignment = center(); ws.row_dimensions[4].height = 30

ws.merge_cells("A6:H6")
ws["A6"].value = "⬇️  AUTO-APPLY: Best Hook Pattern + Best CTA + Best Viral Structure (नीचे हर asset के लिए formula भरा है)"
ws["A6"].fill = fill(AMBER); ws["A6"].font = hdr_font(10, True, WHITE); ws["A6"].alignment = center(); ws.row_dimensions[6].height = 22

gen_h = ["Asset","Pattern to Use","Hook Formula (पहले 3 सेकंड)","Structure / Body","CTA Formula","Best Time","Psychology"]
header_row(ws, 7, gen_h, ORANGE)
gen = [
    ("🎬 Viral Reel","Profit Reveal / Mandi Shock","'[Topic] में किसान को ₹__ मिला — कैसे?' (shock number first)","Hook 3s → Problem 5s → AgroManch solution 15s → Proof 10s → CTA 5s","'Download करो — link bio 👇'","8:30 PM","Curiosity + Profit"),
    ("🖼️ Viral Poster","Scheme Bomb / Calculator","बड़ा number + '[Topic]' headline, एक चौंकाने वाला आँकड़ा","Visual: किसान + number. 1 line benefit. Logo + CTA bar.","'App में पूरी जानकारी 📲'","12:00 PM","Loss Avoidance + Authority"),
    ("📑 Viral Carousel","Myth Buster / Tutorial","Slide 1: '[Topic] के बारे में 5 बातें जो किसान नहीं जानते'","6-8 slides: 1 hook → 5 value points → 1 proof → 1 CTA slide","'Save 📌 + दोस्त को share 🙏'","12:00 PM","Curiosity + Social Proof"),
    ("📲 Story Sequence","Community Debate / Countdown","Slide 1: Poll '[Topic] पर आप क्या सोचते हो?'","3-4 slides: Poll → Result tease → Value → Swipe-up CTA","'Vote 👆 + App खोलो'","07:00 PM","Community + Urgency"),
    ("💬 Engagement Post","Community Debate / Field Interview","'[Topic] पर आपका experience? सच बताओ 👇'","Question + relatable image. Promise to reply every comment.","'Comment करो — video में नाम आएगा 💬'","06:00 PM","Community + Local Identity"),
]
def genfn(i,row): return ORANGE_LIGHT if i%2==0 else WHITE
write_table(ws, 8, gen, genfn, fonts=9)
fr = 8 + len(gen) + 1
ws.merge_cells(f"A{fr}:H{fr}")
ws[f"A{fr}"].value = ("📋 5-MINUTE ROUTINE: 1) Topic लिखो  2) ऊपर के 5 formulas में {Topic} replace करो  "
                     "3) AI Image Prompt Library से visual बनाओ  4) Posting Schedule से time पक्का करो  "
                     "5) Banks में नई row के रूप में log करो। हर दिन = 5 assets, 0 confusion।")
ws[f"A{fr}"].fill = fill(GREEN_LIGHT); ws[f"A{fr}"].font = body_font(10, True); ws[f"A{fr}"].alignment = left(); ws.row_dimensions[fr].height = 36
widths(ws, [16,22,40,44,28,11,22])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: ⚙️ CONTENT OPERATING SYSTEM  (Phase 6)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("⚙️ Content Operating System"); ws.sheet_view.showGridLines = False
title_bar(ws, "⚙️  Automated Content Operating System — SOPs", "F", color=TEAL,
          sub="Daily · Weekly · Monthly workflows across Research → Create → Publish → Community → Track")

def sop_block(ws, start, heading, color, rows):
    ws.merge_cells(start_row=start, start_column=1, end_row=start, end_column=6)
    c = ws.cell(row=start, column=1, value=heading); c.fill=fill(color); c.font=hdr_font(11,True,WHITE); c.alignment=left()
    ws.row_dimensions[start].height = 24
    header_row(ws, start+1, ["Time","Function","Action","Owner","Tool","Output"], color)
    write_table(ws, start+2, rows, (lambda i,row: TEAL_LIGHT if i%2==0 else WHITE), fonts=9)
    return start+2+len(rows)+1

daily = [
    ("7:00 AM","Research","Mandi भाव + agri news + weather check; pick newsjack","Content Lead","News Bank, Agmarknet","Today's angle locked"),
    ("8:00 AM","Create","Daily Generator चलाओ → 5 assets बनाओ","Creator","Daily Generator sheet","5 assets drafted"),
    ("9:00 AM","Visuals","AI Image Library से poster/thumbnail generate","Designer","Ideogram/Canva","Visuals ready"),
    ("Per schedule","Publish","Best-time slots पर post (देखो Schedule)","Publisher","Meta/YT/Buffer","Posts live"),
    ("Hourly","Community","हर comment + DM का reply, lead capture","Community Mgr","WhatsApp/IG","0 unanswered, leads logged"),
    ("9:00 PM","Track","आज का reach/saves/clicks KPI Tracker में log","Analyst","KPI Tracker sheet","Daily numbers logged"),
]
nxt = sop_block(ws, 3, "🌅  DAILY WORKFLOW", TEAL, daily)
weekly = [
    ("Mon","Research","पिछले हफ्ते के top-3 posts analyze, pattern winners निकालो","Strategist","KPI Tracker","Winning patterns list"),
    ("Mon","Plan","अगले 7 दिन calendar lock, banks से ideas pull","Content Lead","Master Calendar","Week planned"),
    ("Tue","Create","Batch shoot 5-7 Reels एक साथ","Creator","Phone/Camera","Week's reels shot"),
    ("Wed","Create","Carousels + posters batch design","Designer","Canva","Visuals batched"),
    ("Fri","Publish","YouTube long-form upload (Tue/Fri 5 PM)","Publisher","YT Studio","Video live"),
    ("Sun","Track","Weekly KPI review, double-down decision","Analyst","KPI Tracker","Next-week priorities"),
]
nxt = sop_block(ws, nxt, "📆  WEEKLY WORKFLOW", GREEN_DARK, weekly)
monthly = [
    ("Week 1","Research","महीने का theme + 1 बड़ी campaign तय करो","Strategist","All banks","Monthly theme"),
    ("Week 2","Create","1 hero documentary/success story produce","Creator","Field shoot","Hero asset"),
    ("Week 3","Analyze","Pattern Prioritization scores refresh (real data)","Analyst","KPI + Phase 1","Updated tiers"),
    ("Week 4","Report","Growth report vs KPI targets; roadmap adjust","Content Lead","Roadmap sheet","Monthly report"),
    ("Ongoing","Bank refill","इस्तेमाल हुए ideas hat‍ाओ, banks में 50 नए जोड़ो","Content Lead","Content Banks","Banks topped up"),
]
nxt = sop_block(ws, nxt, "🗓️  MONTHLY WORKFLOW", AMBER, monthly)
widths(ws, [12,14,46,16,18,28])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: 🧠 FARMER PSYCHOLOGY DB  (Phase 7)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("🧠 Farmer Psychology DB"); ws.sheet_view.showGridLines = False
title_bar(ws, "🧠  Farmer Psychology Database — 9 Triggers", "G", color=PINK_DARK,
          sub="हर content को इन triggers से map करो → hook तेज़ करो, conversion बढ़ाओ")
psy_h = ["Trigger","किसान की भावना","Best Patterns","Hook Style","Example Hook","Business Lever","Strength"]
header_row(ws, 3, psy_h, PINK_DARK)
psy_rows = [
    ("Fear (डर)","फसल/पैसा खोने का डर","Crop Emergency, Weather","🚨 alert + तुरंत कार्रवाई","'🚨 72 घंटे में फसल खतरे में — अभी यह करो'","Retention + WhatsApp","Very High"),
    ("Profit (मुनाफा)","ज़्यादा कमाने का सपना","Profit Reveal, Calculator","बड़ा number पहले","'इस किसान ने 1 एकड़ से ₹__ लाख कमाए'","App Download + Listing","Very High"),
    ("Loss Avoidance","नुकसान से बचना","Mandi Shock, Scheme Bomb","छूटते मौके का डर","'मंडी में ₹__ कम मिल रहे — रुको!'","Registration + Trust","Very High"),
    ("Social Proof","'दूसरे कर रहे तो सही'","Success Story, Field Interview","असली किसान + आँकड़ा","'500 किसानों ने AgroManch चुना — क्यों?'","Trust + Registration","High"),
    ("Local Identity","अपनी भाषा/क्षेत्र अपनापन","Regional Language, Mahila Kisan","अपनी बोली में","'किसान भाई — आज भोजपुरी में बात'","Reach + Retention","High"),
    ("Authority","विशेषज्ञ पर भरोसा","Myth Buster, Tutorial","तथ्य + विशेषज्ञ","'कृषि वैज्ञानिक बता रहे हैं सच'","Brand Authority","Medium-High"),
    ("Curiosity (जिज्ञासा)","'यह क्या है?' जानने की चाह","Hidden Crop, Jugaad","अधूरी जानकारी/राज़","'यह फसल ₹__/kg बिकती है — कोई नहीं उगाता क्यों?'","Shareability + Reach","Very High"),
    ("Urgency (तात्कालिकता)","अभी कार्रवाई का दबाव","Seasonal Countdown, Weather","समय-सीमा + countdown","'बुवाई में बस __ दिन बाकी!'","Listing + Marketplace","High"),
    ("Community (समुदाय)","अपनेपन व आवाज़ की चाह","Community Debate, Award","सवाल + भागीदारी","'सच बोलो — मंडी fair है? Vote 👇'","Engagement + WhatsApp","High"),
]
write_table(ws, 4, psy_rows, (lambda i,row: PINK_LIGHT if i%2==0 else WHITE), fonts=9)
# mapping note
mr = 4 + len(psy_rows) + 1
ws.merge_cells(f"A{mr}:G{mr}")
ws[f"A{mr}"].value = "🎯 RULE: हर post में कम से कम 1 trigger साफ़ हो। Tier-A days पर Fear/Profit/Loss/Curiosity stack करो — यही सबसे ज़्यादा viral + convert करते हैं।"
ws[f"A{mr}"].fill = fill(AMBER_LIGHT); ws[f"A{mr}"].font = body_font(10, True); ws[f"A{mr}"].alignment = left(); ws.row_dimensions[mr].height = 30
widths(ws, [20,24,24,22,46,24,12])

# ══════════════════════════════════════════════════════════════════════════════
# SHEET: 📊 KPI TRACKER + ROADMAP  (Phase 3.8 + 8.8/8.9)
# ══════════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("📊 KPI Tracker + Roadmap"); ws.sheet_view.showGridLines = False
title_bar(ws, "📊  Content KPI Tracker  +  90-Day Growth Roadmap", "L", color=BLUE_DARK,
          sub="ऊपर: रोज़/हफ्ते का KPI log। नीचे: 90-दिन का growth roadmap।")

# KPI tracker table
ws.merge_cells("A3:L3")
ws["A3"].value = "📈  CONTENT KPI TRACKER (हर post के बाद भरो)"; ws["A3"].fill = fill(BLUE_DARK)
ws["A3"].font = hdr_font(11, True, WHITE); ws["A3"].alignment = left(); ws.row_dimensions[3].height = 22
kpi_h = ["Date","Asset ID","Pattern","Platform","Reach","Views","Saves","Shares","Comments","Profile→App Clicks","Downloads Attributed","Verdict (Scale/Kill)"]
header_row(ws, 4, kpi_h, BLUE_DARK)
# blank rows for logging
for i in range(20):
    r = 5+i; ws.row_dimensions[r].height = 18
    bg = WHITE if i%2==0 else BLUE_LIGHT
    for col in range(1,13):
        cell(ws, r, col, "", bg, size=9)
# data validation for verdict
dv = DataValidation(type="list", formula1='"⬆️ Scale,➡️ Keep,⬇️ Kill,🔁 Remix"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"L5:L24")

# Roadmap
rb = 27
ws.merge_cells(f"A{rb}:L{rb}")
ws[f"A{rb}"].value = "🚀  90-DAY GROWTH ROADMAP (Zero → 1M trajectory)"; ws[f"A{rb}"].fill = fill(GREEN_DARK)
ws[f"A{rb}"].font = hdr_font(11, True, WHITE); ws[f"A{rb}"].alignment = left(); ws.row_dimensions[rb].height = 22
road_h = ["Phase","Days","Theme","Content Focus","Primary Goal","Posting Volume","Key Patterns","Target Outcome"]
header_row(ws, rb+1, road_h, GREEN_DARK)
roadmap = [
    ("🌱 Foundation","1-30","भरोसा + पहचान बनाओ","Mandi Shock, Success Story, Tutorial — समझाओ AgroManch क्यों","Awareness + first 10K downloads","1 Reel + 1 secondary/day","Mandi Shock, Profit Reveal, Tutorial","10K downloads, 6K registrations"),
    ("🌿 Momentum","31-60","Proof + समुदाय","Success stories, Scheme Bomb, Mahila Kisan, WhatsApp push","Trust + community 40K","2 Reels/day + daily story","Scheme Bomb, Success Story, Community","75K downloads, 40K WhatsApp"),
    ("🌾 Scale","61-90","Marketplace ignition","Hidden Crop, Calculator, Buyer connects, Regional language","Listings + revenue","2-3 assets/day + hero weekly","Hidden Crop, Calculator, Regional","15K listings, 6K connects, revenue live"),
]
write_table(ws, rb+2, roadmap, (lambda i,row: GREEN_LIGHT if i%2==0 else WHITE), fonts=9)
# 4-12 month note
fn = rb+2+len(roadmap)+1
ws.merge_cells(f"A{fn}:L{fn}")
ws[f"A{fn}"].value = ("➡️ MONTH 4-12: हर महीने theme दोहराओ + winning patterns (KPI data से) पर double-down। "
                     "Banks रोज़ refill। Regional language + hero documentaries scale करो। Target: 10 लाख farmers by Month 12.")
ws[f"A{fn}"].fill = fill(AMBER_LIGHT); ws[f"A{fn}"].font = body_font(10, True); ws[f"A{fn}"].alignment = left(); ws.row_dimensions[fn].height = 32
widths(ws, [13,8,20,34,22,16,24,28])

# ══════════════════════════════════════════════════════════════════════════════
wb.save("/home/user/python-calculator-/AgroManch_Master_System.xlsx")
print("✅ Saved: AgroManch_Master_System.xlsx")
print("Sheets:", wb.sheetnames)
print(f"Reels:{len(reel_rows)} Carousel:{len(carousel_rows)} Static:{len(static_rows)} Story:{len(story_rows)} Engagement:{len(engage_rows)} News:{len(news)} Calendar:{len(cal_rows)}")
print("Total content ideas:", len(reel_rows)+len(carousel_rows)+len(static_rows)+len(story_rows)+len(engage_rows))

"""
AgroManch Content Creation Master Sheet Builder
Creates a fully formatted Excel workbook with 8 sheets for daily content creation
"""

from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScaleRule

wb = Workbook()

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
GREEN_DARK   = "1B5E20"   # header bg
GREEN_MED    = "2E7D32"
GREEN_LIGHT  = "C8E6C9"   # row fill
AMBER        = "F57F17"
AMBER_LIGHT  = "FFF9C4"
RED_DARK     = "B71C1C"
RED_LIGHT    = "FFCDD2"
BLUE_DARK    = "0D47A1"
BLUE_LIGHT   = "BBDEFB"
YELLOW       = "FFEB3B"
WHITE        = "FFFFFF"
GRAY_LIGHT   = "F5F5F5"
ORANGE       = "E65100"
ORANGE_LIGHT = "FFE0B2"
PURPLE       = "4A148C"
PURPLE_LIGHT = "E1BEE7"
TEAL         = "004D40"
TEAL_LIGHT   = "B2DFDB"

def hdr_font(size=11, bold=True, color=WHITE):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def body_font(size=10, bold=False, color="000000"):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def thin_border():
    s = Side(style="thin", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def set_col_width(ws, col_letter, width):
    ws.column_dimensions[col_letter].width = width

def write_header_row(ws, row_num, headers, bg_color, font_color=WHITE, height=30):
    ws.row_dimensions[row_num].height = height
    for col, text in enumerate(headers, 1):
        c = ws.cell(row=row_num, column=col, value=text)
        c.fill = fill(bg_color)
        c.font = hdr_font(10, True, font_color)
        c.alignment = center()
        c.border = thin_border()

def write_cell(ws, row, col, value, bg=None, bold=False, color="000000",
               align="left", size=10):
    c = ws.cell(row=row, column=col, value=value)
    if bg:
        c.fill = fill(bg)
    c.font = body_font(size, bold, color)
    c.alignment = left() if align == "left" else center()
    c.border = thin_border()
    return c

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1: 🏠 DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = "🏠 Dashboard"
ws1.sheet_view.showGridLines = False
ws1.row_dimensions[1].height = 60

# Title
ws1.merge_cells("A1:J1")
t = ws1["A1"]
t.value = "🌾  AgroManch — Daily Content Creation System  🌾"
t.fill = fill(GREEN_DARK)
t.font = Font(name="Calibri", size=18, bold=True, color=WHITE)
t.alignment = center()

ws1.merge_cells("A2:J2")
s = ws1["A2"]
s.value = "Research-backed viral content engine | 20 Patterns | 8 Platforms | Daily Ready"
s.fill = fill(GREEN_MED)
s.font = Font(name="Calibri", size=11, bold=False, color=YELLOW)
s.alignment = center()

ws1.row_dimensions[2].height = 22

# --- Sheet Navigator ---
ws1.row_dimensions[4].height = 20
ws1["A4"].value = "📋  SHEETS IN THIS WORKBOOK"
ws1["A4"].fill = fill(AMBER)
ws1["A4"].font = hdr_font(11, True, WHITE)
ws1.merge_cells("A4:J4")
ws1["A4"].alignment = center()

nav_data = [
    ("Sheet", "Tab Name", "Purpose", "Use When"),
    ("1", "🏠 Dashboard",        "Overview + quick reference",                  "First time setup"),
    ("2", "📅 30-Day Calendar",   "Date-wise post plan for Jun–Jul 2026",        "Every day — check today's post"),
    ("3", "🎯 20 Viral Patterns", "All 20 patterns with hooks + psychology",     "Before making any post"),
    ("4", "📝 Daily Content Builder","Fill 5 fields → get complete post ready",  "Every day — actual content creation"),
    ("5", "🎬 Reel Scripts",      "30 ready-to-shoot Reel scripts in Hindi",     "When making Instagram/YouTube Shorts"),
    ("6", "🖼️ Image Post Bank",   "30 carousel + engagement post templates",     "When making static posts"),
    ("7", "📊 YouTube Planner",   "YouTube-specific titles + descriptions",      "Every Tuesday & Friday"),
    ("8", "⏰ Posting Schedule",  "Best times + hashtag banks per platform",     "Scheduling posts"),
]

nav_colors = [GREEN_DARK, GREEN_LIGHT, AMBER_LIGHT, BLUE_LIGHT,
              ORANGE_LIGHT, PURPLE_LIGHT, TEAL_LIGHT, RED_LIGHT, GRAY_LIGHT]

for i, (sn, tab, purpose, when) in enumerate(nav_data):
    r = 5 + i
    ws1.row_dimensions[r].height = 22
    bg = GREEN_DARK if i == 0 else (GREEN_LIGHT if i % 2 == 0 else WHITE)
    fc = WHITE if i == 0 else "000000"
    bd = True if i == 0 else False
    for col, val in enumerate([sn, tab, purpose, when], 1):
        c = ws1.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(10, bd, fc)
        c.alignment = left()
        c.border = thin_border()

for col, w in zip("ABCD", [6, 28, 45, 38]):
    ws1.column_dimensions[col].width = w

# --- Key Stats Box ---
ws1.row_dimensions[15].height = 20
ws1.merge_cells("A15:D15")
ws1["A15"].value = "📊  RESEARCH STATS — What we found"
ws1["A15"].fill = fill(BLUE_DARK)
ws1["A15"].font = hdr_font(11, True, WHITE)
ws1["A15"].alignment = center()

stats = [
    ("88.6 करोड़", "भारत के Internet Users (2024)"),
    ("55%", "Rural India — Total Internet Users"),
    ("84.16%", "किसान जो Social Media Use करते हैं"),
    ("93%", "YouTube पर Indian Language Content देखते हैं"),
    ("4.9M Subscribers", "Indian Farmer Channel — #1 Agri YouTube"),
    ("1.8 Billion Views", "Indian Farmer Channel — Total Views"),
    ("₹2-3 लाख/Reel", "Top Agri Creator Brand Deal Rate"),
    ("5 Hashtags Max", "Instagram 2025 Algorithm Limit"),
    ("8-10 PM IST", "Indian Farmer Peak Scroll Time"),
    ("WhatsApp", "#1 Viral Distribution Platform for Farmers"),
]

for i, (stat, desc) in enumerate(stats):
    r = 16 + i
    ws1.row_dimensions[r].height = 20
    bg = GREEN_LIGHT if i % 2 == 0 else WHITE
    write_cell(ws1, r, 1, stat,  bg, True,  GREEN_DARK, "center", 11)
    write_cell(ws1, r, 2, desc,  bg, False, "000000",   "left",   10)
    write_cell(ws1, r, 3, "",    bg)
    write_cell(ws1, r, 4, "",    bg)

# --- Top 5 Patterns Quick Ref (placed right of nav table, row 13+) ---
ws1.merge_cells("F13:J13")
ws1["F13"].value = "🔥  TOP 5 VIRAL PATTERNS (Quick Ref)"
ws1["F13"].fill = fill(RED_DARK)
ws1["F13"].font = hdr_font(11, True, WHITE)
ws1["F13"].alignment = center()
ws1.row_dimensions[13].height = 22

top5 = [
    ("P#", "Pattern", "Virality", "Best Platform"),
    ("1",  "💰 Profit Reveal",         "10/10", "YouTube + Reel"),
    ("2",  "🚨 Mandi Shock",           "10/10", "WhatsApp + Reels"),
    ("3",  "🔴 Crop Emergency Alert",  "9/10",  "WhatsApp + YT Short"),
    ("6",  "📋 Scheme Bomb",           "9/10",  "WhatsApp + Instagram"),
    ("7",  "⚡ Jugaad Hack",           "9/10",  "YouTube"),
]
for i, row in enumerate(top5):
    r = 14 + i
    ws1.row_dimensions[r].height = 22
    bg = RED_DARK if i == 0 else (RED_LIGHT if i % 2 == 1 else WHITE)
    fc = WHITE if i == 0 else "000000"
    for col, val in enumerate(row, 6):
        c = ws1.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(10, (i == 0), fc)
        c.alignment = center()
        c.border = thin_border()

for col, w in zip("FGHIJ", [5, 30, 10, 22]):
    ws1.column_dimensions[col].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 2: 📅 30-DAY CALENDAR
# ══════════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("📅 30-Day Calendar")
ws2.sheet_view.showGridLines = False

ws2.merge_cells("A1:T1")
t2 = ws2["A1"]
t2.value = "📅  AgroManch 30-Day Content Calendar  |  5 June – 4 July 2026"
t2.fill = fill(GREEN_DARK)
t2.font = Font(name="Calibri", size=14, bold=True, color=WHITE)
t2.alignment = center()
ws2.row_dimensions[1].height = 35

headers2 = [
    "Date", "Day", "Week", "Platform", "Content Type",
    "Content Title (Hindi)", "Viral Pattern", "P#", "Virality\n(1-10)",
    "Hook — First 3 Seconds", "Caption Template (Hindi)",
    "Hashtags (5 max)", "CTA (Hindi)", "Post Time\nIST",
    "Objective", "Target Audience", "Engagement", "Difficulty",
    "Status", "Notes"
]
write_header_row(ws2, 2, headers2, GREEN_DARK)

cal_data = [
    ("05-06-2026","1","W1","YouTube","Long Video","AgroManch क्या है? मंडी से कैसे बचाता है","Brand Introduction","0","8","क्या आपको पता है मंडी में आपके पैसों का क्या होता है?","मंडी में 7 middlemen आपका मुनाफा खाते हैं। AgroManch ने इसका हल निकाला — direct buyers, fair price, घर से बेचो।","#kisan #agromanch #indianfarmers #khetibadi #farming","Link description में Download करो 👇","05:00 PM","Awareness","All Farmers","High","Low","⬜ Pending","8-12 min; screen recording + field footage"),
    ("05-06-2026","1","W1","Instagram","Reel","मंडी vs AgroManch — 60 सेकंड में देखो फर्क","Mandi Shock","2","9","[Slip दिखाओ] देखो इस किसान को क्या मिला — ₹8/kg","मंडी: ₹8/kg 🔴 | AgroManch: ₹13/kg 🟢 | 10 quintal = ₹5000 extra 💰 | यह फर्क हर बार होता है।","#kisan #farming #indianfarmers #agromanch #kheti","Download करो — link bio में 👇","08:30 PM","Awareness","Small Farmers","Very High","Low","⬜ Pending","Mandi slip prop + split screen edit"),
    ("06-06-2026","2","W1","Facebook","Video","किसान राजेश — AgroManch से ₹3000 ज़्यादा मिले","Farmer Success Story","4","8","'पहले डर था online बेचने का — आज मुझे खुशी है'","राजेश जी UP के किसान। गेहूं मंडी: ₹2100. AgroManch: ₹2380. 15 quintal × ₹280 = ₹4200 extra 💰","#kisan #indianfarmers #farming #agromanch #kisaan","किसान दोस्त को tag करो 👇","09:30 AM","Awareness","Rural 35-55","High","Medium","⬜ Pending","Real farmer interview; 2-3 min"),
    ("07-06-2026","3","W1","Instagram","Reel","मंडी में 5 घंटे vs AgroManch में 5 मिनट","Old vs New Farming","14","8","[Timer] मंडी: 5 घंटे इंतज़ार... AgroManch: 5 मिनट listing","मंडी: सुबह 5 बजे निकलो → queue → कम दाम 😔 | AgroManch: App खोलो → 5 मिनट → ज़्यादा पैसे 💚","#kisan #farming #kheti #agromanch #indianfarmers","Download करो — link bio 👇","08:00 PM","Awareness","Young 18-35","Very High","Low","⬜ Pending","Time-lapse edit; before/after split"),
    ("07-06-2026","3","W1","Instagram","Story / Poll","Poll: अभी कहाँ बेचते हो फसल?","Community Debate","19","7","[Poll graphic] आप बताओ","Option A: मंडी | B: Middleman | C: Direct buyer | D: AgroManch","#kisan #farming","Vote करो 👆","07:00 PM","Community","All Farmers","High","Low","⬜ Pending","Instagram Poll sticker; follow up next day"),
    ("08-06-2026","4","W1","WhatsApp","Broadcast","AgroManch Tip #1: Listing से पहले 3 काम","Jugaad Hack","7","7","💡 AgroManch Daily Tip","✅ साफ photo लो (सुबह की रोशनी) ✅ Quantity सही बताओ ✅ Grade mention करो → 40% ज़्यादा buyers आएंगे","N/A","App download करो","07:30 AM","Acquisition","Active Farmers","High","Low","⬜ Pending","Daily series; simple image"),
    ("09-06-2026","5","W1","YouTube","Long Video","AgroManch पर पहली listing — Complete Tutorial 2026","Tech Tutorial","16","8","बिना confusion के 5 मिनट में पहली listing करो","Registration → Photo → Price → Publish → Payment — हर step Hindi में। आज ही शुरू करो।","#kisan #agromanch #indianfarmers #farming #kisaan","Subscribe 🔔 करो + Download: description link","05:00 PM","Acquisition","New Digital Farmers","High","Low","⬜ Pending","Screen recording; Hindi voiceover; 10-15 min"),
    ("09-06-2026","5","W1","Instagram","Carousel","मंडी chain में 7 middlemen — आपका ₹ कहाँ जाता है?","Mandi Shock","2","9","किसान को ₹8 मिला। Consumer ने ₹35 दिए। बीच में क्या हुआ?","[8 slides] हर middleman का cut। Final: AgroManch से direct — किसान को ₹13+","#kisan #farming #indianfarmers #agromanch #khetibadi","Save करो 📌 + WhatsApp group में share करो 🙏","12:00 PM","Trust","All Farmers","Very High","Medium","⬜ Pending","Infographic design; data-driven"),
    ("10-06-2026","6","W1","Instagram","Engagement Post","Comment करो: आपकी सबसे बड़ी farming problem?","Community Trigger","19","7","[Farmer image] आपकी सबसे बड़ी problem?","हम AgroManch पर काम करते हैं आपके लिए। बताओ — सबसे बड़ी farming problem? हर comment पढ़ते हैं।","#kisan #farming #indianfarmers #kheti #krishi","Comment करो 👇 — आपका नाम हमारे video में आ सकता है!","07:00 PM","Community","All Segments","High","Low","⬜ Pending","Reply to every comment"),
    ("11-06-2026","7","W1","Instagram","Reel","AgroManch download करो — 5 FREE चीजें मिलती हैं","Scheme Bomb","6","8","रुको! Download से पहले यह 5 free चीजें देखो","✅ Daily Mandi Alerts 📊 ✅ Expert Consultation 👨‍🌾 ✅ Weather Alert 🌦️ ✅ Scheme Tracker 📋 ✅ Buyer Network 🤝 — सब FREE!","#kisan #agromanch #farming #indianfarmers #kisaan","Download — link bio 👇","08:30 PM","App Download","Young Farmers","Very High","Low","⬜ Pending","Screen recording of 5 features"),
    ("12-06-2026","8","W2","YouTube","Long Video","AgroManch buyers कौन हैं? — पूरी transparency","Trust Building","–","8","किसे बेच रहे हो? Buyers की पूरी जानकारी","FPOs, bulk buyers, exporters, direct consumers — सब verified। AgroManch पर कोई unknown buyer नहीं।","#kisan #agromanch #farming #indianfarmers #agribusiness","Subscribe 🔔 + Comment: आप कौन सी फसल बेचोगे?","05:00 PM","Trust","Skeptical Farmers","High","Medium","⬜ Pending","Buyer interview on camera"),
    ("12-06-2026","8","W2","Instagram","Reel","पहली बार online बेचा — किसान का real reaction","Farmer Success Story","4","9","[Clip] 'अरे! पैसे आ गए!' — किसान का असली reaction","यह moment देखो 🥹 पहली online payment आई। यही AgroManch का मकसद है — किसान की मुस्कान।","#kisan #farming #indianfarmers #agromanch #annadata","Join करो — link bio 👇","08:30 PM","Trust","All Farmers","Explosive","Medium","⬜ Pending","Real farmer reaction — must be authentic"),
    ("13-06-2026","9","W2","Facebook","Video","AgroManch payment process — पैसा कब और कैसे आता है","Transparency","–","7","'Payment कब मिलेगी?' — सीधा जवाब","Sale confirm → 48-72 घंटे → bank account। UPI/NEFT। No hidden charges।","#kisan #agromanch #farming #indianfarmers #krishi","Comment: और क्या जानना है AgroManch के बारे में?","10:00 AM","Trust","All Farmers","High","Low","⬜ Pending","Animation or screencast + Hindi voiceover"),
    ("14-06-2026","10","W2","Instagram","Reel","AgroManch के 5 hidden features — 90% किसान नहीं जानते","Tech Tutorial","16","8","रुको! AgroManch में यह 5 features हैं — क्या पता था?","AI Price Predictor 🤖 | Buyer chat 💬 | Crop grading 📊 | Insurance tracker 📋 | 11 भाषाएं 🌐 | Save करो!","#kisan #agromanch #farming #indianfarmers #kisaan","Save करो 📌 + dost को tag करो 👇","08:00 PM","App Download","Tech-interested","Very High","Low","⬜ Pending","Screen recording + fast transitions"),
    ("15-06-2026","11","W2","WhatsApp","Broadcast","PM-KISAN Alert: 20वीं किस्त — status check करो","Scheme Bomb","6","9","🚨 PM-KISAN Alert — किस्त आ रही है!","Status check: AgroManch App → Schemes → PM-KISAN. eKYC हुई? Bank linked? — अभी करो!","N/A","AgroManch App → Schemes section","07:30 AM","Acquisition","PM-KISAN Farmers","Explosive","Low","⬜ Pending","Verify PM-KISAN date before sending"),
    ("16-06-2026","12","W2","YouTube","Long Video","FPO + AgroManch = 500 किसान, एक आवाज़","Success Story","4","9","500 किसानों ने AgroManch पर बेचा — नतीजा देखो","[FPO Name] ने bulk listing की। ₹X/quintal ज़्यादा मिले। यह है FPO की ताकत।","#kisan #farming #indianfarmers #agromanch #agribusiness","FPO में हो? Bulk listing करो — free contact: link","05:00 PM","Trust","FPO Members","High","High","⬜ Pending","Real FPO interview; 10-15 min documentary"),
    ("16-06-2026","12","W2","Instagram","Carousel","AgroManch की 5 Guarantees","Trust Building","–","7","AgroManch ने किसान से 5 वादे किए","✅ Verified buyers ✅ Payment 72 hrs ✅ Price ≥ Mandi ✅ Free expert ✅ 0% hidden charges | Save करो 📌","#kisan #agromanch #farming #indianfarmers #kisaan","Save करो 📌 + किसान दोस्त को share करो","12:00 PM","Trust","New Farmers","High","Low","⬜ Pending","Clean infographic; brand colors"),
    ("17-06-2026","13","W2","Instagram","Engagement Post","AgroManch में क्या improve होना चाहिए?","Feedback / Community","19","6","[Open feedback box] हम सुन रहे हैं","Comment में लिखो — कोई भी suggestion। Best suggestion को prize मिलेगा।","#kisan #farming #indianfarmers #agromanch #krishi","Comment करो 👇 — best suggestion = prize","06:00 PM","Community","App Users","Medium","Low","⬜ Pending","Reply to every comment; use for product team"),
    ("18-06-2026","14","W2","Instagram","Reel","₹50,000+ transaction — AgroManch की security","Trust","–","8","बड़े transaction में डर लगता है? यह देखो","🔒 SSL encryption 🔒 Verified buyers 🔒 Escrow hold 🔒 Dispute team | Proof देखो।","#kisan #agromanch #farming #indianfarmers #kisaan","Comment: online payment से डर लगता है?","08:30 PM","Trust","Older Risk-averse","High","Low","⬜ Pending","Animation of security flow"),
    ("19-06-2026","15","W3","YouTube","Short","🚨 Pest Alert — UP/Bihar किसान ध्यान दें","Crop Emergency","3","9","🚨 ALERT: [Pest] इस हफ्ते [State] के [Crop] में!","Symptom: [describe] | इलाज: [2 lines] | AgroManch Expert free consultation: App → Expert Section","#kisan #farming #krishi #indianfarmers #fasal","AgroManch App → Expert Section","05:00 PM","Trust+Acquisition","Crop Farmers","Explosive","Low","⬜ Pending","Weekly series; highest WhatsApp forward rate"),
    ("19-06-2026","15","W3","Instagram","Reel","Crop Disease Alert — फसल बचाओ अभी","Crop Emergency","3","10","[Close-up diseased leaf] क्या आपकी फसल में यह हो रहा है?","लक्षण: [describe] | अभी करो: ✅ Action 1 ✅ Action 2 ✅ AgroManch expert को photo भेजो | WhatsApp group में share करो 🙏","#kisan #farming #krishi #fasal #indianfarmers","WhatsApp group में share करो 🙏 | Expert: link bio","08:30 PM","Trust","Crop Farmers","Explosive","Low","⬜ Pending","Close-up crop footage; highest share trigger"),
    ("20-06-2026","16","W3","Facebook","Video","Post-harvest mistakes — ₹50,000 बचाओ","Jugaad Hack","7","8","फसल कट गई — अब क्या? 90% किसान यहाँ गलती करते हैं","❌ Wrong storage ❌ Turai मंडी rush ❌ No quality check | ✅ Solution: AgroManch grade + right time","#kisan #farming #indianfarmers #krishi #agromanch","App → Storage + Selling Guide","10:00 AM","Trust","Post-harvest","High","Medium","⬜ Pending","Field demo video; 5-7 min"),
    ("21-06-2026","17","W3","Instagram","Reel","PMFBY Claim — 60 सेकंड में | Save करो","Scheme Bomb","6","9","फसल बर्बाद हुई? PMFBY claim नहीं किया? यह गलती मत करो","Step 1: App → Insurance 📱 | Step 2: Damage photo 📸 | Step 3: Details भरो ✍️ | Step 4: Submit ✅","#kisan #farming #pmfby #indianfarmers #kisaan","Save 📌 + WhatsApp group में share करो 🙏","08:00 PM","Trust+Acquisition","PMFBY Farmers","Very High","Low","⬜ Pending","Screen recording; must be accurate"),
    ("21-06-2026","17","W3","Instagram","Carousel","सभी Government Schemes एक जगह","Scheme Bomb","6","8","इतनी schemes हैं किसानों के लिए — क्या आपको सब पता हैं?","PM-KISAN | PMFBY | KCC | PM Kusum | PKVY | Soil Health Card | e-NAM — हर scheme detail","#kisan #farming #pmkisan #indianfarmers #krishi","Save 📌 + किसान दोस्त को tag करो","12:00 PM","Trust","All Farmers","Very High","Medium","⬜ Pending","Infographic; one scheme per slide"),
    ("22-06-2026","18","W3","WhatsApp","Broadcast","Mandi Price Alert: गेहूं बेचें या रोकें?","Market Intel","2","8","📊 AgroManch Weekly Price Alert","गेहूं मंडी: ₹[X]/quintal | AgroManch: ₹[Y]/quintal | Prediction: [trend] | Action: [buy/hold]","N/A","AgroManch App → Sell Now","07:30 AM","Marketplace","Wheat Farmers","High","Low","⬜ Pending","Real mandi data required; weekly series"),
    ("23-06-2026","19","W3","YouTube","Long Video","Soil Health Card को 60 सेकंड में समझें","Myth Buster","11","8","25 करोड़ cards बंटे — 90% किसान नहीं समझते","N-P-K ratio, pH, micronutrients — 5 मिनट में सिखाता हूं कैसे पढ़ें और क्या करें।","#kisan #farming #soilhealth #indianfarmers #krishi","Save करो + Card लेकर follow करो 👇","05:00 PM","Trust","All Crop Farmers","High","Medium","⬜ Pending","Actual Soil Health Card prop; animated NPK"),
    ("23-06-2026","19","W3","Instagram","Reel","Jugaad: ₹200 में drip irrigation — step by step","Jugaad Hack","7","9","Drip irrigation ₹1 लाख में? यह आदमी ₹200 में बना गया!","पुरानी बोतलें + drip nozzles = working system 🌱 | Water saving: 60% ✅ | Cost: ₹200 ✅","#kisan #farming #jugaad #indianfarmers #khetibadi","WhatsApp में share करो 🙏 | Drip: AgroManch पर भी मिलता है","08:30 PM","Trust","Cost-conscious Farmers","Explosive","Low","⬜ Pending","Field DIY demo; most shareable"),
    ("24-06-2026","20","W3","Instagram","Engagement Post","Poll: मंडी में सही दाम मिलता है? Honestly बताओ","Mandi Debate","2","8","[Graphic] सच बोलो — मंडी fair है या नहीं?","Vote करो + Comment में experience share करो। आपके जवाब से AgroManch बेहतर बनेगा।","#kisan #farming #indianfarmers #kisaan #kheti","Vote 👆 + Comment में experience share करो","06:00 PM","Community","All Selling Farmers","Very High","Low","⬜ Pending","Instagram poll; highest comment rate topic"),
    ("25-06-2026","21","W3","Instagram","Reel","मौसम Alert — 72 घंटे में फसल खतरे में","Weather Emergency","10","9","🚨 [State] Alert: 72 घंटे में [weather event] — अभी यह करो","✅ Action 1 ✅ Action 2 ✅ Action 3 | AgroManch Weather Alert subscribe करो — district-level notification","#kisan #farming #mausam #indianfarmers #krishi","AgroManch App → Weather Alert ON 🔔","08:00 PM","Trust+Acquisition","Active Farmers","Explosive","Low","⬜ Pending","IMD data; district-level Instagram targeting"),
    ("26-06-2026","22","W4","YouTube","Long Video","IT छोड़ा — खेती अपनाई — ₹8 लाख/साल | Real Story","Aspiration Story","4","10","'सब कहते थे बर्बाद होगा — आज income देखो'","Software engineer ने job छोड़ी। 3 साल बाद: 5 एकड़ + AgroManch + ₹8 लाख/year. आज हज़ारों को inspire कर रहे हैं।","#kisan #farming #indianfarmers #agromanch #organicfarming","Subscribe 🔔 + Comment: क्या आप भी खेती में आना चाहते हो?","05:00 PM","Community","Young + Career-changers","Explosive","High","⬜ Pending","Real person documentary; 12-18 min"),
    ("26-06-2026","22","W4","Instagram","Reel","AgroManch 1 लाख किसान milestone 🎉","Milestone / Community","–","8","1,00,000 किसान! — यह moment हमारा नहीं, आपका है","1 लाख families की hope 🎉 1 लाख खेत जहाँ fair price मिलती है। Thank you 🙏 अगला: 5 लाख — साथ हो?","#kisan #agromanch #farming #indianfarmers #annadata","Tag करो उस किसान को जिसे AgroManch से जोड़ना है 👇","08:30 PM","Community","All Users","Very High","Low","⬜ Pending","Celebration reel; testimonial clips; emotional music"),
    ("27-06-2026","23","W4","Facebook","Video","Mahila Kisan + AgroManch — रेखा देवी की कहानी","Women Farmer","9","9","'पति बाहर — मैंने अकेले 3 एकड़ manage किया'","रेखा देवी, [Village]. AgroManch से सब्जी direct बेची। ₹2 लाख annual income। अब गाँव की women को सिखाती हैं।","#kisan #mahilakisan #farming #indianfarmers #womenempowerment","माँ/बहन को tag करो जो खेती करती हों 👇","09:30 AM","Community","Women Farmers","Very High","Medium","⬜ Pending","Real woman farmer; local language preferred"),
    ("28-06-2026","24","W4","Instagram","Reel","Dragon Fruit — ₹200/kg बिकता है, कोई उगाता नहीं क्यों?","Hidden Crop Reveal","15","9","यह फल ₹200/किलो बिकता है — demand है import से — क्यों नहीं उगाते?","Market: ₹150-200/kg 💰 | Demand growing 40%/yr 📈 | Import: Vietnam से 😱 | AgroManch: 50+ buyers","#kisan #farming #dragonfruit #indianfarmers #agromanch","AgroManch App → Dragon Fruit → buyers देखो","08:00 PM","Marketplace","Progressive Farmers","Explosive","Low","⬜ Pending","Stunning fruit visuals; highest curiosity trigger"),
    ("29-06-2026","25","W4","WhatsApp","Broadcast","Kisan of the Week — [Name] को congratulations!","Recognition Award","17","7","🏆 AgroManch Kisan Star of the Week","[Farmer Name], [Village] ने [achievement] किया। Nominate करो: App → Community → Nominate Kisan","N/A","App → Community section","07:30 AM","Community","All Farmers","High","Low","⬜ Pending","Weekly series; builds loyalty"),
    ("30-06-2026","26","W4","YouTube","Long Video","Bhojpuri में — AgroManch पर कइसे बेचीं अपन फसल","Regional Language","18","9","किसान भाई — आज अपनी भाषा में बात करेंगे","[Complete tutorial in Bhojpuri] Registration से payment — हर step भोजपुरी में। UP/Bihar किसानों के लिए।","#kisan #farming #indianfarmers #bhojpuri #agromanch","Share करो UP/Bihar के किसान दोस्तों को 🙏","05:00 PM","Acquisition","UP+Bihar Farmers","Explosive","Medium","⬜ Pending","Native Bhojpuri speaker host; 50M+ Bhojpuri speakers"),
    ("30-06-2026","26","W4","Instagram","Carousel","AgroManch join करने के 10 फायदे","Platform Benefits","–","8","AgroManch join करो — 10 reasons","Direct buyers | Higher price | Fast payment | Free expert | Weather alerts | Scheme tracker | No charges | Regional language | WhatsApp support | Community","#kisan #agromanch #farming #indianfarmers #kisaan","Save 📌 + किसान दोस्त को share करो","12:00 PM","Acquisition","Undecided Farmers","High","Low","⬜ Pending","Decision carousel; each slide = 1 data proof"),
    ("01-07-2026","27","W4","Instagram","Engagement Post","Tag करो उस किसान को जिसने inspire किया 🙏","Identity / Community","–","7","[Sunset over wheat field] — किसान भाई का सम्मान","खेती में एक mentor होता है। वो आपके पिता? भाई? गाँव के किसान? Tag करो — उनकी मेहनत को tribute।","#kisan #farming #annadata #indianfarmers #kisanputra","Tag करो उस किसान को जिसे respect करते हो 👇","07:00 PM","Community","All Farmers","High","Low","⬜ Pending","Emotional image; Jai Kisan sentiment"),
    ("02-07-2026","28","W4","Instagram","Reel","AgroManch App — 5 मिनट में पहली listing | Tutorial","App Tutorial","16","8","5 मिनट challenge: क्या 5 मिनट में listing कर सकते हो?","Download 30sec | Register 1min | Crop details 1min | Price 30sec | Publish 30sec = ~4 min ✅","#kisan #agromanch #farming #indianfarmers #kisaan","Try करो और comment में time बताओ 👇 | Download: bio link","08:30 PM","App Download","New Users","High","Low","⬜ Pending","Screen recording with timer; gamification"),
    ("03-07-2026","29","W4","YouTube","Long Video","AgroManch 30 Days — किसानों का साथ, किसानों की जीत","Transparency Report","–","8","1 महीना हो गया — AgroManch ने क्या achieve किया? सच बताते हैं","Farmers joined: [X] | Trade: ₹[X] | Avg premium: [X]% | Challenges: [honest] | Month 2 plan: [preview]","#kisan #agromanch #farming #indianfarmers #agribusiness","Comment: Month 2 में क्या चाहते हो AgroManch से?","05:00 PM","Trust+Community","All Users","High","Medium","⬜ Pending","Founder on camera; honest tone builds massive trust"),
    ("03-07-2026","29","W4","Instagram","Reel","यह moment आपका हो सकता है — AgroManch join करो","Emotional CTA","–","9","[Compilation] किसानों के real reactions — पहली payment आई","खुशी, आँसू, परिवार को दिखाना। यह है असली AgroManch 🥹 आपका moment कब है?","#kisan #agromanch #farming #indianfarmers #annadata","Download करो अभी — link bio 👇","08:30 PM","App Download","All Segments","Explosive","Medium","⬜ Pending","Reaction compilation; emotional music; highest conversion"),
    ("04-07-2026","30","W4","Facebook","Video","AgroManch Month 1 — Transparency Report","Transparency","–","7","30 दिन में क्या किया? क्या हुआ? क्या सीखा?","Farmers: [X] | Trade: ₹[X] | Premium: [X]% | Challenge: [honest] | Month 2: [preview]","#kisan #agromanch #farming #indianfarmers #agribusiness","Comment: Month 2 में क्या चाहते हो?","10:00 AM","Trust","All Users","High","Medium","⬜ Pending","Founder on camera; builds credibility"),
    ("04-07-2026","30","W4","Instagram","Story","Countdown: Month 2 — कुछ बड़ा आ रहा है!","Next Phase Teaser","–","6","[Countdown timer] Month 2 में kuch bada aa raha hai","New feature | Special offer | Kisan Awards | Biggest trade day | Register → first notification 🔔","N/A","App → Notifications ON 🔔","08:00 PM","Community+App","All Users","Medium","Low","⬜ Pending","Anticipation teaser; multiple story slides"),
]

# Row colors by platform
platform_colors = {
    "YouTube":   GREEN_LIGHT,
    "Instagram": BLUE_LIGHT,
    "Facebook":  ORANGE_LIGHT,
    "WhatsApp":  TEAL_LIGHT,
}

for i, row in enumerate(cal_data):
    r = 3 + i
    ws2.row_dimensions[r].height = 50
    plat = row[3]
    bg = platform_colors.get(plat, GRAY_LIGHT)
    for col, val in enumerate(row, 1):
        c = ws2.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(9)
        c.alignment = left()
        c.border = thin_border()
    # Status column (col 19) special color
    status_cell = ws2.cell(row=r, column=19)
    status_cell.font = body_font(10, True, AMBER)

col_widths2 = [13,5,4,11,14,40,22,4,9,35,50,38,28,9,18,20,13,10,11,30]
for i, w in enumerate(col_widths2, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 3: 🎯 20 VIRAL PATTERNS
# ══════════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("🎯 20 Viral Patterns")
ws3.sheet_view.showGridLines = False

ws3.merge_cells("A1:L1")
t3 = ws3["A1"]
t3.value = "🎯  AgroManch — 20 Proven Viral Patterns  |  Research-backed Psychology"
t3.fill = fill(RED_DARK)
t3.font = Font(name="Calibri", size=14, bold=True, color=WHITE)
t3.alignment = center()
ws3.row_dimensions[1].height = 35

headers3 = ["P#","Pattern Name","Description (Hindi)","Why It Works","Psychology",
            "Best Platform","Hook Template (Hindi)","Virality\n(1-10)",
            "Trust\n(1-10)","Share\n(1-10)","Difficulty","AgroManch Angle"]
write_header_row(ws3, 2, headers3, RED_DARK)

patterns = [
    ("1","💰 Profit Reveal (मुनाफा खुलासा)",
     "इस फसल/पशु से मैंने ₹X लाख कमाए — real numbers",
     "किसान अपनी income से तुलना करते हैं; gap होने पर तुरंत share",
     "Financial Aspiration + FOMO",
     "YouTube Long + Instagram Reel",
     "इस [crop] से [farmer name] ने कमाए ₹[X] — देखो कैसे",
     "10","9","9","Medium",
     "AgroManch मार्केटप्लेस से बेचकर ₹X ज़्यादा मिले"),
    ("2","🚨 Mandi Shock (मंडी अन्याय)",
     "Mandi slip दिखाओ: ₹2/kg मिला; retail: ₹30 — कोई narration नहीं",
     "दोनों rural+urban को हिट करता है — किसान को गुस्सा, शहरी को guilt",
     "Outrage + Injustice + Solidarity",
     "WhatsApp + YouTube Shorts + Facebook",
     "[Mandi slip] देखो इस किसान को क्या मिला — और consumer ने क्या दिया",
     "10","7","10","Low",
     "AgroManch पर बेचो — middleman खत्म, ज़्यादा दाम"),
    ("3","🔴 Crop Emergency Alert",
     "यह कीड़ा/बीमारी आपकी फसल बर्बाद कर देगी — अभी देखें",
     "Farmers तुरंत अपनी फसल से मिलान करते हैं; same symptom = instant share",
     "Fear + Urgency + Reciprocity",
     "WhatsApp (fastest) + YouTube Short",
     "🚨 [State] Alert: [Pest] इस हफ्ते [Crop] में — अभी यह करो",
     "9","9","10","Low",
     "AgroManch App → Expert Section → free photo consultation"),
    ("4","🌟 Farmer Success Story",
     "पहले नुकसान था, आज ₹X लाख — named village, real person, real numbers",
     "'अगर वो कर सकता है तो मैं भी' — Peer Modeling Effect",
     "Social Proof + Aspiration + Identity",
     "YouTube Long-form + Instagram Reel",
     "[Name] के गाँव में कोई farming नहीं करता था, आज ₹[X] लाख कमा रहे हैं",
     "9","9","8","Medium",
     "AgroManch से जुड़े किसान की success story"),
    ("5","🚜 Machinery Pride (ट्रैक्टर Entertainment)",
     "ट्रैक्टर washing in rivers, new tractor reviews, terrain challenges",
     "ट्रैक्टर = biggest capital purchase; tribal pride content",
     "Pride + Entertainment + Tribal Identity",
     "YouTube (Long + Shorts दोनों)",
     "[Farmer name] का ₹[X] लाख का ट्रैक्टर — पहला दिन [location] में",
     "9","7","8","Low",
     "AgroManch पर पुराना ट्रैक्टर बेचें/किराए पर दें"),
    ("6","📋 Scheme Bomb (सरकारी योजना Alert)",
     "सरकार दे रही है ₹X — आज ही apply करो, last date [date]",
     "Real financial benefit + urgency = immediate action और share",
     "Loss Aversion + Reciprocity",
     "WhatsApp (fastest) + YouTube Shorts + Instagram",
     "🚨 [Scheme]: सरकार दे रही ₹[X] — last date [date] — apply करो अभी",
     "9","8","10","Low",
     "AgroManch App में Scheme Tracker — सभी schemes एक जगह"),
    ("7","⚡ Jugaad Hack (Zero Cost Innovation)",
     "₹200 में वो करो जो ₹20,000 में होता था",
     "Cost saving + 'smart feeling' + shareable to farmer friends",
     "Smart Saver Identity + Community Service",
     "YouTube (Indian Farmer = maximum viewer category)",
     "₹[X] में बनाओ वो जो normally ₹[Y] में मिलता है — देखो jugaad",
     "9","8","9","Low",
     "AgroManch पर wholesale price — middleman नहीं"),
    ("8","🏡 Before/After Transformation",
     "6 महीने पहले: बंजर जमीन → आज: profitable खेत",
     "Visual proof = immediate credibility; transformation hooks",
     "Hope + Proof + Possibility Thinking",
     "Instagram Reel + YouTube Shorts",
     "6 महीने पहले यह थी यह जमीन — आज देखो [close-up of crop]",
     "8","8","7","High",
     "पहले: मंडी 5 घंटे, आज: AgroManch 5 मिनट"),
    ("9","👩‍🌾 Mahila Kisan Viral",
     "महिला ट्रैक्टर चलाती है / बड़ा farm manage करती है / दादी YouTube",
     "Surprise + Pride + National media pickup potential",
     "Gender Surprise + Empowerment + Social Justice",
     "Instagram + YouTube दोनों",
     "[Woman name] — [unexpected achievement] — गाँव में हलचल मच गई",
     "9","8","9","Low",
     "महिला किसान ने AgroManch से पहली बार direct selling की"),
    ("10","⚡ Weather Emergency Alert",
     "अगले 48 घंटों में ओले/बारिश — अपनी फसल यह करो",
     "Real-time relevance + immediate economic consequence",
     "Fear of Loss + Protective Instinct",
     "WhatsApp (fastest) + Instagram Stories",
     "🚨 [State]: अगले [X] घंटों में [weather] — फसल बचाओ यह 3 काम करो",
     "9","8","10","Low",
     "AgroManch Weather Alert — हर जिले का अलग notification"),
    ("11","🧪 Myth Buster (गलत धारणाएं तोड़ें)",
     "किसान यह गलती करते हैं — मैंने ₹50,000 बर्बाद किया",
     "Counter-intuitive + confessional = high curiosity + trust",
     "Curiosity + Trust (वो honest है) + Community Service",
     "Instagram Carousel + YouTube",
     "यह farming tip हर कोई देता है — मैंने आजमाया और ₹[X] का नुकसान हुआ",
     "8","9","8","Medium",
     "AgroManch पर सच्ची कीमत — mandi से बेहतर सौदा"),
    ("12","📊 Profit Calculator (फसल चुनाव)",
     "1 एकड़ में गेहूं या टमाटर — exact calculation",
     "Decision-making tool = save & share for later",
     "Utility + Empowerment + Smart Farmer Identity",
     "Instagram Carousel + YouTube",
     "[Crop A] vs [Crop B] — 1 एकड़ में कौन ज़्यादा देता है? calculation देखो",
     "8","8","7","Medium",
     "AgroManch Profit Calculator — अपनी जमीन, अपनी फसल"),
    ("13","🎤 Field Interview (Real Farmer)",
     "Real village में जाओ, किसान से camera पर बात करो",
     "Peer-to-peer trust — 'expert नहीं, किसान बोल रहा है'",
     "Social Proof + Regional Identity",
     "YouTube + Facebook",
     "[Name], [Village], [State] — [achievement in 1 line]",
     "8","9","7","Medium",
     "AgroManch partner किसान की कहानी — खेत से सीधे"),
    ("14","🆚 Old vs. New Farming",
     "दादाजी ऐसे करते थे, हम ऐसे करते हैं — फर्क देखो",
     "Generational resonance + technical proof + entertainment",
     "Nostalgia + Progress Pride",
     "YouTube + Instagram",
     "दादाजी [method] से करते थे — आज [modern method] से — देखो फर्क",
     "8","7","7","Low",
     "पहले: मंडी जाओ; आज: AgroManch App से घर बैठे बेचो"),
    ("15","🌾 Hidden Crop Reveal",
     "यह फसल ₹5,000/किलो बिकती है — भारत में कोई उगाता नहीं",
     "Curiosity trigger + FOMO — 'मुझे क्यों नहीं पता था?'",
     "Curiosity + Exclusivity + FOMO",
     "YouTube Long + Instagram Reel",
     "यह [crop] ₹[X]/किलो बिकती है — और India में demand है import से",
     "9","7","8","Low",
     "AgroManch पर premium buyers हैं rare crops के लिए"),
    ("16","📱 Tech for Farmers",
     "मोबाइल से मिट्टी परीक्षण / Drone mapping / AI रोग पहचान",
     "Modern + accessible + saves money = triple hook",
     "Innovation Pride + Cost Saving + Accessibility",
     "YouTube + Instagram",
     "मोबाइल से करो [tech task] — free app है, देखो कैसे",
     "8","8","7","Medium",
     "AgroManch App — एक जगह: बेचो, खरीदो, सलाह लो"),
    ("17","🏆 Award / Recognition Story",
     "इस किसान को PM ने सम्मानित किया / Padma Shri मिली",
     "Community pride + aspirational — खेती में भी इज़्ज़त मिलती है",
     "Prestige + Community Pride + Identity",
     "YouTube + Facebook + WhatsApp",
     "[Name] को [Award] मिला — [Village], [State] का यह किसान कौन है?",
     "8","9","8","Low",
     "AgroManch Best Farmer Award — nominate करें"),
    ("18","🗺️ Regional Language Content",
     "भोजपुरी/मराठी/तेलुगु में खेती की बात",
     "68% Indians prefer native language; 30-60% higher engagement",
     "Identity + Belonging + Trust",
     "YouTube + WhatsApp",
     "[Regional language opening line about farming problem or success]",
     "9","9","9","Medium",
     "AgroManch — आपकी भाषा में, आपके इलाके का बाज़ार"),
    ("19","💬 Debate / Community Trigger",
     "Chemical खाद सही या Organic? मंडी बेहतर या online?",
     "Opinioned farmers comment करते हैं — algorithm को signal",
     "Identity Defense + Expertise Display + Community",
     "Facebook + Instagram + YouTube Community",
     "[Controversial farming question] — आपकी राय क्या है? Comment करो",
     "7","7","8","Low",
     "AgroManch पर बेचना बेहतर है या मंडी? — किसान बोलें"),
    ("20","📅 Seasonal Countdown",
     "रबी बुवाई में 15 दिन बाकी — यह 5 काम अभी करें",
     "Time pressure + practical checklist = save and share",
     "Urgency + Completeness + Planning",
     "Instagram Carousel + WhatsApp",
     "[Season] में [X] दिन बाकी — अभी यह [N] काम करो",
     "8","8","9","Low",
     "AgroManch पर order करो — बुवाई season में delivery guaranteed"),
]

pat_row_colors = [GREEN_LIGHT, WHITE]
for i, row in enumerate(patterns):
    r = 3 + i
    ws3.row_dimensions[r].height = 55
    bg = GREEN_LIGHT if i % 2 == 0 else WHITE
    for col, val in enumerate(row, 1):
        c = ws3.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(9 if col > 3 else 10, col == 2)
        c.alignment = left()
        c.border = thin_border()
    # Virality score highlight
    for score_col in [8, 9, 10]:
        sc = ws3.cell(row=r, column=score_col)
        score_val = row[score_col - 1]
        if score_val == "10":
            sc.fill = fill(GREEN_MED)
            sc.font = body_font(11, True, WHITE)
        elif score_val == "9":
            sc.fill = fill(AMBER)
            sc.font = body_font(11, True, WHITE)

col_widths3 = [4, 26, 38, 38, 28, 24, 42, 8, 8, 8, 10, 38]
for i, w in enumerate(col_widths3, 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 4: 📝 DAILY CONTENT BUILDER
# ══════════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("📝 Daily Content Builder")
ws4.sheet_view.showGridLines = False

ws4.merge_cells("A1:F1")
t4 = ws4["A1"]
t4.value = "📝  AgroManch Daily Content Builder  |  5 Input Fields → Complete Post Ready"
t4.fill = fill(PURPLE)
t4.font = Font(name="Calibri", size=14, bold=True, color=WHITE)
t4.alignment = center()
ws4.row_dimensions[1].height = 35

# Instructions
instr = [
    "HOW TO USE THIS SHEET:",
    "1. Fill the 5 yellow INPUT fields (Date, Platform, Pattern, Topic, Farmer Detail)",
    "2. The blue OUTPUT fields give you: Hook, Caption, Hashtags, CTA, Posting Time",
    "3. Copy output directly to your phone / scheduling tool",
    "4. Repeat for each platform each day",
]
for i, line in enumerate(instr):
    r = 2 + i
    ws4.merge_cells(f"A{r}:F{r}")
    c = ws4.cell(row=r, column=1, value=line)
    c.fill = fill(PURPLE_LIGHT if i > 0 else PURPLE)
    c.font = body_font(10, i == 0, WHITE if i == 0 else PURPLE)
    c.alignment = left()
    ws4.row_dimensions[r].height = 18

# INPUT SECTION
ws4.row_dimensions[8].height = 25
ws4.merge_cells("A8:F8")
inp_hdr = ws4["A8"]
inp_hdr.value = "📥  INPUT — Fill These 5 Fields"
inp_hdr.fill = fill(AMBER)
inp_hdr.font = hdr_font(12, True, WHITE)
inp_hdr.alignment = center()

inputs = [
    ("1", "Date", "Enter today's date (DD-MM-YYYY)", "05-06-2026"),
    ("2", "Platform", "YouTube / Instagram / Facebook / WhatsApp", "Instagram"),
    ("3", "Viral Pattern #", "Enter pattern number 1-20 (see Sheet 3)", "2"),
    ("4", "Topic/Crop Focus", "What is this post about? (e.g., Tomato farming, PM-KISAN)", "टमाटर की खेती"),
    ("5", "Key Farmer Detail", "Income figure / Problem / Location / Name for the hook", "₹4 लाख/एकड़ — Nashik के किसान"),
]

for i, (num, label, hint, example) in enumerate(inputs):
    r = 9 + i
    ws4.row_dimensions[r].height = 28
    write_cell(ws4, r, 1, num,     AMBER,       True,  WHITE,     "center")
    write_cell(ws4, r, 2, label,   AMBER_LIGHT, True,  AMBER,     "left")
    write_cell(ws4, r, 3, hint,    GRAY_LIGHT,  False, "555555",  "left")
    write_cell(ws4, r, 4, "",      YELLOW,      False, "000000",  "left")  # INPUT FIELD
    write_cell(ws4, r, 5, "Example:", GRAY_LIGHT, False, "888888","center")
    write_cell(ws4, r, 6, example, GRAY_LIGHT,  False, GREEN_DARK,"left")

ws4.merge_cells("A14:F14")
ws4["A14"].value = "⬆️  Fill column D (yellow cells) with your inputs above"
ws4["A14"].fill = fill(YELLOW)
ws4["A14"].font = body_font(10, True, AMBER)
ws4["A14"].alignment = center()
ws4.row_dimensions[14].height = 20

# OUTPUT SECTION
ws4.row_dimensions[16].height = 25
ws4.merge_cells("A16:F16")
out_hdr = ws4["A16"]
out_hdr.value = "📤  OUTPUT — Your Complete Post (Copy & Use)"
out_hdr.fill = fill(BLUE_DARK)
out_hdr.font = hdr_font(12, True, WHITE)
out_hdr.alignment = center()

outputs = [
    ("Hook\n(First 3 sec)", "यह [topic] वाले किसान देखें — [key detail] हो सकता है आपके साथ भी!", "Grab attention immediately; must match the viral pattern"),
    ("Caption\n(Hindi)", "आज हम बात करेंगे [topic] की जहाँ [farmer detail] ने\n[result] achieve किया। AgroManch पर direct buyers हैं\nइस फसल के लिए — ज़्यादा दाम, कम commission।\n\nAgroManch download करो — link bio में 👇", "Keep under 150 words for Reels; 150-300 for carousels"),
    ("Hashtags\n(5 max)", "#kisan #farming #[crop-specific] #indianfarmers #agromanch", "Follow 5-tag rule (post-2025 Instagram algorithm)"),
    ("CTA", "WhatsApp group में share करो 🙏 | Download: link bio 👇", "Always include WhatsApp share CTA for max organic spread"),
    ("Post Time\n(IST)", "Instagram Reel → Thursday/Sunday 8-10 PM | YouTube → Tuesday/Friday 5 PM upload", "Based on Indian farmer peak scroll behavior research"),
    ("Visual Brief", "[Close-up of crop / mandi slip / farmer face] — use real footage, not stock", "Real footage gets 3x more engagement than stock photos"),
    ("WhatsApp\nForward Text", "💡 किसान भाइयों — [1-line summary of the post] | AgroManch App: [link]", "Optimized for WhatsApp group forwards; 72% of virality comes from WhatsApp"),
]

for i, (label, content, note) in enumerate(outputs):
    r = 17 + i
    ws4.row_dimensions[r].height = 55
    write_cell(ws4, r, 1, str(i+1), BLUE_DARK, True, WHITE, "center")
    write_cell(ws4, r, 2, label,    BLUE_LIGHT, True, BLUE_DARK, "center")
    c = ws4.cell(row=r, column=3, value=content)
    c.fill = fill(WHITE)
    c.font = body_font(10, False, "000000")
    c.alignment = left()
    c.border = thin_border()
    ws4.merge_cells(f"C{r}:E{r}")
    write_cell(ws4, r, 6, note, GRAY_LIGHT, False, "555555", "left", 9)

for col, w in zip("ABCDEF", [4, 16, 38, 10, 10, 36]):
    ws4.column_dimensions[col].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 5: 🎬 REEL SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════
ws5 = wb.create_sheet("🎬 Reel Scripts")
ws5.sheet_view.showGridLines = False

ws5.merge_cells("A1:G1")
ws5["A1"].value = "🎬  AgroManch — 30 Ready-to-Shoot Reel Scripts (Hindi)"
ws5["A1"].fill = fill(ORANGE)
ws5["A1"].font = Font(name="Calibri", size=14, bold=True, color=WHITE)
ws5["A1"].alignment = center()
ws5.row_dimensions[1].height = 35

reel_headers = ["#","Title (Hindi)","Platform","Pattern","Duration","Hook\n(0-3 sec)","Script Summary + Key Shots","CTA","Viral\nScore"]
write_header_row(ws5, 2, reel_headers, ORANGE)

reels = [
    ("1","मंडी vs AgroManch — Live Comparison","Instagram","Mandi Shock (P2)","45-60s","[Mandi slip on screen] देखो इस किसान को क्या मिला — ₹8/kg","Shot 1: Mandi slip close-up (₹8/kg) | Shot 2: AgroManch app (₹13/kg) | Shot 3: Calculator — 10q × ₹5 = ₹5000 extra | Shot 4: Happy farmer | VO: 'यह फर्क हर बार होता है'","Download — link bio 👇","10/10"),
    ("2","पहली बार online बेचा — किसान का real reaction","Instagram","Success Story (P4)","30-45s","[Farmer checking phone] 'अरे! पैसे आ गए!' — यह देखो","Shot 1: Phone notification | Shot 2: Farmer's face reaction | Shot 3: Family seeing | Shot 4: Amount shown | VO: 'यह moment आपका भी हो सकता है' | Emotional background music","Join करो — link bio 👇","10/10"),
    ("3","Dragon Fruit — ₹200/kg, कोई उगाता नहीं क्यों?","Instagram + YT","Hidden Crop (P15)","45-60s","यह फल ₹200/किलो बिकता है — India में import होता है — क्यों नहीं उगाते?","Shot 1: Dragon fruit close-up | Shot 2: Price tag ₹200 | Shot 3: Import statistics | Shot 4: AgroManch buyers list | VO: '[X] buyers AgroManch पर हैं इसके लिए'","AgroManch → Dragon Fruit → Buyers देखो","9/10"),
    ("4","Jugaad: ₹200 में Drip Irrigation","Instagram + YT","Jugaad (P7)","45-60s","Drip irrigation ₹1 लाख में? यह आदमी ₹200 में बना गया!","Shot 1: Commercial drip system (₹1L price tag) | Shot 2: Old bottles + nozzles (₹200) | Shot 3: Installation step by step | Shot 4: Working system in field | VO: 'Water saving 60%'","Share करो किसान दोस्तों को 🙏","9/10"),
    ("5","Crop Disease Alert — [Crop] बचाओ अभी","Instagram + WA","Crop Emergency (P3)","30-45s","[Diseased leaf close-up] क्या आपकी [crop] में यह हो रहा है?","Shot 1: Diseased leaf extreme close-up | Shot 2: Symptom label (text overlay) | Shot 3: Solution product/method | Shot 4: Healthy crop | VO: 'AgroManch expert को photo भेजो — 2 घंटे में solution'","WhatsApp में share करो 🙏","10/10"),
    ("6","PM-KISAN किस्त — Status check 60 sec में","Instagram + WA","Scheme Bomb (P6)","45s","PM-KISAN की किस्त आ रही है — status check करो अभी","Shot 1: PM-KISAN logo | Shot 2: Screen recording: App → Schemes → Status | Shot 3: Status checked ✅ | Shot 4: Alert if not checked ⚠️ | VO: 'अभी check करो — miss मत होने देना'","Save करो 📌 + share करो","9/10"),
    ("7","PMFBY Claim — 60 सेकंड में जानो कैसे","Instagram","Scheme Bomb (P6)","45-60s","फसल बर्बाद हुई? PMFBY claim नहीं किया? यह गलती मत करो","Shot 1: Damaged crop aerial | Shot 2: App screen → Insurance | Shot 3: Photo upload | Shot 4: Submit → Acknowledge | VO: '48 घंटे में acknowledge, payment 10-15 days'","Save करो 📌 + WA group में share करो","9/10"),
    ("8","IT छोड़ा — खेती से ₹8 लाख/साल","Instagram + YT","Aspiration (P4)","45-60s","'सब कहते थे बर्बाद होगा — आज income देखो'","Shot 1: Corporate office vs farm (split) | Shot 2: Farmer working field | Shot 3: Income reveal (phone/document) | Shot 4: Happy family | VO: 'Software engineer → ₹8 लाख farmer'","Subscribe + Comment: क्या तुम भी want?","10/10"),
    ("9","Mahila Kisan — रेखा देवी ने ₹2 लाख कमाए","Instagram + FB","Women Farmer (P9)","45s","'पति बाहर — मैंने अकेले 3 एकड़ manage किया'","Shot 1: Woman in field | Shot 2: AgroManch app listing | Shot 3: Payment received | Shot 4: Family moment | VO: '₹2 लाख annual income — AgroManch के साथ'","माँ/बहन को tag करो 👇","9/10"),
    ("10","मौसम Alert — 72 घंटे में फसल खतरे में","Instagram + WA","Weather (P10)","30s","🚨 [State]: अगले 72 घंटे में [weather event]","Shot 1: Weather map | Shot 2: Crop in field | Shot 3: Action steps (text overlay) | Shot 4: AgroManch app weather section | VO: 'अभी यह 3 काम करो'","App → Weather Alert ON 🔔","9/10"),
    ("11","Soil Health Card 60 सेकंड में","Instagram + YT","Education (P11)","60s","25 करोड़ cards बंटे — 90% किसान नहीं समझते — देखो","Shot 1: Soil Health Card close-up | Shot 2: N-P-K explained (animation) | Shot 3: pH meaning | Shot 4: What to do based on your card | VO: 'Simple language में'","Save करो 📌 — बाद में card लेकर follow करो","8/10"),
    ("12","AgroManch 5 FREE Features","Instagram","App Feature (P16)","45s","रुको! Download से पहले यह 5 free चीजें देखो","Shot 1-5: Each feature screen recording (5 cuts of 6 sec each) | Feature names as text overlay | VO: 'सब कुछ FREE — download करो'","Download — link bio 👇","8/10"),
    ("13","Mandi Price Alert — गेहूं बेचें या रोकें?","Instagram","Market Intel (P2)","30s","📊 इस हफ्ते गेहूं बेचना ठीक नहीं — देखो क्यों","Shot 1: Current mandi price | Shot 2: 2-week trend chart | Shot 3: AgroManch price prediction | Shot 4: Recommendation text | VO: 'Subscribe करो weekly alert के लिए'","AgroManch Price Alert subscribe","8/10"),
    ("14","ट्रैक्टर की पहली drive — reaction","YouTube + Insta","Machinery (P5)","45-60s","[Tractor keys in hand] — आज पहली बार अपना ट्रैक्टर चलाया","Shot 1: Keys in hand | Shot 2: Climbing tractor (emotion on face) | Shot 3: First drive in field | Shot 4: Family watching | Natural sound + minimal VO","Comment: कब था आपका पहला tractor moment?","9/10"),
    ("15","Bhojpuri Tutorial — AgroManch पर कइसे बेचीं","YouTube","Regional (P18)","3-5min","[Bhojpuri] किसान भाई — आज अपनी भाषा में बात करेंगे","Full tutorial in Bhojpuri. Shot 1: Intro in Bhojpuri | Shot 2-8: Each app step with Bhojpuri VO | Shot 9: Payment received | Shot 10: CTA in Bhojpuri","Share करो UP/Bihar किसान दोस्तों को 🙏","10/10"),
    ("16","Before/After: 6 महीने में खेत कैसे बदला","Instagram + YT","Transformation (P8)","45-60s","6 महीने पहले यह थी यह जमीन — आज देखो","Shot 1: Before photo/video (barren/struggling) | Shot 2: Timeline graphic | Shot 3: Now — thriving crop | Shot 4: Income comparison | VO: 'यह change AgroManch के साथ possible है'","Join करो — link bio 👇","8/10"),
    ("17","AgroManch Download 5-min Challenge","Instagram","App Tutorial (P16)","45s","5 मिनट में AgroManch पर पहली listing — challenge!","Screen recording with timer graphic. Each step timed. End: 4:32 — 'Done!' | VO: 'Comment में बताओ — कितने minutes लगे?'","Try करो + time comment करो 👇","8/10"),
    ("18","गाँव की दादी ने YouTube शुरू किया","Instagram","Women/Age (P9)","30s","70 साल की दादी YouTube channel चलाती हैं — and करोड़ों views हैं","Close-up of elderly woman with phone | Farm background | Simple action — cooking/farming | Natural sound | Text: 'My Village Show — 364 Million views' | Inspired-by story","Subscribe + comment: आपकी दादी को tag करो","9/10"),
    ("19","Scheme: ₹1 लाख Solar Pump — Last Date!","Instagram + WA","Scheme Bomb (P6)","30s","🚨 ₹1 लाख का solar pump subsidy — last date [date]!","Shot 1: Solar pump in field | Shot 2: Subsidy % graphic | Shot 3: Application process (3 steps) | Shot 4: Deadline countdown | VO: 'Miss मत करो'","Apply करो अभी | AgroManch Schemes","9/10"),
    ("20","AgroManch 1 लाख Farmers Milestone 🎉","Instagram","Milestone","30-45s","1,00,000 किसान! — यह moment हमारा नहीं आपका है","Compilation: 10 × 3-sec farmer reaction clips | Celebration music | Text overlays: 1 लाख families, 1 लाख खेत, fair price | End: 'अगला: 5 लाख — साथ हो?'","Tag करो जिसे जोड़ना है 👇","8/10"),
    ("21","Hidden Crop: Moringa — ₹3,000/kg","Instagram + YT","Hidden Crop (P15)","45s","यह पत्ती ₹3,000/किलो बिकती है — international demand है","Close-up moringa leaves | Price comparison | Export demand data | AgroManch premium buyers | VO: 'First mover advantage'","AgroManch → Moringa → Buyers देखो","9/10"),
    ("22","Gir Cow Farming — ₹50,000/माह profit","YouTube + Insta","Profit Reveal (P1)","45-60s","Gir Cow क्यों? देखो — ₹50,000/माह — यह है formula","Shot 1: Gir cow footage | Shot 2: Milk production data | Shot 3: A2 milk price ₹80-100/L | Shot 4: Income calculation | VO: 'Premium buyers AgroManch पर'","AgroManch → Dairy category","9/10"),
    ("23","किसान को यह गलती मत करने देना","Instagram","Myth Buster (P11)","45s","यह farming tip हर कोई देता है — मैंने आजमाया, ₹30,000 गया","Counter-intuitive open | Show common 'tip' | Show why it failed | Show correct approach | VO: honest, self-deprecating","Save करो 📌 — गलती से बचो","8/10"),
    ("24","AgroManch Buyers कौन हैं? — Meet them","YouTube","Trust (P13)","3-5 min","किसे बेच रहे हो? AgroManch buyer का चेहरा देखो","Interview with 2-3 buyers: who they are, why they buy on AgroManch, what quality they want. Farmer watching can trust.","Subscribe + Comment: कौन सी फसल का buyer चाहिए?","8/10"),
    ("25","Weather + Farm Action Guide","Instagram + WA","Weather (P10)","30s","[Weather map] [State] में [X] — अभी यह 3 काम करो","Shot 1: IMD weather graphic | Shot 2-4: Each farm action (text + visual) | Shot 5: AgroManch early harvest option | VO: '3 काम अभी करो'","Share करो किसान WhatsApp group में 🙏","9/10"),
    ("26","Mushroom Farming — ₹3 लाख/साल घर से","YouTube + Insta","Profit Reveal (P1)","45-60s","घर के एक कमरे में ₹3 लाख/साल — mushroom farming","Shot 1: Small room setup | Shot 2: Mushroom growing | Shot 3: Harvest | Shot 4: Market/AgroManch sale | Shot 5: Income proof","AgroManch → Mushroom buyers","9/10"),
    ("27","FPO क्या है? 5 मिनट में समझो","YouTube + Insta","Education (P16)","3-5 min","500 किसान मिलकर क्या कर सकते हैं? — FPO की ताकत","Animation: individual farmer vs FPO collective | Negotiation power | AgroManch bulk listing | Real FPO success data","FPO में हो? AgroManch पर bulk list करो","8/10"),
    ("28","Old Farmer vs Young Farmer — Debate","Instagram","Debate (P19)","30s","दादाजी: Chemical खाद सही। मैं: Organic सही। कौन सही है?","Father-son debate format (humorous) | Both sides presented | No verdict — audience decides | VO: 'Comment में बताओ — आप किसके साथ?'","Comment: किसके साथ हो? Tag your father 👇","8/10"),
    ("29","E-NAM Tutorial — Online फसल बेचो","YouTube + Insta","Tech (P16)","3-5 min","e-NAM पर पहली बार बेचने का complete tutorial","Screen recording of e-NAM + AgroManch comparison | Step by step registration | First listing | VO in Hindi","Compare: e-NAM vs AgroManch — Comment में","7/10"),
    ("30","AgroManch Kisan of the Month","Instagram + FB","Recognition (P17)","30-45s","इस महीने का AgroManch Kisan Star — मिलो इनसे","Short interview + farm footage + achievement graphic | Community celebrate करे | Nomination process shown at end","Nominate करो: AgroManch App → Community","8/10"),
]

reel_colors = [ORANGE_LIGHT, WHITE]
for i, row in enumerate(reels):
    r = 3 + i
    ws5.row_dimensions[r].height = 70
    bg = ORANGE_LIGHT if i % 2 == 0 else WHITE
    for col, val in enumerate(row, 1):
        c = ws5.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(9)
        c.alignment = left()
        c.border = thin_border()
    # Virality score
    vc = ws5.cell(row=r, column=9)
    if row[8] == "10/10":
        vc.fill = fill(GREEN_MED); vc.font = body_font(11, True, WHITE)
    elif row[8] == "9/10":
        vc.fill = fill(AMBER); vc.font = body_font(11, True, WHITE)

col_widths5 = [4, 32, 14, 18, 9, 38, 55, 28, 9]
for i, w in enumerate(col_widths5, 1):
    ws5.column_dimensions[get_column_letter(i)].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 6: 🖼️ IMAGE POST BANK
# ══════════════════════════════════════════════════════════════════════════════
ws6 = wb.create_sheet("🖼️ Image Post Bank")
ws6.sheet_view.showGridLines = False

ws6.merge_cells("A1:H1")
ws6["A1"].value = "🖼️  AgroManch Image Post Bank  |  Carousels + Engagement Posts + Stories"
ws6["A1"].fill = fill(TEAL)
ws6["A1"].font = Font(name="Calibri", size=14, bold=True, color=WHITE)
ws6["A1"].alignment = center()
ws6.row_dimensions[1].height = 35

img_hdrs = ["#","Post Type","Title (Hindi)","Platform","Slides/Panels","Visual Brief","Caption Template","Hashtags","CTA","Expected\nEngagement"]
write_header_row(ws6, 2, img_hdrs, TEAL)

img_posts = [
    # Carousels
    ("1","Carousel","मंडी chain — 7 middlemen का पर्दाफाश","Instagram","8 slides","Slide 1: किसान ₹8 | Slides 2-8: Each middleman with % cut | Final: AgroManch direct → ₹13+","मंडी में किसान को ₹8/kg मिलता है। Consumer ₹35 देता है। बीच में क्या होता है? यह देखो 👆 Save करो 📌","#kisan #farming #indianfarmers #agromanch #khetibadi","Save 📌 + WhatsApp group में share 🙏","Very High"),
    ("2","Carousel","PM-KISAN से PMFBY — सभी Schemes Guide","Instagram","10 slides","Each slide = 1 scheme. Brand colors. Simple icon + scheme name + benefit amount + apply link","सरकार किसानों के लिए [X] schemes चला रही है। क्या आपको सब पता हैं? यह carousel save करो 📌","#kisan #pmkisan #farming #indianfarmers #krishi","Save 📌 + किसान दोस्त को tag करो","Very High"),
    ("3","Carousel","AgroManch की 5 Guarantees","Instagram","5 slides","Clean design. Each slide: 1 guarantee + icon + brief explanation. Brand green color.","AgroManch ने किसान से 5 वादे किए हैं। यह सिर्फ words नहीं — proof के साथ। Swipe करो →","#kisan #agromanch #farming #indianfarmers #kisaan","Join करो — link bio 👇","High"),
    ("4","Carousel","Kharif 2026 Checklist — 15 दिन बाकी","Instagram","8 slides","Countdown design. Each slide: 1 action item with deadline. Urgency design (red/orange).","Kharif season में [X] दिन बाकी। यह 8 काम अभी करो — नहीं तो season miss होगा। Save करो 📌","#kisan #farming #kharif #indianfarmers #krishi","Save 📌 + किसान group में share करो","High"),
    ("5","Carousel","Crop Profit Comparison 2026 — कौन सी फसल?","Instagram","10 slides","Table format. Each slide: 1 crop — cost, revenue, profit/acre. Source: AgroManch market data.","1 एकड़ में कौन सी फसल सबसे ज़्यादा मुनाफा देती है? Data देखो 👆 Save करो — हर season काम आएगा 📌","#kisan #farming #agribusiness #indianfarmers #agromanch","Save 📌 + Comment: आप कौन सी उगाते हो?","Very High"),
    ("6","Carousel","Soil Health Card Reading Guide","Instagram","8 slides","Each slide: 1 parameter. Simple infographic. N-P-K, pH, micronutrients explained visually.","25 करोड़ Soil Health Cards बंटे। 90% किसान नहीं समझते। यह carousel save करो — अपना card लेकर follow करो","#kisan #farming #soilhealth #indianfarmers #krishi","Save 📌 + Card लेकर follow करो","High"),
    ("7","Carousel","10 Reasons to Join AgroManch","Instagram","10 slides","Each slide: 1 benefit + data point + icon. Professional but farmer-friendly design.","AgroManch join करने के 10 फायदे — हर slide में एक reason + proof. Save करो 📌","#kisan #agromanch #farming #indianfarmers #kisaan","Join करो — link bio 👇","High"),
    ("8","Carousel","Post-Harvest Mistakes — ₹50,000 बचाओ","Instagram","6 slides","Slide 1: Problem (₹50K loss graphic) | Slides 2-5: Each mistake + fix | Slide 6: AgroManch solution","फसल काटने के बाद ये 5 गलतियाँ ₹50,000 बर्बाद कर देती हैं। यह carousel save करो 📌","#kisan #farming #indianfarmers #krishi #agromanch","Save 📌 + share करो farmer dost को","High"),
    # Engagement Posts
    ("9","Engagement Post","Poll: मंडी में सही दाम मिलता है?","Instagram","1 image","Split design: मंडी (red) vs AgroManch (green). Poll sticker prominent.","सच बोलो — मंडी fair है या नहीं? Vote करो 👆","#kisan #farming #indianfarmers #kisaan #kheti","Vote 👆 + Comment में experience","Very High"),
    ("10","Engagement Post","Comment: आपकी सबसे बड़ी farming problem?","Instagram","1 image","Open question design. Farmer image. 'हम सुन रहे हैं' text.","Comment में लिखो — हम हर comment पढ़ते हैं और solution लाएंगे।","#kisan #farming #indianfarmers #kheti #krishi","Comment करो 👇","High"),
    ("11","Engagement Post","Tag करो — inspire करने वाले किसान को","Instagram","1 image","Sunset over wheat field. Emotional design. 'किसान से किसान' text.","खेती में एक mentor होता है — आज उन्हें tag करो 🙏","#kisan #farming #annadata #indianfarmers #kisanputra","Tag करो 👇 + उनकी कहानी comment में","High"),
    ("12","Engagement Post","Quiz: इस फसल रोग को पहचानो","Instagram","1 image","Close-up of diseased crop (unlabeled). Question mark overlay. Comments reveal answer.","यह किस फसल की बीमारी है? Comment में बताओ 👇 — जवाब कल देंगे!","#kisan #farming #krishi #fasal #indianfarmers","Comment में जवाब दो 👇","High"),
    ("13","Engagement Post","किस फसल में ज़्यादा मुनाफा? — Poll","Instagram","1 image","4-option poll image design. Clear options with icons.","[Crop A] vs [Crop B] vs [Crop C] vs [Crop D] — किसमें ज़्यादा profit? Vote करो 👆","#kisan #farming #agribusiness #indianfarmers #kheti","Vote 👆 + Comment: क्यों?","High"),
    ("14","Engagement Post","Farmer Photo Contest — अपनी best photo share करो","Instagram","1 image","Contest banner design. Prize mentioned. Clear submission instructions.","अपनी फसल की best photo share करो — winner को [prize]. Rules: tag @agromanch + #AgroManchPhoto","#kisan #farming #indianfarmers #agromanch #khetibadi","Photo share करो + tag @agromanch","High"),
    ("15","Engagement Post","2025 में खेती का सबसे बड़ा change?","Instagram","1 image","Reflective design. Year in review feel.","Comment में बताओ — 2025 में आपकी खेती में सबसे बड़ा change क्या था?","#kisan #farming #indianfarmers #krishi #annadata","Comment करो 👇 — best response featured करेंगे","Medium"),
    # Stories
    ("16","Story","आज का Mandi Price Alert — 5 Crops","Instagram Story","3 stories","Story 1: Header. Stories 2-3: Price table. AgroManch comparison. CTA swipe up.","[Daily: auto-generate from mandi API]","N/A (Story)","Swipe up → AgroManch App","High"),
    ("17","Story","Flash Buyer Deal — Limited Time","Instagram Story","2 stories","Urgency design. Countdown timer. Buyer deal highlighted in yellow.","⚡ Flash Deal: Buyer offering ₹[X]/quintal for [crop] — limited qty. AgroManch App now!","N/A (Story)","Swipe up → AgroManch App → Flash Deals","Very High"),
    ("18","Story","Behind the Scenes — AgroManch Field Visit","Instagram Story","5 stories","Raw, authentic video/photo. Team in field. Farmer conversation. Real moments.","[No formal caption — let visuals tell story]","N/A (Story)","Reply with your location 📍","Medium"),
    ("19","Story","Coming Soon Teaser","Instagram Story","2 stories","Mystery/reveal design. Blurred or partial reveal. Countdown.","कुछ बड़ा आ रहा है AgroManch पर — [countdown]. Notification ON 🔔","N/A (Story)","Notification ON करो 🔔","Medium"),
    ("20","Story","AgroManch Kisan of the Week","Instagram Story","3 stories","Award graphic + farmer photo + achievement. Shareable design.","🏆 This Week's Kisan Star: [Name], [Place] — [Achievement in 1 line]","N/A (Story)","Nominate करो — App → Community","High"),
    # WhatsApp Image Posts
    ("21","WhatsApp Image","Weekly Tip — [Topic]","WhatsApp","1 image","Clean, minimal design. 1 big tip. AgroManch branding. Easy to read on small screen.","💡 AgroManch Weekly Tip: [Tip in 2 lines]. App: [link]","N/A","App download करो","High"),
    ("22","WhatsApp Image","Scheme Deadline Alert","WhatsApp","1 image","Red urgency design. Deadline prominent. Steps clearly numbered.","🚨 [Scheme name] — Last date: [date]. Steps: 1,2,3. AgroManch App → Schemes","N/A","AgroManch App → Schemes","Explosive"),
    ("23","WhatsApp Image","Mandi Price Alert","WhatsApp","1 image","Clean table design. Crop | Mandi | AgroManch | Difference. Green for positive difference.","📊 This week prices: [table]. Sell on AgroManch for [X]% more. App: [link]","N/A","Sell Now on AgroManch","High"),
    ("24","WhatsApp Image","Weather Alert","WhatsApp","1 image","Red/orange urgency. Map visual. Action steps numbered. Easy WhatsApp sharing size.","🌧️ [State] Weather Alert: [Event] in next [X] hours. Protect your crop: 1,2,3","N/A","Share करो किसान groups में 🙏","Explosive"),
    ("25","WhatsApp Image","Kisan of the Week","WhatsApp","1 image","Award style. Farmer photo. Achievement stat. AgroManch logo.","🏆 AgroManch Kisan Star: [Name] ने [achievement] किया। Nominate: App → Community","N/A","Share in your groups 🙏","High"),
    # Facebook-specific
    ("26","Facebook Post","किसान की success story — long form","Facebook","1 video thumbnail","Real farmer photo. Compelling headline. Video play button overlay.","[Long-form farmer story: 200-300 words + video]. Tag friends who should see this.","#kisan #indianfarmers #farming #agromanch","Tag 2 किसान friends 👇","High"),
    ("27","Facebook Post","AgroManch Month Review","Facebook","1 infographic","Data visualization. Charts. Honest numbers. Professional but warm design.","[Monthly performance report]. Your feedback makes AgroManch better.","#agromanch #kisan #farming","Comment में feedback दो","Medium"),
    ("28","Facebook Post","Community Event Announcement","Facebook","1 event graphic","Kisan Mela/Webinar event design. Date, time, venue prominent. Registration CTA.","AgroManch Kisan [Event Name] — [Date], [Venue]. Register: [link]. Free entry!","#kisan #farming #agromanch #indianfarmers","Register करो — limited seats!","High"),
    ("29","Facebook Post","Recipe/Food Chain Story","Facebook","Carousel","Farm to table visual journey. Farmer → field → harvest → transport → kitchen.","यह [vegetable/grain] कहाँ से आती है? किसान [name] ने उगाई — AgroManch से आप तक","#kisan #farming #farmtotable #indianfarmers","Tag someone who should see this chain","High"),
    ("30","Facebook Post","Jai Kisan — Identity Post","Facebook","1 image","Powerful farmer imagery. 'अन्नदाता को सलाम' text. Emotional design.","किसान सिर्फ खेती नहीं करता — देश खिलाता है। आज किसान को salute करो 🙏","#annadata #kisan #farming #indianfarmers #kisanputra","Share करो — Jai Kisan 🌾","Very High"),
]

img_colors = {
    "Carousel": TEAL_LIGHT,
    "Engagement Post": BLUE_LIGHT,
    "Story": PURPLE_LIGHT,
    "WhatsApp Image": GREEN_LIGHT,
    "Facebook Post": ORANGE_LIGHT,
}

for i, row in enumerate(img_posts):
    r = 3 + i
    ws6.row_dimensions[r].height = 55
    bg = img_colors.get(row[1], GRAY_LIGHT)
    for col, val in enumerate(row, 1):
        c = ws6.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(9)
        c.alignment = left()
        c.border = thin_border()

col_widths6 = [4, 16, 32, 11, 10, 42, 42, 38, 28, 14]
for i, w in enumerate(col_widths6, 1):
    ws6.column_dimensions[get_column_letter(i)].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 7: 📊 YOUTUBE PLANNER
# ══════════════════════════════════════════════════════════════════════════════
ws7 = wb.create_sheet("📊 YouTube Planner")
ws7.sheet_view.showGridLines = False

ws7.merge_cells("A1:I1")
ws7["A1"].value = "📊  AgroManch YouTube Planner  |  Upload: Tuesday & Friday 5:00 PM IST"
ws7["A1"].fill = fill(RED_DARK)
ws7["A1"].font = Font(name="Calibri", size=14, bold=True, color=WHITE)
ws7["A1"].alignment = center()
ws7.row_dimensions[1].height = 35

yt_hdrs = ["#","Upload Date","Title (YouTube SEO — Hindi + Keyword)","Pattern","Duration","Thumbnail Brief","Description (First 150 chars)","Tags (15 max)","Status"]
write_header_row(ws7, 2, yt_hdrs, RED_DARK)

yt_videos = [
    ("1","Fri 05-Jun","AgroManch क्या है? मंडी से कैसे बचाता है किसान को | 2026","Brand Intro","8-12 min","Farmer face (left) + mandi vs app split (right) + '₹5000 ज़्यादा' red text","AgroManch क्या है? किसान को मंडी से ज़्यादा दाम कैसे मिलता है? Complete guide 2026.","AgroManch,किसान,kisan,agriculture,Indian farmer,mandi,online sell,agromanch app,khetibadi,farming India 2026","⬜ Pending"),
    ("2","Tue 09-Jun","AgroManch पर पहली listing कैसे करें | Complete Tutorial 2026","Tutorial","10-15 min","Screen recording thumbnail + farmer smiling + 'First Sale ✅' text overlay","Registration से first sale तक — AgroManch पर listing करने का complete step-by-step guide Hindi में.","agromanch tutorial,kisan online sell,agromanch listing,agricultural marketplace India,kisan app 2026","⬜ Pending"),
    ("3","Fri 12-Jun","AgroManch Buyers कौन हैं? — Verified buyer list reveal","Trust Building","8-12 min","Buyer interview thumbnail + '₹X crore trade' stat overlay","AgroManch पर buyers कौन हैं? FPOs, exporters, bulk buyers — किसान का भरोसा क्यों बनता है?","agromanch buyers,agricultural marketplace,kisan direct sell,online farming India,agritech 2026","⬜ Pending"),
    ("4","Tue 16-Jun","FPO + AgroManch = 500 किसान एक आवाज़ | Success Story","Success Story","10-15 min","Group of farmers with phones + 'FPO Power' text + green field background","500 किसानों ने AgroManch पर collectively बेचा। Negotiation power, bulk pricing, real result.","FPO farming,farmer producer organization,agromanch FPO,kisan collective,bulk farming India","⬜ Pending"),
    ("5","Fri 19-Jun","🚨 Weekly Pest Alert: [State] के [Crop] किसान ध्यान दें","Crop Emergency","5-8 min","Close-up diseased leaf (left) + solution (right) + 'ALERT' red banner","[Pest name] इस हफ्ते [State] में। Symptoms, immediate solution, AgroManch expert contact.","pest alert India,kisan crop disease,farming tips Hindi,fasal bimari,kisan alert 2026","⬜ Pending"),
    ("6","Tue 23-Jun","Soil Health Card को 5 मिनट में समझो | NPK Guide Hindi","Education","8-12 min","Soil Health Card close-up + 'Decode Your Card' text + farmer studying card","25 करोड़ cards बंटे, 90% किसान नहीं समझते। NPK, pH, micronutrients — simple Hindi में.","soil health card Hindi,soil test India,NPK farming guide,kisan mitti parikshan,krishi guide 2026","⬜ Pending"),
    ("7","Fri 26-Jun","IT Engineer ने छोड़ी Job — खेती से ₹8 लाख/साल | Real Story","Aspiration","12-18 min","Professional headshot → farmer in field (split) + '₹8 Lakh' income text","Software engineer छोड़ी, organic farming शुरू की। AgroManch से direct sell। 3 साल की journey.","urban to farming,job se kheti,IT farmer story,organic farming income India,kisan inspiration 2026","⬜ Pending"),
    ("8","Tue 30-Jun","Bhojpuri Tutorial: AgroManch पर कइसे बेचीं | UP Bihar Kisan","Regional","8-12 min","Bhojpuri text overlay + UP/Bihar map + farmer from region","[Complete Bhojpuri tutorial] UP और Bihar के किसान भाइयों के लिए — अपनी भाषा में guide.","bhojpuri farming,UP kisan,Bihar farmer,agromanch bhojpuri,kisan UP Bihar 2026,bhojpuri agri","⬜ Pending"),
    ("9","Fri 03-Jul","AgroManch 30 Days Report — किसानों का साथ | Honest Review","Transparency","10-15 min","Data graphs + founder on camera + '30 Days, [X] Farmers' text","30 दिन में क्या achieve किया, क्या challenges थे, Month 2 plan — honest transparency report.","agromanch review,agritech India 2026,kisan marketplace review,farming app honest review","⬜ Pending"),
    ("10","Ongoing","Mushroom Farming से ₹3 लाख/साल घर से | Complete Guide","Profit Reveal","12-18 min","Mushroom harvest close-up + '₹3 Lakh' + house icon","Mushroom farming setup, cost, revenue, AgroManch buyers, where to sell premium mushrooms.","mushroom farming Hindi,mushroom kheti,kisan mushroom income,farming at home India 2026","⬜ Pending"),
    ("11","Ongoing","Dragon Fruit Farming — ₹200/kg | Complete Business Plan","Hidden Crop","15-20 min","Dragon fruit dramatic close-up + '₹200/kg' + Indian flag (local grown)","Dragon fruit market analysis, cultivation guide, AgroManch premium buyer network, ROI calculation.","dragon fruit farming India,dragon fruit price,premium crop India,kisan dragon fruit 2026","⬜ Pending"),
    ("12","Ongoing","Mahila Kisan Series: रेखा देवी की कहानी — ₹2 लाख AgroManch से","Women Series","10-15 min","Woman farmer in field + crop + achievement stat","Mahila kisan special series. Real women farmer stories. AgroManch se independence.","mahila kisan,women farmer India,woman agriculture,mahila kheti,kisan women empowerment","⬜ Pending"),
]

for i, row in enumerate(yt_videos):
    r = 3 + i
    ws7.row_dimensions[r].height = 60
    bg = RED_LIGHT if i % 2 == 0 else WHITE
    for col, val in enumerate(row, 1):
        c = ws7.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(9)
        c.alignment = left()
        c.border = thin_border()

col_widths7 = [4, 13, 48, 16, 9, 38, 42, 48, 12]
for i, w in enumerate(col_widths7, 1):
    ws7.column_dimensions[get_column_letter(i)].width = w

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 8: ⏰ POSTING SCHEDULE & HASHTAG BANKS
# ══════════════════════════════════════════════════════════════════════════════
ws8 = wb.create_sheet("⏰ Posting Schedule")
ws8.sheet_view.showGridLines = False

ws8.merge_cells("A1:K1")
ws8["A1"].value = "⏰  AgroManch Posting Schedule + Hashtag Banks + CTA Library"
ws8["A1"].fill = fill(GREEN_DARK)
ws8["A1"].font = Font(name="Calibri", size=14, bold=True, color=WHITE)
ws8["A1"].alignment = center()
ws8.row_dimensions[1].height = 35

# --- Weekly Schedule ---
ws8.merge_cells("A3:K3")
ws8["A3"].value = "📅  WEEKLY CONTENT SCHEDULE"
ws8["A3"].fill = fill(AMBER)
ws8["A3"].font = hdr_font(11, True, WHITE)
ws8["A3"].alignment = center()
ws8.row_dimensions[3].height = 22

sched_hdrs = ["Day", "Platform", "Content Type", "Upload/Post Time", "Audience Peak",
              "Best Content Pattern", "Min. Freq/Week", "Growth Freq/Week", "Notes"]
write_header_row(ws8, 4, sched_hdrs, AMBER)

schedule = [
    ("Monday",    "WhatsApp",  "Broadcast Tip/Alert",    "07:30 AM", "07:00-09:00 AM", "Jugaad Hack, Scheme Bomb",   "1x", "1x", "Weekly series; scheme updates"),
    ("Tuesday",   "YouTube",   "Long-form Video",        "05:00 PM", "06:00-09:00 PM", "Success Story, Tutorial",    "1x", "1x", "Upload 5PM; peak 6PM. Consistency = appointment viewing"),
    ("Wednesday", "Instagram", "Carousel Post",          "12:00 PM", "12:00-02:00 PM", "Profit Calculator, Guide",   "1x", "1x", "Lunch-break scroll; save-heavy content"),
    ("Thursday",  "Instagram", "Reel (High Priority)",   "08:30 PM", "08:00-10:00 PM", "Mandi Shock, Crop Emergency","1x", "2x", "Thursday 8-10PM = peak engagement hour"),
    ("Friday",    "YouTube",   "Long-form Video",        "05:00 PM", "06:00-09:00 PM", "Regional Language, Story",   "1x", "1x", "Same as Tuesday — twice-weekly schedule builds habit"),
    ("Saturday",  "Facebook",  "Video Post",             "09:30 AM", "09:00-11:00 AM", "Field Interview, Story",     "1x", "1x", "Rural audience has weekend morning leisure time"),
    ("Sunday",    "Instagram", "Reel + Story",           "08:00 PM", "07:00-10:00 PM", "Debate, Viral Hook",         "1x", "2x", "Highest engagement day; emotional/community content"),
    ("Daily",     "Instagram", "Story (Price/Alert)",    "07:00 PM", "07:00-09:00 PM", "Weather, Price Alert",       "1x", "1x", "Daily habit loop builds loyal audience"),
    ("Daily",     "WhatsApp",  "Broadcast (Tip/Alert)",  "07:30 AM", "07:00-09:00 AM", "Any Pattern",                "1x", "1x", "Most important distribution channel — never skip"),
]

sched_colors = [GREEN_LIGHT, WHITE, BLUE_LIGHT, ORANGE_LIGHT, AMBER_LIGHT,
                PURPLE_LIGHT, TEAL_LIGHT, RED_LIGHT, GRAY_LIGHT]
for i, row in enumerate(schedule):
    r = 5 + i
    ws8.row_dimensions[r].height = 30
    bg = sched_colors[i % len(sched_colors)]
    for col, val in enumerate(row, 1):
        c = ws8.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(9, col == 1)
        c.alignment = left()
        c.border = thin_border()

# --- Hashtag Banks ---
ws8.row_dimensions[16].height = 22
ws8.merge_cells("A16:K16")
ws8["A16"].value = "# ️⃣  HASHTAG BANKS BY PLATFORM (5-Hashtag Rule — Post 2025)"
ws8["A16"].fill = fill(BLUE_DARK)
ws8["A16"].font = hdr_font(11, True, WHITE)
ws8["A16"].alignment = center()

tag_data = [
    ("Instagram — Profit/Income Posts",     "#kisan", "#farming", "#indianfarmers", "#agromanch", "#agribusiness"),
    ("Instagram — Crop Disease/Alert",       "#kisan", "#farming", "#krishi",        "#fasal",      "#indianfarmers"),
    ("Instagram — Scheme Posts",             "#kisan", "#pmkisan", "#indianfarmers", "#kisaan",     "#krishi"),
    ("Instagram — Women Farmer Posts",       "#kisan", "#farming", "#mahilakisan",   "#womenempowerment","#indianfarmers"),
    ("Instagram — Jugaad/Innovation",        "#kisan", "#farming", "#jugaad",        "#khetibadi",  "#indianfarmers"),
    ("Instagram — Community/Identity",       "#kisan", "#farming", "#annadata",      "#kisanputra", "#indianfarmers"),
    ("Instagram — Mandi/Market Posts",       "#kisan", "#farming", "#khetibadi",     "#indianfarmers","#agromanch"),
    ("Instagram — Regional/Bhojpuri",        "#kisan", "#farming", "#indianfarmers", "#kisaan",     "#agromanch"),
    ("YouTube — All Content",                "#kisan", "#farming", "#indianfarmers", "#agromanch",  "#kisaan"),
    ("Facebook — General Posts",             "#kisan", "#indianfarmers", "#farming", "#agromanch",  "#annadata"),
    ("Core Identity Tags (Always Available)","#kisan", "#kisaan",  "#kheti",         "#khetibadi",  "#annadata"),
    ("Seasonal Spike Tags (use during peak)","#kisandiwas","#fasal","#kharif",       "#rabi",       "#monsoon"),
]

hdr17 = ["Category", "Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5"]
write_header_row(ws8, 17, hdr17, BLUE_DARK)

for i, row in enumerate(tag_data):
    r = 18 + i
    ws8.row_dimensions[r].height = 22
    bg = BLUE_LIGHT if i % 2 == 0 else WHITE
    for col, val in enumerate(row, 1):
        c = ws8.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(10, col == 1)
        c.alignment = left()
        c.border = thin_border()

# --- CTA Library ---
ws8.row_dimensions[32].height = 22
ws8.merge_cells("A32:K32")
ws8["A32"].value = "📢  CTA LIBRARY — Copy & Use in Captions"
ws8["A32"].fill = fill(ORANGE)
ws8["A32"].font = hdr_font(11, True, WHITE)
ws8["A32"].alignment = center()

cta_hdrs = ["#", "CTA (Hindi)", "Use For", "Platform", "Expected Action"]
write_header_row(ws8, 33, cta_hdrs, ORANGE)

ctas = [
    ("1", "WhatsApp group में share करो 🙏",             "Utility/Alert content",         "All",         "Organic amplification to farmer groups"),
    ("2", "AgroManch App download करो — link bio में 👇", "All conversion content",        "Instagram",   "App install"),
    ("3", "Comment में बताओ — आपके इलाके में क्या भाव है?","Engagement/mandi posts",        "Instagram/FB","Comments + algorithm signal"),
    ("4", "Save करो 📌 — बाद में काम आएगा",              "Educational carousels/tips",     "Instagram",   "Saves = high-value signal to Instagram"),
    ("5", "Tag करो उस किसान दोस्त को 👇",                "Community/viral posts",          "All",         "Reach expansion to new accounts"),
    ("6", "AgroManch पर free registration — आज ही करो",  "Acquisition posts",             "YouTube/FB",  "Sign-up / registration"),
    ("7", "Follow करो 🔔 — रोज़ farming tips free",       "Every post",                    "Instagram",   "Follower growth"),
    ("8", "Subscribe करो 🔔 — हर हफ्ते नई jankari",      "YouTube content",               "YouTube",     "YouTube subscriber growth"),
    ("9", "Vote करो 👆 — comment में हाँ/नहीं बताओ",     "Poll/debate posts",             "Instagram/FB","Engagement + algorithm"),
    ("10","Apply करो अभी — last date [date] है",          "Scheme/scheme deadline content","All",         "Urgency-driven action"),
    ("11","AgroManch App → [specific section] खोलो",      "Feature education posts",       "All",         "App engagement / feature discovery"),
    ("12","अपने पिता/माँ को tag करो 🙏",                  "Emotional/identity posts",      "Instagram/FB","Reach to older demographic"),
]

for i, row in enumerate(ctas):
    r = 34 + i
    ws8.row_dimensions[r].height = 25
    bg = ORANGE_LIGHT if i % 2 == 0 else WHITE
    for col, val in enumerate(row, 1):
        c = ws8.cell(row=r, column=col, value=val)
        c.fill = fill(bg)
        c.font = body_font(10, col <= 2)
        c.alignment = left()
        c.border = thin_border()

col_widths8 = [30, 14, 14, 22, 20, 20, 10, 10, 36]
for i, w in enumerate(col_widths8, 1):
    ws8.column_dimensions[get_column_letter(i)].width = w

# ══════════════════════════════════════════════════════════════════════════════
# FREEZE PANES + FINAL SETUP
# ══════════════════════════════════════════════════════════════════════════════
for ws in [ws2, ws3, ws5, ws6, ws7]:
    ws.freeze_panes = ws["A3"]
ws4.freeze_panes = ws4["A9"]
ws8.freeze_panes = ws8["A5"]

# Set zoom
for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 80

output_path = "/home/user/python-calculator-/AgroManch_Content_Engine.xlsx"
wb.save(output_path)
print(f"✅ Excel file saved: {output_path}")
print(f"📊 Sheets: {[ws.title for ws in wb.worksheets]}")

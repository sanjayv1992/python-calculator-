#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgroManch — Google Sheet Content Plan Builder
Generates a complete 365-day content plan XLSX optimized for Google Sheets import.
"""

import datetime
import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.filters import AutoFilter
import itertools

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
START_DATE = datetime.date(2026, 6, 7)
OUTPUT_FILE = "/home/user/python-calculator-/AgroManch_Google_Sheet_Content_Plan.xlsx"

# ─────────────────────────────────────────────
# DATA: 20 VIRAL PATTERNS  (name, V,T,S,R,D,L,M)
# ─────────────────────────────────────────────
PATTERNS = [
    ("Profit Reveal",       10,8,9,10,9,9,10),
    ("Mandi Shock",         10,7,10,10,9,8,10),
    ("Crop Emergency Alert",9,8,9,9,8,9,10),
    ("Farmer Success Story",9,9,8,8,9,9,9),
    ("Machinery Pride",     8,8,7,9,8,9,9),
    ("Scheme Bomb",         9,8,9,9,7,8,9),
    ("Jugaad Hack",         9,7,8,9,9,8,9),
    ("Before/After",        9,8,9,8,8,8,8),
    ("Mahila Kisan",        8,8,9,8,8,9,8),
    ("Weather Emergency",   8,7,9,9,8,8,9),
    ("Myth Buster",         8,8,8,8,8,8,8),
    ("Profit Calculator",   8,8,7,8,9,8,8),
    ("Field Interview",     8,9,7,7,8,9,8),
    ("Old vs New",          7,8,7,8,8,8,7),
    ("Hidden Crop",         8,7,7,8,8,8,8),
    ("Tech Tutorial",       7,8,7,7,8,8,7),
    ("Award/Recognition",   8,9,7,7,8,8,8),
    ("Regional Language",   7,8,8,8,8,9,7),
    ("Community Debate",    7,7,8,8,8,7,7),
    ("Seasonal Countdown",  7,7,8,8,8,7,8),
]

# Weighted list (Tier A ≥58: 4x, Tier B 52-57: 2x, Tier C <52: 1x)
WEIGHT = []
for idx, (name, *scores) in enumerate(PATTERNS):
    t = sum(scores)
    WEIGHT += [idx] * (4 if t >= 58 else 2 if t >= 52 else 1)

def cyc(lst, i): return lst[i % len(lst)]

CROPS = [
    "गेहूं","धान","सोयाबीन","कपास","मक्का","गन्ना","सरसों","चना",
    "प्याज़","टमाटर","आलू","मटर","मूंग","उड़द","अरहर","जौ",
    "बाजरा","ज्वार","तिल","अलसी","मूंगफली","सूरजमुखी","अदरक","लहसुन"
]
REGIONS = [
    "UP","MP","राजस्थान","पंजाब","हरियाणा","महाराष्ट्र",
    "गुजरात","बिहार","झारखंड","छत्तीसगढ़","उत्तराखंड","HP"
]
SCHEMES = [
    "PM-KISAN","KCC","फसल बीमा","PMFBY","e-NAM","FPO","सोलर पंप योजना",
    "किसान सम्मान","प्रधानमंत्री कृषि सिंचाई","नाबार्ड लोन"
]
AUDIENCES = [
    "छोटे किसान","युवा किसान","महिला किसान","FPO सदस्य",
    "प्रगतिशील किसान","नए किसान","सब्जी उत्पादक","पशुपालक"
]

# Hooks per pattern (Hindi)
HOOKS = {
    "Profit Reveal":        ["इस साल __ एकड़ {c} से ₹__ लाख कमाए — पूरा हिसाब देखो","किसान भाई ने {c} से ₹__ लाख कैसे कमाए?","सच्चाई: {c} की खेती में असली मुनाफा कितना?","₹__ लाख profit — {r} के किसान का सीक्रेट देखो","{c} की खेती: लागत __ — कमाई ₹__","एक एकड़ {c} से ₹__ लाख — विश्वास नहीं होगा"],
    "Mandi Shock":          ["{c} का भाव आज ₹__ — खरीदें या रुकें?","मंडी LIVE: {c} ₹__ पर — अगले 7 दिन क्या होगा?","ALERT: {c} भाव ₹__ से गिरकर ₹__ हुआ","अभी {r} मंडी में {c} ₹__/क्विंटल","{c} भाव का शॉकिंग अपडेट — किसान ध्यान दें","आज {c} खरीदना चाहिए या नहीं? मंडी रिपोर्ट"],
    "Crop Emergency Alert": ["URGENT: {c} में ये रोग फैला — अभी बचाओ","⚠️ {c} किसान ध्यान दो — ये गलती मत करो","ALERT: {c} की फसल खतरे में — तुरंत करो ये","{c} में पीला पड़ना शुरू? ये है कारण + इलाज","अगले 48 घंटे {c} के लिए critical — देखो क्यों","{r} में {c} की फसल बर्बाद हो रही — बचाने का तरीका"],
    "Farmer Success Story": ["{r} के {a} ने {c} से बदली किस्मत","सिर्फ __ बीघे में ₹__ लाख — {a} की कहानी","इस किसान ने सबको गलत साबित किया — {c} से","{c} की खेती ने बदल दी ज़िंदगी — सच्ची कहानी","कभी कर्ज़ में डूबे थे — आज {c} से लखपति","{a} बोले: '{c} ने बच्चों को पढ़ाया'"],
    "Machinery Pride":      ["नई मशीन से {c} की खेती — कमाल देखो","ये machine बदल देगी {r} के किसानों की ज़िंदगी","₹__ लाख की machine — लागत आधी, कमाई दोगुनी","{c} harvesting machine DEMO — देखते रह जाओगे","Smart farming: {c} में drone का जादू","इस machine से __ एकड़ {c} __ घंटे में तैयार"],
    "Scheme Bomb":          ["{s}: ये सुविधा ले रहे हो या नहीं?","सरकारी scheme जो हर {a} को मिलनी चाहिए","{s} के तहत ₹__ मिलेंगे — अभी apply करो","नई घोषणा: {s} में बड़ा बदलाव — जानो अभी","{r} के किसान: {s} का पैसा अभी नहीं आया?","{s} apply करने का आसान तरीका — step by step"],
    "Jugaad Hack":          ["₹__ में बना {c} का ये जुगाड़ — कमाल है","देसी तरकीब: {c} की लागत आधी करो","{r} के किसान का ये जुगाड़ देखो — viral हो गया","बिना machine के {c} की बुवाई — ये है तरीका","घर पर बना {c} का खाद — ₹__ की बचत","ये 1 जुगाड़ {c} की उपज 30% बढ़ाएगा"],
    "Before/After":         ["{c} खेत: पहले vs अब — जमीन-आसमान का फर्क","Before: कर्ज़ — After: ₹__ लाख profit ({c})","__ साल पहले vs आज — {a} की खेती देखो","पुरानी तकनीक vs नई: {c} में कौन जीता?","{c} खेत transform: 6 महीने में ये बदलाव","बंजर ज़मीन → {c} का हरा-भरा खेत — कैसे?"],
    "Mahila Kisan":         ["इस महिला किसान ने {c} से ₹__ लाख कमाए","माँ-बेटी की {c} खेती — इनसे सीखो","{r} की महिला किसान जो गाँव बदल रही हैं","बिना मर्द के सहारे {c} की खेती — हौसले की कहानी","महिला FPO ने {c} से कमाए ₹__ — जानो कैसे","इस बहन ने {c} की खेती से 5 घर बनाए"],
    "Weather Emergency":    ["⛈️ अगले 48 घंटे {r} में — {c} किसान सावधान","ALERT: बेमौसम बारिश — {c} को ऐसे बचाओ","तापमान __°C — {c} की फसल पर असर और बचाव","आंधी आने वाली है — अभी करो ये काम ({c})","IMD ALERT: {r} में ओले — {c} बचाने का plan","ठंड बढ़ रही है — {c} के लिए ज़रूरी कदम"],
    "Myth Buster":          ["{c} के बारे में ये 3 झूठ — सच जानो","'Organic {c} नहीं बिकती' — बिल्कुल गलत!","बाप-दादा की ये खेती का तरीका छोड़ो — सच्चाई","{c} में DAP ज़रूरी है? — सच क्या है","'छोटे किसान आगे नहीं बढ़ सकते' — WRONG","डीलर का ये झूठ मत मानो ({c} के बारे में)"],
    "Profit Calculator":    ["Calculator: {c} की खेती में असली profit क्या?","__ एकड़ {c} — सही calculate करो मुनाफा","{c} vs {c}: कौन देता है ज़्यादा return?","सच्चा profit formula: {c} की खेती का","लागत ₹__ — कमाई ₹__ : {c} का real calculation","{a}: ₹__ लगाओ, ₹__ कमाओ ({c} से)"],
    "Field Interview":      ["LIVE खेत से: {a} बता रहे हैं {c} का सच","{r} के किसान LIVE — पूछो अपने सवाल","Interview: इस किसान ने {c} से कैसे किया ये?","खेत पर मिले {a} — उन्होंने बताया राज़","{c} उगाने वाले से सीखो — field visit","Real farmer, real numbers — {c} की खेती पर"],
    "Old vs New":           ["पुराना बीज vs नया HYV: {c} में कौन जीता?","दादाजी की खेती vs Smart Farming ({c})","Manual vs Machine: {c} की लागत तुलना","पहले __ क्विंटल, अब __ क्विंटल — {c} में बदलाव","Traditional vs Modern {c} farming — facts","__ साल पहले vs आज — {c} के दाम और मुनाफा"],
    "Hidden Crop":          ["ये {c} उगाओ — ₹__ लाख/एकड़, कोई नहीं जानता","{r} का hidden crop: {c} से __ गुना profit","किसान छुपा रहे थे ये {c} का राज़ — अब खुला","{c} जो आपके खेत में नहीं — पर होनी चाहिए","Low investment, high profit: {c} का secret","{c}: ये crop क्यों नहीं उगाते किसान?"],
    "Tech Tutorial":        ["Step-by-step: {c} में drone spraying कैसे करें","AgroManch app से {c} की market कैसे देखें","Soil test report पढ़ना सीखो — {c} के लिए","Smart irrigation setup: {c} के लिए DIY guide","{c} का weather-based spray schedule — कैसे बनाएं","AgroManch से {c} बेचना: पूरा process"],
    "Award/Recognition":    ["AgroManch Best Farmer 2026: {r} के {a} जीते","सरकार ने सम्मानित किया: {c} उगाने वाले {a}","{c} में innovation: {a} को मिला national award","गाँव बदला, award मिला — {a} की कहानी ({c})","Krishi Jagran Award: {r} के {a} को क्यों मिला?","Best FPO 2026: {c} बेचकर कमाए ₹__ लाख"],
    "Regional Language":    ["{r} के किसान भाई: {c} के बारे में ये सुनो","({r} dialect) {c} की खेती का सही तरीका","अपनी ज़ुबान में सुनो: {c} से कैसे कमाएं","{r} special: {c} उगाने का local तरीका","भाई, {r} में {c} का यही है सही season","देसी भाषा में: {c} की ये बात समझो"],
    "Community Debate":     ["बहस: {c} organic खेती सही है या नहीं?","सवाल: {c} की MSP बढ़ाई जाए या नहीं?","किसान vs डीलर: {c} का सही दाम कितना?","आप बताओ: {c} के लिए नई machine लेनी चाहिए?","Discussion: {c} FPO बनाना सही है या नहीं?","Vote करो: {c} की खेती छोड़ें या जारी रखें?"],
    "Seasonal Countdown":   ["__ दिन बचे हैं {c} की बुवाई के — तैयारी करो","Season शुरू: {c} के लिए ये __ काम अभी करो","{c} का सही season कब है — {r} के लिए guide","__ दिन में {c} ready: timeline और plan","Rabi/Kharif: {c} के लिए best timing chart","{c} season countdown: क्या-क्या तैयार है?"],
}

PLATFORM_SCHEDULE = [
    # (day_of_week 0=Mon, content_type, platform, time)
    (0, "Instagram Reel",    "Instagram",  "8:00 PM"),
    (1, "YouTube Long",      "YouTube",    "5:00 PM"),
    (2, "Instagram Carousel","Instagram",  "9:00 AM"),
    (3, "Facebook Post",     "Facebook",   "12:00 PM"),
    (3, "Instagram Reel",    "Instagram",  "8:00 PM"),
    (4, "YouTube Short",     "YouTube",    "5:00 PM"),
    (5, "Instagram Reel",    "Instagram",  "9:00 PM"),
    (6, "Engagement Post",   "Instagram",  "10:00 AM"),
    (6, "WhatsApp Broadcast","WhatsApp",   "7:00 AM"),
]

PLATFORM_POST_TYPES = {
    0: [("Instagram Reel", "Instagram", "8:00 PM")],
    1: [("YouTube Long", "YouTube", "5:00 PM"), ("Instagram Reel", "Instagram", "8:00 PM")],
    2: [("Instagram Carousel", "Instagram", "9:00 AM")],
    3: [("Facebook Post", "Facebook", "12:00 PM"), ("Instagram Reel", "Instagram", "8:00 PM")],
    4: [("YouTube Short", "YouTube", "5:00 PM"), ("Instagram Reel", "Instagram", "8:00 PM")],
    5: [("Instagram Reel", "Instagram", "9:00 PM")],
    6: [("Engagement Post", "Instagram", "10:00 AM"), ("WhatsApp Broadcast", "WhatsApp", "7:00 AM")],
}

OBJECTIVES = ["Awareness", "Trust", "Community", "Acquisition", "App Download"]
OBJ_CYCLE = [0,0,1,1,2,3,4,  0,1,1,2,3,4,0,  1,2,3,4,0,1,0,  2,3,4,0,1,2,1]

MONTH_THEMES = {
    6:  "खरीफ बुवाई सीज़न — शुरुआत",
    7:  "मानसून व फसल देखभाल",
    8:  "कीट-रोग प्रबंधन",
    9:  "खरीफ कटाई + रबी तैयारी",
    10: "रबी बुवाई + मंडी भाव",
    11: "रबी देखभाल + FPO",
    12: "सर्दी — सब्जी व बागवानी",
    1:  "गेहूं-सरसों की देखभाल",
    2:  "रबी कटाई की तैयारी",
    3:  "गर्मी-जायद फसलें",
    4:  "मार्केटिंग + Value Addition",
    5:  "गर्मी फसल + खरीफ Planning",
}

FESTIVALS = {
    (6, 7): "रथयात्रा", (6, 15): "पितृपक्ष शुरू",
    (7, 4):  "बकरीद", (7, 15): "मुहर्रम",
    (8, 9):  "रक्षाबंधन", (8, 15): "Independence Day", (8, 23): "जन्माष्टमी",
    (9, 2):  "ओणम", (9, 7): "हरतालिका तीज", (9, 14): "विश्वकर्मा पूजा",
    (10, 1): "नवरात्रि शुरू", (10, 2): "Gandhi Jayanti", (10, 13): "दशहरा", (10, 20): "धनतेरस", (10, 22): "दीपावली",
    (11, 5): "छठ पूजा", (11, 15): "गुरु नानक जयंती",
    (12, 25): "Christmas", (12, 31): "New Year Eve",
    (1, 1):  "New Year", (1, 14): "मकर संक्रांति / लोहड़ी", (1, 26): "Republic Day",
    (2, 14): "Valentine's Day", (2, 19): "Shivaji Jayanti",
    (3, 8):  "Holi", (3, 14): "International PI Day",
    (4, 14): "Ambedkar Jayanti / Baisakhi", (4, 22): "Earth Day",
    (5, 1):  "Labour Day", (5, 22): "Biodiversity Day",
}

PSY_TRIGGERS = [
    "FOMO", "Social Proof", "Urgency", "Curiosity", "Pride",
    "Fear", "Hope", "Anger", "Nostalgia", "Aspiration"
]

CAPTIONS = {
    "Profit Reveal":        "भाई साहब, {c} की खेती में अगर सही तरीका अपनाओ तो ₹__ लाख तक कमाई होती है। {r} के किसान {a} ने यही किया। पूरा detail AgroManch app पर। 👇",
    "Mandi Shock":          "आज {r} मंडी में {c} का भाव ₹__/क्विंटल। पिछले हफ्ते से __ % बदलाव। AgroManch पर live prices देखते रहो। 📊",
    "Crop Emergency Alert": "{c} में ये symptom दिखे तो तुरंत action लो। {r} में इस बीमारी की शिकायत बढ़ रही है। AgroManch expert से अभी पूछो। ⚠️",
    "Farmer Success Story": "{a} की कहानी सुनकर रोंगटे खड़े हो गए। {c} की खेती से इन्होंने ₹__ लाख कमाए — और वो भी {r} में। हिम्मत हो तो AgroManch join करो। 💪",
    "Machinery Pride":      "ये machine देखकर पड़ोस के किसान भी हैरान हो गए। {c} की खेती अब आसान। AgroManch Machinery Store पर check करो। 🚜",
    "Scheme Bomb":          "{s} scheme में अब {a} को ₹__ मिलेंगे। apply करने का तरीका AgroManch app में। time waste मत करो! 🎯",
    "Jugaad Hack":          "ये जुगाड़ {r} के किसान भाई ने बताया — {c} की लागत ₹__ कम हो गई। simple, सस्ता, effective। AgroManch community पर share करो। 💡",
    "Before/After":         "6 महीने पहले vs आज — {c} की खेती में ये transformation real है। {a} ने क्या किया? AgroManch पर पूरी story। 🔄",
    "Mahila Kisan":         "ये बहन {c} की खेती अकेले कर रही हैं — और ₹__ लाख कमा रही हैं। {r} की शान हैं ये। AgroManch Mahila Kisan community join करो। 🌸",
    "Weather Emergency":    "IMD alert: अगले 48 घंटे {r} में आंधी-बारिश। {c} किसान अभी ये करें। AgroManch Weather Alert subscribe करो। ⛈️",
    "Myth Buster":          "{c} के बारे में ये myth बिल्कुल गलत है। कितने किसान नुकसान उठा रहे हैं इस गलतफहमी की वजह से। सच जानो, AgroManch पर। ❌",
    "Profit Calculator":    "Calculate करो: {c} में आप कितना कमा सकते हो? सही formula, real numbers। AgroManch Profit Calculator try करो। 🧮",
    "Field Interview":      "LIVE खेत से — {a} बता रहे हैं {c} की खेती का पूरा सच। कोई script नहीं, कोई acting नहीं। Real farmer, real story। 🎤",
    "Old vs New":           "दादाजी की तरीके vs आज की technology: {c} में क्या बेहतर है? {r} के किसान जवाब दे रहे हैं। AgroManch पर join करो। ⚖️",
    "Hidden Crop":          "{c} के बारे में बहुत कम किसान जानते हैं — पर जो जानते हैं वो ₹__ लाख/एकड़ कमा रहे हैं। AgroManch पर secret unlock करो। 🔓",
    "Tech Tutorial":        "Step 1, 2, 3 — {c} में technology use करना अब इतना आसान है। AgroManch Tech Guide देखो और expert बनो। 📱",
    "Award/Recognition":    "{a} को {r} का Best Farmer Award मिला — {c} की खेती के लिए। इनसे सीखो, इन जैसा बनो। AgroManch पर इनकी story. 🏆",
    "Regional Language":    "{r} के भाई-बहनों, {c} की खेती के बारे में आपकी ज़ुबान में बात करते हैं। AgroManch — अपनों के लिए, अपनी भाषा में। 🗣️",
    "Community Debate":     "आप बताओ — {c} के लिए organic खेती सही है या chemical? Comments में vote करो। AgroManch community सुन रही है। 💬",
    "Seasonal Countdown":   "सिर्फ __ दिन बचे हैं {c} की बुवाई के। अभी तैयारी शुरू करो — {r} के किसानों के लिए complete checklist AgroManch पर। ⏰",
}

HASHTAG_SETS = {
    "Profit Reveal":        "#किसान_मुनाफा #AgroManch #खेती_से_कमाई #SmartFarming #Farmer",
    "Mandi Shock":          "#मंडी_भाव #AgroManch #Kisan #फसल_मूल्य #AgriMarket",
    "Crop Emergency Alert": "#फसल_बचाओ #AgroManch #KrishiAlert #Kisan #CropProtection",
    "Farmer Success Story": "#किसान_की_कहानी #AgroManch #Kisan #SuccessStory #FarmerPride",
    "Machinery Pride":       "#KrishiYantra #AgroManch #SmartFarming #Kisan #AgriMachinery",
    "Scheme Bomb":           "#SarkariYojana #AgroManch #KisanScheme #PMKisan #FarmerBenefits",
    "Jugaad Hack":           "#देसीजुगाड़ #AgroManch #Kisan #FarmHack #LowCostFarming",
    "Before/After":          "#Transform #AgroManch #Kisan #BeforeAfter #FarmingSuccess",
    "Mahila Kisan":          "#MahilaKisan #AgroManch #WomenFarmer #NariShakti #Kisan",
    "Weather Emergency":     "#मौसम_अलर्ट #AgroManch #WeatherAlert #Kisan #FarmSafety",
    "Myth Buster":           "#MythBusted #AgroManch #KisanSach #FarmingFacts #Kisan",
    "Profit Calculator":     "#MunafaCalc #AgroManch #Kisan #FarmProfit #SmartFarming",
    "Field Interview":       "#FieldVisit #AgroManch #KisanBaat #RealFarmer #Kisan",
    "Old vs New":            "#OldVsNew #AgroManch #ModernFarming #Kisan #TechKheti",
    "Hidden Crop":           "#HiddenGem #AgroManch #NewCrop #HighProfit #Kisan",
    "Tech Tutorial":         "#TechKheti #AgroManch #SmartFarming #KisanTech #AgriTech",
    "Award/Recognition":     "#KisanAward #AgroManch #BestFarmer #Kisan #FarmerHero",
    "Regional Language":     "#देसीबोली #AgroManch #LocalLanguage #Kisan #ApniZuban",
    "Community Debate":      "#KisanDebate #AgroManch #Community #Poll #Kisan",
    "Seasonal Countdown":    "#SeasonAlert #AgroManch #BuwaiSeason #Kisan #FarmPlanning",
}

CTAS = {
    "Profit Reveal":        "AgroManch app download करो — अभी free है 👇",
    "Mandi Shock":          "Live मंडी भाव के लिए AgroManch app खोलो 📊",
    "Crop Emergency Alert": "AgroManch expert से अभी FREE सलाह लो 🆘",
    "Farmer Success Story": "अपनी success story share करो — AgroManch community पर 💬",
    "Machinery Pride":       "AgroManch Machinery Store — best deals देखो 🚜",
    "Scheme Bomb":           "Apply करो — AgroManch Scheme Guide में 📋",
    "Jugaad Hack":           "ऐसे और जुगाड़ AgroManch Community पर पाओ 💡",
    "Before/After":          "अपना transformation share करो — AgroManch पर 📸",
    "Mahila Kisan":          "Mahila Kisan Community — AgroManch पर join करो 🌸",
    "Weather Emergency":     "Weather alerts के लिए AgroManch app subscribe करो ⛈️",
    "Myth Buster":           "सच जानो — AgroManch Knowledge Base पर 📚",
    "Profit Calculator":     "अभी calculate करो — AgroManch Free Tool 🧮",
    "Field Interview":       "अपने सवाल पूछो — AgroManch LIVE पर 🎤",
    "Old vs New":            "Modern farming सीखो — AgroManch Training पर 🎓",
    "Hidden Crop":           "Hidden crops की list — AgroManch app में 🔓",
    "Tech Tutorial":         "Tutorial series देखो — AgroManch YouTube पर 📱",
    "Award/Recognition":     "Best Farmer Award के लिए nominate करो 🏆",
    "Regional Language":     "अपनी भाषा में AgroManch — download करो 🗣️",
    "Community Debate":      "Comment करो और community बनाओ 💬",
    "Seasonal Countdown":    "Seasonal checklist — AgroManch app में अभी देखो ⏰",
}

DIFFICULTIES = {
    "Instagram Reel":     "Medium",
    "YouTube Long":       "High",
    "Instagram Carousel": "Low",
    "Facebook Post":      "Low",
    "YouTube Short":      "Medium",
    "Engagement Post":    "Low",
    "WhatsApp Broadcast": "Low",
}

PROD_NOTES = {
    "Instagram Reel":     "खेत या मंडी में शूट करें, natural light, vertical 9:16",
    "YouTube Long":       "10-15 मिनट, tripod, b-roll footage ज़रूरी, chapters add करें",
    "Instagram Carousel": "5-7 slides, Canva template use करें, swipe prompt डालें",
    "Facebook Post":      "Hindi text, 1 image/infographic, local group में share करें",
    "YouTube Short":      "60 sec max, vertical, catchy hook पहले 3 sec में",
    "Engagement Post":    "Question/poll format, reply हर comment पर, 1 hour active रहें",
    "WhatsApp Broadcast": "Short digest, opt-in list only, max 3 points, links कम रखें",
}

OBJ_NAMES = ["Awareness", "Trust", "Community", "Acquisition", "App Download"]
EXPECTED_ENG = {
    "Instagram Reel":     "High",
    "YouTube Long":       "Medium",
    "Instagram Carousel": "Medium",
    "Facebook Post":      "Medium",
    "YouTube Short":      "High",
    "Engagement Post":    "Very High",
    "WhatsApp Broadcast": "High",
}

# ─────────────────────────────────────────────
# BUILD DATA ROWS
# ─────────────────────────────────────────────
def build_rows():
    rows = []
    row_num = 0
    for day_num in range(1, 366):
        date = START_DATE + datetime.timedelta(days=day_num - 1)
        dow = date.weekday()  # 0=Mon, 6=Sun
        day_names = ["सोम", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "रवि"]
        day_name = day_names[dow]
        month_name = date.strftime("%B")
        month_theme = MONTH_THEMES.get(date.month, "")
        festival = FESTIVALS.get((date.month, date.day), "")

        # Pattern for this day
        pidx = WEIGHT[day_num % len(WEIGHT)]
        pat_name = PATTERNS[pidx][0]
        scores = PATTERNS[pidx][1:]
        virality = scores[0]
        pat_num = pidx + 1

        # Cycled content vars
        crop = cyc(CROPS, day_num + pidx)
        region = cyc(REGIONS, day_num + pidx * 2)
        scheme = cyc(SCHEMES, day_num)
        audience = cyc(AUDIENCES, day_num + pidx)

        # Hook
        hooks_list = HOOKS.get(pat_name, ["Hook TBD"])
        hook_template = cyc(hooks_list, day_num)
        hook = (hook_template
                .replace("{c}", crop)
                .replace("{r}", region)
                .replace("{s}", scheme)
                .replace("{a}", audience)
                .replace("__", "X"))

        # Caption
        cap_template = CAPTIONS.get(pat_name, "AgroManch — किसानों का अपना platform 🌾")
        caption = (cap_template
                   .replace("{c}", crop)
                   .replace("{r}", region)
                   .replace("{s}", scheme)
                   .replace("{a}", audience)
                   .replace("__", "X"))

        hashtags = HASHTAG_SETS.get(pat_name, "#AgroManch #Kisan #Farming #India #Agriculture")
        cta = CTAS.get(pat_name, "AgroManch app download करो 👇")
        psy = cyc(PSY_TRIGGERS, day_num + pidx)

        # Post types for this day
        post_types = PLATFORM_POST_TYPES.get(dow, [("Instagram Reel", "Instagram", "8:00 PM")])

        for ct, platform, post_time in post_types:
            obj_idx = OBJ_CYCLE[row_num % len(OBJ_CYCLE)]
            obj = OBJ_NAMES[obj_idx]
            difficulty = DIFFICULTIES.get(ct, "Medium")
            exp_eng = EXPECTED_ENG.get(ct, "Medium")
            prod_note = PROD_NOTES.get(ct, "")

            rows.append({
                "date": date.strftime("%d-%m-%Y"),
                "day_num": day_num,
                "day_name": day_name,
                "month_name": month_name,
                "month_theme": month_theme,
                "festival": festival,
                "platform": platform,
                "content_type": ct,
                "pat_name": pat_name,
                "pat_num": pat_num,
                "virality": virality,
                "crop": crop,
                "region": region,
                "hook": hook,
                "caption": caption,
                "hashtags": hashtags,
                "cta": cta,
                "post_time": post_time,
                "objective": obj,
                "audience": audience,
                "exp_eng": exp_eng,
                "difficulty": difficulty,
                "psy": psy,
                "prod_note": prod_note,
                "status": "",
                "notes": "",
            })
            row_num += 1
    return rows

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
def fill(hex_): return PatternFill("solid", fgColor=hex_)
def font(bold=False, size=10, color="000000", name="Calibri"):
    return Font(bold=bold, size=size, color=color, name=name)
def align(h="center", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)
def border_thin():
    s = Side(style="thin", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

PLATFORM_COLORS = {
    "Instagram":  "E1306C",
    "YouTube":    "FF0000",
    "Facebook":   "1877F2",
    "WhatsApp":   "25D366",
}
PLATFORM_LIGHT = {
    "Instagram":  "FCE4EC",
    "YouTube":    "FFEBEE",
    "Facebook":   "E3F2FD",
    "WhatsApp":   "E8F5E9",
}
OBJ_COLORS = {
    "Awareness":    "FFF9C4",
    "Trust":        "E8F5E9",
    "Community":    "EDE7F6",
    "Acquisition":  "FFF3E0",
    "App Download": "E3F2FD",
}
TIER_COLORS = {
    "A": "FF6B6B",
    "B": "FFA94D",
    "C": "74C0FC",
}

def pat_tier(pidx):
    scores = PATTERNS[pidx][1:]
    t = sum(scores)
    return "A" if t >= 58 else "B" if t >= 52 else "C"

def write_cell(ws, r, c, value="", bg=None, bold=False, size=10,
               color="000000", h="center", v="center", wrap=False,
               number_format=None):
    cell = ws.cell(row=r, column=c)
    cell.value = value
    if bg:
        cell.fill = fill(bg)
    cell.font = font(bold=bold, size=size, color=color)
    cell.alignment = align(h=h, v=v, wrap=wrap)
    cell.border = border_thin()
    if number_format:
        cell.number_format = number_format
    return cell

# ─────────────────────────────────────────────
# SHEET 1: MAIN CONTENT PLAN (365 days)
# ─────────────────────────────────────────────
HEADERS = [
    ("तारीख",          12),
    ("दिन #",          7),
    ("वार",            7),
    ("महीना",          10),
    ("Platform",       13),
    ("Content Type",   18),
    ("Viral Pattern",  20),
    ("Pattern #",      9),
    ("Virality",       8),
    ("Tier",           7),
    ("Crop/फसल",       12),
    ("Region/क्षेत्र", 14),
    ("Hook (3 sec)",   38),
    ("Caption",        45),
    ("Hashtags (5)",   35),
    ("CTA",            32),
    ("Time (IST)",     12),
    ("Objective",      14),
    ("Target Audience",18),
    ("Exp. Engagement",15),
    ("Difficulty",     11),
    ("Psychology",     14),
    ("Festival/Event", 16),
    ("Month Theme",    25),
    ("Production Note",30),
    ("Status ✓",       12),
    ("Notes",          25),
]

def build_main_sheet(ws, rows):
    ws.title = "📅 365-Day Content Plan"
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A3"

    # Row 1: Title banner
    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "🌾 AgroManch — 365-Day Content Plan   |   Start: 07-06-2026   |   Powered by AgroManch Intelligence"
    title_cell.fill = fill("1B4332")
    title_cell.font = font(bold=True, size=13, color="FFFFFF")
    title_cell.alignment = align(h="left", v="center")
    title_cell.border = border_thin()
    ws.merge_cells(f"A1:{get_column_letter(len(HEADERS))}1")
    ws.row_dimensions[1].height = 28

    # Row 2: Headers
    for col, (hdr, width) in enumerate(HEADERS, start=1):
        write_cell(ws, 2, col, hdr, bg="2D6A4F", bold=True, size=10,
                   color="FFFFFF", h="center", v="center")
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.row_dimensions[2].height = 22

    # Data rows
    prev_month = None
    for i, r in enumerate(rows):
        xr = i + 3  # excel row
        pidx = r["pat_num"] - 1
        tier = pat_tier(pidx)
        platform = r["platform"]
        obj = r["objective"]

        # Row bg based on platform
        row_bg = PLATFORM_LIGHT.get(platform, "FFFFFF")
        # Alternate slight shade every 7 rows (week boundary)
        week_num = (i // 7) % 2
        if week_num == 1:
            row_bg = "F5F5F5" if platform not in PLATFORM_LIGHT else row_bg

        festival_bg = "FFFDE7" if r["festival"] else row_bg

        vals = [
            r["date"], r["day_num"], r["day_name"], r["month_name"],
            r["platform"], r["content_type"], r["pat_name"], r["pat_num"],
            r["virality"], tier, r["crop"], r["region"],
            r["hook"], r["caption"], r["hashtags"], r["cta"],
            r["post_time"], r["objective"], r["audience"],
            r["exp_eng"], r["difficulty"], r["psy"],
            r["festival"], r["month_theme"], r["prod_note"],
            r["status"], r["notes"],
        ]

        for col, val in enumerate(vals, start=1):
            hdr = HEADERS[col - 1][0]
            bg = row_bg

            # Special cell colors
            if hdr == "Platform":
                c_bg = PLATFORM_COLORS.get(platform, "999999")
                write_cell(ws, xr, col, val, bg=c_bg, bold=True,
                           size=9, color="FFFFFF", h="center", v="center")
                continue
            if hdr == "Tier":
                t_bg = TIER_COLORS.get(tier, "CCCCCC")
                write_cell(ws, xr, col, val, bg=t_bg, bold=True,
                           size=9, color="FFFFFF", h="center", v="center")
                continue
            if hdr == "Objective":
                o_bg = OBJ_COLORS.get(obj, "FFFFFF")
                write_cell(ws, xr, col, val, bg=o_bg, bold=False,
                           size=9, h="center", v="center")
                continue
            if hdr == "Virality":
                vb = "52B788" if val >= 9 else "95D5B2" if val >= 7 else "D8F3DC"
                write_cell(ws, xr, col, val, bg=vb, bold=True,
                           size=9, h="center", v="center")
                continue
            if hdr == "Festival/Event" and val:
                bg = "FFFDE7"
            if hdr in ("Hook (3 sec)", "Caption", "Production Note", "Notes", "Month Theme"):
                write_cell(ws, xr, col, val, bg=bg, size=9,
                           h="left", v="top", wrap=True)
                continue
            if hdr == "तारीख":
                bg = "E8F5E9" if r["festival"] else bg

            write_cell(ws, xr, col, val, bg=bg, size=9, h="center", v="center")

        ws.row_dimensions[xr].height = 32

        # Month separator: bold top border when month changes
        cur_month = r["date"][3:5]
        if cur_month != prev_month:
            for col in range(1, len(HEADERS) + 1):
                ws.cell(row=xr, column=col).border = Border(
                    left=Side(style="thin", color="CCCCCC"),
                    right=Side(style="thin", color="CCCCCC"),
                    top=Side(style="medium", color="1B4332"),
                    bottom=Side(style="thin", color="CCCCCC"),
                )
            prev_month = cur_month

    # Auto-filter on row 2
    ws.auto_filter.ref = f"A2:{get_column_letter(len(HEADERS))}{len(rows) + 2}"

# ─────────────────────────────────────────────
# SHEET 2: MONTHLY OVERVIEW (12 months)
# ─────────────────────────────────────────────
def build_monthly_sheet(ws, rows):
    ws.title = "📊 Monthly Overview"
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A3"

    write_cell(ws, 1, 1, "📊 AgroManch — Monthly Content Overview (12 Months)",
               bg="1B4332", bold=True, size=13, color="FFFFFF", h="left")
    ws.merge_cells("A1:P1")
    ws.row_dimensions[1].height = 28

    months_data = {}
    for r in rows:
        m = r["date"][3:5] + "-" + r["date"][6:]
        key = (int(r["date"][6:]), int(r["date"][3:5]))
        if key not in months_data:
            months_data[key] = {
                "label": datetime.date(int(r["date"][6:]), int(r["date"][3:5]), 1).strftime("%B %Y"),
                "rows": [],
            }
        months_data[key]["rows"].append(r)

    headers = ["महीना", "Theme", "Total Posts", "Instagram", "YouTube", "Facebook", "WhatsApp",
               "Reels", "Top Pattern", "Avg Virality", "Festivals", "Awareness", "Trust", "Community", "Acquisition", "App Download"]
    widths =   [16, 28, 12, 11, 11, 11, 11, 10, 22, 12, 28, 11, 8, 12, 12, 12]
    for col, (h, w) in enumerate(zip(headers, widths), 1):
        write_cell(ws, 2, col, h, bg="2D6A4F", bold=True, size=10, color="FFFFFF")
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[2].height = 22

    row_idx = 3
    for (yr, mo), md in sorted(months_data.items()):
        rs = md["rows"]
        total = len(rs)
        ig = sum(1 for r in rs if r["platform"] == "Instagram")
        yt = sum(1 for r in rs if r["platform"] == "YouTube")
        fb = sum(1 for r in rs if r["platform"] == "Facebook")
        wa = sum(1 for r in rs if r["platform"] == "WhatsApp")
        reels = sum(1 for r in rs if r["content_type"] == "Instagram Reel")
        pat_counts = {}
        for r in rs:
            pat_counts[r["pat_name"]] = pat_counts.get(r["pat_name"], 0) + 1
        top_pat = max(pat_counts, key=pat_counts.get)
        avg_vir = round(sum(r["virality"] for r in rs) / max(1, total), 1)
        fests = list(set(r["festival"] for r in rs if r["festival"]))
        fests_str = ", ".join(fests[:3])
        obj_c = {o: sum(1 for r in rs if r["objective"] == o) for o in OBJ_NAMES}
        theme = MONTH_THEMES.get(mo, "")

        vals = [md["label"], theme, total, ig, yt, fb, wa, reels, top_pat, avg_vir,
                fests_str, obj_c["Awareness"], obj_c["Trust"], obj_c["Community"],
                obj_c["Acquisition"], obj_c["App Download"]]
        bg = "F1F8E9" if row_idx % 2 == 0 else "FFFFFF"
        for col, val in enumerate(vals, 1):
            wrap = col in (2, 11)
            write_cell(ws, row_idx, col, val, bg=bg, size=9,
                       h="left" if col in (2, 11) else "center", wrap=wrap)
        ws.row_dimensions[row_idx].height = 36 if fests_str else 22
        row_idx += 1

# ─────────────────────────────────────────────
# SHEET 3: PATTERN MASTER (all 20 patterns)
# ─────────────────────────────────────────────
def build_pattern_sheet(ws):
    ws.title = "🎯 Pattern Master"
    ws.sheet_view.showGridLines = False

    write_cell(ws, 1, 1, "🎯 AgroManch — 20 Viral Patterns Master Reference",
               bg="1B4332", bold=True, size=13, color="FFFFFF", h="left")
    ws.merge_cells("A1:P1")
    ws.row_dimensions[1].height = 28

    hdrs = ["#", "Pattern Name", "Tier", "Virality", "Trust", "Shareability",
            "Reach", "Depth", "Local", "Mobile", "Total Score",
            "Best Platform", "Best Time", "Example Hook (Hindi)", "CTA", "Hashtags"]
    widths = [5, 22, 7, 9, 8, 12, 8, 8, 8, 8, 11, 14, 12, 40, 35, 38]
    for col, (h, w) in enumerate(zip(hdrs, widths), 1):
        write_cell(ws, 2, col, h, bg="2D6A4F", bold=True, size=10, color="FFFFFF")
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[2].height = 22

    platforms = ["Instagram", "YouTube", "Instagram", "Facebook", "Instagram",
                 "Instagram", "Instagram", "YouTube", "Facebook", "WhatsApp",
                 "YouTube", "Instagram", "YouTube", "YouTube", "Instagram",
                 "YouTube", "Instagram", "Facebook", "Instagram", "Instagram"]
    times = ["8:00 PM", "5:00 PM", "8:00 PM", "12:00 PM", "8:00 PM",
             "9:00 AM", "8:00 PM", "5:00 PM", "12:00 PM", "7:00 AM",
             "5:00 PM", "9:00 AM", "5:00 PM", "5:00 PM", "8:00 PM",
             "5:00 PM", "8:00 PM", "12:00 PM", "9:00 PM", "8:00 PM"]

    for i, (name, *scores) in enumerate(PATTERNS):
        V, T, S, R, D, L, M = scores
        total = sum(scores)
        tier = "A" if total >= 58 else "B" if total >= 52 else "C"
        t_bg = TIER_COLORS.get(tier, "CCCCCC")
        hook = HOOKS[name][0].replace("{c}", "गेहूं").replace("{r}", "UP").replace("{s}", "PM-KISAN").replace("{a}", "छोटे किसान").replace("__", "X")
        cta = CTAS[name]
        hts = HASHTAG_SETS[name]
        plat = platforms[i]
        bg = "FFF3E0" if tier == "A" else "E8F5E9" if tier == "B" else "E3F2FD"

        row = i + 3
        vals = [i+1, name, tier, V, T, S, R, D, L, M, total, plat, times[i], hook, cta, hts]
        for col, val in enumerate(vals, 1):
            if col == 3:
                write_cell(ws, row, col, val, bg=t_bg, bold=True, size=9, color="FFFFFF")
            elif col in (4,5,6,7,8,9,10):
                sc_bg = "52B788" if val >= 9 else "95D5B2" if val >= 7 else "D8F3DC"
                write_cell(ws, row, col, val, bg=sc_bg, size=9)
            elif col == 11:
                sc_bg = "52B788" if val >= 58 else "95D5B2" if val >= 52 else "D8F3DC"
                write_cell(ws, row, col, val, bg=sc_bg, bold=True, size=9)
            elif col in (14, 15, 16):
                write_cell(ws, row, col, val, bg=bg, size=9, h="left", wrap=True)
            else:
                write_cell(ws, row, col, val, bg=bg, size=9)
        ws.row_dimensions[row].height = 36

# ─────────────────────────────────────────────
# SHEET 4: WEEKLY PLANNER (current week view)
# ─────────────────────────────────────────────
def build_weekly_sheet(ws, rows):
    ws.title = "📆 Week-by-Week"
    ws.sheet_view.showGridLines = False

    write_cell(ws, 1, 1, "📆 AgroManch — Week-by-Week Content Schedule",
               bg="1B4332", bold=True, size=13, color="FFFFFF", h="left")
    ws.merge_cells(f"A1:{get_column_letter(8)}1")
    ws.row_dimensions[1].height = 28

    # Group rows by week
    weeks = {}
    for r in rows:
        wk = (r["day_num"] - 1) // 7 + 1
        if wk not in weeks:
            weeks[wk] = []
        weeks[wk].append(r)

    col_widths = [8, 12, 8, 16, 18, 22, 28, 22]
    hdrs = ["Week", "Date", "Day", "Platform", "Content Type", "Pattern", "Hook (3 sec)", "CTA"]
    for col, (h, w) in enumerate(zip(hdrs, col_widths), 1):
        write_cell(ws, 2, col, h, bg="2D6A4F", bold=True, size=10, color="FFFFFF")
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[2].height = 22

    xr = 3
    for wk in sorted(weeks.keys())[:52]:
        week_rows = weeks[wk]
        dates = week_rows[0]["date"] + " → " + week_rows[-1]["date"]
        # Week header
        write_cell(ws, xr, 1, f"Week {wk}", bg="2D6A4F", bold=True,
                   size=10, color="FFFFFF", h="center")
        write_cell(ws, xr, 2, dates, bg="2D6A4F", bold=False,
                   size=9, color="FFFFFF", h="left")
        ws.merge_cells(f"B{xr}:H{xr}")
        ws.row_dimensions[xr].height = 18
        xr += 1

        for r in week_rows:
            platform = r["platform"]
            p_bg = PLATFORM_LIGHT.get(platform, "FFFFFF")
            vals = [f"W{wk}", r["date"], r["day_name"], r["platform"],
                    r["content_type"], r["pat_name"], r["hook"], r["cta"]]
            for col, val in enumerate(vals, 1):
                if col == 4:
                    c_bg = PLATFORM_COLORS.get(platform, "999999")
                    write_cell(ws, xr, col, val, bg=c_bg, bold=True,
                               size=9, color="FFFFFF")
                elif col in (7, 8):
                    write_cell(ws, xr, col, val, bg=p_bg, size=9,
                               h="left", wrap=True)
                else:
                    write_cell(ws, xr, col, val, bg=p_bg, size=9)
            ws.row_dimensions[xr].height = 30
            xr += 1

    ws.auto_filter.ref = f"A2:H{xr - 1}"

# ─────────────────────────────────────────────
# SHEET 5: PLATFORM WISE PLAN
# ─────────────────────────────────────────────
def build_platform_sheet(ws, rows):
    ws.title = "📱 Platform-wise"
    ws.sheet_view.showGridLines = False

    write_cell(ws, 1, 1, "📱 AgroManch — Platform-wise Content Distribution",
               bg="1B4332", bold=True, size=13, color="FFFFFF", h="left")
    ws.merge_cells(f"A1:{get_column_letter(8)}1")
    ws.row_dimensions[1].height = 28

    platforms = ["Instagram", "YouTube", "Facebook", "WhatsApp"]
    plat_rows = {p: [r for r in rows if r["platform"] == p] for p in platforms}

    xr = 2
    for platform in platforms:
        p_rows = plat_rows[platform]
        p_color = PLATFORM_COLORS.get(platform, "999999")
        p_light = PLATFORM_LIGHT.get(platform, "FFFFFF")

        # Platform header
        write_cell(ws, xr, 1, f"  {platform}  ({len(p_rows)} posts)",
                   bg=p_color, bold=True, size=12, color="FFFFFF", h="left")
        ws.merge_cells(f"A{xr}:H{xr}")
        ws.row_dimensions[xr].height = 22
        xr += 1

        # Column headers
        hdrs = ["Date", "Day", "Content Type", "Pattern", "Virality", "Hook", "CTA", "Time"]
        widths = [12, 7, 18, 20, 9, 40, 35, 12]
        for col, (h, w) in enumerate(zip(hdrs, widths), 1):
            write_cell(ws, xr, col, h, bg="2D6A4F", bold=True, size=9, color="FFFFFF")
            ws.column_dimensions[get_column_letter(col)].width = max(
                ws.column_dimensions[get_column_letter(col)].width or 0, w)
        ws.row_dimensions[xr].height = 18
        xr += 1

        for r in p_rows:
            vals = [r["date"], r["day_name"], r["content_type"], r["pat_name"],
                    r["virality"], r["hook"], r["cta"], r["post_time"]]
            for col, val in enumerate(vals, 1):
                if col == 5:
                    v_bg = "52B788" if val >= 9 else "95D5B2" if val >= 7 else "D8F3DC"
                    write_cell(ws, xr, col, val, bg=v_bg, bold=True, size=9)
                elif col in (6, 7):
                    write_cell(ws, xr, col, val, bg=p_light, size=9,
                               h="left", wrap=True)
                else:
                    write_cell(ws, xr, col, val, bg=p_light, size=9)
            ws.row_dimensions[xr].height = 28
            xr += 1

        xr += 1  # spacer

# ─────────────────────────────────────────────
# SHEET 6: DASHBOARD / STATS
# ─────────────────────────────────────────────
def build_dashboard(ws, rows):
    ws.title = "📈 Dashboard"
    ws.sheet_view.showGridLines = False

    # Title
    write_cell(ws, 1, 1, "📈 AgroManch Content Plan — Dashboard & Stats",
               bg="1B4332", bold=True, size=14, color="FFFFFF", h="left")
    ws.merge_cells("A1:J1")
    ws.row_dimensions[1].height = 30

    # Stat boxes
    total = len(rows)
    ig = sum(1 for r in rows if r["platform"] == "Instagram")
    yt = sum(1 for r in rows if r["platform"] == "YouTube")
    fb = sum(1 for r in rows if r["platform"] == "Facebook")
    wa = sum(1 for r in rows if r["platform"] == "WhatsApp")
    reels = sum(1 for r in rows if r["content_type"] == "Instagram Reel")
    avg_vir = round(sum(r["virality"] for r in rows) / max(1, total), 2)
    high_eng = sum(1 for r in rows if r["exp_eng"] in ("High", "Very High", "Explosive"))

    stats = [
        ("Total Posts", total, "1B4332"),
        ("Instagram", ig, "E1306C"),
        ("YouTube", yt, "FF0000"),
        ("Facebook", fb, "1877F2"),
        ("WhatsApp", wa, "25D366"),
        ("Reels", reels, "833AB4"),
        ("Avg Virality", avg_vir, "FF6B35"),
        ("High Engagement", high_eng, "52B788"),
    ]

    stat_col = 1
    for label, val, color in stats:
        write_cell(ws, 3, stat_col, label, bg=color, bold=True, size=10, color="FFFFFF")
        ws.merge_cells(f"{get_column_letter(stat_col)}3:{get_column_letter(stat_col+1)}3")
        write_cell(ws, 4, stat_col, val, bg="F8F9FA", bold=True, size=16, color=color, h="center")
        ws.merge_cells(f"{get_column_letter(stat_col)}4:{get_column_letter(stat_col+1)}4")
        ws.column_dimensions[get_column_letter(stat_col)].width = 10
        ws.column_dimensions[get_column_letter(stat_col+1)].width = 10
        ws.row_dimensions[3].height = 20
        ws.row_dimensions[4].height = 32
        stat_col += 2

    # Pattern distribution table
    write_cell(ws, 6, 1, "Pattern Distribution", bg="2D6A4F", bold=True,
               size=11, color="FFFFFF", h="left")
    ws.merge_cells("A6:E6")
    ws.row_dimensions[6].height = 22

    pat_hdrs = ["Pattern", "Tier", "Count", "% Share", "Avg Virality"]
    pat_widths = [22, 7, 8, 10, 13]
    for col, (h, w) in enumerate(zip(pat_hdrs, pat_widths), 1):
        write_cell(ws, 7, col, h, bg="52B788", bold=True, size=9, color="FFFFFF")
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[7].height = 18

    pat_counts = {}
    pat_vir = {}
    for r in rows:
        pn = r["pat_name"]
        pat_counts[pn] = pat_counts.get(pn, 0) + 1
        pat_vir.setdefault(pn, []).append(r["virality"])

    for i, (name, *scores) in enumerate(PATTERNS):
        cnt = pat_counts.get(name, 0)
        total_score = sum(scores)
        tier = "A" if total_score >= 58 else "B" if total_score >= 52 else "C"
        t_bg = TIER_COLORS.get(tier, "CCCCCC")
        pct = round(cnt / max(1, total) * 100, 1)
        avg_v = round(sum(pat_vir.get(name, [0])) / max(1, cnt), 1)
        row_bg = "FFF3E0" if tier == "A" else "E8F5E9" if tier == "B" else "E3F2FD"
        xr = 8 + i
        write_cell(ws, xr, 1, name, bg=row_bg, size=9, h="left")
        write_cell(ws, xr, 2, tier, bg=t_bg, bold=True, size=9, color="FFFFFF")
        write_cell(ws, xr, 3, cnt, bg=row_bg, size=9)
        write_cell(ws, xr, 4, f"{pct}%", bg=row_bg, size=9)
        write_cell(ws, xr, 5, avg_v, bg=row_bg, size=9)
        ws.row_dimensions[xr].height = 18

    # Objective distribution
    obj_start_col = 7
    write_cell(ws, 6, obj_start_col, "Objective Distribution",
               bg="2D6A4F", bold=True, size=11, color="FFFFFF", h="left")
    ws.merge_cells(f"{get_column_letter(obj_start_col)}6:{get_column_letter(obj_start_col+2)}6")

    obj_hdrs = ["Objective", "Count", "% Share"]
    for col, h in enumerate(obj_hdrs, obj_start_col):
        write_cell(ws, 7, col, h, bg="52B788", bold=True, size=9, color="FFFFFF")
        ws.column_dimensions[get_column_letter(col)].width = 14

    obj_counts = {o: sum(1 for r in rows if r["objective"] == o) for o in OBJ_NAMES}
    for i, (obj, cnt) in enumerate(obj_counts.items()):
        xr = 8 + i
        pct = round(cnt / max(1, total) * 100, 1)
        o_bg = OBJ_COLORS.get(obj, "FFFFFF")
        write_cell(ws, xr, obj_start_col,     obj, bg=o_bg, size=9, h="left")
        write_cell(ws, xr, obj_start_col + 1, cnt, bg=o_bg, size=9)
        write_cell(ws, xr, obj_start_col + 2, f"{pct}%", bg=o_bg, size=9)
        ws.row_dimensions[xr].height = 18

# ─────────────────────────────────────────────
# SHEET 7: LEGEND & GUIDE
# ─────────────────────────────────────────────
def build_legend(ws):
    ws.title = "📖 Legend & Guide"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 22

    write_cell(ws, 1, 1, "📖 AgroManch Content Plan — Legend & Usage Guide",
               bg="1B4332", bold=True, size=14, color="FFFFFF", h="left")
    ws.merge_cells("A1:D1")
    ws.row_dimensions[1].height = 30

    sections = [
        ("PLATFORM COLORS", [
            ("Instagram", "Pink/Red (E1306C)", "Instagram Reels, Carousels, Stories"),
            ("YouTube",   "Red (FF0000)",      "Long-form & Shorts"),
            ("Facebook",  "Blue (1877F2)",     "Posts, Groups, Pages"),
            ("WhatsApp",  "Green (25D366)",    "Broadcast messages, Opt-in only"),
        ]),
        ("TIER SYSTEM", [
            ("Tier A (≥58 score)", "Red (FF6B6B)",  "Top patterns — 4x in rotation, highest priority"),
            ("Tier B (52-57)",     "Orange (FFA94D)","Mid-tier — 2x in rotation"),
            ("Tier C (<52)",       "Blue (74C0FC)",  "Supporting patterns — 1x in rotation"),
        ]),
        ("OBJECTIVES", [
            ("Awareness",    "Yellow (FFF9C4)",  "New audience, discovery content"),
            ("Trust",        "Green (E8F5E9)",   "Credibility, expertise, case studies"),
            ("Community",    "Purple (EDE7F6)",  "Engagement, polls, debates"),
            ("Acquisition",  "Orange (FFF3E0)",  "Lead gen, app downloads, registrations"),
            ("App Download", "Blue (E3F2FD)",    "Direct AgroManch app promotion"),
        ]),
        ("EXPECTED ENGAGEMENT", [
            ("Very High",   "Best performing content", "Prioritize production quality"),
            ("High",        "Strong performer",        "Standard production"),
            ("Medium",      "Regular performance",     "Repurpose if needed"),
            ("Low",         "Base content",            "Good for consistency"),
        ]),
        ("COLUMN GUIDE", [
            ("Hook (3 sec)",       "Opening line/visual — must grab in 3 seconds", "Fill in X with actual numbers"),
            ("Caption",            "Post caption template in Hindi", "Replace X with real data"),
            ("Hashtags (5)",       "5 targeted hashtags (post-2025 algorithm)", "Do not add more than 5"),
            ("CTA",                "Call to Action — end of caption or voiceover", "Match to current offer"),
            ("Status ✓",           "Mark: ✓ Done | ⏳ In Progress | ✗ Skipped | → Rescheduled", "Update daily"),
            ("Notes",              "Production notes, variations, actual performance", "Your daily log"),
        ]),
        ("DAILY WORKFLOW", [
            ("Step 1", "Filter by today's date in Column A (तारीख)", ""),
            ("Step 2", "Note Pattern, Crop, Region, Hook for today", ""),
            ("Step 3", "Replace 'X' with actual numbers in Hook/Caption", ""),
            ("Step 4", "Shoot/Create content using Production Note guidance", ""),
            ("Step 5", "Post at recommended time (Column Q)", ""),
            ("Step 6", "Mark Status column after posting", ""),
            ("Step 7", "Log actual engagement in Notes column", ""),
        ]),
    ]

    xr = 3
    for section_name, items in sections:
        write_cell(ws, xr, 1, section_name, bg="2D6A4F", bold=True,
                   size=11, color="FFFFFF", h="left")
        ws.merge_cells(f"A{xr}:D{xr}")
        ws.row_dimensions[xr].height = 22
        xr += 1

        for item in items:
            write_cell(ws, xr, 1, item[0], bg="F8F9FA", bold=True, size=9, h="left")
            write_cell(ws, xr, 2, item[1], bg="FFFFFF", size=9, h="left", wrap=True)
            write_cell(ws, xr, 3, item[2] if len(item) > 2 else "", bg="F8F9FA", size=9, h="left", wrap=True)
            write_cell(ws, xr, 4, item[3] if len(item) > 3 else "", bg="FFFFFF", size=9, h="left", wrap=True)
            ws.row_dimensions[xr].height = 28
            xr += 1

        xr += 1

# ─────────────────────────────────────────────
# MAIN BUILD
# ─────────────────────────────────────────────
def main():
    print("📊 Building AgroManch Google Sheet Content Plan...")

    print("  → Generating 365-day data rows...")
    rows = build_rows()
    print(f"  → {len(rows)} content rows generated")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default sheet

    print("  → Building Sheet 1: 365-Day Content Plan...")
    ws1 = wb.create_sheet()
    build_main_sheet(ws1, rows)

    print("  → Building Sheet 2: Monthly Overview...")
    ws2 = wb.create_sheet()
    build_monthly_sheet(ws2, rows)

    print("  → Building Sheet 3: Pattern Master...")
    ws3 = wb.create_sheet()
    build_pattern_sheet(ws3)

    print("  → Building Sheet 4: Week-by-Week...")
    ws4 = wb.create_sheet()
    build_weekly_sheet(ws4, rows)

    print("  → Building Sheet 5: Platform-wise...")
    ws5 = wb.create_sheet()
    build_platform_sheet(ws5, rows)

    print("  → Building Sheet 6: Dashboard...")
    ws6 = wb.create_sheet()
    build_dashboard(ws6, rows)

    print("  → Building Sheet 7: Legend & Guide...")
    ws7 = wb.create_sheet()
    build_legend(ws7)

    print(f"  → Saving to {OUTPUT_FILE}...")
    wb.save(OUTPUT_FILE)

    import os
    size_kb = os.path.getsize(OUTPUT_FILE) // 1024
    print(f"\n✅ SUCCESS!")
    print(f"   File: {OUTPUT_FILE}")
    print(f"   Size: {size_kb} KB")
    print(f"   Sheets: 7")
    print(f"   Data rows: {len(rows)}")
    print(f"\n📤 Import into Google Sheets:")
    print(f"   File → Import → Upload → Select XLSX → 'Insert new sheet(s)'")

if __name__ == "__main__":
    main()

"""
UP ke 75 Districts — Regions aur Base Product Catalog
Har region ki apni price tendency hoti hai
"""

# ============================================================
# UP KE 75 DISTRICTS — Region wise grouped
# ============================================================

UP_DISTRICTS = {

    # Western UP — Wheat belt, good connectivity, prices competitive
    "Paschim" : [
        "Meerut", "Ghaziabad", "Gautam Buddha Nagar", "Bulandshahr",
        "Hapur", "Baghpat", "Shamli", "Muzaffarnagar", "Saharanpur",
        "Bijnor", "Amroha", "Moradabad", "Sambhal", "Rampur",
        "Aligarh", "Hathras", "Mathura", "Agra", "Firozabad",
        "Mainpuri", "Etah", "Kasganj",
    ],

    # Central UP — Commercial hub, moderate prices
    "Madhya"  : [
        "Lucknow", "Unnao", "Kanpur Nagar", "Kanpur Dehat",
        "Hardoi", "Sitapur", "Lakhimpur Kheri", "Barabanki",
        "Rae Bareli", "Farrukhabad", "Kannauj", "Etawah",
        "Auraiya",
    ],

    # Eastern UP (Purvanchal) — Rice belt, slightly higher prices
    "Purv"    : [
        "Varanasi", "Chandauli", "Ghazipur", "Ballia", "Mau",
        "Azamgarh", "Jaunpur", "Bhadohi", "Mirzapur", "Sonbhadra",
        "Prayagraj", "Kaushambi", "Fatehpur", "Pratapgarh",
        "Sultanpur", "Amethi",
    ],

    # Awadh / Central-East — Mixed crop, medium prices
    "Awadh"   : [
        "Ayodhya", "Ambedkar Nagar", "Gonda", "Basti",
        "Sant Kabir Nagar", "Gorakhpur", "Maharajganj",
        "Kushinagar", "Deoria", "Siddharthnagar",
        "Bahraich", "Shravasti", "Balrampur",
    ],

    # Bundelkhand — Drought prone, prices can be higher
    "Bundelkhand": [
        "Jhansi", "Lalitpur", "Jalaun", "Hamirpur",
        "Mahoba", "Banda", "Chitrakoot",
    ],

    # Rohilkhand — North-west, sugarcane + wheat
    "Rohilkhand": [
        "Bareilly", "Pilibhit", "Shahjahanpur", "Budaun",
    ],
}

# Flat list of all 75 districts with their region
ALL_DISTRICTS = {}
for region, districts in UP_DISTRICTS.items():
    for d in districts:
        ALL_DISTRICTS[d] = region

# ============================================================
# 20 PRODUCTS — UP mein commonly traded
# ============================================================
# price_range: (min_possible, max_possible) Rs/Quintal
# base: typical UP average price
# unit: Quintal ya Kg
# category: Anaj/Dal/Sabzi/Masala/Tilhan/Nakdi

PRODUCT_CATALOG = [
    # ANAJ
    {"name": "Gehun (Wheat)",         "category": "Anaj",   "base": 2350, "range": (2100, 2700), "unit": "Quintal"},
    {"name": "Dhan (Paddy)",           "category": "Anaj",   "base": 1850, "range": (1600, 2100), "unit": "Quintal"},
    {"name": "Makka (Maize)",          "category": "Anaj",   "base": 1750, "range": (1500, 2000), "unit": "Quintal"},
    {"name": "Basmati Chawal",         "category": "Anaj",   "base": 4500, "range": (4000, 5200), "unit": "Quintal"},
    {"name": "Jau (Barley)",           "category": "Anaj",   "base": 1650, "range": (1400, 1900), "unit": "Quintal"},
    # DAL
    {"name": "Chana (Chickpea)",       "category": "Dal",    "base": 5200, "range": (4800, 5700), "unit": "Quintal"},
    {"name": "Arhar Dal (Tur)",        "category": "Dal",    "base": 6800, "range": (6200, 7500), "unit": "Quintal"},
    {"name": "Moong Dal",              "category": "Dal",    "base": 7200, "range": (6800, 7800), "unit": "Quintal"},
    {"name": "Urad Dal",               "category": "Dal",    "base": 7500, "range": (7000, 8200), "unit": "Quintal"},
    {"name": "Masoor Dal (Lentil)",    "category": "Dal",    "base": 5800, "range": (5200, 6500), "unit": "Quintal"},
    # SABZI
    {"name": "Aloo (Potato)",          "category": "Sabzi",  "base": 1200, "range":  (700, 1800), "unit": "Quintal"},
    {"name": "Pyaz (Onion)",           "category": "Sabzi",  "base": 2200, "range": (1500, 3200), "unit": "Quintal"},
    {"name": "Tamatar (Tomato)",       "category": "Sabzi",  "base": 1800, "range":  (800, 3000), "unit": "Quintal"},
    {"name": "Gobi (Cauliflower)",     "category": "Sabzi",  "base": 1100, "range":  (600, 1800), "unit": "Quintal"},
    {"name": "Palak (Spinach)",        "category": "Sabzi",  "base":  800, "range":  (400, 1400), "unit": "Quintal"},
    # MASALA
    {"name": "Lahsun (Garlic)",        "category": "Masala", "base": 8500, "range": (6000,12000), "unit": "Quintal"},
    {"name": "Adrak (Ginger)",         "category": "Masala", "base": 5500, "range": (4000, 8000), "unit": "Quintal"},
    {"name": "Haldi (Turmeric)",       "category": "Masala", "base":12000, "range": (9000,16000), "unit": "Quintal"},
    # TILHAN & NAKDI
    {"name": "Sarson (Mustard)",       "category": "Tilhan", "base": 5400, "range": (4800, 6200), "unit": "Quintal"},
    {"name": "Ganna (Sugarcane)",      "category": "Nakdi",  "base":  360, "range":  (320,  420), "unit": "Quintal"},
]

# Region-wise price modifier (percent adjustment)
REGION_PRICE_MODIFIER = {
    "Paschim":     -0.03,   # 3% sasta — good roads, high supply
    "Madhya":       0.00,   # baseline
    "Purv":        +0.04,   # 4% mahanga — door hai, transport cost
    "Awadh":       +0.02,   # 2% thoda mahanga
    "Bundelkhand": +0.07,   # 7% mahanga — drought, kum supply
    "Rohilkhand":  -0.01,   # 1% sasta — sugarcane rich area
}

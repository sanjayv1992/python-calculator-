"""
Mandi Bhav Data — India ke major districts ka real-style data
Har district mein 15-20 products with price, trend, category
"""

from datetime import date

TODAY = date.today().strftime("%d-%m-%Y")

# ============================================================
# COMPLETE MANDI DATA — STATE > DISTRICT > PRODUCTS
# Price unit: Rs per Quintal (100 kg) unless noted
# trend: "UP" / "DOWN" / "STABLE"
# ============================================================

MANDI_DATA = {

    # ==================== UTTAR PRADESH ====================
    "Uttar Pradesh": {

        "Lucknow": {
            "mandi_name": "Lucknow Krishi Upaj Mandi",
            "products": [
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2350, "min": 2200, "max": 2500, "unit": "Quintal", "trend": "UP",     "change": 45},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 1850, "min": 1700, "max": 1950, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1720, "min": 1600, "max": 1800, "unit": "Quintal", "trend": "DOWN",   "change": -30},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5200, "min": 5000, "max": 5400, "unit": "Quintal", "trend": "UP",     "change": 100},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 6800, "min": 6500, "max": 7100, "unit": "Quintal", "trend": "UP",     "change": 150},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7200, "min": 7000, "max": 7500, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1200, "min": 1000, "max": 1400, "unit": "Quintal", "trend": "DOWN",   "change": -80},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2200, "min": 2000, "max": 2500, "unit": "Quintal", "trend": "UP",     "change": 200},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 1800, "min": 1500, "max": 2200, "unit": "Quintal", "trend": "UP",     "change": 300},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 8500, "min": 8000, "max": 9000, "unit": "Quintal", "trend": "DOWN",   "change": -200},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 5500, "min": 5000, "max": 6000, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 12000,"min":11000, "max":13000, "unit": "Quintal", "trend": "UP",     "change": 500},
                {"name": "Ganna (Sugarcane)",     "category": "Nakdi",     "price": 360,  "min": 340,  "max": 380,  "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5400, "min": 5200, "max": 5600, "unit": "Quintal", "trend": "UP",     "change": 80},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4200, "min": 4000, "max": 4400, "unit": "Quintal", "trend": "DOWN",   "change": -50},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 4800, "min": 4500, "max": 5100, "unit": "Quintal", "trend": "UP",     "change": 120},
                {"name": "Palak (Spinach)",       "category": "Sabzi",     "price": 800,  "min": 600,  "max": 1000, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 1100, "min": 900,  "max": 1300, "unit": "Quintal", "trend": "DOWN",   "change": -100},
                {"name": "Basmati Chawal",        "category": "Anaj",      "price": 4500, "min": 4200, "max": 4800, "unit": "Quintal", "trend": "UP",     "change": 200},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7500, "min": 7200, "max": 7800, "unit": "Quintal", "trend": "STABLE", "change": 0},
            ]
        },

        "Varanasi": {
            "mandi_name": "Varanasi Krishi Mandi",
            "products": [
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2380, "min": 2250, "max": 2520, "unit": "Quintal", "trend": "UP",     "change": 50},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 1870, "min": 1720, "max": 1980, "unit": "Quintal", "trend": "UP",     "change": 20},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5250, "min": 5050, "max": 5450, "unit": "Quintal", "trend": "UP",     "change": 110},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 6850, "min": 6600, "max": 7100, "unit": "Quintal", "trend": "UP",     "change": 160},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1150, "min": 950,  "max": 1350, "unit": "Quintal", "trend": "DOWN",   "change": -90},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2300, "min": 2100, "max": 2600, "unit": "Quintal", "trend": "UP",     "change": 220},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 1900, "min": 1600, "max": 2300, "unit": "Quintal", "trend": "UP",     "change": 280},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5350, "min": 5100, "max": 5550, "unit": "Quintal", "trend": "UP",     "change": 70},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 8200, "min": 7800, "max": 8700, "unit": "Quintal", "trend": "DOWN",   "change": -180},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 11800,"min":10800, "max":12800, "unit": "Quintal", "trend": "UP",     "change": 450},
                {"name": "Ganna (Sugarcane)",     "category": "Nakdi",     "price": 355,  "min": 340,  "max": 375,  "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1750, "min": 1620, "max": 1850, "unit": "Quintal", "trend": "DOWN",   "change": -25},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7350, "min": 7100, "max": 7600, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7600, "min": 7300, "max": 7900, "unit": "Quintal", "trend": "UP",     "change": 80},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 15000,"min":14000, "max":16500, "unit": "Quintal", "trend": "UP",     "change": 800},
                {"name": "Saunf (Fennel)",        "category": "Masala",    "price": 9000, "min": 8500, "max": 9500, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Basmati Chawal",        "category": "Anaj",      "price": 4600, "min": 4300, "max": 4900, "unit": "Quintal", "trend": "UP",     "change": 180},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 1000, "min": 800,  "max": 1200, "unit": "Quintal", "trend": "DOWN",   "change": -120},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4300, "min": 4100, "max": 4500, "unit": "Quintal", "trend": "DOWN",   "change": -40},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 5800, "min": 5300, "max": 6300, "unit": "Quintal", "trend": "UP",     "change": 150},
            ]
        },

        "Agra": {
            "mandi_name": "Agra Krishi Upaj Mandi",
            "products": [
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2330, "min": 2180, "max": 2480, "unit": "Quintal", "trend": "UP",     "change": 40},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5500, "min": 5300, "max": 5700, "unit": "Quintal", "trend": "UP",     "change": 90},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1100, "min": 900,  "max": 1300, "unit": "Quintal", "trend": "DOWN",   "change": -100},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2100, "min": 1900, "max": 2400, "unit": "Quintal", "trend": "UP",     "change": 190},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 1700, "min": 1400, "max": 2100, "unit": "Quintal", "trend": "UP",     "change": 260},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5100, "min": 4900, "max": 5300, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 6700, "min": 6400, "max": 7000, "unit": "Quintal", "trend": "UP",     "change": 130},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 8000, "min": 7500, "max": 8500, "unit": "Quintal", "trend": "DOWN",   "change": -220},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 11500,"min":10500, "max":12500, "unit": "Quintal", "trend": "UP",     "change": 420},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 1820, "min": 1680, "max": 1920, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1700, "min": 1580, "max": 1800, "unit": "Quintal", "trend": "DOWN",   "change": -35},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7100, "min": 6900, "max": 7400, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4150, "min": 3950, "max": 4350, "unit": "Quintal", "trend": "DOWN",   "change": -60},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 14500,"min":13500, "max":15800, "unit": "Quintal", "trend": "UP",     "change": 700},
                {"name": "Ganna (Sugarcane)",     "category": "Nakdi",     "price": 350,  "min": 335,  "max": 370,  "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7400, "min": 7100, "max": 7700, "unit": "Quintal", "trend": "UP",     "change": 70},
                {"name": "Palak (Spinach)",       "category": "Sabzi",     "price": 850,  "min": 650,  "max": 1050, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 950,  "min": 750,  "max": 1150, "unit": "Quintal", "trend": "DOWN",   "change": -110},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 5600, "min": 5100, "max": 6100, "unit": "Quintal", "trend": "UP",     "change": 130},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 4900, "min": 4600, "max": 5200, "unit": "Quintal", "trend": "UP",     "change": 110},
            ]
        },
    },

    # ==================== MADHYA PRADESH ====================
    "Madhya Pradesh": {

        "Indore": {
            "mandi_name": "Indore Krishi Upaj Mandi Samiti",
            "products": [
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4350, "min": 4150, "max": 4550, "unit": "Quintal", "trend": "DOWN",   "change": -45},
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2420, "min": 2280, "max": 2560, "unit": "Quintal", "trend": "UP",     "change": 55},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5350, "min": 5150, "max": 5550, "unit": "Quintal", "trend": "UP",     "change": 120},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2400, "min": 2200, "max": 2700, "unit": "Quintal", "trend": "UP",     "change": 240},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9000, "min": 8500, "max": 9600, "unit": "Quintal", "trend": "DOWN",   "change": -250},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1300, "min": 1100, "max": 1500, "unit": "Quintal", "trend": "DOWN",   "change": -70},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2000, "min": 1700, "max": 2400, "unit": "Quintal", "trend": "UP",     "change": 320},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5600, "min": 5400, "max": 5800, "unit": "Quintal", "trend": "UP",     "change": 95},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1780, "min": 1650, "max": 1880, "unit": "Quintal", "trend": "DOWN",   "change": -20},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 6900, "min": 6650, "max": 7200, "unit": "Quintal", "trend": "UP",     "change": 170},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 12500,"min":11500, "max":13500, "unit": "Quintal", "trend": "UP",     "change": 600},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7800, "min": 7500, "max": 8100, "unit": "Quintal", "trend": "UP",     "change": 100},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7400, "min": 7200, "max": 7700, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 16000,"min":15000, "max":17500, "unit": "Quintal", "trend": "UP",     "change": 900},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 1900, "min": 1760, "max": 2000, "unit": "Quintal", "trend": "UP",     "change": 30},
                {"name": "Til (Sesame)",          "category": "Tilhan",    "price": 13000,"min":12000, "max":14000, "unit": "Quintal", "trend": "UP",     "change": 500},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6000, "min": 5500, "max": 6500, "unit": "Quintal", "trend": "UP",     "change": 200},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 5000, "min": 4700, "max": 5300, "unit": "Quintal", "trend": "UP",     "change": 130},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 1200, "min": 1000, "max": 1400, "unit": "Quintal", "trend": "DOWN",   "change": -90},
                {"name": "Basmati Chawal",        "category": "Anaj",      "price": 4700, "min": 4400, "max": 5000, "unit": "Quintal", "trend": "UP",     "change": 210},
            ]
        },

        "Bhopal": {
            "mandi_name": "Bhopal Krishi Mandi",
            "products": [
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4280, "min": 4080, "max": 4480, "unit": "Quintal", "trend": "DOWN",   "change": -50},
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2400, "min": 2260, "max": 2540, "unit": "Quintal", "trend": "UP",     "change": 50},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5300, "min": 5100, "max": 5500, "unit": "Quintal", "trend": "UP",     "change": 115},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2350, "min": 2150, "max": 2650, "unit": "Quintal", "trend": "UP",     "change": 230},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 8800, "min": 8300, "max": 9400, "unit": "Quintal", "trend": "DOWN",   "change": -230},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1250, "min": 1050, "max": 1450, "unit": "Quintal", "trend": "DOWN",   "change": -75},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 1950, "min": 1650, "max": 2350, "unit": "Quintal", "trend": "UP",     "change": 310},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5550, "min": 5350, "max": 5750, "unit": "Quintal", "trend": "UP",     "change": 88},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 6800, "min": 6550, "max": 7100, "unit": "Quintal", "trend": "UP",     "change": 155},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7300, "min": 7100, "max": 7600, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7700, "min": 7400, "max": 8000, "unit": "Quintal", "trend": "UP",     "change": 90},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 12200,"min":11200, "max":13200, "unit": "Quintal", "trend": "UP",     "change": 550},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 15500,"min":14500, "max":17000, "unit": "Quintal", "trend": "UP",     "change": 820},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1760, "min": 1630, "max": 1860, "unit": "Quintal", "trend": "DOWN",   "change": -28},
                {"name": "Til (Sesame)",          "category": "Tilhan",    "price": 12800,"min":11800, "max":13800, "unit": "Quintal", "trend": "UP",     "change": 480},
                {"name": "Palak (Spinach)",       "category": "Sabzi",     "price": 820,  "min": 620,  "max": 1020, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 5900, "min": 5400, "max": 6400, "unit": "Quintal", "trend": "UP",     "change": 180},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 1880, "min": 1740, "max": 1980, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Basmati Chawal",        "category": "Anaj",      "price": 4650, "min": 4350, "max": 4950, "unit": "Quintal", "trend": "UP",     "change": 195},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 4950, "min": 4650, "max": 5250, "unit": "Quintal", "trend": "UP",     "change": 125},
            ]
        },
    },

    # ==================== PUNJAB ====================
    "Punjab": {

        "Ludhiana": {
            "mandi_name": "Ludhiana Grain Market",
            "products": [
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2450, "min": 2300, "max": 2600, "unit": "Quintal", "trend": "UP",     "change": 60},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 2050, "min": 1900, "max": 2200, "unit": "Quintal", "trend": "UP",     "change": 50},
                {"name": "Basmati Chawal",        "category": "Anaj",      "price": 5500, "min": 5200, "max": 5800, "unit": "Quintal", "trend": "UP",     "change": 280},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1850, "min": 1720, "max": 1950, "unit": "Quintal", "trend": "DOWN",   "change": -15},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5800, "min": 5600, "max": 6000, "unit": "Quintal", "trend": "UP",     "change": 110},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1400, "min": 1200, "max": 1600, "unit": "Quintal", "trend": "DOWN",   "change": -60},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2500, "min": 2300, "max": 2800, "unit": "Quintal", "trend": "UP",     "change": 260},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2100, "min": 1800, "max": 2500, "unit": "Quintal", "trend": "UP",     "change": 350},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5500, "min": 5300, "max": 5700, "unit": "Quintal", "trend": "UP",     "change": 140},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 7100, "min": 6800, "max": 7400, "unit": "Quintal", "trend": "UP",     "change": 180},
                {"name": "Urad Dal",              "category": "Dal",       "price": 8000, "min": 7700, "max": 8300, "unit": "Quintal", "trend": "UP",     "change": 120},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7600, "min": 7400, "max": 7900, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9200, "min": 8700, "max": 9800, "unit": "Quintal", "trend": "DOWN",   "change": -270},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 13000,"min":12000, "max":14000, "unit": "Quintal", "trend": "UP",     "change": 650},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6200, "min": 5700, "max": 6700, "unit": "Quintal", "trend": "UP",     "change": 220},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 16500,"min":15500, "max":18000, "unit": "Quintal", "trend": "UP",     "change": 950},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 1300, "min": 1100, "max": 1500, "unit": "Quintal", "trend": "DOWN",   "change": -80},
                {"name": "Palak (Spinach)",       "category": "Sabzi",     "price": 900,  "min": 700,  "max": 1100, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4500, "min": 4300, "max": 4700, "unit": "Quintal", "trend": "DOWN",   "change": -30},
                {"name": "Ganna (Sugarcane)",     "category": "Nakdi",     "price": 380,  "min": 360,  "max": 400,  "unit": "Quintal", "trend": "STABLE", "change": 0},
            ]
        },

        "Amritsar": {
            "mandi_name": "Amritsar Sabzi Mandi",
            "products": [
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2470, "min": 2320, "max": 2620, "unit": "Quintal", "trend": "UP",     "change": 65},
                {"name": "Dhan (Paddy)",          "category": "Anaj",      "price": 2080, "min": 1930, "max": 2230, "unit": "Quintal", "trend": "UP",     "change": 55},
                {"name": "Basmati Chawal",        "category": "Anaj",      "price": 5600, "min": 5300, "max": 5900, "unit": "Quintal", "trend": "UP",     "change": 300},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5850, "min": 5650, "max": 6050, "unit": "Quintal", "trend": "UP",     "change": 115},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1450, "min": 1250, "max": 1650, "unit": "Quintal", "trend": "DOWN",   "change": -55},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2550, "min": 2350, "max": 2850, "unit": "Quintal", "trend": "UP",     "change": 270},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2150, "min": 1850, "max": 2550, "unit": "Quintal", "trend": "UP",     "change": 360},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5550, "min": 5350, "max": 5750, "unit": "Quintal", "trend": "UP",     "change": 145},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 7150, "min": 6850, "max": 7450, "unit": "Quintal", "trend": "UP",     "change": 185},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9400, "min": 8900, "max": 10000,"unit": "Quintal", "trend": "DOWN",   "change": -280},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 13200,"min":12200, "max":14200, "unit": "Quintal", "trend": "UP",     "change": 680},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6400, "min": 5900, "max": 6900, "unit": "Quintal", "trend": "UP",     "change": 240},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1870, "min": 1740, "max": 1970, "unit": "Quintal", "trend": "DOWN",   "change": -12},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7650, "min": 7450, "max": 7950, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 8050, "min": 7750, "max": 8350, "unit": "Quintal", "trend": "UP",     "change": 125},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 1350, "min": 1150, "max": 1550, "unit": "Quintal", "trend": "DOWN",   "change": -75},
                {"name": "Palak (Spinach)",       "category": "Sabzi",     "price": 950,  "min": 750,  "max": 1150, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 16800,"min":15800, "max":18300, "unit": "Quintal", "trend": "UP",     "change": 980},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4550, "min": 4350, "max": 4750, "unit": "Quintal", "trend": "DOWN",   "change": -25},
                {"name": "Til (Sesame)",          "category": "Tilhan",    "price": 13500,"min":12500, "max":14500, "unit": "Quintal", "trend": "UP",     "change": 550},
            ]
        },
    },

    # ==================== GUJARAT ====================
    "Gujarat": {

        "Rajkot": {
            "mandi_name": "Rajkot APMC Market",
            "products": [
                {"name": "Mungfali (Groundnut)",  "category": "Tilhan",    "price": 6500, "min": 6200, "max": 6800, "unit": "Quintal", "trend": "UP",     "change": 200},
                {"name": "Til (Sesame)",          "category": "Tilhan",    "price": 14000,"min":13000, "max":15000, "unit": "Quintal", "trend": "UP",     "change": 600},
                {"name": "Kapas (Cotton)",        "category": "Nakdi",     "price": 7200, "min": 6900, "max": 7600, "unit": "Quintal", "trend": "DOWN",   "change": -150},
                {"name": "Jeera (Cumin)",         "category": "Masala",    "price": 42000,"min":40000, "max":44000, "unit": "Quintal", "trend": "UP",     "change": 2000},
                {"name": "Saunf (Fennel)",        "category": "Masala",    "price": 10000,"min": 9500, "max":10500, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Dhaniya (Coriander)",   "category": "Masala",    "price": 8500, "min": 8000, "max": 9000, "unit": "Quintal", "trend": "UP",     "change": 300},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9500, "min": 9000, "max":10200, "unit": "Quintal", "trend": "DOWN",   "change": -300},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2600, "min": 2400, "max": 2900, "unit": "Quintal", "trend": "UP",     "change": 280},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1500, "min": 1300, "max": 1700, "unit": "Quintal", "trend": "DOWN",   "change": -50},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2200, "min": 1900, "max": 2600, "unit": "Quintal", "trend": "UP",     "change": 380},
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2500, "min": 2360, "max": 2640, "unit": "Quintal", "trend": "UP",     "change": 70},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5600, "min": 5400, "max": 5800, "unit": "Quintal", "trend": "UP",     "change": 150},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 7200, "min": 6900, "max": 7500, "unit": "Quintal", "trend": "UP",     "change": 190},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7700, "min": 7500, "max": 8000, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 13500,"min":12500, "max":14500, "unit": "Quintal", "trend": "UP",     "change": 700},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6500, "min": 6000, "max": 7000, "unit": "Quintal", "trend": "UP",     "change": 250},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 17000,"min":16000, "max":18500, "unit": "Quintal", "trend": "UP",     "change": 1000},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5900, "min": 5700, "max": 6100, "unit": "Quintal", "trend": "UP",     "change": 120},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4600, "min": 4400, "max": 4800, "unit": "Quintal", "trend": "DOWN",   "change": -20},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 5200, "min": 4900, "max": 5500, "unit": "Quintal", "trend": "UP",     "change": 150},
            ]
        },

        "Ahmedabad": {
            "mandi_name": "Ahmedabad APMC Yard",
            "products": [
                {"name": "Mungfali (Groundnut)",  "category": "Tilhan",    "price": 6400, "min": 6100, "max": 6700, "unit": "Quintal", "trend": "UP",     "change": 190},
                {"name": "Jeera (Cumin)",         "category": "Masala",    "price": 41000,"min":39000, "max":43000, "unit": "Quintal", "trend": "UP",     "change": 1900},
                {"name": "Kapas (Cotton)",        "category": "Nakdi",     "price": 7100, "min": 6800, "max": 7500, "unit": "Quintal", "trend": "DOWN",   "change": -140},
                {"name": "Dhaniya (Coriander)",   "category": "Masala",    "price": 8300, "min": 7800, "max": 8800, "unit": "Quintal", "trend": "UP",     "change": 280},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2550, "min": 2350, "max": 2850, "unit": "Quintal", "trend": "UP",     "change": 265},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1480, "min": 1280, "max": 1680, "unit": "Quintal", "trend": "DOWN",   "change": -45},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2150, "min": 1850, "max": 2550, "unit": "Quintal", "trend": "UP",     "change": 360},
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2480, "min": 2340, "max": 2620, "unit": "Quintal", "trend": "UP",     "change": 65},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5550, "min": 5350, "max": 5750, "unit": "Quintal", "trend": "UP",     "change": 145},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 7150, "min": 6850, "max": 7450, "unit": "Quintal", "trend": "UP",     "change": 185},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9300, "min": 8800, "max": 9900, "unit": "Quintal", "trend": "DOWN",   "change": -290},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 13200,"min":12200, "max":14200, "unit": "Quintal", "trend": "UP",     "change": 680},
                {"name": "Til (Sesame)",          "category": "Tilhan",    "price": 13800,"min":12800, "max":14800, "unit": "Quintal", "trend": "UP",     "change": 580},
                {"name": "Saunf (Fennel)",        "category": "Masala",    "price": 9800, "min": 9300, "max":10300, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7600, "min": 7400, "max": 7900, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7900, "min": 7600, "max": 8200, "unit": "Quintal", "trend": "UP",     "change": 110},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5820, "min": 5620, "max": 6020, "unit": "Quintal", "trend": "UP",     "change": 105},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6300, "min": 5800, "max": 6800, "unit": "Quintal", "trend": "UP",     "change": 230},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 16500,"min":15500, "max":18000, "unit": "Quintal", "trend": "UP",     "change": 950},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 5100, "min": 4800, "max": 5400, "unit": "Quintal", "trend": "UP",     "change": 140},
            ]
        },
    },

    # ==================== RAJASTHAN ====================
    "Rajasthan": {

        "Jaipur": {
            "mandi_name": "Jaipur Krishi Upaj Mandi",
            "products": [
                {"name": "Jeera (Cumin)",         "category": "Masala",    "price": 43000,"min":41000, "max":45000, "unit": "Quintal", "trend": "UP",     "change": 2200},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 5700, "min": 5500, "max": 5900, "unit": "Quintal", "trend": "UP",     "change": 100},
                {"name": "Mungfali (Groundnut)",  "category": "Tilhan",    "price": 6300, "min": 6000, "max": 6600, "unit": "Quintal", "trend": "UP",     "change": 180},
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2400, "min": 2260, "max": 2540, "unit": "Quintal", "trend": "UP",     "change": 55},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5400, "min": 5200, "max": 5600, "unit": "Quintal", "trend": "UP",     "change": 125},
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2450, "min": 2250, "max": 2750, "unit": "Quintal", "trend": "UP",     "change": 255},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9100, "min": 8600, "max": 9700, "unit": "Quintal", "trend": "DOWN",   "change": -260},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 12800,"min":11800, "max":13800, "unit": "Quintal", "trend": "UP",     "change": 620},
                {"name": "Dhaniya (Coriander)",   "category": "Masala",    "price": 8200, "min": 7700, "max": 8700, "unit": "Quintal", "trend": "UP",     "change": 270},
                {"name": "Saunf (Fennel)",        "category": "Masala",    "price": 9500, "min": 9000, "max":10000, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1350, "min": 1150, "max": 1550, "unit": "Quintal", "trend": "DOWN",   "change": -65},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2050, "min": 1750, "max": 2450, "unit": "Quintal", "trend": "UP",     "change": 340},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7500, "min": 7300, "max": 7800, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 7800, "min": 7500, "max": 8100, "unit": "Quintal", "trend": "UP",     "change": 95},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 6950, "min": 6700, "max": 7250, "unit": "Quintal", "trend": "UP",     "change": 165},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4250, "min": 4050, "max": 4450, "unit": "Quintal", "trend": "DOWN",   "change": -55},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 15800,"min":14800, "max":17300, "unit": "Quintal", "trend": "UP",     "change": 860},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6100, "min": 5600, "max": 6600, "unit": "Quintal", "trend": "UP",     "change": 210},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 5050, "min": 4750, "max": 5350, "unit": "Quintal", "trend": "UP",     "change": 135},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1740, "min": 1610, "max": 1840, "unit": "Quintal", "trend": "DOWN",   "change": -32},
            ]
        },
    },

    # ==================== MAHARASHTRA ====================
    "Maharashtra": {

        "Pune": {
            "mandi_name": "Pune Market Yard (Gultekdi)",
            "products": [
                {"name": "Pyaz (Onion)",          "category": "Sabzi",     "price": 2700, "min": 2500, "max": 3000, "unit": "Quintal", "trend": "UP",     "change": 300},
                {"name": "Tamatar (Tomato)",      "category": "Sabzi",     "price": 2300, "min": 2000, "max": 2700, "unit": "Quintal", "trend": "UP",     "change": 400},
                {"name": "Aloo (Potato)",         "category": "Sabzi",     "price": 1600, "min": 1400, "max": 1800, "unit": "Quintal", "trend": "DOWN",   "change": -40},
                {"name": "Gobi (Cauliflower)",    "category": "Sabzi",     "price": 1400, "min": 1200, "max": 1600, "unit": "Quintal", "trend": "DOWN",   "change": -70},
                {"name": "Palak (Spinach)",       "category": "Sabzi",     "price": 1000, "min": 800,  "max": 1200, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Lahsun (Garlic)",       "category": "Masala",    "price": 9800, "min": 9300, "max":10500, "unit": "Quintal", "trend": "DOWN",   "change": -320},
                {"name": "Adrak (Ginger)",        "category": "Masala",    "price": 6800, "min": 6300, "max": 7300, "unit": "Quintal", "trend": "UP",     "change": 280},
                {"name": "Haldi (Turmeric)",      "category": "Masala",    "price": 14000,"min":13000, "max":15000, "unit": "Quintal", "trend": "UP",     "change": 750},
                {"name": "Laal Mirch (Red Chili)","category": "Masala",   "price": 18000,"min":17000, "max":19500, "unit": "Quintal", "trend": "UP",     "change": 1100},
                {"name": "Gehun (Wheat)",        "category": "Anaj",      "price": 2550, "min": 2410, "max": 2690, "unit": "Quintal", "trend": "UP",     "change": 75},
                {"name": "Chana (Chickpea)",      "category": "Dal",       "price": 5700, "min": 5500, "max": 5900, "unit": "Quintal", "trend": "UP",     "change": 160},
                {"name": "Arhar Dal (Tur)",       "category": "Dal",       "price": 7300, "min": 7000, "max": 7600, "unit": "Quintal", "trend": "UP",     "change": 200},
                {"name": "Moong Dal",             "category": "Dal",       "price": 7800, "min": 7600, "max": 8100, "unit": "Quintal", "trend": "STABLE", "change": 0},
                {"name": "Urad Dal",              "category": "Dal",       "price": 8200, "min": 7900, "max": 8500, "unit": "Quintal", "trend": "UP",     "change": 130},
                {"name": "Soyabean",              "category": "Tilhan",    "price": 4700, "min": 4500, "max": 4900, "unit": "Quintal", "trend": "DOWN",   "change": -15},
                {"name": "Sarson (Mustard)",      "category": "Tilhan",    "price": 6000, "min": 5800, "max": 6200, "unit": "Quintal", "trend": "UP",     "change": 130},
                {"name": "Kapas (Cotton)",        "category": "Nakdi",     "price": 7400, "min": 7100, "max": 7800, "unit": "Quintal", "trend": "DOWN",   "change": -120},
                {"name": "Makka (Maize)",         "category": "Anaj",      "price": 1900, "min": 1770, "max": 2000, "unit": "Quintal", "trend": "DOWN",   "change": -10},
                {"name": "Dhaniya (Coriander)",   "category": "Masala",    "price": 8700, "min": 8200, "max": 9200, "unit": "Quintal", "trend": "UP",     "change": 310},
                {"name": "Methi (Fenugreek)",     "category": "Masala",    "price": 5300, "min": 5000, "max": 5600, "unit": "Quintal", "trend": "UP",     "change": 160},
            ]
        },
    },
}

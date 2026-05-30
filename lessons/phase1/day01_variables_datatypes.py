"""
=============================================================
DAY 1 — Variables aur Data Types
Python 90-Day Course | AgroManch ke liye Python Seekhna
=============================================================

AAJ KA TOPIC: Variables kya hote hain? Data Types kya hote hain?

REAL LIFE CONNECTION:
Ek kisan (farmer) ki diary sochiye.
Usme likha hota hai:
  - Kisan ka naam     -> text (string)
  - Uski umar        -> number (int)
  - Zameen ka area   -> decimal number (float)
  - Kya woh organic farmer hai? -> yes/no (bool)

Yahi sab Python mein VARIABLES hote hain!
=============================================================
"""

# ============================================================
# SECTION 1: Variable kya hota hai?
# ============================================================
# Variable = ek dabba (box) jisme hum koi value rakhte hain
# Jaise: naam = "Ramesh"  ->  "naam" ek dabba hai, "Ramesh" uske andar hai

# SYNTAX: variable_name = value

kisan_naam = "Ramesh Kumar"       # String (text)
kisan_umar = 35                    # Integer (pura number)
zameen_area = 2.5                  # Float (decimal number)
organic_farmer = True              # Boolean (True/False)

print("Kisan ka naam:", kisan_naam)
print("Umar:", kisan_umar)
print("Zameen (acres):", zameen_area)
print("Organic farmer hai?", organic_farmer)


# ============================================================
# SECTION 2: Python ke 4 Main Data Types
# ============================================================

# 1. STRING (str) — Text ke liye
# Quotes ke andar likhte hain — single ya double dono chalta hai
fasal_naam = "Gehun"              # double quotes
mandi_naam = 'Azadpur Mandi'     # single quotes

# 2. INTEGER (int) — Pura number (bina decimal ke)
fasal_quantity_kg = 500
price_per_kg = 25

# 3. FLOAT (float) — Decimal number
moisture_percent = 14.5
gst_rate = 0.18

# 4. BOOLEAN (bool) — Sirf True ya False
kya_becha = False
kya_registered = True

print("\n--- Fasal ki Jankari ---")
print("Fasal:", fasal_naam)
print("Mandi:", mandi_naam)
print("Matra (kg):", fasal_quantity_kg)
print("Rate (Rs/kg):", price_per_kg)
print("Moisture %:", moisture_percent)
print("Kya becha?", kya_becha)


# ============================================================
# SECTION 3: type() function — Data type pata karna
# ============================================================
# type() se hum jaante hain ki variable kis type ka hai

print("\n--- Data Types Check ---")
print(type(kisan_naam))       # <class 'str'>
print(type(kisan_umar))       # <class 'int'>
print(type(zameen_area))      # <class 'float'>
print(type(organic_farmer))   # <class 'bool'>


# ============================================================
# SECTION 4: Variable Naming Rules (Important!)
# ============================================================

# SAHI tarike (valid):
fasal_rate = 50           # underscore allowed
_private_var = "ok"       # underscore se shuru kar sakte hain
rate2024 = 100            # number end mein allowed

# GALAT tarike (invalid) — ye lines comment mein hain, run mat karo:
# 2fasal = "wheat"        # number se shuru NAHI kar sakte
# fasal-naam = "rice"     # hyphen NAHI allowed
# class = 10              # Python ke reserved words use NAHI kar sakte

# Tips: naam hamesha meaningful rakho
# x = 50         <- BAD (kuch pata nahi)
# fasal_price = 50  <- GOOD (clearly samajh aata hai)


# ============================================================
# SECTION 5: Multiple Assignment (ek saath kai variables)
# ============================================================

# Ek line mein kai values assign karna
length, width, height = 10, 5, 2
print("\nLength:", length, "Width:", width, "Height:", height)

# Sabko same value dena
a = b = c = 0
print("a, b, c:", a, b, c)


# ============================================================
# SECTION 6: Real AgroManch Example
# ============================================================
# Maan lo AgroManch app mein ek farmer register karta hai
# Uski profile kuch aisi hogi:

farmer_id = 1001
farmer_name = "Suresh Patel"
farmer_village = "Karjan"
farmer_state = "Gujarat"
land_in_acres = 3.75
primary_crop = "Cotton"
is_verified = False
annual_income = 180000

print("\n========== AGROМАНCH FARMER PROFILE ==========")
print("Farmer ID   :", farmer_id)
print("Name        :", farmer_name)
print("Village     :", farmer_village)
print("State       :", farmer_state)
print("Land (acres):", land_in_acres)
print("Main Crop   :", primary_crop)
print("Verified    :", is_verified)
print("Income (Rs) :", annual_income)
print("===============================================")


# ============================================================
# PRACTICE QUESTIONS — Khud solve karo pehle!
# ============================================================
"""
QUESTION 1:
Apne aap ke liye ek profile banao:
- naam (string)
- umar (int)
- shahar (string)
- height in meters (float)
- kya aap student ho? (bool)
Sab print karo.

QUESTION 2:
Ek fasal ki detail banao:
- fasal_naam = "Chawal"
- rate_per_quintal = 2200 (int)
- quality_grade = "A"
- organic = True
type() se har ek ka data type print karo.

QUESTION 3:
Mand likhne ki galti dhundho — kya sahi hai?
a) my name = "Raju"
b) myname = "Raju"
c) 1name = "Raju"
d) my-name = "Raju"

QUESTION 4:
Teen variables ek saath assign karo:
lat, lon, altitude = 23.5, 72.8, 150
Inhe print karo.

QUESTION 5:
Ek e-commerce product ki details store karo variables mein:
product name, price, stock count, is_available
"""


# ============================================================
# CODING TASK — Aaj ka homework!
# ============================================================
"""
TASK: "Kisan Card" banao

Ek chhota program likho jo ek farmer ka digital card dikhaye.
Variables use karo — name, village, district, state, land_acres,
main_crop, year_of_registration.

Output aisa dikhna chahiye:

============ KISAN CARD ============
Naam       : [farmer name]
Gaon       : [village]
Zila       : [district]
State      : [state]
Zameen     : [X] acres
Fasal      : [crop name]
Registered : [year]
====================================

Khud try karo pehle! Neecha answer hai.
"""


# ============================================================
# ANSWER — CODING TASK
# ============================================================
# (Pehle khud try karo, phir dekho!)

naam = "Mohan Lal Sharma"
gaon = "Rampur"
zila = "Muzaffarnagar"
state = "Uttar Pradesh"
zameen = 5.25
fasal = "Ganna (Sugarcane)"
saal = 2024

print("\n============ KISAN CARD ============")
print("Naam       :", naam)
print("Gaon       :", gaon)
print("Zila       :", zila)
print("State      :", state)
print(f"Zameen     : {zameen} acres")
print("Fasal      :", fasal)
print("Registered :", saal)
print("====================================")

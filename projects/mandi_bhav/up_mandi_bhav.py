"""
╔══════════════════════════════════════════════════════════════════╗
║       AGROМАНCH — UP COMPLETE MANDI BHAV SYSTEM                 ║
║   Uttar Pradesh ke 75 Districts ka Daily Mandi Bhav             ║
║   Data Source: Agmarknet.gov.in + Smart Fallback               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
from datetime import date, timedelta

from up_districts_config import ALL_DISTRICTS, UP_DISTRICTS, REGION_PRICE_MODIFIER
from up_data_generator   import generate_district_data, generate_all_up_data
from agmarknet_fetcher   import (
    test_connection, fetch_all_up_commodities,
    get_district_data_from_agmarknet
)

TODAY      = date.today()
TODAY_STR  = TODAY.strftime("%d-%m-%Y")
TREND_ICON = {"UP": "▲", "DOWN": "▼", "STABLE": "━"}
CAT_ICON   = {
    "Anaj": "🌾", "Dal": "🫘", "Sabzi": "🥬",
    "Masala": "🌶", "Tilhan": "🌻", "Nakdi": "💰",
}

DATA_CACHE_FILE = os.path.join(
    os.path.dirname(__file__), "data_cache", "up_daily_data.json"
)


# ============================================================
# DATA LOADER — Live ya Generated
# ============================================================

def load_today_data(force_live=False):
    """
    Pehle cache dekhta hai. Nahi mila to generate karta hai.
    force_live=True karne par Agmarknet se live data lata hai.
    """
    os.makedirs(os.path.dirname(DATA_CACHE_FILE), exist_ok=True)

    # Cache check
    if not force_live and os.path.exists(DATA_CACHE_FILE):
        with open(DATA_CACHE_FILE, "r", encoding="utf-8") as f:
            cached = json.load(f)
        if cached.get("date") == TODAY_STR:
            return cached["data"], cached.get("source", "cache")

    # Try live data
    if force_live:
        ok, msg = test_connection()
        if ok:
            print(f"\n  Internet available hai! Agmarknet se data la rahe hain...")
            live_data = fetch_all_up_commodities()
            if live_data:
                merged = merge_live_with_generated(live_data)
                _save_cache(merged, "Agmarknet (Live)")
                return merged, "Agmarknet (Live)"
            else:
                print("  Live data nahi mila — generated data use ho raha hai.")
        else:
            print(f"  Internet nahi hai ({msg}) — generated data use ho raha hai.")

    # Fallback: generate
    all_data = generate_all_up_data(TODAY)
    _save_cache(all_data, "Generated (Agmarknet fallback)")
    return all_data, "Generated"


def _save_cache(data, source):
    os.makedirs(os.path.dirname(DATA_CACHE_FILE), exist_ok=True)
    with open(DATA_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"date": TODAY_STR, "source": source, "data": data},
                  f, ensure_ascii=False, indent=2)


def merge_live_with_generated(live_commodity_data):
    """
    Live data aur generated data ko merge karta hai.
    Jahan live data hai — woh use karo; baaki generated.
    """
    gen_data = generate_all_up_data(TODAY)

    for district, dist_data in gen_data.items():
        live_district = get_district_data_from_agmarknet(district)
        if not live_district:
            continue
        for product in dist_data["products"]:
            commodity_key = _map_product_to_commodity(product["name"])
            if commodity_key and commodity_key in live_district:
                live = live_district[commodity_key]
                product["price"]  = live["modal_price"]
                product["min"]    = live["min_price"]
                product["max"]    = live["max_price"]
                product["source"] = "Agmarknet (Live)"
                product["trend"]  = "STABLE"
                product["change"] = 0

    return gen_data


def _map_product_to_commodity(product_name):
    mapping = {
        "Gehun (Wheat)":       "Wheat",
        "Dhan (Paddy)":        "Paddy",
        "Makka (Maize)":       "Maize",
        "Aloo (Potato)":       "Potato",
        "Pyaz (Onion)":        "Onion",
        "Tamatar (Tomato)":    "Tomato",
        "Arhar Dal (Tur)":     "Arhar",
        "Moong Dal":           "Moong",
        "Urad Dal":            "Urad",
        "Masoor Dal (Lentil)": "Masoor",
        "Sarson (Mustard)":    "Mustard",
        "Ganna (Sugarcane)":   "Sugarcane",
        "Lahsun (Garlic)":     "Garlic",
        "Adrak (Ginger)":      "Ginger",
        "Haldi (Turmeric)":    "Turmeric",
        "Chana (Chickpea)":    "Chana",
        "Jau (Barley)":        "Barley",
    }
    return mapping.get(product_name)


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def divider(char="═", width=72):
    print(char * width)

def header(title, width=72):
    divider(width=width)
    pad = (width - 2 - len(title)) // 2
    print("║" + " " * pad + title + " " * (width - 2 - pad - len(title)) + "║")
    divider(width=width)


def show_district(district, data, show_source=False):
    dist_data = data.get(district)
    if not dist_data:
        print(f"  '{district}' ka data nahi mila.")
        return

    products = dist_data["products"]
    region   = dist_data.get("region", "")
    mandi    = dist_data.get("mandi_name", f"{district} Mandi")
    src      = dist_data["products"][0].get("source", "Generated") if products else ""

    header(f"MANDI BHAV — {district.upper()}")
    print(f"  Mandi    : {mandi}")
    print(f"  Region   : {region}")
    print(f"  Date     : {TODAY_STR}")
    print(f"  Source   : {src}")
    print(f"  Products : {len(products)}")
    divider("─", 72)
    print(f"  {'#':<3} {'Fasal / Udpaj':<26} {'Rate/Qtl':>9}  {'Min':>7}  {'Max':>7}  {'Trend':>6}  {'Badlav':>6}")
    divider("─", 72)

    # Group by category
    cats = {}
    for p in products:
        cats.setdefault(p["category"], []).append(p)

    rank = 1
    for cat in ["Anaj", "Dal", "Sabzi", "Masala", "Tilhan", "Nakdi"]:
        if cat not in cats:
            continue
        icon = CAT_ICON.get(cat, "  ")
        print(f"\n  {icon} ── {cat.upper()} ──")
        for p in cats[cat]:
            t = TREND_ICON[p["trend"]]
            ch = p["change"]
            ch_str = f"+{ch}" if ch > 0 else (str(ch) if ch != 0 else "  —")
            print(
                f"  {rank:<3} {p['name']:<26} Rs{p['price']:>6}  "
                f"{p['min']:>7}  {p['max']:>7}  {t:>6}  {ch_str:>6}"
            )
            rank += 1

    divider("─", 72)
    print(f"  ▲=Upar  ▼=Neeche  ━=Stable  |  Sabhi rates Rs/Quintal mein")
    divider(width=72)
    print()


def show_all_districts_list(data):
    header("UP KE SABHI 75 DISTRICTS — MANDI LIST")
    divider("─", 72)
    for region_name, districts in UP_DISTRICTS.items():
        mod = REGION_PRICE_MODIFIER.get(region_name, 0)
        mod_str = f"+{int(mod*100)}%" if mod > 0 else (f"{int(mod*100)}%" if mod < 0 else "avg")
        print(f"\n  📍 {region_name} UP  [{mod_str}]")
        for i, d in enumerate(sorted(districts), 1):
            dist_data = data.get(d, {})
            products  = dist_data.get("products", [])
            up_count  = sum(1 for p in products if p.get("trend") == "UP")
            dn_count  = sum(1 for p in products if p.get("trend") == "DOWN")
            print(f"     {i:>2}. {d:<22}  ▲{up_count}  ▼{dn_count}  ({len(products)} products)")

    divider("─", 72)
    print(f"  Total Districts: {len(ALL_DISTRICTS)}  |  Total Products: {len(ALL_DISTRICTS)*20}")
    divider(width=72)
    print()


def show_region_bhav(region_name, data):
    """Ek region ke sabhi districts ka summary"""
    districts = UP_DISTRICTS.get(region_name, [])
    if not districts:
        print(f"  Region '{region_name}' nahi mila.")
        return

    header(f"{region_name.upper()} UP — REGION MANDI BHAV SUMMARY")
    divider("─", 72)
    print(f"  {'District':<20} {'Gehun':>7}  {'Pyaz':>7}  {'Aloo':>7}  {'Dhan':>7}  {'Sarson':>7}")
    divider("─", 72)

    key_products = ["Gehun (Wheat)", "Pyaz (Onion)", "Aloo (Potato)",
                    "Dhan (Paddy)", "Sarson (Mustard)"]

    for d in sorted(districts):
        dist_data = data.get(d, {})
        products  = {p["name"]: p for p in dist_data.get("products", [])}
        prices    = []
        for kp in key_products:
            p = products.get(kp)
            prices.append(f"{p['price']:>7}" if p else "   N/A")

        print(f"  {d:<20} {'  '.join(prices)}")

    divider("─", 72)
    print(f"  Rates Rs/Quintal mein | Region: {region_name}")
    divider(width=72)
    print()


def search_cheapest_across_up(product_keyword, data):
    """UP mein sabse sasta product kahan milega"""
    kw = product_keyword.lower()
    results = []

    for district, dist_data in data.items():
        for p in dist_data.get("products", []):
            if kw in p["name"].lower():
                results.append({
                    "district": district,
                    "region":   dist_data.get("region", ""),
                    **p
                })

    results.sort(key=lambda x: x["price"])

    if not results:
        print(f"  '{product_keyword}' nahi mila.")
        return

    header(f"UP MEIN SABSE SASTA '{product_keyword.upper()}'")
    divider("─", 72)
    print(f"  {'#':<3} {'District':<20} {'Region':<14} {'Rate':>8}  {'Min':>8}  {'Max':>8}  Trend")
    divider("─", 72)
    for i, r in enumerate(results[:20], 1):
        t  = TREND_ICON[r["trend"]]
        mk = "  ← SABSE SASTA!" if i == 1 else ""
        mk2= "  ← 2nd SASTA" if i == 2 else mk
        print(
            f"  {i:<3} {r['district']:<20} {r['region']:<14} "
            f"Rs{r['price']:>6}  {r['min']:>8}  {r['max']:>8}  {t}{mk2}"
        )
    divider("─", 72)
    print(f"  Kul {len(results)} districts mein mila | Sorted by price")
    divider(width=72)
    print()


def show_up_trending(direction, data):
    """UP mein aaj sabse zyada bade ya gire bhav"""
    label = "UP MEIN SABSE ZYADA BADE BHAV AAJ" if direction == "UP" else "UP MEIN SABSE ZYADA GIRE BHAV AAJ"
    header(label)

    results = []
    for district, dist_data in data.items():
        for p in dist_data.get("products", []):
            if p.get("trend") == direction and abs(p.get("change", 0)) > 0:
                results.append({"district": district, **p})

    results.sort(key=lambda x: abs(x.get("change", 0)), reverse=True)

    divider("─", 72)
    print(f"  {'#':<3} {'Product':<26} {'District':<20} {'Rate':>8}  {'Badlav':>8}")
    divider("─", 72)
    for i, r in enumerate(results[:20], 1):
        ch = r.get("change", 0)
        ch_str = f"+{ch}" if ch > 0 else str(ch)
        print(f"  {i:<3} {r['name']:<26} {r['district']:<20} Rs{r['price']:>6}  {ch_str:>8}")
    divider(width=72)
    print()


def show_category_across_up(category, data):
    """UP ke sabhi districts mein ek category ke products"""
    header(f"UP — {category.upper()} PRICES — ALL DISTRICTS")
    divider("─", 72)

    for region_name, districts in UP_DISTRICTS.items():
        printed_header = False
        for district in sorted(districts):
            dist_data = data.get(district, {})
            cat_products = [p for p in dist_data.get("products", [])
                           if p["category"].lower() == category.lower()]
            if not cat_products:
                continue
            if not printed_header:
                print(f"\n  📍 {region_name} UP")
                print(f"  {'District':<20} {'Product':<26} {'Rate':>8}  Trend")
                print("  " + "─" * 60)
                printed_header = True
            for p in cat_products:
                t = TREND_ICON[p["trend"]]
                print(f"  {district:<20} {p['name']:<26} Rs{p['price']:>6}  {t}")

    divider(width=72)
    print()


def show_today_stats(data):
    """Aaj ka UP Mandi Overview"""
    header(f"UP MANDI BHAV — AAJ KA OVERVIEW ({TODAY_STR})")

    total_products   = 0
    up_count         = 0
    down_count       = 0
    stable_count     = 0
    max_rise_product = None
    max_fall_product = None
    max_rise         = 0
    max_fall         = 0

    for district, dist_data in data.items():
        for p in dist_data.get("products", []):
            total_products += 1
            t = p.get("trend")
            ch = abs(p.get("change", 0))
            if t == "UP":
                up_count += 1
                if ch > max_rise:
                    max_rise = ch
                    max_rise_product = (p["name"], district, p["price"], ch)
            elif t == "DOWN":
                down_count += 1
                if ch > max_fall:
                    max_fall = ch
                    max_fall_product = (p["name"], district, p["price"], ch)
            else:
                stable_count += 1

    divider("─", 72)
    print(f"  Districts covered  : {len(data)} / 75")
    print(f"  Total price entries: {total_products}")
    print(f"  Bhav Upar (▲)     : {up_count} products")
    print(f"  Bhav Neeche (▼)   : {down_count} products")
    print(f"  Stable (━)        : {stable_count} products")
    divider("─", 72)

    if max_rise_product:
        n, d, p, ch = max_rise_product
        print(f"  SABSE BADA UTHA  : {n} — {d}  Rs{p}  (+{ch})")
    if max_fall_product:
        n, d, p, ch = max_fall_product
        print(f"  SABSE ZYADA GIRA : {n} — {d}  Rs{p}  (-{ch})")

    divider("─", 72)
    print()


# ============================================================
# INTERACTIVE MENU
# ============================================================

def main():
    print()
    divider(width=72)
    print("║" + " " * 10 + "AGROМАНCH — UP MANDI BHAV SYSTEM" + " " * 10 + "║")
    print("║" + " " * 14 + "Uttar Pradesh ke 75 Districts" + " " * 15 + "║")
    print("║" + " " * 20 + f"Date: {TODAY_STR}" + " " * 21 + "║")
    divider(width=72)

    print("\n  Data load ho raha hai...", end="", flush=True)
    data, source = load_today_data(force_live=False)
    print(f" Done! ({len(data)} districts)  Source: {source}\n")

    while True:
        divider("─", 72)
        print("\n  MENU:")
        print("  1.  Kisi bhi district ka Mandi Bhav dekho (75 districts)")
        print("  2.  Region-wise summary (Paschim/Madhya/Purv/Awadh/Bundelkhand)")
        print("  3.  UP ke sabhi districts ki list")
        print("  4.  Koi product search karo (UP ke sare districts mein)")
        print("  5.  Category dekho UP mein (Anaj/Dal/Sabzi/Masala/Tilhan)")
        print("  6.  Sabse Zyada Bade Bhav aaj — UP mein")
        print("  7.  Sabse Zyada Gire Bhav aaj — UP mein")
        print("  8.  Aaj ka UP Mandi Overview")
        print("  9.  Live data Agmarknet se refresh karo")
        print("  0.  Exit")
        print()

        choice = input("  Option chuniye (0-9): ").strip()

        if choice == "1":
            show_all_districts_list(data)
            district = input("  District ka naam likhiye: ").strip().title()
            if district in data:
                show_district(district, data)
            else:
                close = [d for d in ALL_DISTRICTS if district.lower() in d.lower()]
                if close:
                    print(f"  '{district}' nahi mila. Kya yeh matalab tha?")
                    for i, d in enumerate(close[:5], 1):
                        print(f"    {i}. {d}")
                    pick = input("  Number daalo: ").strip()
                    if pick.isdigit() and 1 <= int(pick) <= len(close):
                        show_district(close[int(pick)-1], data)
                else:
                    print(f"  '{district}' nahi mila UP ke districts mein.")

        elif choice == "2":
            print("\n  Regions: Paschim | Madhya | Purv | Awadh | Bundelkhand | Rohilkhand")
            region = input("  Region ka naam: ").strip().title()
            show_region_bhav(region, data)

        elif choice == "3":
            show_all_districts_list(data)

        elif choice == "4":
            kw = input("  Product ka naam (e.g. Pyaz, Gehun, Aloo): ").strip()
            search_cheapest_across_up(kw, data)

        elif choice == "5":
            print("  Categories: Anaj | Dal | Sabzi | Masala | Tilhan | Nakdi")
            cat = input("  Category: ").strip().title()
            show_category_across_up(cat, data)

        elif choice == "6":
            show_up_trending("UP", data)

        elif choice == "7":
            show_up_trending("DOWN", data)

        elif choice == "8":
            show_today_stats(data)

        elif choice == "9":
            print("\n  Agmarknet se live data la raha hai...")
            data, source = load_today_data(force_live=True)
            print(f"  Done! Source: {source}")

        elif choice == "0":
            print("\n  Jai Kisan! AgroManch Mandi Bhav System")
            break

        else:
            print("  Galat option. 0-9 mein se chuniye.")


def run_demo():
    """Quick demo — sab features ek saath"""
    print()
    divider(width=72)
    print("║" + " " * 18 + "UP MANDI BHAV — DEMO MODE" + " " * 19 + "║")
    divider(width=72)

    data, source = load_today_data(force_live=False)
    print(f"  Data loaded: {len(data)} districts | Source: {source}\n")

    # Demo 1: All districts list
    show_all_districts_list(data)

    # Demo 2: Few specific districts
    for d in ["Lucknow", "Varanasi", "Jhansi", "Meerut", "Gorakhpur"]:
        show_district(d, data)

    # Demo 3: Region summary
    show_region_bhav("Bundelkhand", data)

    # Demo 4: Search
    search_cheapest_across_up("Gehun", data)
    search_cheapest_across_up("Pyaz", data)

    # Demo 5: Trending
    show_up_trending("UP", data)

    # Demo 6: Category
    show_category_across_up("Anaj", data)

    # Demo 7: Today stats
    show_today_stats(data)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        main()

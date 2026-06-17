"""
╔══════════════════════════════════════════════════════════════╗
║           AGROМАНCH — ADVANCED MANDI BHAV SYSTEM            ║
║         India ke Major Districts ka Live Mandi Rate          ║
╚══════════════════════════════════════════════════════════════╝

Features:
  - 6 States, 10 Districts, 200+ Price Entries
  - Category filter: Anaj / Dal / Sabzi / Masala / Tilhan
  - Price trend: UP / DOWN / STABLE with arrows
  - Highest / Lowest price finder
  - State-wise summary
  - Product search across all mandis
"""

from mandi_data import MANDI_DATA, TODAY

# ============================================================
# DISPLAY HELPERS
# ============================================================

TREND_ICON = {"UP": "▲", "DOWN": "▼", "STABLE": "━"}
TREND_COLOR = {"UP": "[+]", "DOWN": "[-]", "STABLE": "[=]"}

CATEGORY_ICONS = {
    "Anaj":   "🌾",
    "Dal":    "🫘",
    "Sabzi":  "🥬",
    "Masala": "🌶",
    "Tilhan": "🌻",
    "Nakdi":  "💰",
}

def divider(char="═", width=70):
    print(char * width)

def header(title):
    divider()
    pad = (68 - len(title)) // 2
    print("║" + " " * pad + title + " " * (68 - pad - len(title)) + "║")
    divider()

def print_product_row(p, rank=None):
    trend  = TREND_ICON[p["trend"]]
    signal = TREND_COLOR[p["trend"]]
    icon   = CATEGORY_ICONS.get(p["category"], "  ")
    change = f"+{p['change']}" if p['change'] > 0 else str(p['change']) if p['change'] < 0 else "  0"
    rank_str = f"{rank:>2}." if rank else "  "

    print(
        f"  {rank_str} {icon} {p['name']:<26} "
        f"Rs {p['price']:>6}/Qtl  "
        f"Min:{p['min']:>5}  Max:{p['max']:>6}  "
        f"{trend} {signal} {change:>5}"
    )


# ============================================================
# FEATURE 1: District Mandi Bhav (full table)
# ============================================================

def show_district_bhav(state_name, district_name):
    state = MANDI_DATA.get(state_name)
    if not state:
        print(f"  [ERROR] State '{state_name}' nahi mili.")
        return

    district = state.get(district_name)
    if not district:
        print(f"  [ERROR] District '{district_name}' nahi mila.")
        return

    products = district["products"]

    header(f"MANDI BHAV — {district_name.upper()}, {state_name.upper()}")
    print(f"  Mandi    : {district['mandi_name']}")
    print(f"  Date     : {TODAY}")
    print(f"  Products : {len(products)}")
    print(f"  Trend    : ▲ Upar  ▼ Neeche  ━ Stable")
    divider("─")
    print(f"  {'#':<4} {'Product':<28} {'Rate/Quintal':>12}  {'Min':>8}  {'Max':>8}  Trend")
    divider("─")

    # Group by category
    categories = {}
    for p in products:
        categories.setdefault(p["category"], []).append(p)

    rank = 1
    for cat, items in sorted(categories.items()):
        icon = CATEGORY_ICONS.get(cat, "")
        print(f"\n  {icon}  ── {cat.upper()} ──")
        for p in items:
            print_product_row(p, rank)
            rank += 1

    divider("─")
    print(f"  Total {len(products)} products | Date: {TODAY}")
    divider()
    print()


# ============================================================
# FEATURE 2: Category Filter
# ============================================================

def show_by_category(state_name, district_name, category):
    state    = MANDI_DATA.get(state_name)
    district = state.get(district_name) if state else None

    if not district:
        print("  District nahi mila.")
        return

    products = [p for p in district["products"] if p["category"].lower() == category.lower()]

    if not products:
        print(f"  '{category}' category mein koi product nahi mila.")
        return

    header(f"{category.upper()} — {district_name}, {state_name}")
    divider("─")
    for i, p in enumerate(products, 1):
        print_product_row(p, i)
    divider("─")
    print()


# ============================================================
# FEATURE 3: Search Product Across All Mandis
# ============================================================

def search_product(product_keyword):
    keyword = product_keyword.lower()

    header(f"SEARCH: '{product_keyword}' — ALL MANDIS")
    divider("─")
    print(f"  {'State':<15} {'District':<12} {'Product':<26} {'Rate':>8}  {'Trend':>6}")
    divider("─")

    found = 0
    results = []

    for state_name, districts in MANDI_DATA.items():
        for dist_name, dist_data in districts.items():
            for p in dist_data["products"]:
                if keyword in p["name"].lower():
                    results.append((state_name, dist_name, p))

    results.sort(key=lambda x: x[2]["price"])

    for state_name, dist_name, p in results:
        trend = TREND_ICON[p["trend"]]
        signal = TREND_COLOR[p["trend"]]
        print(
            f"  {state_name:<15} {dist_name:<12} {p['name']:<26} "
            f"Rs {p['price']:>6}  {trend} {signal}"
        )
        found += 1

    if found == 0:
        print(f"  Koi result nahi mila '{product_keyword}' ke liye.")
    else:
        divider("─")
        print(f"  {found} results mile | Sorted by price (low → high)")
    divider()
    print()


# ============================================================
# FEATURE 4: Top 10 Highest Priced Products
# ============================================================

def show_top_prices(top_n=10):
    all_products = []

    for state, districts in MANDI_DATA.items():
        for dist, data in districts.items():
            for p in data["products"]:
                all_products.append({**p, "state": state, "district": dist})

    all_products.sort(key=lambda x: x["price"], reverse=True)
    top = all_products[:top_n]

    header(f"TOP {top_n} SABSE MEHNGE PRODUCTS — ALL INDIA")
    divider("─")
    print(f"  {'#':<3} {'Product':<26} {'State':<15} {'District':<12} {'Rate':>8}")
    divider("─")
    for i, p in enumerate(top, 1):
        print(f"  {i:<3} {p['name']:<26} {p['state']:<15} {p['district']:<12} Rs {p['price']:>7}/Qtl")
    divider()
    print()


# ============================================================
# FEATURE 5: Cheapest Products (Best Buy)
# ============================================================

def show_cheapest(product_keyword):
    keyword = product_keyword.lower()
    results = []

    for state, districts in MANDI_DATA.items():
        for dist, data in districts.items():
            for p in data["products"]:
                if keyword in p["name"].lower():
                    results.append({**p, "state": state, "district": dist})

    if not results:
        print(f"  '{product_keyword}' kahi nahi mila.")
        return

    results.sort(key=lambda x: x["price"])

    header(f"SABSE SASTA '{product_keyword.upper()}' KAHAN MILEGA?")
    divider("─")
    print(f"  {'#':<3} {'State':<15} {'District':<12} {'Rate':>8}  {'Trend':>8}")
    divider("─")
    for i, p in enumerate(results, 1):
        trend = TREND_ICON[p["trend"]]
        signal = TREND_COLOR[p["trend"]]
        marker = "  ← SABSE SASTA!" if i == 1 else ""
        print(f"  {i:<3} {p['state']:<15} {p['district']:<12} Rs {p['price']:>6}/Qtl  {trend} {signal}{marker}")
    divider()
    print()


# ============================================================
# FEATURE 6: State Summary
# ============================================================

def show_state_summary(state_name):
    state = MANDI_DATA.get(state_name)
    if not state:
        print(f"  State '{state_name}' nahi mili.")
        return

    header(f"STATE SUMMARY — {state_name.upper()}")
    divider("─")

    total_products = 0
    for dist_name, data in state.items():
        products = data["products"]
        up_count     = sum(1 for p in products if p["trend"] == "UP")
        down_count   = sum(1 for p in products if p["trend"] == "DOWN")
        stable_count = sum(1 for p in products if p["trend"] == "STABLE")
        avg_price    = sum(p["price"] for p in products) // len(products)
        total_products += len(products)

        print(f"\n  📍 {dist_name} — {data['mandi_name']}")
        print(f"     Products : {len(products)}")
        print(f"     Avg Rate : Rs {avg_price}/Quintal")
        print(f"     Trends   : ▲ UP({up_count})  ▼ DOWN({down_count})  ━ STABLE({stable_count})")

    divider("─")
    print(f"  Total Districts : {len(state)}")
    print(f"  Total Products  : {total_products}")
    divider()
    print()


# ============================================================
# FEATURE 7: All States & Districts List
# ============================================================

def show_all_mandis():
    header("ALL MANDIS — COMPLETE LIST")
    divider("─")
    total_dist = 0
    for state, districts in MANDI_DATA.items():
        print(f"\n  📌 {state}")
        for dist, data in districts.items():
            count = len(data["products"])
            print(f"       → {dist:<15}  {data['mandi_name']:<35} ({count} products)")
            total_dist += 1
    divider("─")
    print(f"  Total States: {len(MANDI_DATA)} | Total Mandis: {total_dist}")
    divider()
    print()


# ============================================================
# FEATURE 8: Price Alert — Upar ya Neeche wale dikhao
# ============================================================

def show_trending(direction="UP"):
    label = "SABSE TEZI SE BADE BHAV" if direction == "UP" else "SABSE ZYADA GIRE BHAV"
    header(label)

    results = []
    for state, districts in MANDI_DATA.items():
        for dist, data in districts.items():
            for p in data["products"]:
                if p["trend"] == direction and abs(p["change"]) > 0:
                    results.append({**p, "state": state, "district": dist})

    results.sort(key=lambda x: abs(x["change"]), reverse=True)

    divider("─")
    icon = CATEGORY_ICONS
    print(f"  {'#':<3} {'Product':<26} {'State':<14} {'District':<12} {'Rate':>8}  {'Change':>8}")
    divider("─")
    for i, p in enumerate(results[:15], 1):
        change_str = f"+{p['change']}" if p['change'] > 0 else str(p['change'])
        print(f"  {i:<3} {p['name']:<26} {p['state']:<14} {p['district']:<12} Rs {p['price']:>6}  {change_str:>8}")
    divider()
    print()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    while True:
        print()
        divider("═")
        print("║" + " " * 15 + "AGROМАНCH MANDI BHAV SYSTEM" + " " * 15 + "║")
        print("║" + " " * 20 + f"Date: {TODAY}" + " " * 21 + "║")
        divider("═")
        print()
        print("  1. Kisi bhi District ka Mandi Bhav dekho")
        print("  2. Category wise filter karo (Anaj/Dal/Sabzi/Masala/Tilhan)")
        print("  3. Koi bhi product search karo (all mandis mein)")
        print("  4. Top 10 Mehnge Products — All India")
        print("  5. Sabse Sasta Product kahan milega?")
        print("  6. State Summary dekho")
        print("  7. Sabhi Mandis ki list dekho")
        print("  8. Sabse Zyada Bade/Gire Bhav dekho")
        print("  0. Exit")
        print()
        divider("─")
        choice = input("  Option chuniye (0-8): ").strip()

        if choice == "1":
            show_all_mandis()
            state = input("  State ka naam daalo: ").strip().title()
            dist  = input("  District ka naam daalo: ").strip().title()
            show_district_bhav(state, dist)

        elif choice == "2":
            show_all_mandis()
            state    = input("  State: ").strip().title()
            dist     = input("  District: ").strip().title()
            print("  Categories: Anaj | Dal | Sabzi | Masala | Tilhan | Nakdi")
            category = input("  Category: ").strip().title()
            show_by_category(state, dist, category)

        elif choice == "3":
            keyword = input("  Product ka naam likhiye (e.g. Pyaz, Gehun, Haldi): ").strip()
            search_product(keyword)

        elif choice == "4":
            show_top_prices(10)

        elif choice == "5":
            keyword = input("  Kaun sa product dhundna hai?: ").strip()
            show_cheapest(keyword)

        elif choice == "6":
            print("  States:", ", ".join(MANDI_DATA.keys()))
            state = input("  State ka naam: ").strip().title()
            show_state_summary(state)

        elif choice == "7":
            show_all_mandis()

        elif choice == "8":
            print("  1 = Tezi (UP)  |  2 = Giraat (DOWN)")
            sub = input("  Chuniye: ").strip()
            direction = "UP" if sub == "1" else "DOWN"
            show_trending(direction)

        elif choice == "0":
            print("\n  AgroManch Mandi Bhav System — Jai Kisan! 🌾")
            break

        else:
            print("  Galat option. 0-8 mein se chuniye.")


# ============================================================
# QUICK DEMO — seedha run karne ke liye
# ============================================================

def run_demo():
    print("\n" + "=" * 70)
    print("   AGROМАНCH MANDI BHAV — QUICK DEMO (All Features)")
    print("=" * 70 + "\n")

    # Demo 1: Lucknow full bhav
    show_district_bhav("Uttar Pradesh", "Lucknow")

    # Demo 2: Indore ka Anaj
    show_by_category("Madhya Pradesh", "Indore", "Anaj")

    # Demo 3: Pyaz search all India
    search_product("Pyaz")

    # Demo 4: Top 10 prices
    show_top_prices(10)

    # Demo 5: Sabse sasta Gehun
    show_cheapest("Gehun")

    # Demo 6: Gujarat summary
    show_state_summary("Gujarat")

    # Demo 7: All mandis list
    show_all_mandis()

    # Demo 8: Tezi wale bhav
    show_trending("UP")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        main_menu()

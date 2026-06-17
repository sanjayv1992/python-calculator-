"""
UP Districts Smart Data Generator
Jab Agmarknet se data nahi aata — realistic fallback data generate karta hai.

Logic:
  - Har district ke region ke hisaab se price modifier apply hota hai
  - Date-based seed se har din alag alag (realistic) prices milte hain
  - Aaj, kal, aur parso ke prices alag honge
"""

import random
import hashlib
from datetime import date, timedelta
from up_districts_config import ALL_DISTRICTS, PRODUCT_CATALOG, REGION_PRICE_MODIFIER


def get_seed(district, product_name, for_date=None):
    """
    Ek unique seed banata hai — district + product + date se.
    Isse har din prices thode alag honge lekin consistent rahenge.
    """
    if for_date is None:
        for_date = date.today()
    seed_str = f"{district}_{product_name}_{for_date.isoformat()}"
    return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)


def generate_price(product, district, for_date=None):
    """
    Ek product ka realistic price generate karta hai.
    Region modifier + daily variation consider karta hai.
    """
    if for_date is None:
        for_date = date.today()

    region = ALL_DISTRICTS.get(district, "Madhya")
    modifier = REGION_PRICE_MODIFIER.get(region, 0.0)

    base_price = product["base"]
    min_price, max_price = product["range"]

    # Region adjustment
    regional_base = int(base_price * (1 + modifier))
    regional_base = max(min_price, min(max_price, regional_base))

    # Daily variation: ±8% around regional base
    seed = get_seed(district, product["name"], for_date)
    rng = random.Random(seed)

    variation = rng.uniform(-0.08, 0.08)
    price = int(regional_base * (1 + variation))
    price = max(min_price, min(max_price, price))
    price = round(price / 50) * 50  # round to nearest 50

    # Min / Max spread
    spread_pct = rng.uniform(0.06, 0.12)
    p_min = int(price * (1 - spread_pct))
    p_max = int(price * (1 + spread_pct))
    p_min = round(p_min / 50) * 50
    p_max = round(p_max / 50) * 50

    # Yesterday's price (to calculate trend)
    yesterday = for_date - timedelta(days=1)
    seed_y = get_seed(district, product["name"], yesterday)
    rng_y = random.Random(seed_y)
    var_y = rng_y.uniform(-0.08, 0.08)
    yesterday_price = int(regional_base * (1 + var_y))
    yesterday_price = round(yesterday_price / 50) * 50

    change = price - yesterday_price
    if abs(change) < 30:
        trend = "STABLE"
        change = 0
    elif change > 0:
        trend = "UP"
    else:
        trend = "DOWN"

    return {
        "name":     product["name"],
        "category": product["category"],
        "price":    price,
        "min":      p_min,
        "max":      p_max,
        "unit":     product["unit"],
        "trend":    trend,
        "change":   change,
        "source":   "Generated (Agmarknet fallback)",
    }


def generate_district_data(district, for_date=None):
    """
    Ek district ke sabhi 20 products ka data generate karta hai.
    """
    if for_date is None:
        for_date = date.today()

    region = ALL_DISTRICTS.get(district, "Madhya")
    products = []

    for product in PRODUCT_CATALOG:
        p = generate_price(product, district, for_date)
        products.append(p)

    return {
        "mandi_name": f"{district} Krishi Upaj Mandi",
        "district":   district,
        "region":     region,
        "date":       for_date.strftime("%d-%m-%Y"),
        "products":   products,
    }


def generate_all_up_data(for_date=None):
    """
    UP ke sabhi 75 districts ka data generate karta hai.
    """
    if for_date is None:
        for_date = date.today()

    all_data = {}
    for district in sorted(ALL_DISTRICTS.keys()):
        all_data[district] = generate_district_data(district, for_date)

    return all_data


if __name__ == "__main__":
    from datetime import date
    data = generate_district_data("Lucknow")
    print(f"District: Lucknow | {data['date']}")
    print(f"Products: {len(data['products'])}")
    for p in data["products"]:
        trend = "▲" if p["trend"] == "UP" else ("▼" if p["trend"] == "DOWN" else "━")
        print(f"  {trend} {p['name']:<25} Rs {p['price']:>6}/Qtl  (Min:{p['min']} Max:{p['max']})")

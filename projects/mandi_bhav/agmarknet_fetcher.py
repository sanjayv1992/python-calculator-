"""
Agmarknet Data Fetcher
Government of India ka official agricultural market data portal
URL: https://agmarknet.gov.in

Yeh file real data fetch karti hai Agmarknet se.
Agar internet nahi hai ya site down hai — fallback data use hota hai.
"""

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import json
import os
import time

# ============================================================
# AGMARKNET API / SCRAPER
# ============================================================

AGMARKNET_BASE = "https://agmarknet.gov.in"
AGMARKNET_SEARCH = "https://agmarknet.gov.in/SearchCommodityWise.aspx"

# State code for UP on Agmarknet
STATE_CODE_UP = "34"

# Commodity codes on Agmarknet (common ones)
COMMODITY_CODES = {
    "Wheat":         "53",
    "Paddy":         "78",
    "Maize":         "64",
    "Potato":        "79",
    "Onion":         "23",
    "Tomato":        "52",
    "Arhar":         "3",
    "Moong":         "14",
    "Urad":          "51",
    "Masoor":        "13",
    "Mustard":       "70",
    "Sugarcane":     "47",
    "Garlic":        "20",
    "Ginger":        "21",
    "Turmeric":      "50",
    "Cauliflower":   "64",
    "Chana":         "7",
    "Barley":        "5",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": AGMARKNET_BASE,
}

CACHE_FILE = os.path.join(os.path.dirname(__file__), "data_cache", "agmarknet_cache.json")


def ensure_cache_dir():
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data):
    ensure_cache_dir()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_agmarknet_commodity(commodity_name, commodity_code, state_code="34"):
    """
    Agmarknet se ek commodity ka UP data fetch karta hai.
    Returns list of {district, market, price, min_price, max_price, date}
    """
    today = date.today().strftime("%d-%b-%Y")

    session = requests.Session()

    try:
        # Step 1: Main page load (viewstate lena)
        resp = session.get(AGMARKNET_SEARCH, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        viewstate = ""
        vs_tag = soup.find("input", {"id": "__VIEWSTATE"})
        if vs_tag:
            viewstate = vs_tag.get("value", "")

        evval = ""
        ev_tag = soup.find("input", {"id": "__EVENTVALIDATION"})
        if ev_tag:
            evval = ev_tag.get("value", "")

        vsg = ""
        vsg_tag = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})
        if vsg_tag:
            vsg = vsg_tag.get("value", "")

        # Step 2: POST request with form data
        form_data = {
            "__EVENTTARGET":          "",
            "__EVENTARGUMENT":        "",
            "__VIEWSTATE":            viewstate,
            "__VIEWSTATEGENERATOR":   vsg,
            "__EVENTVALIDATION":      evval,
            "cboState":               f"0{state_code}",
            "cboDistrict":            "0",
            "cboMarket":              "0",
            "txtDate":                today,
            "cboArrival":             commodity_code,
            "txtDateTo":              today,
            "Submit":                 "Go",
        }

        resp2 = session.post(AGMARKNET_SEARCH, data=form_data, headers=HEADERS, timeout=20)
        resp2.raise_for_status()

        return parse_agmarknet_table(resp2.text, commodity_name)

    except requests.exceptions.ConnectionError:
        return None, "Internet connection nahi hai"
    except requests.exceptions.Timeout:
        return None, "Agmarknet site respond nahi kar rahi (timeout)"
    except Exception as e:
        return None, str(e)


def parse_agmarknet_table(html, commodity_name):
    """HTML table parse karke structured data nikalta hai"""
    soup = BeautifulSoup(html, "lxml")
    results = []

    table = soup.find("table", {"id": "cphBody_GridPriceData"})
    if not table:
        table = soup.find("table", class_="tableagmark_new")

    if not table:
        return None, "Table nahi mili page mein"

    rows = table.find_all("tr")[1:]  # header skip

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 7:
            try:
                district = cols[0].text.strip()
                market   = cols[1].text.strip()
                variety  = cols[2].text.strip()
                group    = cols[3].text.strip()
                min_p    = float(cols[4].text.strip().replace(",", "") or 0)
                max_p    = float(cols[5].text.strip().replace(",", "") or 0)
                modal_p  = float(cols[6].text.strip().replace(",", "") or 0)

                if modal_p > 0 and district:
                    results.append({
                        "district": district,
                        "market":   market,
                        "commodity": commodity_name,
                        "variety":  variety,
                        "min_price":  int(min_p),
                        "max_price":  int(max_p),
                        "modal_price": int(modal_p),
                        "date":     date.today().strftime("%d-%m-%Y"),
                        "source":   "Agmarknet (Live)"
                    })
            except (ValueError, IndexError):
                continue

    if results:
        return results, "OK"
    return None, "Table empty hai — aaj ka data available nahi"


def fetch_all_up_commodities():
    """
    UP ke sabhi major commodities ka data fetch karta hai.
    Results cache mein save hote hain.
    """
    print("\n  Agmarknet se data fetch ho raha hai...")
    print("  (Yeh 2-3 minute le sakta hai — sabar rakho!)\n")

    cache = load_cache()
    today = date.today().isoformat()
    all_results = {}
    errors = []

    for commodity_name, code in COMMODITY_CODES.items():
        cache_key = f"{today}_{commodity_name}"

        if cache_key in cache:
            print(f"  [CACHE]  {commodity_name:<15} — cached data use ho raha hai")
            all_results[commodity_name] = cache[cache_key]
            continue

        print(f"  [FETCH]  {commodity_name:<15} — downloading...", end="", flush=True)
        data, msg = fetch_agmarknet_commodity(commodity_name, code)

        if data:
            print(f"  {len(data)} records mile")
            all_results[commodity_name] = data
            cache[cache_key] = data
        else:
            print(f"  FAILED: {msg}")
            errors.append(f"{commodity_name}: {msg}")

        time.sleep(1.5)  # server pe load na daalo

    save_cache(cache)

    if errors:
        print(f"\n  {len(errors)} commodities fetch nahi hue:")
        for e in errors:
            print(f"    - {e}")

    return all_results


def get_district_data_from_agmarknet(district_name):
    """
    Cache se specific district ka data nikalta hai.
    Returns dict: {commodity -> {min, max, modal, source}}
    """
    cache = load_cache()
    today = date.today().isoformat()
    district_data = {}

    for commodity_name in COMMODITY_CODES:
        cache_key = f"{today}_{commodity_name}"
        if cache_key in cache:
            for entry in cache[cache_key]:
                if district_name.lower() in entry.get("district", "").lower():
                    district_data[commodity_name] = {
                        "min_price":   entry["min_price"],
                        "max_price":   entry["max_price"],
                        "modal_price": entry["modal_price"],
                        "market":      entry.get("market", ""),
                        "source":      "Agmarknet (Live)",
                    }
                    break

    return district_data


def test_connection():
    """Agmarknet se connectivity check karta hai"""
    try:
        r = requests.get(AGMARKNET_BASE, headers=HEADERS, timeout=10)
        return r.status_code == 200, f"Status: {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Internet nahi hai"
    except requests.exceptions.Timeout:
        return False, "Site timeout"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    print("Agmarknet connection test...")
    ok, msg = test_connection()
    if ok:
        print(f"  Connected! {msg}")
        print("  Wheat ka data fetch karte hain UP se...")
        data, status = fetch_agmarknet_commodity("Wheat", "53", "34")
        if data:
            print(f"  {len(data)} records mile!")
            for row in data[:5]:
                print(f"  {row['district']:<20} {row['market']:<20} Rs {row['modal_price']}")
        else:
            print(f"  Error: {status}")
    else:
        print(f"  Connection fail: {msg}")

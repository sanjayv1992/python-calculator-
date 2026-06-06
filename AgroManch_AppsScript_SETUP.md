# 🌾 AgroManch — Google Apps Script Setup (5 मिनट)

यह script आपकी Google Sheet में रोज़ का content **अपने आप** दिखाता है और **live मंडी भाव** भी लाता है।

---

## 📥 Step 1 — Workbook को Google Sheets में import करो
1. [sheets.google.com](https://sheets.google.com) खोलो → **Blank** sheet बनाओ
2. **File → Import → Upload** → `AgroManch_Content_Factory.xlsx` चुनो
3. "Import location" में **"Insert new sheet(s)"** select करो → **Import data**
4. अब सारे 20 tabs आपकी sheet में आ गए ✅

## ⚙️ Step 2 — Script जोड़ो
1. **Extensions → Apps Script** खोलो
2. वहाँ का पुराना code हटाओ → `AgroManch_AppsScript.gs` का **पूरा code paste** करो
3. ऊपर **💾 Save** दबाओ
4. एक बार **▶️ Run** दबाओ → Google permission माँगेगा → **Allow** करो
   *(पहली बार "unsafe" warning आए तो: Advanced → Go to project → Allow)*

## 🔄 Step 3 — इस्तेमाल करो
1. Google Sheet **reload** करो (F5)
2. ऊपर menu bar में नया **🌾 AgroManch** menu दिखेगा
3. क्लिक करो:
   - **⚡ आज का Content दिखाओ** → एक नया `⚡ Today` tab बनता है जिसमें आज का **Reel + Post + Plan** सब एक जगह
   - **📅 किसी भी दिन का Content** → कोई भी Day (1–365) देखो
   - **💹 मंडी भाव लाओ (Live)** → फसल का नाम डालो, live भाव आ जाएँगे

---

## 💹 मंडी भाव (Live) — एक बार setup
1. [data.gov.in](https://data.gov.in) पर **free account** बनाओ
2. **My Account → API Key** copy करो
3. Apps Script में ऊपर इस line में paste करो:
   ```js
   var DATA_GOV_API_KEY = "यहाँ-अपनी-key";
   ```
4. Save → अब "💹 मंडी भाव लाओ" काम करेगा
   *(key के बिना भी एक public demo key try होती है, पर वो rate-limited है)*

फसल नाम English में डालो: `Wheat`, `Paddy`, `Onion`, `Tomato`, `Potato`, `Soybean` आदि।

---

## 🛠️ Config (script के ऊपर)
| Setting | मतलब | Default |
|---|---|---|
| `START_DATE` | Calendar का Day 1 कौन सी तारीख है | 7 June 2026 |
| `DATA_GOV_API_KEY` | मंडी भाव API key | खाली (demo key) |

> Calendar 365 दिन में अपने आप **wrap** होता है — साल खत्म होने पर फिर Day 1 से शुरू। तारीख बदलते ही "आज का Content" अपने आप अगले दिन का दिखाने लगता है।

---

## ❓ अगर menu न दिखे
- Sheet को reload करो (F5)
- Apps Script में एक बार `onOpen` function manually Run करो
- Tab नाम वैसे ही होने चाहिए जैसे XLSX में हैं (emoji सहित) — import करते वक्त नाम मत बदलो

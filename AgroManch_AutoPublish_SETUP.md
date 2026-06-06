# 🚀 AgroManch Auto-Publish — Setup Guide

रोज़ अपने आप **WhatsApp digest** भेजो और **Instagram/YouTube** पर post/schedule करो।

> ⚠️ **असलियत पहले समझो:** ये platforms (Meta, Google) सीधे API से auto-posting सिर्फ़ **Business accounts** और **approved tokens** के साथ देते हैं। नीचे हर एक लेने का तरीका है। एक बार setup, फिर रोज़ अपने आप।

---

## 📦 इंस्टॉल
1. अपनी AgroManch Google Sheet खोलो → **Extensions → Apps Script**
2. **+ → Script** से नई file बनाओ → `AgroManch_AutoPublish.gs` का पूरा code paste करो → Save
3. ऊपर `CFG` block में अपनी details भरो (नीचे हर field समझाई है)
4. Sheet reload → नया menu **🚀 AgroManch Auto** दिखेगा

---

## 📲 PART A — WhatsApp रोज़ auto-message

### क्या चाहिए (WhatsApp Cloud API — FREE tier)
1. [developers.facebook.com](https://developers.facebook.com) → **My Apps → Create App → Business**
2. App में **WhatsApp** product add करो
3. वहाँ से मिलेंगे:
   - **Phone number ID** → `CFG.WA_PHONE_ID` में डालो
   - **Temporary token** (24h) — टेस्ट के लिए। Permanent के लिए: **Business Settings → System User → token generate** (`whatsapp_business_messaging` permission) → `CFG.WA_TOKEN`
4. **Recipients**: जिन numbers पर भेजना है (country code सहित, `+` नहीं) → `CFG.WA_RECIPIENTS`
   - उदा. `["919876543210", "918887776655"]`

### ज़रूरी नियम
- किसी को **पहली बार** message करने के लिए **approved Template** चाहिए (`sendWhatsAppTemplate`).
- अगर user ने आपको पिछले **24 घंटे** में message किया है, तो साधारण text (`sendWhatsAppText`) चलेगा — digest इसी से जाता है।
- बड़े **community broadcast** के लिए WhatsApp **Business API + opt-in** चाहिए (spam नियम सख्त हैं)।

### चालू करो
- Menu → **⏰ रोज़ auto-run चालू करो** → रोज़ सुबह 7 बजे (CFG.DAILY_HOUR) digest अपने आप जाएगा
- अभी टेस्ट: Menu → **📲 अभी WhatsApp digest भेजो**

---

## 📸 PART B — Instagram auto-publish

### क्या चाहिए (Meta Graph API)
1. **Instagram account** को **Business/Creator** बनाओ → किसी **Facebook Page** से connect करो
2. ऊपर वाली ही Meta App में **Instagram Graph API** add करो
3. [Graph API Explorer](https://developers.facebook.com/tools/explorer/) से **long-lived Page Access Token** लो
   (permissions: `instagram_basic`, `instagram_content_publish`, `pages_show_list`)
4. अपना **Instagram Business Account ID** निकालो (Graph API से) → `CFG.IG_USER_ID`
5. Token → `CFG.IG_TOKEN`

### Media का PUBLIC URL ज़रूरी
Instagram API सीधे file upload नहीं लेता — image/reel का **public URL** चाहिए। आसान तरीका:
- Image/Reel को **Google Drive** में डालो → "Anyone with link" → या किसी hosting (Cloudinary/Imgur/अपनी site) पर
- वो URL `publishInstagram(mediaUrl, caption, isReel)` को दो

### इस्तेमाल
- Menu → **📸 Instagram पर post करो** → media URL डालो → आज का caption + hashtags अपने आप लगकर publish
- `.mp4` URL = Reel, `.jpg/.png` = photo (script खुद पहचान लेता है)

> **Scheduling:** Instagram API "तय समय" पर खुद publish नहीं करता — इसलिए हम **daily trigger** से सही समय पर publish चलाते हैं। तय समय चाहिए तो `dailyAutoRun` में IG line uncomment करके media URL sheet में डालो।

---

## ▶️ PART C — YouTube upload + schedule

### क्या चाहिए
1. Apps Script editor में बायीं ओर **Services (➕)** → **YouTube Data API v3** → **Add**
2. पहली बार चलाने पर Google **YouTube permission** माँगेगा → Allow
3. जो video upload/schedule करनी है उसे **Google Drive** में रखो → उसका **File ID** लो
   (Drive में file खोलो → URL में `/d/` के बाद का हिस्सा = File ID)

### इस्तेमाल
- Menu → **▶️ YouTube schedule करो** →
  1. Drive video **File ID** डालो
  2. **publish समय** डालो (ISO): `2026-06-10T17:00:00+05:30` (शाम 5 बजे IST)
     - खाली छोड़ोगे = तुरंत **private** upload
- Title/description/tags आज की reel row से अपने आप बन जाते हैं
- तय समय पर YouTube खुद video **public** कर देगा ✅

### पहले से uploaded video schedule करनी है?
`scheduleYouTubeVideo("VIDEO_ID", "2026-06-10T17:00:00+05:30")` चलाओ।

---

## 🔧 CONFIG cheat-sheet

| Field | क्या डालें | कहाँ से |
|---|---|---|
| `WA_TOKEN` | WhatsApp permanent token | Meta App → System User |
| `WA_PHONE_ID` | Phone number ID | Meta App → WhatsApp → API Setup |
| `WA_RECIPIENTS` | भेजने वाले numbers | खुद के/team के (opt-in) |
| `WA_TEMPLATE` | approved template नाम | Meta → WhatsApp Manager → Templates |
| `IG_TOKEN` | long-lived page token | Graph API Explorer |
| `IG_USER_ID` | IG Business account ID | Graph API |
| `DAILY_HOUR` | auto-run का घंटा | आपकी पसंद (24h) |

---

## 🧪 टेस्ट क्रम (recommended)
1. `CFG` भरो → Menu → **🧪 Test: आज की row दिखाओ** (data सही आ रहा?)
2. Menu → **📲 अभी WhatsApp digest भेजो** (अपने number पर)
3. Instagram एक image URL से try करो
4. YouTube एक छोटी video Drive से try करो
5. सब ठीक → Menu → **⏰ रोज़ auto-run चालू करो**

## ❓ दिक्कतें
- **WhatsApp नहीं गया** → token expire (24h temp), या recipient ने opt-in नहीं किया → template भेजो पहले
- **Instagram error** → media URL public नहीं, या Reel encode हो रहा (script 20s रुकता है, बड़ी video पर और रुको)
- **YouTube error** → "YouTube Data API v3" advanced service enable नहीं, या Drive File ID गलत
- सारे auto-run के नतीजे **"📜 Auto Log"** tab में दिखते हैं

> ⚖️ हर platform के **API नियम + rate limits** का पालन करो। WhatsApp पर बिना opt-in bulk broadcast block हो सकता है। यह setup आपके **अपने verified accounts** के लिए है।

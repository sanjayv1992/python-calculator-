/***********************************************************************
 * AgroManch — Daily Content Automation (Google Apps Script)
 * =====================================================================
 * इसे अपनी Google Sheet में जोड़ने का तरीका:
 *   1. AgroManch_Content_Factory.xlsx को Google Sheets में import करो
 *      (File → Import → Upload → "Insert new sheet(s)")
 *   2. Extensions → Apps Script खोलो
 *   3. पूरा code copy-paste करो → Save (💾) → Run एक बार (permission दो)
 *   4. Sheet reload करो — ऊपर नया menu "🌾 AgroManch" दिखेगा
 *
 * Features:
 *   • 🌾 AgroManch → "आज का Content दिखाओ"  → एक "⚡ Today" sheet बनाता है
 *     जिसमें आज का Reel + Post + Calendar row अपने आप आ जाता है।
 *   • हर दिन date बदलते ही नया content (365-day rotation)।
 *   • मंडी भाव (live) — data.gov.in API से (नीचे API key डालो)।
 ***********************************************************************/

// ── CONFIG ───────────────────────────────────────────────────────────
// Calendar किस तारीख से शुरू होता है (Day 1)। XLSX में यही default है:
var START_DATE = new Date(2026, 5, 7);   // 7 June 2026 (month 0-based: 5 = June)

// मंडी भाव के लिए FREE API key यहाँ से लो: https://data.gov.in (Sign up → My Account → API key)
var DATA_GOV_API_KEY = "";   // <-- यहाँ अपनी key paste करो (खाली रखोगे तो demo key try होगी)

// Sheet tab नाम (XLSX जैसे ही — emoji के साथ)
var SH_REEL = "🎬 Daily Reel Generator";
var SH_POST = "📝 Daily Post Generator";
var SH_CAL  = "🗓️ 365-Day Calendar";
var SH_TODAY = "⚡ Today";
var SH_MANDI = "💹 Mandi Bhav (Live)";

// ── MENU ─────────────────────────────────────────────────────────────
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("🌾 AgroManch")
    .addItem("⚡ आज का Content दिखाओ", "showToday")
    .addItem("📅 किसी भी दिन का Content", "showByDayPrompt")
    .addSeparator()
    .addItem("💹 मंडी भाव लाओ (Live)", "fetchMandiPrompt")
    .addItem("ℹ️ मदद / Setup", "showHelp")
    .addToUi();
}

// ── HELPERS ──────────────────────────────────────────────────────────
function _ss() { return SpreadsheetApp.getActiveSpreadsheet(); }

function _todayDayIndex() {
  var now = new Date();
  var t0 = new Date(START_DATE.getFullYear(), START_DATE.getMonth(), START_DATE.getDate());
  var t1 = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var diff = Math.floor((t1 - t0) / (1000 * 60 * 60 * 24));
  var idx = ((diff % 365) + 365) % 365;   // 0..364, wraps yearly, handles pre-start dates
  return idx + 1;                          // 1..365
}

// किसी sheet में Day-number (column 1, data row 4 से) के हिसाब से row निकालो
function _rowByDay(sheetName, day) {
  var sh = _ss().getSheetByName(sheetName);
  if (!sh) return null;
  var values = sh.getDataRange().getValues();
  // header row 3 (index 2) → data starts index 3
  for (var i = 3; i < values.length; i++) {
    if (Number(values[i][0]) === Number(day)) return values[i];
  }
  return null;
}

function _ensureSheet(name) {
  var ss = _ss();
  var sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name, 0);
  else { sh.clear(); ss.setActiveSheet(sh); ss.moveActiveSheet(1); }
  return sh;
}

function _style(sh, r, c, val, bg, fc, bold, size) {
  var cell = sh.getRange(r, c);
  cell.setValue(val);
  if (bg) cell.setBackground(bg);
  cell.setFontColor(fc || "#000000");
  cell.setFontWeight(bold ? "bold" : "normal");
  cell.setFontSize(size || 10);
  cell.setWrap(true);
  cell.setVerticalAlignment("middle");
}

// ── MAIN: TODAY DASHBOARD ────────────────────────────────────────────
function showToday() { _renderDay(_todayDayIndex(), true); }

function showByDayPrompt() {
  var ui = SpreadsheetApp.getUi();
  var res = ui.prompt("Day number डालो (1 से 365):", ui.ButtonSet.OK_CANCEL);
  if (res.getSelectedButton() !== ui.Button.OK) return;
  var d = parseInt(res.getResponseText(), 10);
  if (isNaN(d) || d < 1 || d > 365) { ui.alert("कृपया 1 से 365 के बीच number डालो।"); return; }
  _renderDay(d, false);
}

function _renderDay(day, isToday) {
  var reel = _rowByDay(SH_REEL, day);
  var post = _rowByDay(SH_POST, day);
  var cal  = _rowByDay(SH_CAL,  day);
  if (!reel && !post && !cal) {
    SpreadsheetApp.getUi().alert(
      "Content sheets नहीं मिले। पहले AgroManch_Content_Factory.xlsx import करो " +
      "(tabs: '🎬 Daily Reel Generator', '📝 Daily Post Generator', '🗓️ 365-Day Calendar').");
    return;
  }
  var sh = _ensureSheet(SH_TODAY);
  sh.setHiddenGridlines(true);
  var dateStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd-MM-yyyy");

  // Title
  sh.getRange("A1:B1").merge();
  _style(sh, 1, 1, "🌾  आज का AgroManch Content  —  Day " + day + (isToday ? "  (" + dateStr + ")" : ""),
         "#1B5E20", "#FFFFFF", true, 15);
  sh.setRowHeight(1, 38);

  var r = 3;
  function section(title, color) {
    sh.getRange(r, 1, 1, 2).merge();
    _style(sh, r, 1, title, color, "#FFFFFF", true, 12);
    sh.setRowHeight(r, 26); r++;
  }
  function kv(k, v, bg) {
    _style(sh, r, 1, k, bg || "#F5F5F5", "#1B5E20", true, 10);
    _style(sh, r, 2, v || "—", "#FFFFFF", "#000000", false, 10);
    sh.setRowHeight(r, 38); r++;
  }

  if (cal) {
    section("🗓️  आज का Plan", "#0D47A1");
    kv("Weekday / Week", (cal[2] || "") + "  |  " + (cal[3] || ""));
    kv("Month Theme", cal[4]);
    kv("Pattern", cal[6]);
    kv("Topic", cal[7]);
    kv("Platform Mix", cal[9]);
    kv("Objective", cal[11]);
    kv("Psych Trigger", cal[12]);
    if (cal[13]) kv("🎉 Festival/Season", cal[13], "#FFF9C4");
  }

  if (reel) {
    section("🎬  आज का Reel", "#E65100");
    kv("Hook (0-3s)", reel[3], "#FFE0B2");
    kv("Shot 1", reel[4]); kv("Shot 2", reel[5]); kv("Shot 3", reel[6]);
    kv("Shot 4", reel[7]); kv("Shot 5", reel[8]);
    kv("Voiceover", reel[9]);
    kv("On-Screen Text", reel[10]);
    kv("CTA", reel[11], "#C8E6C9");
    kv("Hashtags", reel[12]);
    kv("Audio Idea", reel[13]);
    kv("Best Time", reel[14], "#FFF9C4");
  }

  if (post) {
    section("📝  आज का Post", "#4A148C");
    kv("Format", post[2]);
    kv("Headline", post[4], "#E1BEE7");
    kv("Body Copy", post[5]);
    kv("Layout / Slides", post[6]);
    kv("CTA", post[7], "#C8E6C9");
    kv("Hashtags", post[8]);
    kv("Image Prompt Type", post[9]);
    kv("Best Time", post[10], "#FFF9C4");
  }

  sh.setColumnWidth(1, 170);
  sh.setColumnWidth(2, 640);
  sh.getRange(1, 1, r, 2).setBorder(true, true, true, true, true, true, "#BBBBBB", SpreadsheetApp.BorderStyle.SOLID);
  _ss().setActiveSheet(sh);
}

// ── MANDI PRICE (LIVE) ───────────────────────────────────────────────
function fetchMandiPrompt() {
  var ui = SpreadsheetApp.getUi();
  var res = ui.prompt("फसल का नाम (English में, जैसे: Wheat, Onion, Tomato, Potato):", ui.ButtonSet.OK_CANCEL);
  if (res.getSelectedButton() !== ui.Button.OK) return;
  var commodity = (res.getResponseText() || "").trim();
  if (!commodity) { ui.alert("फसल का नाम ज़रूरी है।"); return; }
  fetchMandiPrice(commodity);
}

function fetchMandiPrice(commodity) {
  var ui = SpreadsheetApp.getUi();
  var key = DATA_GOV_API_KEY || "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"; // public sample key (rate-limited)
  var resource = "9ef84268-d588-465a-a308-a864a43d0070"; // Daily mandi prices
  var url = "https://api.data.gov.in/resource/" + resource +
            "?api-key=" + key + "&format=json&limit=30" +
            "&filters%5Bcommodity%5D=" + encodeURIComponent(commodity);
  try {
    var resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var data = JSON.parse(resp.getContentText());
    var recs = data.records || [];
    var sh = _ensureSheet(SH_MANDI);
    sh.setHiddenGridlines(true);
    sh.getRange("A1:G1").merge();
    _style(sh, 1, 1, "💹  मंडी भाव (Live) — " + commodity + "   [" +
           Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd-MM-yyyy HH:mm") + "]",
           "#B71C1C", "#FFFFFF", true, 14);
    sh.setRowHeight(1, 32);
    var heads = ["State", "District", "Market", "Variety", "Min ₹/Q", "Max ₹/Q", "Modal ₹/Q"];
    for (var c = 0; c < heads.length; c++)
      _style(sh, 3, c + 1, heads[c], "#1B5E20", "#FFFFFF", true, 10);
    if (recs.length === 0) {
      sh.getRange("A4:G4").merge();
      _style(sh, 4, 1, "इस फसल का आज का data नहीं मिला। दूसरी फसल या spelling try करो (जैसे Wheat, Paddy(Dhan), Onion).",
             "#FFF9C4", "#000000", false, 10);
    } else {
      for (var i = 0; i < recs.length; i++) {
        var x = recs[i], row = 4 + i, bg = i % 2 ? "#FFCDD2" : "#FFFFFF";
        _style(sh, row, 1, x.state, bg); _style(sh, row, 2, x.district, bg);
        _style(sh, row, 3, x.market, bg); _style(sh, row, 4, x.variety, bg);
        _style(sh, row, 5, x.min_price, bg, "#000000", false, 10);
        _style(sh, row, 6, x.max_price, bg, "#000000", false, 10);
        _style(sh, row, 7, x.modal_price, bg, "#B71C1C", true, 10);
      }
    }
    [120, 110, 140, 130, 80, 80, 90].forEach(function (w, idx) { sh.setColumnWidth(idx + 1, w); });
    _ss().setActiveSheet(sh);
  } catch (e) {
    ui.alert("मंडी भाव लाने में दिक्कत: " + e + "\n\nApna FREE API key data.gov.in से लेकर ऊपर DATA_GOV_API_KEY में डालो।");
  }
}

// ── HELP ─────────────────────────────────────────────────────────────
function showHelp() {
  var msg =
    "🌾 AgroManch Daily Content Automation\n\n" +
    "1) ⚡ आज का Content दिखाओ — आज का Reel + Post + Plan एक जगह।\n" +
    "2) 📅 किसी भी दिन का Content — कोई भी Day (1-365) देखो।\n" +
    "3) 💹 मंडी भाव लाओ — live भाव (data.gov.in API key चाहिए)।\n\n" +
    "Setup: AgroManch_Content_Factory.xlsx को Google Sheets में import करो, " +
    "फिर Extensions → Apps Script में यह code paste करो।\n\n" +
    "मंडी भाव के लिए: data.gov.in पर free account बनाओ → API key लो → " +
    "ऊपर DATA_GOV_API_KEY में paste करो।";
  SpreadsheetApp.getUi().alert(msg);
}

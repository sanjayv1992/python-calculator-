/***********************************************************************
 * AgroManch — Auto-Publish Engine (Google Apps Script)
 * =====================================================================
 * रोज़ अपने आप:
 *   • WhatsApp पर आज का content digest भेजना (WhatsApp Cloud API)
 *   • Instagram पर image/Reel publish करना (Meta Graph API)
 *   • YouTube पर video upload/schedule करना (YouTube Data API)
 *
 * इसे पिछली sheet (AgroManch_Content_Factory) के Apps Script में
 * जोड़ो — यह उसी "🎬 Daily Reel / 📝 Daily Post / 🗓️ 365-Day Calendar"
 * data को इस्तेमाल करता है।
 *
 * Setup guide: AgroManch_AutoPublish_SETUP.md देखो।
 ***********************************************************************/

// ══════════════════════════════════════════════════════════════════════
// CONFIG — अपनी details यहाँ भरो (guide में हर एक लेने का तरीका है)
// ══════════════════════════════════════════════════════════════════════
var CFG = {
  // Calendar Day 1 की तारीख (Content Factory जैसी)
  START_DATE: new Date(2026, 5, 7),            // 7 June 2026

  // रोज़ किस समय auto-run चले (24h, घंटा)
  DAILY_HOUR: 7,                               // सुबह 7 बजे

  // ---- WhatsApp Cloud API (Meta) ----
  WA_TOKEN:        "",                         // permanent access token
  WA_PHONE_ID:     "",                         // phone number ID
  WA_RECIPIENTS:   ["91XXXXXXXXXX"],           // किन numbers पर भेजना (country code सहित, + नहीं)
  WA_TEMPLATE:     "",                         // approved template name (पहले message के लिए ज़रूरी)
  WA_LANG:         "hi",                       // template language

  // ---- Instagram (Meta Graph API) ----
  IG_TOKEN:        "",                         // long-lived page access token
  IG_USER_ID:      "",                         // Instagram Business account ID
  // image/reel का PUBLIC URL कहाँ से आएगा — आप daily post में media URL डालो
  // (नीचे publishInstagram में manually या sheet से)

  // ---- YouTube ----
  YT_DEFAULT_PRIVACY: "private",               // upload के बाद की privacy (scheduled के लिए private)

  GRAPH_VER: "v21.0",
};

// Sheet tab नाम (Content Factory जैसे)
var T_REEL = "🎬 Daily Reel Generator";
var T_POST = "📝 Daily Post Generator";
var T_CAL  = "🗓️ 365-Day Calendar";

// ══════════════════════════════════════════════════════════════════════
// MENU
// ══════════════════════════════════════════════════════════════════════
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("🚀 AgroManch Auto")
    .addItem("⏰ रोज़ auto-run चालू करो", "installDailyTrigger")
    .addItem("⏹️ auto-run बंद करो", "removeDailyTrigger")
    .addSeparator()
    .addItem("📲 अभी WhatsApp digest भेजो", "sendWhatsAppDailyDigest")
    .addItem("📸 Instagram पर post करो (prompt)", "publishInstagramPrompt")
    .addItem("▶️ YouTube schedule करो (prompt)", "scheduleYouTubePrompt")
    .addSeparator()
    .addItem("🧪 Test: आज की row दिखाओ", "testTodayRow")
    .addItem("ℹ️ मदद / Setup", "autoHelp")
    .addToUi();
}

// ══════════════════════════════════════════════════════════════════════
// SHARED — आज की row
// ══════════════════════════════════════════════════════════════════════
function _ssA() { return SpreadsheetApp.getActiveSpreadsheet(); }

function _dayIndex() {
  var s = CFG.START_DATE, n = new Date();
  var t0 = new Date(s.getFullYear(), s.getMonth(), s.getDate());
  var t1 = new Date(n.getFullYear(), n.getMonth(), n.getDate());
  var diff = Math.floor((t1 - t0) / 86400000);
  return (((diff % 365) + 365) % 365) + 1;
}

function _row(tab, day) {
  var sh = _ssA().getSheetByName(tab);
  if (!sh) return null;
  var v = sh.getDataRange().getValues();
  for (var i = 3; i < v.length; i++) if (Number(v[i][0]) === Number(day)) return v[i];
  return null;
}

function _todayBundle() {
  var d = _dayIndex();
  return { day: d, reel: _row(T_REEL, d), post: _row(T_POST, d), cal: _row(T_CAL, d) };
}

// ══════════════════════════════════════════════════════════════════════
// DAILY TRIGGER
// ══════════════════════════════════════════════════════════════════════
function installDailyTrigger() {
  removeDailyTrigger();
  ScriptApp.newTrigger("dailyAutoRun")
    .timeBased().everyDays(1).atHour(CFG.DAILY_HOUR).create();
  SpreadsheetApp.getUi().alert("✅ रोज़ सुबह " + CFG.DAILY_HOUR + " बजे auto-run चालू हो गया।");
}

function removeDailyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === "dailyAutoRun") ScriptApp.deleteTrigger(t);
  });
}

// रोज़ चलने वाला main job
function dailyAutoRun() {
  var b = _todayBundle();
  if (!b.reel && !b.post) { _log("कोई content row नहीं मिली Day " + b.day); return; }
  // 1) WhatsApp digest (हमेशा — सबसे ज़रूरी viral channel)
  try { _waSendDigest(b); } catch (e) { _log("WA error: " + e); }
  // 2) Instagram — अगर post sheet में media URL column है तो auto-publish
  //    (default बंद; guide देखकर media URL का इंतज़ाम करने पर चालू करो)
  // try { _igAutoFromSheet(b); } catch (e) { _log("IG error: " + e); }
  _log("✅ dailyAutoRun done — Day " + b.day);
}

function _log(msg) {
  console.log(msg);
  var sh = _ssA().getSheetByName("📜 Auto Log") || _ssA().insertSheet("📜 Auto Log");
  sh.appendRow([new Date(), msg]);
}

// ══════════════════════════════════════════════════════════════════════
// WHATSAPP — Cloud API
// ══════════════════════════════════════════════════════════════════════
function sendWhatsAppDailyDigest() {
  var b = _todayBundle();
  if (!b.reel && !b.post) { SpreadsheetApp.getUi().alert("आज की content row नहीं मिली।"); return; }
  var res = _waSendDigest(b);
  SpreadsheetApp.getUi().alert("📲 WhatsApp भेजा गया।\n\n" + res);
}

function _digestText(b) {
  var r = b.reel || [], p = b.post || [], c = b.cal || [];
  var lines = [];
  lines.push("🌾 *AgroManch — आज का Content* (Day " + b.day + ")");
  if (c.length) { lines.push("📅 Theme: " + (c[4] || "") ); lines.push("🎯 Pattern: " + (c[6] || "")); }
  if (r.length) {
    lines.push("\n🎬 *Reel Hook:* " + (r[3] || ""));
    lines.push("🗣️ VO: " + (r[9] || ""));
    lines.push("📣 CTA: " + (r[11] || ""));
    lines.push("#️⃣ " + (r[12] || ""));
    lines.push("⏰ Time: " + (r[14] || ""));
  }
  if (p.length) {
    lines.push("\n📝 *Post:* " + (p[4] || ""));
    lines.push("📣 CTA: " + (p[7] || ""));
  }
  lines.push("\n📲 AgroManch App download करो — link bio 👇");
  return lines.join("\n");
}

function _waSendDigest(b) {
  if (!CFG.WA_TOKEN || !CFG.WA_PHONE_ID) return "⚠️ WA_TOKEN / WA_PHONE_ID सेट नहीं हैं।";
  var text = _digestText(b);
  var out = [];
  CFG.WA_RECIPIENTS.forEach(function (to) {
    out.push(to + ": " + sendWhatsAppText(to, text));
  });
  return out.join("\n");
}

// साधारण text message (24-घंटे window में reply पर allowed)
function sendWhatsAppText(to, text) {
  var url = "https://graph.facebook.com/" + CFG.GRAPH_VER + "/" + CFG.WA_PHONE_ID + "/messages";
  var payload = {
    messaging_product: "whatsapp",
    to: String(to),
    type: "text",
    text: { preview_url: false, body: text }
  };
  return _post(url, payload, CFG.WA_TOKEN);
}

// Template message (किसी को पहली बार message करने के लिए ज़रूरी — approved template चाहिए)
function sendWhatsAppTemplate(to, templateName, lang) {
  var url = "https://graph.facebook.com/" + CFG.GRAPH_VER + "/" + CFG.WA_PHONE_ID + "/messages";
  var payload = {
    messaging_product: "whatsapp",
    to: String(to),
    type: "template",
    template: { name: templateName, language: { code: lang || CFG.WA_LANG } }
  };
  return _post(url, payload, CFG.WA_TOKEN);
}

// ══════════════════════════════════════════════════════════════════════
// INSTAGRAM — Graph API (image या Reel)
// ══════════════════════════════════════════════════════════════════════
function publishInstagramPrompt() {
  var ui = SpreadsheetApp.getUi();
  var m = ui.prompt("Media का PUBLIC URL (image .jpg या reel .mp4):", ui.ButtonSet.OK_CANCEL);
  if (m.getSelectedButton() !== ui.Button.OK) return;
  var mediaUrl = (m.getResponseText() || "").trim();
  if (!mediaUrl) { ui.alert("Media URL ज़रूरी है।"); return; }
  var b = _todayBundle();
  var caption = _igCaption(b);
  var isReel = /\.mp4($|\?)/i.test(mediaUrl);
  var res = publishInstagram(mediaUrl, caption, isReel);
  ui.alert("📸 Instagram:\n\n" + res);
}

function _igCaption(b) {
  var p = b.post || [], r = b.reel || [];
  var head = (p[4] || r[3] || "AgroManch");
  var body = (p[5] || r[9] || "");
  var cta  = (p[7] || r[11] || "");
  var tags = (p[8] || r[12] || "#Kisan #AgroManch");
  return head + "\n\n" + body + "\n\n" + cta + "\n\n" + tags;
}

// image_url या video_url से publish (दो-step: container → publish)
function publishInstagram(mediaUrl, caption, isReel) {
  if (!CFG.IG_TOKEN || !CFG.IG_USER_ID) return "⚠️ IG_TOKEN / IG_USER_ID सेट नहीं हैं।";
  var base = "https://graph.facebook.com/" + CFG.GRAPH_VER + "/" + CFG.IG_USER_ID + "/media";
  var p1 = { caption: caption, access_token: CFG.IG_TOKEN };
  if (isReel) { p1.media_type = "REELS"; p1.video_url = mediaUrl; }
  else { p1.image_url = mediaUrl; }
  var c = JSON.parse(_postForm(base, p1));
  if (!c.id) return "container बनाने में दिक्कत: " + JSON.stringify(c);

  // Reels को encode होने में वक़्त लगता है — थोड़ा रुको
  if (isReel) Utilities.sleep(20000);

  var pub = "https://graph.facebook.com/" + CFG.GRAPH_VER + "/" + CFG.IG_USER_ID + "/media_publish";
  var r = JSON.parse(_postForm(pub, { creation_id: c.id, access_token: CFG.IG_TOKEN }));
  return r.id ? "✅ Published! Media ID: " + r.id : "publish error: " + JSON.stringify(r);
}

// ══════════════════════════════════════════════════════════════════════
// YOUTUBE — Data API (advanced service "YouTube" enable करना है)
// ══════════════════════════════════════════════════════════════════════
function scheduleYouTubePrompt() {
  var ui = SpreadsheetApp.getUi();
  var f = ui.prompt("Google Drive video File ID:", ui.ButtonSet.OK_CANCEL);
  if (f.getSelectedButton() !== ui.Button.OK) return;
  var fileId = (f.getResponseText() || "").trim();
  if (!fileId) { ui.alert("File ID ज़रूरी है।"); return; }

  var w = ui.prompt("कब publish करना है? (ISO, जैसे 2026-06-10T17:00:00+05:30)\nखाली छोड़ोगे तो तुरंत private upload होगा:", ui.ButtonSet.OK_CANCEL);
  if (w.getSelectedButton() !== ui.Button.OK) return;
  var publishAt = (w.getResponseText() || "").trim();

  var b = _todayBundle();
  var meta = _ytMeta(b);
  var res = uploadYouTubeFromDrive(fileId, meta.title, meta.desc, meta.tags, publishAt);
  ui.alert("▶️ YouTube:\n\n" + res);
}

function _ytMeta(b) {
  var r = b.reel || [], c = b.cal || [];
  var title = (r[3] || "AgroManch") + " | AgroManch";
  if (title.length > 95) title = title.substring(0, 95);
  var desc = (r[9] || "") + "\n\n" + (r[11] || "") + "\n\n📲 AgroManch App download करो।\n\n" +
             "#Kisan #AgroManch #Farming #IndianFarmer #Kheti";
  var tags = ["Kisan", "AgroManch", "Farming", "IndianFarmer", "Kheti",
              "खेती", "किसान", String(c[6] || "agriculture")];
  return { title: title, desc: desc, tags: tags };
}

// Drive के video file को YouTube पर upload + (optional) schedule
function uploadYouTubeFromDrive(driveFileId, title, description, tags, publishAtISO) {
  try {
    var file = DriveApp.getFileById(driveFileId);
    var blob = file.getBlob();
    var status = { privacyStatus: publishAtISO ? "private" : CFG.YT_DEFAULT_PRIVACY, selfDeclaredMadeForKids: false };
    if (publishAtISO) status.publishAt = new Date(publishAtISO).toISOString();
    var resource = {
      snippet: { title: title, description: description, tags: tags, categoryId: "26" }, // 26 = Howto & Style
      status: status
    };
    // YouTube advanced service (Resources → Services → YouTube Data API enable करना ज़रूरी)
    var res = YouTube.Videos.insert(resource, "snippet,status", blob);
    var link = "https://youtu.be/" + res.id;
    return "✅ Upload हुआ: " + link + (publishAtISO ? "\n⏰ Scheduled: " + publishAtISO : " (private)");
  } catch (e) {
    return "YouTube error: " + e + "\n\n(YouTube advanced service enable किया? Drive file ID सही है?)";
  }
}

// पहले से uploaded video को schedule करना (videoId से)
function scheduleYouTubeVideo(videoId, publishAtISO) {
  try {
    var res = YouTube.Videos.update({
      id: videoId,
      status: { privacyStatus: "private", publishAt: new Date(publishAtISO).toISOString() }
    }, "status");
    return "✅ Scheduled: https://youtu.be/" + videoId + " @ " + publishAtISO;
  } catch (e) { return "YouTube error: " + e; }
}

// ══════════════════════════════════════════════════════════════════════
// HTTP helpers
// ══════════════════════════════════════════════════════════════════════
function _post(url, payloadObj, bearer) {
  var res = UrlFetchApp.fetch(url, {
    method: "post", contentType: "application/json",
    headers: { Authorization: "Bearer " + bearer },
    payload: JSON.stringify(payloadObj), muteHttpExceptions: true
  });
  return res.getContentText();
}

function _postForm(url, fields) {
  var res = UrlFetchApp.fetch(url, { method: "post", payload: fields, muteHttpExceptions: true });
  return res.getContentText();
}

// ══════════════════════════════════════════════════════════════════════
// TEST + HELP
// ══════════════════════════════════════════════════════════════════════
function testTodayRow() {
  var b = _todayBundle();
  SpreadsheetApp.getUi().alert("Day " + b.day + "\n\n--- WhatsApp digest preview ---\n\n" + _digestText(b));
}

function autoHelp() {
  SpreadsheetApp.getUi().alert(
    "🚀 AgroManch Auto-Publish\n\n" +
    "1) CONFIG (CFG) में tokens भरो — guide देखो।\n" +
    "2) '⏰ रोज़ auto-run चालू करो' → रोज़ सुबह WhatsApp digest अपने आप।\n" +
    "3) Instagram/YouTube के लिए media का PUBLIC URL / Drive file चाहिए।\n\n" +
    "ज़रूरी:\n" +
    "• WhatsApp/Instagram → Meta Business + Cloud API token\n" +
    "• YouTube → Apps Script में 'YouTube Data API' advanced service enable करो\n\n" +
    "पूरी जानकारी: AgroManch_AutoPublish_SETUP.md");
}

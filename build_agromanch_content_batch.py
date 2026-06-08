#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgroManch Content Batch — 5 Marketing Videos
  V1: Crop Doctor — पत्तियां पीली (Leaf Yellowing)
  V2: Crop Doctor — गलत दवा (Wrong Medicine Warning)
  V3: Crop Doctor — सिर्फ एक फोटो (Core Product Demo)
  V4: Success Story — Crop Doctor saved my crop
  V5: Mandi Price Feature

All vertical 9:16 (1080x1920), Hindi, background music.
Reuses rendering engine from build_agromanch_video.py.
"""
import os, sys, math, tempfile
from PIL import Image, ImageDraw

import build_agromanch_video as B
from build_agromanch_video import (
    W, H, new_frame, draw_accents, fade_io, smooth, ease_out, clamp01,
    text_block, composite, emoji_layer, pill, progress_bar, draw_logo,
    H_, L_, WHITE, SOFT_WHITE, ACCENT, ACCENT_LT, GOLD, GOLD_DEEP,
    GREEN_MID, GREEN_DEEP, RED, render_timeline, make_music,
)

HERE = B.HERE
TEAL   = (72, 191, 200)
ORANGE = (255, 140, 0)
AMBER  = (255, 193, 7)
PURPLE = (156, 39, 176)

# ═══════════════════════════════════════════════════════════════
#  REUSABLE PARAMETERISED SCENE FACTORIES
# ═══════════════════════════════════════════════════════════════

def make_hook_scene(line1, line2, big_line, em1, em2=None, big_color=GOLD):
    """Opening problem hook — stops the scroll."""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.45, 0.45)
        pop = ease_out(t / 0.7)
        em  = emoji_layer(em1, int(165*(0.68+0.32*pop)))
        composite(img, em, W//2, int(H*0.23), a, anchor="mm")
        if em2:
            em_r = emoji_layer(em2, int(100*(0.68+0.32*pop)))
            composite(img, em_r, int(W*0.72), int(H*0.21), a, anchor="mm")
        l1 = text_block(line1, H_(72, "Bold"), WHITE, max_w=W-130,
                        stroke=2, stroke_fill=(0,0,0))
        composite(img, l1, W//2, int(H*0.42), a, anchor="mm")
        big = text_block(big_line, H_(100, "Black"), big_color, max_w=W-110,
                         stroke=3, stroke_fill=(0,0,0))
        composite(img, big, W//2, int(H*0.54), a, anchor="mm")
        if line2:
            l2 = text_block(line2, H_(48, "SemiBold"), ACCENT_LT, max_w=W-150)
            composite(img, l2, W//2, int(H*0.65), a, anchor="mm")
        return img
    return scene


def make_warning_scene(w1, w2, w3, icon="⚠️"):
    """3-point warning / problem-amplifier."""
    points = [w1, w2, w3]
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        sa  = fade_io(t, dur, 0.4, 0.4)
        em  = emoji_layer(icon, 140)
        composite(img, em, W//2, int(H*0.18), sa, anchor="mm")
        head = text_block("क्या हो रहा है आपकी फसल को?", H_(58, "Black"), GOLD, max_w=W-130)
        composite(img, head, W//2, int(H*0.30), sa, anchor="mm")
        y0 = int(H*0.41); row_h = 190
        per = (dur-0.8)/3
        for i, pt in enumerate(points):
            lt = t - i*per*0.85
            if lt < 0: continue
            ia = smooth(lt/0.45)*sa
            slide = (1-ease_out(lt/0.5))*80
            cy = y0 + i*row_h
            pill(img, W//2+int(slide), cy, W-155, 155, GREEN_MID, alpha=0.52*ia)
            bd = Image.new("RGBA",(110,110),(0,0,0,0))
            ImageDraw.Draw(bd).ellipse([0,0,109,109],
                fill=(RED[0],RED[1],RED[2],int(230*ia)))
            composite(img, bd, 145+int(slide), cy)
            nb = text_block(str(i+1), L_(64,"Black"), WHITE)
            composite(img, nb, 145+int(slide), cy, ia, anchor="mm")
            tb = text_block(pt, H_(48,"SemiBold"), WHITE, max_w=W-420, align="left")
            composite(img, tb, 240+tb.width//2+int(slide), cy, ia, anchor="mm")
        return img
    return scene


def make_solution_reveal(tagline, subline, em="🩺"):
    """AgroManch Crop Doctor solution reveal."""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.55, 0.45)
        pop = ease_out(t/0.8)
        emi = emoji_layer(em, int(190*(0.65+0.35*pop)))
        composite(img, emi, W//2, int(H*0.30), a, anchor="mm")
        solv = text_block("समाधान है!", H_(70,"Black"), ACCENT, max_w=W-130)
        composite(img, solv, W//2, int(H*0.46), a, anchor="mm")
        big = text_block(tagline, H_(88,"Black"), GOLD, max_w=W-120,
                         stroke=2, stroke_fill=(0,0,0))
        composite(img, big, W//2, int(H*0.55), a, anchor="mm")
        sub = text_block(subline, H_(48,"SemiBold"), WHITE, max_w=W-150)
        composite(img, sub, W//2, int(H*0.65), a, anchor="mm")
        if t > 0.7:
            progress_bar(img, W//2, int(H*0.55)+130, 500, 10,
                         ease_out((t-0.7)/1.2), fill=TEAL, alpha=a*0.9)
        return img
    return scene


def make_3step_scene(title, steps):
    """How-it-works 3-step scene. steps = [(emoji, title, sub), ...]"""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        sa  = fade_io(t, dur, 0.35, 0.42)
        head = text_block(title, H_(64,"Black"), WHITE, max_w=W-120)
        composite(img, head, W//2, int(H*0.12), sa, anchor="mm")
        y0 = int(H*0.26); row_h = 295
        per = (dur-0.8)/len(steps)
        for i,(em,ttl,sub) in enumerate(steps):
            lt = t - i*per*0.88
            if lt < 0: continue
            ia  = smooth(lt/0.48)*sa
            slid= (1-ease_out(lt/0.52))*88
            cy  = y0 + i*row_h
            pill(img, W//2+int(slid), cy, W-144, 255, GREEN_MID, alpha=0.50*ia)
            bd = Image.new("RGBA",(132,132),(0,0,0,0))
            ImageDraw.Draw(bd).ellipse([0,0,131,131],
                fill=(TEAL[0],TEAL[1],TEAL[2],int(255*ia)))
            composite(img, bd, 162+int(slid), cy)
            nb = text_block(str(i+1), L_(72,"Black"), WHITE)
            composite(img, nb, 162+int(slid), cy, ia, anchor="mm")
            tb = text_block(ttl, H_(52,"Bold"), GOLD, max_w=W-458, align="left")
            composite(img, tb, 262+tb.width//2+int(slid), cy-50, ia, anchor="mm")
            sb = text_block(sub, H_(38,"SemiBold"), SOFT_WHITE, max_w=W-440, align="left")
            composite(img, sb, 262+sb.width//2+int(slid), cy+42, ia, anchor="mm")
            ce = emoji_layer(em, 80)
            composite(img, ce, W-148+int(slid), cy, ia, anchor="mm")
        return img
    return scene


def make_result_card(disease, cause, treatment, schedule, footer):
    """Diagnosis result card — simulates the app output."""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.50, 0.42)
        head = text_block("रिपोर्ट तैयार — सिर्फ़ 60 सेकंड में", H_(48,"Black"), TEAL, max_w=W-130)
        composite(img, head, W//2, int(H*0.11), a, anchor="mm")
        rise = (1-ease_out(t/0.72))*58
        card = Image.new("RGBA",(W-148,990),(0,0,0,0))
        cd   = ImageDraw.Draw(card)
        cd.rounded_rectangle([0,0,W-149,989], radius=46, fill=(248,250,249,int(255*a)))
        cd.rounded_rectangle([0,0,W-149,148], radius=46,
            fill=(GREEN_MID[0],GREEN_MID[1],GREEN_MID[2],int(255*a)))
        composite(img, card, W//2, int(H*0.19)+int(rise), anchor="mt")
        ytop = int(H*0.19)+int(rise); cx0 = 120
        # card header with microscope emoji
        mi = emoji_layer("🔬", 54)
        ht = text_block("रोग पहचाना गया", H_(48,"Bold"), WHITE)
        tw = mi.width+14+ht.width
        composite(img, mi, W//2-tw//2+mi.width//2, ytop+74, a, anchor="mm")
        composite(img, ht, W//2-tw//2+mi.width+14+ht.width//2, ytop+74, a, anchor="mm")
        rows = [("रोग:",      disease,   RED),
                ("कारण:",     cause,     GREEN_DEEP),
                ("इलाज:",     treatment, GREEN_DEEP),
                ("छिड़काव:",   schedule,  GREEN_DEEP)]
        ry = ytop+218
        for i,(lab,val,col) in enumerate(rows):
            ra = a*smooth((t-0.38-i*0.26)/0.42)
            if ra <= 0: continue
            lb = text_block(lab, H_(44,"Bold"), (85,108,96), align="left")
            composite(img, lb, cx0+lb.width//2, ry, ra, anchor="mm")
            vb = text_block(val, H_(44,"SemiBold"), col, max_w=W-150-cx0-255, align="left")
            composite(img, vb, cx0+248+vb.width//2, ry, ra, anchor="mm")
            ry += 152
        fa = a*smooth((t-1.45)/0.40)
        if fa > 0:
            fe = emoji_layer("✅", 52); ft = text_block(footer, H_(44,"Black"), GREEN_MID)
            tw2 = fe.width+14+ft.width
            composite(img, fe, W//2-tw2//2+fe.width//2, ry+12, fa, anchor="mm")
            composite(img, ft, W//2-tw2//2+fe.width+14+ft.width//2, ry+12, fa, anchor="mm")
        return img
    return scene


def make_wrong_medicine_scene():
    """₹ loss counter + stat bars — wrong medicine kills ROI."""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.45, 0.42)
        em  = emoji_layer("💸", 155)
        composite(img, em, W//2, int(H*0.22), a, anchor="mm")
        # animated loss counter
        loss = int(ease_out(clamp01(t/1.5)) * 50000)
        cnt  = text_block(f"₹{loss:,} बर्बाद!", H_(110,"Black"), RED,
                          stroke=3, stroke_fill=(0,0,0))
        composite(img, cnt, W//2, int(H*0.38), a, anchor="mm")
        l2 = text_block("सिर्फ़ गलत दवा की वजह से", H_(58,"Bold"), WHITE, max_w=W-140)
        composite(img, l2, W//2, int(H*0.50), a, anchor="mm")
        # stat pills
        stats = [("85%", "किसान गलत दवा खरीदते हैं"),
                 ("3×",  "ज़्यादा खर्च होता है")]
        y0 = int(H*0.58); rh = 168
        for i,(num,sub) in enumerate(stats):
            lt = t - 0.7 - i*0.4
            if lt < 0: continue
            ia = smooth(lt/0.45)*a
            cy = y0 + i*rh
            pill(img, W//2, cy, W-175, 142, GREEN_MID, alpha=0.52*ia)
            nb = text_block(num, L_(66,"Black"), GOLD)
            composite(img, nb, 200, cy, ia, anchor="mm")
            sb = text_block(sub, H_(46,"SemiBold"), WHITE, max_w=W-420, align="left")
            composite(img, sb, 310+sb.width//2, cy, ia, anchor="mm")
        return img
    return scene


def make_success_story(name, crop, state, before, after, earning):
    """Farmer success story card."""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.52, 0.45)
        em  = emoji_layer("🧑‍🌾", 155)
        composite(img, em, W//2, int(H*0.22), a, anchor="mm")
        nm  = text_block(name, H_(64,"Black"), GOLD)
        composite(img, nm, W//2, int(H*0.37), a, anchor="mm")
        st  = text_block(f"{crop} किसान · {state}", H_(44,"SemiBold"), ACCENT_LT)
        composite(img, st, W//2, int(H*0.44), a, anchor="mm")
        # before/after card
        bfr = Image.new("RGBA",(W-155,560),(0,0,0,0))
        bf  = ImageDraw.Draw(bfr)
        bf.rounded_rectangle([0,0,W-156,559], radius=40, fill=(27,67,50,int(210*a)))
        composite(img, bfr, W//2, int(H*0.58), anchor="mt")
        ba_y = int(H*0.58)+45
        for label,val,col in [("पहले",before,RED),("Crop Doctor से",after,ACCENT),
                               ("कमाई",earning,GOLD)]:
            ll = text_block(label, H_(38,"SemiBold"), ACCENT_LT)
            vv = text_block(val,   H_(54,"Bold"),     col, max_w=W-350)
            ra = a*smooth((t-0.5-[before,after,earning].index(val)*0.3)/0.38)
            composite(img, ll, 170, ba_y, ra, anchor="mm")
            composite(img, vv, 430+vv.width//2, ba_y, ra, anchor="mm")
            ba_y += 150
        return img
    return scene


def make_cd_cta(headline="फसल बीमार? एक फोटो काफ़ी है!", btn_text="Crop Doctor खोलो"):
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.48, 0.38)
        pls = 1.0 + 0.04*math.sin(t*6)
        draw_logo(img, int(H*0.26), scale=0.64, alpha=a, with_tagline=False)
        l1  = text_block(headline, H_(60,"Black"), WHITE, max_w=W-130)
        composite(img, l1, W//2, int(H*0.41), a, anchor="mm")
        # badge: FREE
        bd = Image.new("RGBA",(220,80),(0,0,0,0))
        ImageDraw.Draw(bd).rounded_rectangle([0,0,219,79], radius=40,
            fill=(TEAL[0],TEAL[1],TEAL[2],int(220*a)))
        composite(img, bd, W//2, int(H*0.49), anchor="mm")
        fb = text_block("बिल्कुल FREE", L_(44,"Black"), WHITE)
        composite(img, fb, W//2, int(H*0.49), a, anchor="mm")
        # big CTA button
        bw,bh = int(700*pls), int(148*pls)
        pill(img, W//2, int(H*0.575), bw, bh, GOLD, alpha=a)
        mi = emoji_layer("🩺", 70); bt = text_block(btn_text, H_(56,"Black"), GREEN_DEEP)
        tw = mi.width+16+bt.width
        composite(img, mi, W//2-tw//2+mi.width//2, int(H*0.575), a, anchor="mm")
        composite(img, bt, W//2-tw//2+mi.width+16+bt.width//2, int(H*0.575), a, anchor="mm")
        cta = text_block("अभी AgroManch App Download करें", H_(42,"SemiBold"), ACCENT_LT, max_w=W-155)
        composite(img, cta, W//2, int(H*0.663), a, anchor="mm")
        hnl = text_block("@AgroManch  ·  www.agromanch.in", L_(38,"SemiBold"), ACCENT_LT, max_w=W-160)
        composite(img, hnl, W//2, int(H*0.718), a, anchor="mm")
        return img
    return scene


def make_mandi_ticker(crops_data):
    """Animated mandi price ticker for multiple crops."""
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.42, 0.42)
        em  = emoji_layer("📊", 140)
        composite(img, em, W//2, int(H*0.17), a, anchor="mm")
        head = text_block("आज की मंडी भाव", H_(78,"Black"), GOLD, max_w=W-130)
        composite(img, head, W//2, int(H*0.28), a, anchor="mm")
        dt   = text_block("LIVE · 08 June 2026", L_(44,"SemiBold"), TEAL)
        composite(img, dt, W//2, int(H*0.345), a, anchor="mm")
        per  = (dur-0.8)/len(crops_data)
        y0   = int(H*0.40); row_h = 178
        for i,(crop,price,change,arrow,col) in enumerate(crops_data):
            lt   = t - i*per*0.82
            if lt < 0: continue
            ia   = smooth(lt/0.46)*a
            cy   = y0 + i*row_h
            pill(img, W//2, cy, W-155, 150, GREEN_MID, alpha=0.52*ia)
            cn   = text_block(crop, H_(52,"Bold"), WHITE, align="left")
            composite(img, cn, 155+cn.width//2, cy, ia, anchor="mm")
            # animated count-up price
            pr   = int(ease_out(clamp01(lt/1.2))*price)
            pv   = text_block(f"₹{pr:,}", L_(62,"Black"), col)
            composite(img, pv, W-330, cy, ia, anchor="mm")
            ch   = text_block(change, L_(38,"Bold"), col)
            composite(img, ch, W-140, cy+38, ia, anchor="mm")
        return img
    return scene


def make_mandi_cta():
    def scene(t, dur):
        img = new_frame(); draw_accents(img, t)
        a   = fade_io(t, dur, 0.46, 0.38)
        pls = 1.0 + 0.04*math.sin(t*6)
        draw_logo(img, int(H*0.26), scale=0.64, alpha=a, with_tagline=False)
        l1  = text_block("रोज़ सुबह Live मंडी भाव पाओ", H_(62,"Black"), WHITE, max_w=W-130)
        composite(img, l1, W//2, int(H*0.41), a, anchor="mm")
        bw,bh = int(720*pls), int(148*pls)
        pill(img, W//2, int(H*0.55), bw, bh, GOLD, alpha=a)
        mi = emoji_layer("📊", 70); bt = text_block("मंडी भाव App खोलो", H_(56,"Black"), GREEN_DEEP)
        tw = mi.width+16+bt.width
        composite(img, mi, W//2-tw//2+mi.width//2, int(H*0.55), a, anchor="mm")
        composite(img, bt, W//2-tw//2+mi.width+16+bt.width//2, int(H*0.55), a, anchor="mm")
        sub = text_block("50+ मंडियाँ · हर फसल · हर राज्य", H_(44,"SemiBold"), ACCENT_LT, max_w=W-155)
        composite(img, sub, W//2, int(H*0.635), a, anchor="mm")
        hnl = text_block("@AgroManch  ·  www.agromanch.in", L_(38,"SemiBold"), ACCENT_LT, max_w=W-160)
        composite(img, hnl, W//2, int(H*0.695), a, anchor="mm")
        return img
    return scene


# ═══════════════════════════════════════════════════════════════
#  VIDEO DEFINITIONS
# ═══════════════════════════════════════════════════════════════

# ── V1: Crop Doctor — पत्तियां पीली (Leaf Yellowing) ───────────
CD_HOW_3STEPS = make_3step_scene(
    "Crop Doctor — 3 आसान कदम",
    [("📸", "फसल की फोटो खींचो",      "पत्ती या पूरी फसल — कोई भी"),
     ("🔬", "AI रोग पहचानेगा",         "60 सेकंड में सटीक diagnosis"),
     ("💊", "सही दवा की सलाह मिलेगी", "नाम · मात्रा · छिड़काव — सब हिंदी में")])

V1_TIMELINE = [
    (4.2, make_hook_scene(
        "आपकी फसल की पत्तियां",
        "पीली पड़ रही हैं?",
        "फसल बर्बाद होने से पहले देखो!",
        "🌿", em2="😰", big_color=GOLD)),
    (5.5, make_warning_scene(
        "पत्तियों पर पीले धब्बे",
        "फसल की बढ़त रुक गई",
        "उपज 40% तक घट सकती है",
        "⚠️")),
    (4.2, make_solution_reveal(
        "AgroManch Crop Doctor",
        "फोटो से तुरंत पहचानो असली कारण", "🩺")),
    (10.0, CD_HOW_3STEPS),
    (6.5, make_result_card(
        "नाइट्रोजन की कमी",
        "खराब मिट्टी + कम सिंचाई",
        "यूरिया 2% घोल का छिड़काव",
        "5-7 दिन में फर्क दिखेगा",
        "पत्तियां हरी होंगी — उपज वापस")),
    (5.0, make_cd_cta(
        "पत्तियां पीली? फोटो खींचो अभी!",
        "Crop Doctor से पहचानो")),
]

# ── V2: Crop Doctor — गलत दवा मत डालो ──────────────────────────
V2_TIMELINE = [
    (4.5, make_hook_scene(
        "गलत दवा डालकर",
        "हज़ारों रुपये बर्बाद मत कीजिए",
        "पहले बीमारी पहचानो!",
        "💊", em2="❌", big_color=RED)),
    (5.5, make_wrong_medicine_scene()),
    (4.2, make_solution_reveal(
        "Crop Doctor से",
        "पहले सही diagnosis — फिर सही दवा", "🩺")),
    (10.0, CD_HOW_3STEPS),
    (6.5, make_result_card(
        "धान का झोंका रोग (Blast)",
        "Magnaporthe oryzae फफूंद",
        "Tricyclazole 75 WP — 0.6g/लीटर",
        "7 दिन बाद दूसरा छिड़काव",
        "₹8,000 तक की बचत प्रति एकड़")),
    (5.0, make_cd_cta(
        "सही दवा, सही समय — फसल बचाओ",
        "Crop Doctor खोलो अभी")),
]

# ── V3: Crop Doctor — सिर्फ एक फोटो काफ़ी है (Core Demo) ────────
V3_TIMELINE = [
    (4.2, make_hook_scene(
        "डॉक्टर के पास जाने की ज़रूरत नहीं —",
        "Crop Doctor इस्तेमाल कीजिए",
        "सिर्फ एक फोटो काफ़ी है!",
        "📸", em2="🩺", big_color=GOLD)),
    (4.2, make_solution_reveal(
        "AgroManch फसल डॉक्टर",
        "50+ फसलें · 200+ बीमारियाँ · 24x7 FREE", "🩺")),
    (10.0, make_3step_scene(
        "इतना आसान है Crop Doctor",
        [("📱", "App खोलो → Crop Doctor",   "AgroManch App में जाओ"),
         ("📸", "फसल की फोटो लो",           "बीमार पत्ती की close-up"),
         ("💡", "तुरंत मिलेगा जवाब",        "रोग + कारण + इलाज + दवा")])),
    (6.5, make_result_card(
        "सूखा सड़न (Dry Rot)",
        "Fusarium फफूंद संक्रमण",
        "Carbendazim 50 WP — 1g/लीटर",
        "10 दिन बाद दूसरी spray ज़रूरी",
        "फसल बची — नुकसान रुका")),
    (6.0, make_cd_cta(
        "फसल बचाइए — नुकसान घटाइए",
        "Crop Doctor खोलो — FREE")),
]

# ── V4: Success Story ────────────────────────────────────────────
def scene_ss_intro(t, dur):
    img = new_frame(); draw_accents(img, t)
    a   = fade_io(t, dur, 0.52, 0.42)
    em  = emoji_layer("🌟", 155)
    composite(img, em, W//2, int(H*0.23), a, anchor="mm")
    h1  = text_block("किसान की सच्ची कहानी", H_(60,"Black"), WHITE)
    composite(img, h1, W//2, int(H*0.40), a, anchor="mm")
    h2  = text_block("Crop Doctor ने बचाई फसल", H_(78,"Black"), GOLD, max_w=W-130,
                     stroke=2, stroke_fill=(0,0,0))
    composite(img, h2, W//2, int(H*0.50), a, anchor="mm")
    h3  = text_block("रामलाल जी की असली कहानी — Raebareli, UP", H_(42,"SemiBold"),
                     ACCENT_LT, max_w=W-150)
    composite(img, h3, W//2, int(H*0.60), a, anchor="mm")
    return img

def scene_ss_problem(t, dur):
    img = new_frame(); draw_accents(img, t)
    a   = fade_io(t, dur, 0.46, 0.42)
    em  = emoji_layer("😟", 140)
    composite(img, em, W//2, int(H*0.22), a, anchor="mm")
    q   = text_block('"मेरी गेहूं की फसल में\nअचानक भूरे धब्बे आ गए।\nकोई नहीं बता पाया क्या हुआ।"',
                     H_(56,"SemiBold"), WHITE, max_w=W-130, line_gap=22)
    composite(img, q, W//2, int(H*0.48), a, anchor="mm")
    auth= text_block("— रामलाल जी, 5 एकड़ किसान", H_(40,"SemiBold"), ACCENT_LT)
    composite(img, auth, W//2, int(H*0.67), a, anchor="mm")
    return img

def scene_ss_discovery(t, dur):
    img = new_frame(); draw_accents(img, t)
    a   = fade_io(t, dur, 0.48, 0.42)
    em  = emoji_layer("📱", 140)
    composite(img, em, W//2, int(H*0.22), a, anchor="mm")
    h1  = text_block("फिर किसी ने बताया —", H_(56,"SemiBold"), ACCENT_LT)
    composite(img, h1, W//2, int(H*0.39), a, anchor="mm")
    h2  = text_block("AgroManch Crop Doctor", H_(80,"Black"), GOLD,
                     stroke=2, stroke_fill=(0,0,0))
    composite(img, h2, W//2, int(H*0.49), a, anchor="mm")
    h3  = text_block("फोटो खींची → 45 सेकंड में जवाब मिला", H_(48,"SemiBold"),
                     WHITE, max_w=W-150)
    composite(img, h3, W//2, int(H*0.59), a, anchor="mm")
    return img

def scene_ss_result(t, dur):
    img = new_frame(); draw_accents(img, t)
    a   = fade_io(t, dur, 0.52, 0.42)
    em  = emoji_layer("🎉", 155)
    composite(img, em, W//2, int(H*0.22), a, anchor="mm")
    frac = ease_out(t/(dur*0.72))
    earn = int(2 + frac*0.85)
    num  = text_block(f"₹{earn:.2f} लाख", H_(128,"Black"), GOLD,
                      stroke=3, stroke_fill=(0,0,0))
    composite(img, num, W//2, int(H*0.41), a, anchor="mm")
    s1   = text_block("फसल की कमाई इस बार", H_(52,"Bold"), WHITE)
    composite(img, s1, W//2, int(H*0.53), a, anchor="mm")
    q    = text_block('"Crop Doctor ने ₹80,000 की फसल बचाई।\nअब मैं हर सीज़न इसे इस्तेमाल करता हूँ।"',
                      H_(44,"SemiBold"), ACCENT_LT, max_w=W-140, line_gap=20)
    composite(img, q, W//2, int(H*0.62), a, anchor="mm")
    return img

V4_TIMELINE = [
    (4.2, scene_ss_intro),
    (5.5, scene_ss_problem),
    (4.8, scene_ss_discovery),
    (5.5, scene_ss_result),
    (5.0, make_cd_cta(
        "हज़ारों किसानों की तरह आप भी",
        "Crop Doctor इस्तेमाल करो")),
]

# ── V5: Mandi Price Feature ──────────────────────────────────────
MANDI_CROPS = [
    ("गेहूं",   2680, "+2.4%", "+", ACCENT),
    ("धान",     2100, "-1.1%", "-", RED),
    ("सोयाबीन", 4250, "+3.8%", "+", ACCENT),
    ("प्याज़",   1850, "+5.2%", "+", ACCENT),
    ("कपास",    6800, "-0.8%", "-", RED),
]

def scene_mandi_hook(t, dur):
    img = new_frame(); draw_accents(img, t)
    a   = fade_io(t, dur, 0.48, 0.45)
    em  = emoji_layer("📊", 155)
    composite(img, em, W//2, int(H*0.24), a, anchor="mm")
    l1  = text_block("मंडी जाने से पहले", H_(80,"Bold"), WHITE,
                     stroke=2, stroke_fill=(0,0,0))
    composite(img, l1, W//2, int(H*0.42), a, anchor="mm")
    l2  = text_block("भाव चेक करो!", H_(100,"Black"), GOLD, max_w=W-120,
                     stroke=3, stroke_fill=(0,0,0))
    composite(img, l2, W//2, int(H*0.525), a, anchor="mm")
    l3  = text_block("सही वक्त पर बेचो — ज़्यादा कमाओ", H_(50,"SemiBold"),
                     ACCENT_LT, max_w=W-155)
    composite(img, l3, W//2, int(H*0.625), a, anchor="mm")
    return img

def scene_mandi_loss(t, dur):
    img = new_frame(); draw_accents(img, t)
    a   = fade_io(t, dur, 0.44, 0.42)
    em  = emoji_layer("😔", 130)
    composite(img, em, W//2, int(H*0.21), a, anchor="mm")
    l1  = text_block("बिना भाव जाने फसल बेची?", H_(64,"Bold"), WHITE, max_w=W-130)
    composite(img, l1, W//2, int(H*0.37), a, anchor="mm")
    loss= int(ease_out(clamp01(t/1.4))*15000)
    cnt = text_block(f"₹{loss:,}/क्विंटल नुकसान", H_(90,"Black"), RED,
                     stroke=2, stroke_fill=(0,0,0))
    composite(img, cnt, W//2, int(H*0.50), a, anchor="mm")
    l2  = text_block("सिर्फ़ 1 दिन देर से — बड़ा फ़र्क पड़ता है", H_(48,"SemiBold"),
                     AMBER, max_w=W-155)
    composite(img, l2, W//2, int(H*0.61), a, anchor="mm")
    return img

V5_TIMELINE = [
    (4.5, scene_mandi_hook),
    (4.8, scene_mandi_loss),
    (4.2, make_solution_reveal(
        "AgroManch — Live मंडी भाव",
        "50+ मंडियाँ · रोज़ update · बिल्कुल FREE", "📊")),
    (12.0, make_mandi_ticker(MANDI_CROPS)),
    (5.0, make_mandi_cta()),
]

# ═══════════════════════════════════════════════════════════════
#  MAIN BUILDER
# ═══════════════════════════════════════════════════════════════
VIDEOS = [
    (V1_TIMELINE, "V1_CropDoctor_PattiyaaPeeli.mp4"),
    (V2_TIMELINE, "V2_CropDoctor_GalatDawa.mp4"),
    (V3_TIMELINE, "V3_CropDoctor_EkPhoto.mp4"),
    (V4_TIMELINE, "V4_SuccessStory_CropDoctor.mp4"),
    (V5_TIMELINE, "V5_MandiPrices_Feature.mp4"),
]

def main():
    print("🎬 AgroManch Content Batch — 5 Videos")
    print("=" * 48)
    tmp   = tempfile.mkdtemp()
    music = os.path.join(tmp, "agromanch_bgm.wav")
    print("  → synthesizing soundtrack...")
    make_music(music, duration=42.0)
    for i,(tl,fname) in enumerate(VIDEOS, 1):
        dur  = sum(d for d,_ in tl)
        print(f"\n[{i}/5] {fname}  ({dur:.1f}s)")
        render_timeline(tl, fname, music)
        p = os.path.join(HERE, fname)
        if os.path.exists(p):
            print(f"      → {os.path.getsize(p)//1024} KB")
    print("\n✅ All 5 videos done!")
    print("\nSummary:")
    for _,fname in VIDEOS:
        p = os.path.join(HERE, fname)
        if os.path.exists(p):
            print(f"  {fname}  ({os.path.getsize(p)//1024} KB)")

if __name__ == "__main__":
    main()

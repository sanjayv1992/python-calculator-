#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgroManch — Crop Doctor (फसल डॉक्टर) marketing video.
Vertical 1080x1920, Hindi on-screen text + synthesized soundtrack.
Reuses the rendering engine from build_agromanch_video.py.

Output: AgroManch_CropDoctor.mp4
"""
import os, math, tempfile

import build_agromanch_video as B
from build_agromanch_video import (
    W, H, new_frame, draw_accents, fade_io, smooth, ease_out, clamp01,
    text_block, composite, emoji_layer, pill, progress_bar, draw_logo,
    H_, L_, WHITE, SOFT_WHITE, ACCENT, ACCENT_LT, GOLD, GOLD_DEEP,
    GREEN_MID, GREEN_DEEP, RED, render_timeline, make_music,
)
from PIL import Image, ImageDraw

TEAL = (72, 191, 200)   # medical/trust accent

# ── Scene 1: Problem ────────────────────────────────────────
def scene_problem(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.5, 0.45)
    em = emoji_layer("🌿", 150)
    composite(img, em, W//2, int(H*0.26), a, anchor="mm")
    l1 = text_block("फसल में रोग लग गया?", H_(84, "Bold"), WHITE, max_w=W-130,
                    stroke=2, stroke_fill=(0,0,0))
    composite(img, l1, W//2, int(H*0.44), a, anchor="mm")
    l2 = text_block("पत्तियां पीली · धब्बे · सूख रही फसल", H_(50, "SemiBold"),
                    ACCENT_LT, max_w=W-150)
    composite(img, l2, W//2, int(H*0.54), a, anchor="mm")
    l3 = text_block("डॉक्टर कहाँ ढूंढें? दवा कौन सी लें?", H_(56, "Bold"),
                    GOLD, max_w=W-150)
    composite(img, l3, W//2, int(H*0.63), a, anchor="mm")
    return img

# ── Scene 2: Introduce feature ──────────────────────────────
def scene_intro(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.6, 0.45)
    pop = ease_out(t / 0.8)
    em = emoji_layer("🩺", int(190 * (0.7 + 0.3*pop)))
    composite(img, em, W//2, int(H*0.30), a, anchor="mm")
    l0 = text_block("पेश है", H_(56, "SemiBold"), ACCENT_LT)
    composite(img, l0, W//2, int(H*0.45), a, anchor="mm")
    l1 = text_block("AgroManch फसल डॉक्टर", H_(86, "Black"), GOLD, max_w=W-120,
                    stroke=2, stroke_fill=(0,0,0))
    composite(img, l1, W//2, int(H*0.53), a, anchor="mm")
    l2 = text_block("आपकी जेब में फसल का अपना डॉक्टर", H_(48, "SemiBold"),
                    WHITE, max_w=W-150)
    composite(img, l2, W//2, int(H*0.62), a, anchor="mm")
    if t > 0.6:
        progress_bar(img, W//2, int(H*0.53)+110, 460, 9, ease_out((t-0.6)/1.2), fill=TEAL, alpha=a)
    return img

# ── Scene 3: 3 steps ────────────────────────────────────────
STEPS = [
    ("📸", "1", "फसल की फोटो खींचो", "बस एक तस्वीर — पत्ती या फसल की"),
    ("🔬", "2", "तुरंत रोग की पहचान", "AI + कृषि एक्सपर्ट मिलकर जांचें"),
    ("💊", "3", "सही इलाज की सलाह", "कौन सी दवा, कितनी मात्रा — सब हिंदी में"),
]
def scene_steps(t, dur):
    img = new_frame(); draw_accents(img, t)
    sa = fade_io(t, dur, 0.35, 0.45)
    head = text_block("कैसे काम करता है?", H_(64, "Black"), WHITE, max_w=W-120)
    composite(img, head, W//2, int(H*0.13), sa, anchor="mm")
    y0 = int(H*0.27); row_h = 300
    per = (dur - 0.8) / len(STEPS)
    for i, (em, num, title, sub) in enumerate(STEPS):
        lt = t - i * per * 0.9
        if lt < 0:
            continue
        ia = smooth(lt / 0.5) * sa
        slide = (1 - ease_out(lt / 0.55)) * 90
        cy = y0 + i * row_h
        pill(img, W//2 + int(slide), cy, W-140, 250, GREEN_MID, alpha=0.5*ia)
        # number badge
        bd = Image.new("RGBA", (130, 130), (0,0,0,0))
        ImageDraw.Draw(bd).ellipse([0,0,129,129], fill=(TEAL[0],TEAL[1],TEAL[2],int(255*ia)))
        composite(img, bd, 160 + int(slide), cy)
        nb = text_block(num, L_(72, "Black"), WHITE)
        composite(img, nb, 160 + int(slide), cy, ia, anchor="mm")
        emi = emoji_layer(em, 84)
        composite(img, emi, 160 + int(slide), cy - 150, ia, anchor="mm") if False else None
        # title + sub
        tb = text_block(title, H_(52, "Bold"), GOLD, max_w=W-460, align="left")
        composite(img, tb, 260 + tb.width//2 + int(slide), cy - 48, ia, anchor="mm")
        sb = text_block(sub, H_(38, "SemiBold"), SOFT_WHITE, max_w=W-440, align="left")
        composite(img, sb, 260 + sb.width//2 + int(slide), cy + 40, ia, anchor="mm")
        # corner emoji
        ce = emoji_layer(em, 80)
        composite(img, ce, W-150 + int(slide), cy, ia, anchor="mm")
    return img

# ── Scene 4: Diagnosis result card (concrete demo) ──────────
def scene_result(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.5, 0.45)
    head = text_block("रिपोर्ट तैयार — सिर्फ़ 60 सेकंड में", H_(50, "Black"), TEAL, max_w=W-140)
    composite(img, head, W//2, int(H*0.12), a, anchor="mm")
    # white card
    rise = (1 - ease_out(t / 0.7)) * 60
    card = Image.new("RGBA", (W-150, 1000), (0,0,0,0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0,0,W-151,999], radius=44, fill=(248,250,249,int(255*a)))
    cd.rounded_rectangle([0,0,W-151,150], radius=44, fill=(GREEN_MID[0],GREEN_MID[1],GREEN_MID[2],int(255*a)))
    composite(img, card, W//2, int(H*0.20)+int(rise), anchor="mt")
    cx0 = 120; ytop = int(H*0.20)+int(rise)
    # card header
    h = text_block("🔬 रोग पहचाना गया", H_(48, "Bold"), WHITE)
    ht = text_block("रोग पहचाना गया", H_(48, "Bold"), WHITE)
    he = emoji_layer("🔬", 56)
    tw = he.width + 16 + ht.width
    composite(img, he, W//2 - tw//2 + he.width//2, ytop+75, a, anchor="mm")
    composite(img, ht, W//2 - tw//2 + he.width + 16 + ht.width//2, ytop+75, a, anchor="mm")
    # rows
    rows = [
        ("रोग:", "पत्ती झुलसा (Leaf Blight)", RED),
        ("कारण:", "फफूंद संक्रमण", GREEN_DEEP),
        ("इलाज:", "मैन्कोज़ेब 2g/लीटर पानी", GREEN_DEEP),
        ("छिड़काव:", "7 दिन के अंतर पर, 2 बार", GREEN_DEEP),
    ]
    ry = ytop + 220
    for i,(lab,val,col) in enumerate(rows):
        ra = a * smooth((t - 0.4 - i*0.25)/0.4)
        if ra <= 0: continue
        lb = text_block(lab, H_(44, "Bold"), (90,110,100), align="left")
        composite(img, lb, cx0+lb.width//2, ry, ra, anchor="mm")
        vb = text_block(val, H_(44, "SemiBold"), col, max_w=W-150-cx0-280, align="left")
        composite(img, vb, cx0+250+vb.width//2, ry, ra, anchor="mm")
        ry += 150
    # footer tick
    fa = a * smooth((t-1.4)/0.4)
    if fa > 0:
        fb = text_block("✅ 3 दिन में असर दिखेगा", H_(44, "Black"), GREEN_MID, max_w=W-220)
        ft = text_block("3 दिन में असर दिखेगा", H_(44, "Black"), GREEN_MID)
        fe = emoji_layer("✅", 52)
        tw2 = fe.width+14+ft.width
        composite(img, fe, W//2-tw2//2+fe.width//2, ry+10, fa, anchor="mm")
        composite(img, ft, W//2-tw2//2+fe.width+14+ft.width//2, ry+10, fa, anchor="mm")
    return img

# ── Scene 5: Benefits ───────────────────────────────────────
BENEFITS = [("🆓","100% मुफ़्त"),("⏱️","60 सेकंड में"),("🕒","24x7 उपलब्ध"),("🗣️","आपकी भाषा में")]
def scene_benefits(t, dur):
    img = new_frame(); draw_accents(img, t)
    sa = fade_io(t, dur, 0.4, 0.45)
    head = text_block("क्यों फसल डॉक्टर?", H_(64, "Black"), GOLD, max_w=W-120)
    composite(img, head, W//2, int(H*0.16), sa, anchor="mm")
    y0 = int(H*0.30); row_h = 175
    for i,(em,txt) in enumerate(BENEFITS):
        lt = t - i*0.28
        if lt < 0: continue
        ia = smooth(lt/0.45)*sa
        slide = (1-ease_out(lt/0.5))*70
        cy = y0 + i*row_h
        pill(img, W//2+int(slide), cy, W-180, 140, GREEN_MID, alpha=0.5*ia)
        emi = emoji_layer(em, 84)
        composite(img, emi, 160+int(slide), cy, ia, anchor="mm")
        tb = text_block(txt, H_(56, "Bold"), WHITE, max_w=W-360, align="left")
        composite(img, tb, 250+tb.width//2+int(slide), cy, ia, anchor="mm")
    return img

# ── Scene 6: Proof ──────────────────────────────────────────
def scene_proof(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.55, 0.45)
    em = emoji_layer("🌾", 150)
    composite(img, em, W//2, int(H*0.26), a, anchor="mm")
    frac = ease_out(t/(dur*0.7))
    crops = int(frac*50)
    num = text_block(f"{crops}+ फसलें", H_(118, "Black"), GOLD)
    composite(img, num, W//2, int(H*0.43), a, anchor="mm")
    sub = text_block("गेहूं · धान · कपास · सब्ज़ी · फल — सब कवर", H_(44, "SemiBold"),
                     WHITE, max_w=W-150)
    composite(img, sub, W//2, int(H*0.53), a, anchor="mm")
    sub2 = text_block("हज़ारों किसान रोज़ इस्तेमाल कर रहे हैं", H_(48, "Bold"),
                      ACCENT_LT, max_w=W-160)
    composite(img, sub2, W//2, int(H*0.60), a, anchor="mm")
    return img

# ── Scene 7: CTA ────────────────────────────────────────────
def scene_cta(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.5, 0.4)
    pulse = 1.0 + 0.04*math.sin(t*6)
    draw_logo(img, int(H*0.28), scale=0.66, alpha=a, with_tagline=False)
    l1 = text_block("फसल बीमार? अभी फोटो भेजो", H_(64, "Black"), WHITE, max_w=W-130)
    composite(img, l1, W//2, int(H*0.44), a, anchor="mm")
    bw, bh = int(680*pulse), int(150*pulse)
    pill(img, W//2, int(H*0.56), bw, bh, GOLD, alpha=a)
    emi = emoji_layer("🩺", 72)
    bt = text_block("फसल डॉक्टर खोलो", H_(58, "Black"), GREEN_DEEP)
    tw = emi.width+18+bt.width
    composite(img, emi, W//2-tw//2+emi.width//2, int(H*0.56), a, anchor="mm")
    composite(img, bt, W//2-tw//2+emi.width+18+bt.width//2, int(H*0.56), a, anchor="mm")
    h2 = text_block("AgroManch App पर — बिल्कुल FREE", H_(44, "SemiBold"), ACCENT_LT, max_w=W-160)
    composite(img, h2, W//2, int(H*0.68), a, anchor="mm")
    h3 = text_block("@AgroManch  ·  www.agromanch.in", L_(40, "SemiBold"), ACCENT_LT, max_w=W-160)
    composite(img, h3, W//2, int(H*0.74), a, anchor="mm")
    return img

TIMELINE = [
    (4.5, scene_problem),
    (4.5, scene_intro),
    (10.5, scene_steps),
    (6.5, scene_result),
    (5.0, scene_benefits),
    (4.5, scene_proof),
    (5.0, scene_cta),
]

def main():
    print("🩺 Building AgroManch Crop Doctor video...")
    tmp = tempfile.mkdtemp()
    music = os.path.join(tmp, "bgm.wav")
    make_music(music, duration=42.0)
    render_timeline(TIMELINE, "AgroManch_CropDoctor.mp4", music)
    p = os.path.join(B.HERE, "AgroManch_CropDoctor.mp4")
    if os.path.exists(p):
        print(f"\n✅ Done: AgroManch_CropDoctor.mp4 ({os.path.getsize(p)//1024} KB)")

if __name__ == "__main__":
    main()

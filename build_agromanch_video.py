#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgroManch Marketing Video Builder
Produces two vertical (1080x1920) Hindi marketing videos with on-screen text
and an original royalty-free synthesized soundtrack.

  1. AgroManch_Promo_Vertical.mp4      — App promo
  2. AgroManch_Reel_ProfitReveal.mp4   — Sample viral Reel (Profit Reveal pattern)

Deps: pillow, numpy, imageio-ffmpeg  (auto-checked)
Fonts: assets/fonts/NotoSansDevanagari.ttf, NotoSans.ttf, NotoColorEmoji.ttf
"""

import os, sys, math, wave, struct, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "assets", "fonts")

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import imageio_ffmpeg
except ImportError as e:
    sys.exit(f"Missing dependency: {e}. Run: pip install pillow numpy imageio-ffmpeg")

FF = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
FPS = 30

# ── Palette (AgroManch brand) ───────────────────────────────
GREEN_DEEP = (16, 51, 32)      # 103320 base
GREEN_TOP  = (27, 67, 50)      # 1B4332
GREEN_BOT  = (10, 33, 22)      # darker
GREEN_MID  = (45, 106, 79)     # 2D6A4F
ACCENT     = (82, 183, 136)    # 52B788
ACCENT_LT  = (149, 213, 178)   # 95D5B2
GOLD       = (255, 214, 10)    # FFD60A
GOLD_DEEP  = (255, 183, 3)     # FFB703
WHITE      = (255, 255, 255)
SOFT_WHITE = (236, 245, 240)
RED        = (231, 76, 60)

DEVA  = os.path.join(FONT_DIR, "NotoSansDevanagari.ttf")
LATIN = os.path.join(FONT_DIR, "NotoSans.ttf")
EMOJI = os.path.join(FONT_DIR, "NotoColorEmoji.ttf")
EMOJI_STRIKE = 109  # native CBDT strike size

_font_cache = {}
def font(path, size, weight="Regular"):
    key = (path, size, weight)
    if key not in _font_cache:
        f = ImageFont.truetype(path, size)
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]

def H_(size, weight="Bold"):   return font(DEVA, size, weight)   # Hindi
def L_(size, weight="Bold"):   return font(LATIN, size, weight)  # Latin

_emoji_cache = {}
def emoji_layer(ch, target_px):
    """Render a single emoji to an RGBA image scaled to ~target_px tall."""
    key = (ch, target_px)
    if key in _emoji_cache:
        return _emoji_cache[key]
    ef = font(EMOJI, EMOJI_STRIKE)
    tmp = Image.new("RGBA", (EMOJI_STRIKE * 3, EMOJI_STRIKE * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((EMOJI_STRIKE, EMOJI_STRIKE // 2), ch, font=ef, embedded_color=True)
    bbox = tmp.getbbox()
    if bbox:
        tmp = tmp.crop(bbox)
    scale = target_px / tmp.height
    out = tmp.resize((max(1, int(tmp.width * scale)), target_px), Image.LANCZOS)
    _emoji_cache[key] = out
    return out

# ── Text helpers ────────────────────────────────────────────
def measure(text, fnt):
    bbox = fnt.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def wrap(text, fnt, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if measure(trial, fnt)[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def text_block(text, fnt, fill, max_w=W-140, line_gap=18, align="center", stroke=0, stroke_fill=(0,0,0)):
    """Return an RGBA image of (possibly wrapped) text."""
    lines = wrap(text, fnt, max_w)
    asc, desc = fnt.getmetrics()
    line_h = asc + desc
    widths = [measure(ln, fnt)[0] for ln in lines]
    bw = max(widths) if widths else 1
    bh = line_h * len(lines) + line_gap * (len(lines) - 1)
    img = Image.new("RGBA", (bw + 2*stroke + 4, bh + 2*stroke + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = stroke
    for ln, w in zip(lines, widths):
        if align == "center":
            x = (bw - w) // 2 + stroke
        elif align == "left":
            x = stroke
        else:
            x = bw - w + stroke
        d.text((x, y), ln, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        y += line_h + line_gap
    return img

def composite(base, layer, cx, cy, alpha=1.0, anchor="mm"):
    """Composite RGBA layer onto RGBA base at (cx,cy) with global alpha 0..1."""
    if layer is None:
        return
    a = max(0.0, min(1.0, alpha))
    if a <= 0:
        return
    lw, lh = layer.size
    if anchor == "mm":   x, y = cx - lw // 2, cy - lh // 2
    elif anchor == "ms": x, y = cx - lw // 2, cy - lh   # bottom-center
    elif anchor == "mt": x, y = cx - lw // 2, cy        # top-center
    else:                x, y = cx, cy
    if a < 1.0:
        layer = layer.copy()
        alpha_ch = layer.getchannel("A").point(lambda p: int(p * a))
        layer.putalpha(alpha_ch)
    base.alpha_composite(layer, (int(x), int(y)))

# ── Easing ──────────────────────────────────────────────────
def clamp01(x): return max(0.0, min(1.0, x))
def smooth(x):  x = clamp01(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp01(x); return 1 - (1 - x) ** 3
def fade_io(t, dur, fin=0.5, fout=0.5):
    """Alpha for an element of length `dur` at local time t."""
    a_in = smooth(t / fin) if fin > 0 else 1.0
    a_out = smooth((dur - t) / fout) if fout > 0 else 1.0
    return min(a_in, a_out)

# ── Background ──────────────────────────────────────────────
def make_background():
    """Vertical green gradient + soft radial glow, baked once."""
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    top = np.array(GREEN_TOP, dtype=np.float32)
    bot = np.array(GREEN_BOT, dtype=np.float32)
    ramp = np.linspace(0, 1, H)[:, None]
    grad = (top[None, :] * (1 - ramp) + bot[None, :] * ramp)  # H x 3
    arr = np.repeat(grad[:, None, :], W, axis=1).astype(np.uint8)
    bg = np.dstack([arr, np.full((H, W), 255, np.uint8)])
    base = Image.fromarray(bg, "RGBA")
    # soft radial glow upper-center
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy, r = W // 2, int(H * 0.30), 760
    for i in range(36, 0, -1):
        rr = int(r * i / 36)
        a = int(46 * (i / 36) * (1 - i / 36) * 4)
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                   fill=(ACCENT[0], ACCENT[1], ACCENT[2], max(0, a)))
    base.alpha_composite(glow)
    return base

BG = make_background()

def new_frame():
    return BG.copy()

def draw_accents(img, t):
    """Cheap drifting accent dots for subtle motion."""
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(6):
        ph = t * 0.25 + i * 1.7
        x = int(W * (0.12 + 0.76 * ((math.sin(ph) + 1) / 2)))
        y = int(H * (0.10 + 0.80 * ((i / 6.0 + t * 0.02) % 1.0)))
        rr = 5 + (i % 3) * 3
        a = 26 + 14 * ((i % 2))
        d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=(ACCENT_LT[0], ACCENT_LT[1], ACCENT_LT[2], a))

def pill(img, cx, cy, w, h, fill, alpha=1.0, radius=None):
    radius = radius or h // 2
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([0, 0, w-1, h-1], radius=radius,
                         fill=(fill[0], fill[1], fill[2], int(255*alpha)))
    img.alpha_composite(layer, (cx - w//2, cy - h//2))

def progress_bar(img, cx, cy, w, h, frac, fill=ACCENT, track=(255,255,255,60), alpha=1.0):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([0, 0, w-1, h-1], radius=h//2, fill=track)
    fw = max(h, int(w * clamp01(frac)))
    ld.rounded_rectangle([0, 0, fw-1, h-1], radius=h//2,
                         fill=(fill[0], fill[1], fill[2], int(255*alpha)))
    img.alpha_composite(layer, (cx - w//2, cy - h//2))

# ── Logo lockup ─────────────────────────────────────────────
def draw_logo(img, cy, scale=1.0, alpha=1.0, with_tagline=True):
    em = emoji_layer("🌾", int(120 * scale))
    word = text_block("AgroManch", L_(int(120 * scale), "Black"), WHITE)
    gap = int(24 * scale)
    total_w = em.width + gap + word.width
    x0 = W // 2 - total_w // 2
    composite(img, em, x0, cy, alpha, anchor="default") if False else None
    # place emoji and word baseline-aligned
    composite(img, em, x0 + em.width//2, cy, alpha, anchor="mm")
    composite(img, word, x0 + em.width + gap + word.width//2, cy, alpha, anchor="mm")
    if with_tagline:
        tg = text_block("किसान का अपना डिजिटल साथी", H_(int(52*scale), "SemiBold"), ACCENT_LT)
        composite(img, tg, W//2, cy + int(110*scale), alpha, anchor="mm")

# ════════════════════════════════════════════════════════════
#  SCENE PRIMITIVES
# ════════════════════════════════════════════════════════════
def scene_logo(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.8, 0.6)
    pop = ease_out(t / 0.9)
    scale = 0.82 + 0.18 * pop
    draw_logo(img, int(H*0.40), scale=scale, alpha=a, with_tagline=(t > 0.6))
    # underline accent
    if t > 0.5:
        progress_bar(img, W//2, int(H*0.40)+200, 420, 10, ease_out((t-0.5)/1.2), alpha=a*0.9)
    return img

def scene_statement(t, dur, lines, sub=None, color=WHITE, emoji=None, size=86):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.55, 0.5)
    rise = (1 - ease_out(t / 0.7)) * 70
    y = int(H*0.42)
    if emoji:
        em = emoji_layer(emoji, 150)
        composite(img, em, W//2, int(H*0.30) + int(rise*0.5), a, anchor="mm")
    blk = text_block(lines, H_(size, "Bold"), color, max_w=W-150, line_gap=24,
                     stroke=2, stroke_fill=(0,0,0))
    composite(img, blk, W//2, y + int(rise), a, anchor="mm")
    if sub:
        sb = text_block(sub, H_(50, "SemiBold"), ACCENT_LT, max_w=W-180)
        composite(img, sb, W//2, y + blk.height//2 + 90, a, anchor="mm")
    return img

FEATURES = [
    ("📊", "Live मंडी भाव — रोज़ का सही दाम"),
    ("🧑‍🌾", "Expert कृषि सलाह — मुफ़्त"),
    ("📋", "सरकारी योजना गाइड — पूरा फायदा"),
    ("🛒", "फसल बेचो — सीधे सही दाम पर"),
    ("⛈️", "मौसम Alert — फसल बचाओ"),
]
def scene_features(t, dur):
    img = new_frame(); draw_accents(img, t)
    sa = fade_io(t, dur, 0.4, 0.5)
    head = text_block("AgroManch में क्या मिलेगा?", H_(64, "Black"), GOLD, max_w=W-120)
    composite(img, head, W//2, int(H*0.16), sa, anchor="mm")
    n = len(FEATURES)
    row_h = 200
    y0 = int(H*0.27)
    per = (dur - 0.8) / n
    for i, (em, txt) in enumerate(FEATURES):
        start = i * per * 0.85
        lt = t - start
        if lt < 0:
            continue
        ia = smooth(lt / 0.5) * sa
        slide = (1 - ease_out(lt / 0.55)) * 80
        cy = y0 + i * row_h
        # row pill
        pill(img, W//2 + int(slide), cy, W-150, 150, GREEN_MID, alpha=0.55*ia)
        emi = emoji_layer(em, 96)
        composite(img, emi, 150 + int(slide), cy, ia, anchor="mm")
        tb = text_block(txt, H_(50, "SemiBold"), WHITE, max_w=W-360, align="left")
        composite(img, tb, 230 + int(slide), cy, ia, anchor="default") if False else \
            composite(img, tb, 230 + tb.width//2 + int(slide), cy, ia, anchor="mm")
    return img

def scene_proof(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.6, 0.5)
    # count up number
    em = emoji_layer("🤝", 150)
    composite(img, em, W//2, int(H*0.27), a, anchor="mm")
    frac = ease_out(t / (dur*0.7))
    val = int(12 + frac * (10 - 0)) / 1.0  # 12 lakh
    lakh = 2 + frac * (12 - 2)
    num = text_block(f"{lakh:.0f} लाख+", H_(140, "Black"), GOLD)
    composite(img, num, W//2, int(H*0.45), a, anchor="mm")
    sub = text_block("किसानों का भरोसा", H_(66, "Bold"), WHITE)
    composite(img, sub, W//2, int(H*0.56), a, anchor="mm")
    sub2 = text_block("हर राज्य · हर फसल · हर मौसम", H_(46, "SemiBold"), ACCENT_LT, max_w=W-160)
    composite(img, sub2, W//2, int(H*0.63), a, anchor="mm")
    return img

def scene_cta(t, dur, app=True):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.5, 0.4)
    pulse = 1.0 + 0.04 * math.sin(t * 6)
    draw_logo(img, int(H*0.30), scale=0.7, alpha=a, with_tagline=False)
    if app:
        l1 = text_block("अभी Download करो — FREE", H_(70, "Black"), WHITE, max_w=W-140)
    else:
        l1 = text_block("ऐसे और राज़ AgroManch app पर", H_(64, "Black"), WHITE, max_w=W-140)
    composite(img, l1, W//2, int(H*0.46), a, anchor="mm")
    # download button
    bw, bh = int(640*pulse), int(150*pulse)
    pill(img, W//2, int(H*0.58), bw, bh, GOLD, alpha=a)
    btn = text_block("📲  AgroManch App", L_(60, "Black"), GREEN_DEEP)
    # emoji inside button rendered separately
    emi = emoji_layer("📲", 70)
    bt = text_block("AgroManch App", L_(60, "Black"), GREEN_DEEP)
    tw = emi.width + 18 + bt.width
    composite(img, emi, W//2 - tw//2 + emi.width//2, int(H*0.58), a, anchor="mm")
    composite(img, bt, W//2 - tw//2 + emi.width + 18 + bt.width//2, int(H*0.58), a, anchor="mm")
    handle = text_block("@AgroManch  ·  www.agromanch.in", L_(42, "SemiBold"), ACCENT_LT, max_w=W-160)
    composite(img, handle, W//2, int(H*0.70), a, anchor="mm")
    return img

# ── Reel-specific scenes ────────────────────────────────────
def scene_hook(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.4, 0.45)
    em = emoji_layer("😱", int(170 * (0.7 + 0.3*ease_out(t/0.6))))
    composite(img, em, W//2, int(H*0.26), a, anchor="mm")
    shake = int(6 * math.sin(t * 28)) if t < 1.2 else 0
    l1 = text_block("एक एकड़ गेहूं से", H_(82, "Bold"), WHITE, max_w=W-140)
    composite(img, l1, W//2 + shake, int(H*0.44), a, anchor="mm")
    big = text_block("₹2 लाख कमाए!", H_(128, "Black"), GOLD, max_w=W-120, stroke=3, stroke_fill=(0,0,0))
    composite(img, big, W//2, int(H*0.56), a, anchor="mm")
    return img

def scene_build(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.4, 0.4)
    l1 = text_block("कैसे?", H_(120, "Black"), GOLD)
    composite(img, l1, W//2, int(H*0.40), a, anchor="mm")
    l2 = text_block("पूरा हिसाब देखो", H_(78, "Bold"), WHITE, max_w=W-140)
    composite(img, l2, W//2, int(H*0.52), a, anchor="mm")
    em = emoji_layer("👇", int(120))
    bob = int(18 * math.sin(t*5))
    composite(img, em, W//2, int(H*0.62)+bob, a, anchor="mm")
    return img

BREAKDOWN = [
    ("लागत", 35000, RED, "💸"),
    ("कुल कमाई", 235000, ACCENT, "💰"),
    ("शुद्ध मुनाफ़ा", 200000, GOLD, "🎉"),
]
def scene_breakdown(t, dur):
    img = new_frame(); draw_accents(img, t)
    sa = fade_io(t, dur, 0.3, 0.4)
    head = text_block("1 एकड़ गेहूं — पूरा गणित", H_(58, "Black"), WHITE, max_w=W-120)
    composite(img, head, W//2, int(H*0.14), sa, anchor="mm")
    y0 = int(H*0.28); row_h = 250
    per = (dur - 0.6) / len(BREAKDOWN)
    for i, (label, amount, col, em) in enumerate(BREAKDOWN):
        start = i * per
        lt = t - start
        if lt < 0:
            continue
        ia = smooth(lt / 0.45) * sa
        cy = y0 + i * row_h
        pill(img, W//2, cy, W-150, 210, GREEN_MID, alpha=0.5*ia)
        emi = emoji_layer(em, 92)
        composite(img, emi, 150, cy, ia, anchor="mm")
        lab = text_block(label, H_(54, "SemiBold"), SOFT_WHITE, align="left")
        composite(img, lab, 250 + lab.width//2, cy - 42, ia, anchor="mm")
        cnt = int(ease_out(lt / 1.0) * amount)
        val = text_block(f"₹ {cnt:,}", L_(78, "Black"), col)
        composite(img, val, 250 + val.width//2, cy + 48, ia, anchor="mm")
    return img

def scene_proof_reel(t, dur):
    img = new_frame(); draw_accents(img, t)
    a = fade_io(t, dur, 0.55, 0.45)
    em = emoji_layer("🧑‍🌾", 160)
    composite(img, em, W//2, int(H*0.30), a, anchor="mm")
    l1 = text_block("UP के किसान की", H_(72, "Bold"), WHITE, max_w=W-140)
    composite(img, l1, W//2, int(H*0.46), a, anchor="mm")
    l2 = text_block("सच्ची कहानी", H_(96, "Black"), GOLD, max_w=W-140)
    composite(img, l2, W//2, int(H*0.55), a, anchor="mm")
    l3 = text_block("सही जानकारी · सही फैसला · ज़्यादा मुनाफ़ा",
                    H_(44, "SemiBold"), ACCENT_LT, max_w=W-150)
    composite(img, l3, W//2, int(H*0.64), a, anchor="mm")
    return img

# ════════════════════════════════════════════════════════════
#  TIMELINES
# ════════════════════════════════════════════════════════════
PROMO = [
    (4.5, scene_logo),
    (4.2, lambda t, d: scene_statement(t, d, "मंडी भाव पता नहीं? सही दाम नहीं मिलता?",
                                       emoji="😟", size=78)),
    (4.2, lambda t, d: scene_statement(t, d, "सरकारी योजना का फायदा छूट जाता है?",
                                       emoji="😕", size=78)),
    (14.0, scene_features),
    (4.5, scene_proof),
    (5.2, lambda t, d: scene_cta(t, d, app=True)),
]

REEL = [
    (4.2, scene_hook),
    (3.0, scene_build),
    (12.0, scene_breakdown),
    (4.0, scene_proof_reel),
    (5.0, lambda t, d: scene_cta(t, d, app=False)),
]

def render_timeline(timeline, out_name, music_path):
    total = sum(d for d, _ in timeline)
    nframes = int(total * FPS)
    print(f"  → {out_name}: {total:.1f}s  ({nframes} frames)")
    cmd = [FF, "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "pipe:0",
           "-i", music_path,
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
           os.path.join(HERE, out_name)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # build cumulative scene boundaries
    bounds = []
    acc = 0.0
    for d, fn in timeline:
        bounds.append((acc, acc + d, d, fn))
        acc += d
    for fi in range(nframes):
        gt = fi / FPS
        # find the scene this frame belongs to (last scene catches the final frame)
        s, e, d, fn = bounds[-1]
        for bs, be, bd, bfn in bounds:
            if bs <= gt < be:
                s, e, d, fn = bs, be, bd, bfn
                break
        frame = fn(gt - s, d)
        rgb = frame.convert("RGB")
        proc.stdin.write(rgb.tobytes())
        if fi % 90 == 0:
            print(f"      frame {fi}/{nframes}", flush=True)
    proc.stdin.close()
    proc.wait()
    print(f"  ✓ saved {out_name}")

# ════════════════════════════════════════════════════════════
#  MUSIC (numpy synth, royalty-free original)
# ════════════════════════════════════════════════════════════
def make_music(path, duration=42.0, sr=44100):
    n = int(duration * sr)
    t = np.arange(n) / sr
    out = np.zeros(n, dtype=np.float32)

    def note(freq, t0, dur, amp, harmonics=(1.0, 0.5, 0.25), vib=0.0):
        i0 = int(t0 * sr); i1 = min(n, int((t0 + dur) * sr))
        if i1 <= i0:
            return
        lt = np.arange(i1 - i0) / sr
        env = np.minimum(lt / 0.15, 1.0) * np.minimum((dur - lt) / 0.5, 1.0)
        env = np.clip(env, 0, 1) ** 1.2
        sig = np.zeros_like(lt)
        vibrato = (1 + vib * np.sin(2*np.pi*5*lt))
        for k, ha in enumerate(harmonics, 1):
            sig += ha * np.sin(2*np.pi*freq*k*lt*vibrato)
        out[i0:i1] += amp * env * sig

    # C major progression: C  G  Am  F  (warm, hopeful)
    chords = [
        (("C3","E3","G3"), ),
        (("G2","B2","D3"), ),
        (("A2","C3","E3"), ),
        (("F2","A2","C3"), ),
    ]
    freqs = {"C2":65.41,"D2":73.42,"E2":82.41,"F2":87.31,"G2":98.00,"A2":110.0,"B2":123.47,
             "C3":130.81,"D3":146.83,"E3":164.81,"F3":174.61,"G3":196.0,"A3":220.0,"B3":246.94,
             "C4":261.63,"D4":293.66,"E4":329.63,"F4":349.23,"G4":392.0,"A4":440.0}
    bar = 2.0  # seconds per chord
    nb = int(np.ceil(duration / bar))
    arp_seq = ["C4","E4","G4","E4"]
    for b in range(nb):
        t0 = b * bar
        chord = chords[b % len(chords)][0]
        # pad
        for nm in chord:
            note(freqs[nm], t0, bar*1.02, amp=0.10, harmonics=(1.0,0.45,0.2,0.1), vib=0.004)
        # gentle arpeggio (lighter, higher)
        root = chord[0]
        # build a simple triad arp from root octave up
        base = freqs[root] * 2
        arp = [base, base*1.25, base*1.5, base*1.25]
        for k, fr in enumerate(arp):
            note(fr, t0 + k*(bar/4), bar/4*0.9, amp=0.045,
                 harmonics=(1.0,0.3), vib=0.0)

    # soft global fade in/out
    fin = int(1.5 * sr); fout = int(2.5 * sr)
    out[:fin] *= np.linspace(0, 1, fin)
    out[-fout:] *= np.linspace(1, 0, fout)
    # normalize
    peak = np.max(np.abs(out)) or 1.0
    out = (out / peak) * 0.72
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    print(f"  ✓ music: {path}  ({duration:.0f}s)")

# ════════════════════════════════════════════════════════════
def main():
    print("🎬 Building AgroManch marketing videos...")
    tmp = tempfile.mkdtemp()
    music = os.path.join(tmp, "agromanch_bgm.wav")
    print("  → synthesizing soundtrack...")
    make_music(music, duration=42.0)

    print("  → rendering PROMO video...")
    render_timeline(PROMO, "AgroManch_Promo_Vertical.mp4", music)

    print("  → rendering REEL video...")
    render_timeline(REEL, "AgroManch_Reel_ProfitReveal.mp4", music)

    print("\n✅ Done!")
    for f in ("AgroManch_Promo_Vertical.mp4", "AgroManch_Reel_ProfitReveal.mp4"):
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            print(f"   {f}  ({os.path.getsize(p)//1024} KB)")

if __name__ == "__main__":
    main()

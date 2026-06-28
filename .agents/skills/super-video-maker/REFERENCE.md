# Super Video Maker Reference

## Core Production Modes

| Mode | Primary tools | Typical length |
|------|--------------|----------------|
| Avatar Explainer | HeyGen + FFmpeg + Whisper captions | 60–120 s |
| Screen-recording demo | Playwright recorder + demo_video_composer | 30–90 s |
| Faceless b-roll ad | Seedance + ElevenLabs voice + FFmpeg | 15–60 s |
| Captioned talking head | video_captioner + Remotion CaptionedTalkingHead | any length |
| Motion-graphics explainer | Remotion DistribbExplainer pattern | 30–60 s |
| HyperFrames HTML video | hyperframes-template | 15–90 s |
| Long-form → vertical shorts | video_captioner vertical_shorts mode | 30–90 s clips |

## Editorial Taste System

Every visual must answer: **"What state change should the viewer understand?"**

Five visual jobs — every shot earns its place by serving exactly one:

| Job | Description | Example |
|-----|-------------|---------|
| **Proof** | Shows that the claim is true | Official announcement screenshot |
| **Mechanism** | Shows how or why it works | Feature section UI, system diagram |
| **Consequence** | Shows what happens next | Coverage aggregator, downstream effect |
| **Action** | Shows what the viewer should do | UI screenshot with arrow overlay |
| **Transition** | Bridges two ideas or sections | Pull-quote card, b-roll establishing shot |

If a shot is none of the five, it is filler. Cut it.

## B-roll Design System

**Route every non-hook beat through this priority table:**

| Beat purpose | First choice | Second choice | Last resort |
|-------------|-------------|----------------|-------------|
| News beat | Real screenshot → Ken Burns | Editorial photo | `gpt-image-2` documentary still |
| Source proof | Agent-operated browser recording | Real screenshot callout | — |
| Story/example | Working surface (doc, dashboard, SERP, Slack) | UI micro-story | `gpt-image-2` realistic scene |
| Concept/metaphor | Typographic pull-quote card | UI state change | `gpt-image-2` with strict realism prompt |
| Aggregate | Techmeme / Trends / HN screenshot → Ken Burns | Headline montage | — |
| Action step | Real UI screenshot with arrow overlay | Screen recording | — |

**AI-generated b-roll rules (use only as last resort):**
- Model: `gpt-image-2`, `quality=high`
- Size: `2048x1152` (native 16:9 — no padding)
- Prompt style: documentary-realism, specific location, real people doing real tasks
- Ban list: floating objects, neon grids, dark cosmic backgrounds, symbolic abstractions, glowing icons

## Source Deck Strategy

Build the source deck **before** writing the storyboard. Each asset needs a unique editorial job:

| Asset | Job |
|-------|-----|
| Official announcement hero | Proof / establishing receipt |
| Exact paragraph crop | Proof of technical claim |
| Feature section crop | Mechanism |
| Byline / date crop | Credibility receipt |
| Aggregator or outlet list | Consequence / momentum |
| UI / action surface | Action step |

**Hard rule:** One website can appear more than once only if every appearance proves a **different** fact, phrase, or mechanism. Never use "same page, slightly different zoom" as filler.

## Ken Burns Rules

- Scale-to-fill, never pad. `scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160`
- `zoompan` for slow drift. Keep `z='min(zoom+0.0012,1.08)'` for a subtle push.
- Cut every 2–4 s on AI stills, every 3–6 s on real screenshots.
- Long beats: split into establishing receipt → exact phrase crop → feature crop, not "same zoom slightly adjusted."

## Layout Zones (1920×1080 master)

```
┌─────────────────────────────────────────────────────┐
│ [BADGE top-left 420×80, hook only, fades at 4.5s]   │
│                                           [PiP 492×276│
│                                            top-right] │
│              CENTER B-ROLL                            │
│                                                       │
│ [CAPTIONS bottom-center, MarginV=90, Alignment=2]    │
└─────────────────────────────────────────────────────┘
```

**Non-negotiable rules:**
- Badge (top-left) is gone before PiP appears. Never overlap.
- Captions stay `Alignment=2` (bottom-center). Never left-align.
- PiP is top-right. Never bottom. Never during outro CTA tail.
- Only one overlay at a time per zone. No stacking.

## Avatar PiP Styling

Borderless rounded card with soft drop shadow. Pre-render two PNGs once per job using Pillow:

- `assets/pip_mask.png` — 492×276 RGBA with 24px rounded corners (white inside, transparent outside)
- `assets/pip_shadow.png` — same size, blurred dark ellipse offset +4/+16

FFmpeg compose at `x=1378, y=50` (top-right, 50px from edges):

```bash
ffmpeg -y \
  -i background.mp4 -i avatar_green.mp4 -i assets/pip_mask.png -i assets/pip_shadow.png \
  -filter_complex "\
[1:v]chromakey=0x00ff00:0.18:0.08,scale=492:276,format=rgba[av];\
[2:v]format=rgba[mask];\
[av][mask]alphamerge[avr];\
[3:v]format=rgba[sh];\
[0:v][sh]overlay=x=1382:y=66:enable='between(t,T0,T1)'[bg2];\
[bg2][avr]overlay=x=1378:y=50:enable='between(t,T0,T1)':format=auto[v]" \
  -map "[v]" -map 0:a? \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy with_pip.mp4
```

Do **NOT** add a `pad` color border. The rounded crop + shadow is the modern card look.

Pillow snippet to create pip_mask.png:

```python
from PIL import Image, ImageDraw
W, H, R = 492, 276, 24
mask = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(mask).rounded_rectangle([0, 0, W, H], radius=R, fill=(255, 255, 255, 255))
mask.save("assets/pip_mask.png")
```

Pillow snippet to create pip_shadow.png:

```python
from PIL import Image, ImageDraw, ImageFilter
W, H = 492, 276
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).ellipse([20, 20, W - 20, H - 20], fill=(0, 0, 0, 160))
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=14))
shadow.save("assets/pip_shadow.png")
```

## Disclosure Badge

Render once with Pillow (`build_disclosure_badge.py`). Dark navy fill, orange outline, white text, rounded pill (~420×80 RGBA transparent).

Overlay top-left during hook only:

```bash
ffmpeg -y -i body.mp4 -i assets/disclosure_badge.png \
  -filter_complex "[0:v][1:v]overlay=50:50:enable='between(t,0.5,4.5)'[v]" \
  -map "[v]" -map 0:a? -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy with_badge.mp4
```

## Caption Style (Default ASS)

Hormozi-style karaoke, bottom-center, active word in yellow:

```
Style: Default,Arial Black,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,2,2,80,80,90,1
Style: Active,Arial Black,64,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,2,2,80,80,90,1
```

Key values: `Alignment=2` (bottom-center), `MarginL=MarginR=80`, `MarginV=90`, `Fontsize=64`, `Bold=-1`, `Outline=5`, `Shadow=2`.

## Provider Guidance

### HeyGen

- Use `heygen_client.py`. Set `HEYGEN_AVATAR_ID` and `HEYGEN_VOICE_ID` in `.env`.
- Always use green-screen background (`#00FF00`) for chroma-key compositing.
- Resolution: `1080p`. Aspect: `16:9`.
- Poll up to 600 s. Status: `processing` → `completed` / `failed`.

### Replicate Seedance 2.0

- Use `replicate_video.py generate`. Model: `bytedance/seedance-2.0`.
- Duration: 1–7 s. Resolution: `1080p`. Aspect: `16:9` for landscape, `9:16` for vertical.
- Never loop a clip to fill a long beat. Choose: complementary b-roll, `tpad=stop_mode=clone:stop_duration=N` (≤2 s), or Ken Burns still.

### OpenAI Images

- Use `image_provider.py generate`. Model: `gpt-image-2`, `quality=high`.
- Size: `2048x1152` for 16:9 (native — never pad).
- Documentary-realism prompts only. Ban list: neon grids, floating objects, symbolic abstractions.
- Cut every 2–4 s. Never hold a single AI still for more than ~3.5 s.

### ElevenLabs

- Use `music_provider.py elevenlabs-plan` to validate API key before generation.
- Voice TTS: use in `demo_video_composer.py` or directly via API.
- Music: mix at −20 dB under voice (≈ 12% volume). Loudnorm final audio to −16 LUFS.

### Whisper

- Use `video_captioner.py` or direct OpenAI API call.
- Always request `word`-level timestamps (`timestamp_granularities=["word"]`).
- Master offset = 0 when the master timeline starts with the avatar (no title pre-roll).

### FFmpeg

- Final export defaults: `libx264`, `yuv420p`, `aac 192k`, `30fps`, `CRF 18`.
- See `FFMPEG_PLAYBOOK.md` for every compositing recipe.

## Quality Checklist

Before declaring a video done, verify all of these:

- [ ] No overlapping overlays (badge gone before PiP, PiP gone during outro)
- [ ] Captions are bottom-centered (not left-aligned)
- [ ] PiP is top-right, borderless, rounded, with shadow
- [ ] Outro card is visible during the spoken CTA tail (no dead air)
- [ ] Every shot has exactly one editorial job
- [ ] No repeated source page with same crop/zoom
- [ ] Screen recordings show investigation (not slow scrolling)
- [ ] Generated stills use `gpt-image-2` `quality=high`, 16:9, documentary realism
- [ ] Final codec: h264, yuv420p, AAC, 30fps
- [ ] Duration matches avatar audio (no silent frames at end)
- [ ] `ffmpeg_qc.py` passes with no warnings

#!/usr/bin/env python3
"""Demo video composer — combines screen recordings with professional polish.

Outputs a 2560×1440 demo video with:
  - MacBook bezel frame
  - Gradient background with accent glow orbs
  - Click ripple animations
  - Cursor highlight glow
  - Zoom-in transitions on click events
  - ElevenLabs TTS voiceover with ASS word-level subtitles
  - Background music mixed at low volume
  - Optional S3 upload

Main entry points
-----------------
compose_demo_video()   — full pipeline given a recording + events JSON
compose_from_recording() — convenience wrapper; can auto-generate script via Claude
"""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFilter

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CANVAS_W = 2560
CANVAS_H = 1440
LAPTOP_SCREEN_W = 1920
LAPTOP_SCREEN_H = 1080
FPS = 30
ZOOM_DURATION = 2.0          # seconds
ZOOM_EASE = 0.3              # ease-in / ease-out portion
RIPPLE_DURATION = 0.5        # seconds
RIPPLE_MAX_RADIUS = 80
CURSOR_GLOW_RADIUS = 36
BGM_VOLUME = 0.08
VOICEOVER_VOLUME = 1.0


# ---------------------------------------------------------------------------
# ElevenLabs TTS
# ---------------------------------------------------------------------------

def generate_narration(
    script: str,
    output_mp3: Path,
    timestamps_json: Path,
    voice_id: str | None = None,
) -> dict:
    """Call ElevenLabs with timestamps and save mp3 + word timestamps JSON."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    vid = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps"
    payload = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.35},
    }
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    import base64
    audio_bytes = base64.b64decode(data["audio_base64"])
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    output_mp3.write_bytes(audio_bytes)

    alignment = data.get("alignment", {})
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    ends = alignment.get("character_end_times_seconds", [])
    words = _chars_to_words(chars, starts, ends)
    timestamps_json.parent.mkdir(parents=True, exist_ok=True)
    timestamps_json.write_text(json.dumps(words, indent=2))
    return {"audio": str(output_mp3), "timestamps": str(timestamps_json), "words": words}


def _chars_to_words(chars, starts, ends):
    """Group character-level alignment into word-level records."""
    words = []
    buf = ""
    w_start = None
    w_end = None
    for ch, s, e in zip(chars, starts, ends):
        if ch == " " and buf.strip():
            words.append({"word": buf.strip(), "start": w_start, "end": w_end})
            buf = ""
            w_start = None
        else:
            buf += ch
            if w_start is None:
                w_start = s
            w_end = e
    if buf.strip() and w_start is not None:
        words.append({"word": buf.strip(), "start": w_start, "end": w_end})
    return words


# ---------------------------------------------------------------------------
# S3 upload
# ---------------------------------------------------------------------------

def upload_to_s3(local_path: Path, s3_key: str) -> str:
    """Upload file to S3 and return public URL."""
    import boto3
    bucket = os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise RuntimeError("AWS_S3_BUCKET not set")
    region = os.getenv("AWS_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=region)
    s3.upload_file(str(local_path), bucket, s3_key, ExtraArgs={"ACL": "public-read"})
    base = os.getenv("SOUNDTRACKS_S3_BASE_URL", f"https://{bucket}.s3.{region}.amazonaws.com")
    return f"{base}/{s3_key}"


# ---------------------------------------------------------------------------
# ASS subtitle file
# ---------------------------------------------------------------------------

def _sec_to_ass(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def create_subtitle_file(words: list[dict], output_ass: Path, chunk: int = 3) -> Path:
    """Build karaoke-style ASS with 3-word chunks; current word yellow."""
    header = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 2560
PlayResY: 1440
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,68,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,80,80,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    chunks: list[dict] = []
    for i in range(0, len(words), chunk):
        group = words[i: i + chunk]
        if not group:
            continue
        chunks.append({"words": group, "start": group[0]["start"], "end": group[-1]["end"]})

    lines = [header]
    for ci, ch in enumerate(chunks):
        t_start = _sec_to_ass(ch["start"])
        t_end = _sec_to_ass(ch["end"])
        ws = ch["words"]
        for wi, w in enumerate(ws):
            w_start = _sec_to_ass(w["start"])
            w_end = _sec_to_ass(w["end"])
            parts = []
            for j, ww in enumerate(ws):
                if j < wi:
                    parts.append(f"{{\\c&H888888&}}{ww['word']}{{\\c&HFFFFFF&}}")
                elif j == wi:
                    parts.append(f"{{\\c&H0000FFFF&}}{ww['word']}{{\\c&HFFFFFF&}}")
                else:
                    parts.append(ww["word"])
            text = " ".join(parts)
            lines.append(f"Dialogue: 0,{w_start},{w_end},Default,,0,0,0,,{text}")

    output_ass.parent.mkdir(parents=True, exist_ok=True)
    output_ass.write_text("".join(lines))
    return output_ass


# ---------------------------------------------------------------------------
# Background music
# ---------------------------------------------------------------------------

def download_bgm(output_path: Path) -> Path | None:
    """Try to download BGM from S3. Returns None if unavailable."""
    base = os.getenv("SOUNDTRACKS_S3_BASE_URL", "")
    if not base:
        return None
    url = f"{base}/bgm/demo_upbeat.mp3"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(resp.content)
        return output_path
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Pillow frame rendering helpers
# ---------------------------------------------------------------------------

def render_gradient_background(w: int = CANVAS_W, h: int = CANVAS_H) -> Image.Image:
    """Dark blue-purple gradient with two accent glow orbs."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    c1 = (10, 14, 26)
    c2 = (22, 14, 40)
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for cx, cy, col in [
        (int(w * 0.22), int(h * 0.28), (255, 107, 44)),
        (int(w * 0.78), int(h * 0.72), (94, 99, 234)),
    ]:
        for r in range(500, 0, -10):
            alpha = int(18 * (r / 500))
            gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*col, alpha))
    return Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")


def render_laptop_frame(screen: Image.Image) -> Image.Image:
    """Composite the screen image inside a MacBook-style bezel on the canvas."""
    canvas = render_gradient_background()

    bezel_w = LAPTOP_SCREEN_W + 80
    bezel_h = LAPTOP_SCREEN_H + 100
    bezel_x = (CANVAS_W - bezel_w) // 2
    bezel_y = (CANVAS_H - bezel_h) // 2

    bezel = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bezel)
    bd.rounded_rectangle([0, 0, bezel_w - 1, bezel_h - 1], radius=18,
                         fill=(28, 28, 30, 255), outline=(60, 60, 65, 255), width=2)
    bd.ellipse([bezel_w // 2 - 5, 12, bezel_w // 2 + 5, 22], fill=(50, 50, 52, 255))

    screen_area = screen.resize((LAPTOP_SCREEN_W, LAPTOP_SCREEN_H), Image.Resampling.LANCZOS)
    bezel.paste(screen_area, (40, 50))

    shadow = Image.new("RGBA", (bezel_w + 80, bezel_h + 80), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i in range(40, 0, -1):
        alpha = int(90 * (i / 40))
        sd.rounded_rectangle([40 - i, 40 - i, bezel_w + 40 + i, bezel_h + 40 + i],
                              radius=20 + i, fill=(0, 0, 0, alpha))
    shadow_x = bezel_x - 40
    shadow_y = bezel_y - 40
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(shadow, (shadow_x, shadow_y))
    canvas.alpha_composite(bezel, (bezel_x, bezel_y))
    return canvas.convert("RGB")


def render_click_ripple(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    elapsed: float,
) -> None:
    """Draw expanding ripple ring at (cx, cy) based on elapsed seconds."""
    if elapsed < 0 or elapsed > RIPPLE_DURATION:
        return
    progress = elapsed / RIPPLE_DURATION
    radius = int(RIPPLE_MAX_RADIUS * progress)
    alpha = int(255 * (1.0 - progress))
    color = (255, 200, 80, alpha)
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=color,
        width=max(1, int(4 * (1.0 - progress))),
    )


def render_cursor_glow(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    alpha: int = 180,
) -> None:
    """Draw a soft glow halo at the cursor position."""
    for r in range(CURSOR_GLOW_RADIUS, 0, -2):
        a = int(alpha * (r / CURSOR_GLOW_RADIUS) ** 2)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 220, 100, a))


# ---------------------------------------------------------------------------
# Zoom window helpers
# ---------------------------------------------------------------------------

def _ease_in_out(t: float) -> float:
    return t * t * (3 - 2 * t)


def _build_zoom_windows(events: list[dict]) -> list[dict]:
    """Build zoom window descriptors from click events."""
    windows = []
    for ev in events:
        if ev.get("type") != "click":
            continue
        ts = ev.get("timestamp", 0.0)
        x_pct = ev.get("x_pct", 0.5)
        y_pct = ev.get("y_pct", 0.5)
        windows.append({
            "start": ts,
            "end": ts + ZOOM_DURATION,
            "x_pct": x_pct,
            "y_pct": y_pct,
            "scale": 1.6,
        })
    return windows


def _get_zoom_at_time(windows: list[dict], t: float) -> tuple[float, float, float]:
    """Return (scale, cx_pct, cy_pct) for the current timestamp."""
    for w in windows:
        if t < w["start"] or t > w["end"]:
            continue
        elapsed = t - w["start"]
        duration = w["end"] - w["start"]
        half = ZOOM_EASE
        if elapsed < half * duration:
            progress = _ease_in_out(elapsed / (half * duration))
        elif elapsed > (1 - half) * duration:
            progress = _ease_in_out((w["end"] - t) / (half * duration))
        else:
            progress = 1.0
        scale = 1.0 + (w["scale"] - 1.0) * progress
        return scale, w["x_pct"], w["y_pct"]
    return 1.0, 0.5, 0.5


# ---------------------------------------------------------------------------
# Frame extraction
# ---------------------------------------------------------------------------

def extract_frames(video_path: Path, out_dir: Path, fps: int = FPS) -> list[Path]:
    """Extract frames from video at the given FPS into out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(out_dir / "frame_%06d.jpg")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path), "-vf", f"fps={fps}", "-q:v", "2", pattern],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return sorted(out_dir.glob("frame_*.jpg"))


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def compose_demo_video(
    recording: Path,
    events: list[dict],
    output: Path,
    narration_mp3: Path | None = None,
    narration_words: list[dict] | None = None,
    bgm_path: Path | None = None,
    upload_s3: bool = False,
    fps: int = FPS,
) -> dict:
    """Full demo video composition pipeline.

    Parameters
    ----------
    recording:       path to raw screen recording MP4
    events:          list of event dicts (clicks, scrolls, navigation, markers)
    output:          destination MP4 path
    narration_mp3:   pre-generated ElevenLabs voiceover
    narration_words: word-level timestamps from ElevenLabs
    bgm_path:        optional background music file
    upload_s3:       upload final video + subtitle to S3
    fps:             output frame rate
    """
    tmp = Path(tempfile.mkdtemp(prefix="demo_compose_"))
    frames_dir = tmp / "raw_frames"
    processed_dir = tmp / "processed_frames"
    processed_dir.mkdir(parents=True, exist_ok=True)
    ass_path = tmp / "captions.ass"

    print(f"[demo_composer] Extracting frames from {recording} …", file=sys.stderr)
    raw_frames = extract_frames(recording, frames_dir, fps)
    n_frames = len(raw_frames)
    if n_frames == 0:
        raise RuntimeError("No frames extracted from recording")

    zoom_windows = _build_zoom_windows(events)

    clicks_by_time: dict[float, tuple[int, int]] = {}
    for ev in events:
        if ev.get("type") == "click":
            ts = ev["timestamp"]
            x = int(ev.get("x_pct", 0.5) * LAPTOP_SCREEN_W)
            y = int(ev.get("y_pct", 0.5) * LAPTOP_SCREEN_H)
            clicks_by_time[ts] = (x, y)

    print(f"[demo_composer] Compositing {n_frames} frames …", file=sys.stderr)
    for idx, frame_path in enumerate(raw_frames):
        t = idx / fps

        screen = Image.open(frame_path).convert("RGB")

        scale, cx_pct, cy_pct = _get_zoom_at_time(zoom_windows, t)
        if scale > 1.001:
            sw = int(LAPTOP_SCREEN_W / scale)
            sh = int(LAPTOP_SCREEN_H / scale)
            x0 = int((LAPTOP_SCREEN_W - sw) * cx_pct)
            y0 = int((LAPTOP_SCREEN_H - sh) * cy_pct)
            x0 = max(0, min(LAPTOP_SCREEN_W - sw, x0))
            y0 = max(0, min(LAPTOP_SCREEN_H - sh, y0))
            screen = screen.crop((x0, y0, x0 + sw, y0 + sh)).resize(
                (LAPTOP_SCREEN_W, LAPTOP_SCREEN_H), Image.Resampling.LANCZOS
            )

        overlay = screen.convert("RGBA")
        od = ImageDraw.Draw(overlay)

        for click_t, (cx, cy) in clicks_by_time.items():
            elapsed = t - click_t
            render_cursor_glow(od, cx, cy, alpha=max(0, int(180 * (1 - elapsed / 0.3))))
            render_click_ripple(od, cx, cy, elapsed)

        screen_with_fx = overlay.convert("RGB")
        canvas = render_laptop_frame(screen_with_fx)

        out_frame = processed_dir / f"frame_{idx:06d}.jpg"
        canvas.save(out_frame, quality=88)

    if narration_words:
        create_subtitle_file(narration_words, ass_path)

    print("[demo_composer] Encoding final video …", file=sys.stderr)
    output.parent.mkdir(parents=True, exist_ok=True)
    _encode_video(processed_dir, fps, narration_mp3, bgm_path, ass_path if narration_words else None, output)

    result: dict[str, Any] = {
        "status": "succeeded",
        "local_path": str(output),
        "frame_count": n_frames,
    }
    if narration_words:
        result["subtitle_path"] = str(ass_path)
    if upload_s3:
        s3_key = f"demo_videos/{output.name}"
        url = upload_to_s3(output, s3_key)
        result["s3_url"] = url
        if narration_words:
            ass_s3_key = f"demo_videos/{ass_path.name}"
            result["subtitle_s3_url"] = upload_to_s3(ass_path, ass_s3_key)

    print("RESULT: " + json.dumps(result), flush=True)
    return result


def _encode_video(
    frames_dir: Path,
    fps: int,
    narration: Path | None,
    bgm: Path | None,
    ass: Path | None,
    output: Path,
) -> None:
    """Assemble frames + audio tracks via FFmpeg."""
    inputs = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%06d.jpg"),
    ]
    filter_parts: list[str] = []
    audio_map: list[str] = []
    stream_idx = 1

    if narration and narration.exists():
        inputs += ["-i", str(narration)]
        n_stream = stream_idx
        stream_idx += 1
    else:
        n_stream = None

    if bgm and bgm.exists():
        inputs += ["-i", str(bgm), "-stream_loop", "-1"]
        b_stream = stream_idx
        stream_idx += 1
    else:
        b_stream = None

    if n_stream is not None and b_stream is not None:
        filter_parts.append(
            f"[{n_stream}:a]volume={VOICEOVER_VOLUME}[vo];"
            f"[{b_stream}:a]volume={BGM_VOLUME}[bgm];"
            "[vo][bgm]amix=inputs=2:duration=first[aout]"
        )
        audio_map = ["-map", "[aout]"]
    elif n_stream is not None:
        filter_parts.append(f"[{n_stream}:a]volume={VOICEOVER_VOLUME}[aout]")
        audio_map = ["-map", "[aout]"]
    elif b_stream is not None:
        filter_parts.append(f"[{b_stream}:a]volume={BGM_VOLUME}[aout]")
        audio_map = ["-map", "[aout]"]

    vf_parts: list[str] = []
    if ass and ass.exists():
        escaped = str(ass).replace("\\", "\\\\").replace(":", "\\:")
        vf_parts.append(f"ass={escaped}")

    vf = ",".join(vf_parts) if vf_parts else "copy"
    filter_complex = ";".join(filter_parts)

    cmd = inputs + ["-map", "0:v"]
    if filter_complex:
        cmd += ["-filter_complex", filter_complex]
    if vf_parts:
        cmd += ["-vf", vf]
    cmd += audio_map
    cmd += [
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output),
    ]
    subprocess.run(cmd, check=True, stderr=subprocess.PIPE)


# ---------------------------------------------------------------------------
# Script generation via Claude
# ---------------------------------------------------------------------------

def generate_narration_script(events: list[dict], context: str = "") -> str:
    """Use Claude to write a narration script from recorded events."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    event_summary = json.dumps(
        [{"type": e.get("type"), "timestamp": e.get("timestamp"), "label": e.get("label", "")}
         for e in events],
        indent=2,
    )
    prompt = f"""You are writing voiceover narration for a product demo video.

Events recorded (with timestamps in seconds):
{event_summary}

Additional context:
{context or 'No additional context provided.'}

Write a natural, enthusiastic narrator script that matches the pacing of these events.
The script should:
- Be concise and engaging (aim for ~150 words per minute)
- Highlight key actions at the appropriate timestamps
- Sound professional, not robotic
- Start immediately without preamble

Return ONLY the narration text, no stage directions or markup."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------

def compose_from_recording(
    recording: Path,
    events_json: Path,
    output: Path,
    script: str | None = None,
    generate_script: bool = True,
    context: str = "",
    voice_id: str | None = None,
    upload_s3: bool = False,
) -> dict:
    """Convenience wrapper: events JSON → polished demo video.

    If `script` is None and `generate_script` is True, Claude auto-writes
    the narration from the recorded events.
    """
    events = json.loads(events_json.read_text())
    if isinstance(events, dict) and "events" in events:
        events = events["events"]

    work_dir = output.parent / (output.stem + "_work")
    work_dir.mkdir(parents=True, exist_ok=True)

    narration_mp3 = None
    narration_words = None

    if script is None and generate_script:
        print("[demo_composer] Generating narration script via Claude …", file=sys.stderr)
        script = generate_narration_script(events, context)
        (work_dir / "narration_script.txt").write_text(script)
        print(f"[demo_composer] Script:\n{script}\n", file=sys.stderr)

    if script:
        mp3_path = work_dir / "voiceover.mp3"
        ts_path = work_dir / "word_timestamps.json"
        print("[demo_composer] Generating TTS voiceover …", file=sys.stderr)
        result = generate_narration(script, mp3_path, ts_path, voice_id)
        narration_mp3 = mp3_path
        narration_words = result["words"]

    bgm_path = download_bgm(work_dir / "bgm.mp3")

    return compose_demo_video(
        recording=recording,
        events=events,
        output=output,
        narration_mp3=narration_mp3,
        narration_words=narration_words,
        bgm_path=bgm_path,
        upload_s3=upload_s3,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compose a polished demo video from a screen recording.")
    parser.add_argument("recording", help="Raw screen recording MP4")
    parser.add_argument("events_json", help="Events JSON file from screen_recorder.py")
    parser.add_argument("--output", default="output_videos/demo_composed.mp4")
    parser.add_argument("--script", help="Narration script text (skip Claude generation)")
    parser.add_argument("--no-script", action="store_true", help="Disable TTS entirely")
    parser.add_argument("--context", default="", help="Context for Claude script generation")
    parser.add_argument("--voice-id", help="ElevenLabs voice ID")
    parser.add_argument("--upload-s3", action="store_true")
    args = parser.parse_args()

    result = compose_from_recording(
        recording=Path(args.recording),
        events_json=Path(args.events_json),
        output=Path(args.output),
        script=args.script if not args.no_script else None,
        generate_script=(not args.no_script and args.script is None),
        context=args.context,
        voice_id=args.voice_id,
        upload_s3=args.upload_s3,
    )
    if "RESULT:" not in str(result):
        print("RESULT: " + json.dumps(result), flush=True)

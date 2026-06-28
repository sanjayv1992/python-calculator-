# Super Video Maker Skill

An end-to-end AI video production skill for agentic coding frameworks (Claude Code, Cursor, etc.).

Turns ideas, scripts, or screen recordings into polished videos using HeyGen avatars, Seedance b-roll, OpenAI image generation, Remotion, HyperFrames, FFmpeg, captions, and music.

## Quick start

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Playwright browsers
playwright install chromium

# 3. Install Node dependencies (for Remotion / HyperFrames)
npm install

# 4. Copy and fill in your API keys
cp .env.example .env

# 5. Install FFmpeg (system-level)
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

## Formats supported

- **Avatar Explainer** — HeyGen synthetic presenter + source proof + captions (90 s master)
- **Screen demo** — Playwright recording + laptop mockup + ElevenLabs narration
- **Faceless b-roll ad** — Seedance clips + voiceover + karaoke captions (9:16 / 16:9)
- **Captioned talking head** — Whisper captions burned via Remotion or FFmpeg
- **Motion graphics** — Remotion actor-based composition
- **HyperFrames HTML video** — HTML-native timeline → MP4
- **Vertical shorts** — Long video → multiple 9:16 clips with titles + captions

## Documentation

| File | Contents |
|------|----------|
| `SKILL.md` | Core operating instructions for agents |
| `REFERENCE.md` | Provider guidance, layout rules, quality checklist |
| `FFMPEG_PLAYBOOK.md` | Every FFmpeg recipe used in the pipeline |
| `WORKFLOW_EXAMPLES.md` | End-to-end recipes for each video format |
| `REMOTION_VIDEO_GUIDE.md` | Remotion actor-based composition guide |

## Tools

| Tool | Purpose |
|------|---------|
| `tools/heygen_client.py` | HeyGen avatar video generation + polling + download |
| `tools/replicate_video.py` | Seedance 2.0 b-roll via Replicate |
| `tools/image_provider.py` | OpenAI `gpt-image-2` image generation |
| `tools/video_captioner.py` | Whisper transcription → ASS karaoke captions → burn |
| `tools/screen_recorder.py` | Xvfb + FFmpeg screen capture with event logging |
| `tools/agent_browser_recorder.py` | Playwright + Xvfb browser proof recording |
| `tools/demo_video_composer.py` | Laptop mockup + click effects + narration + subtitles |
| `tools/local_explainer_broll.py` | Pillow-animated fallback b-roll (no API credits needed) |
| `tools/broll_layout_qc.py` | Layout contact sheet with safe-zone guides |
| `tools/ffmpeg_qc.py` | Technical QC (codec, duration, black frames) |
| `tools/music_provider.py` | Music backend adapter (ElevenLabs / local file) |

## Integration

Add to Cursor / Claude Code projects by placing this folder at `.agents/skills/super-video-maker/`. Include `SKILL.md` in the agent system prompt.

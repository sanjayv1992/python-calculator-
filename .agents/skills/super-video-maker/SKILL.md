# Super Video Maker Skill Overview

This is an end-to-end AI video production system for agentic frameworks. It orchestrates HeyGen avatars, Seedance b-roll generation, OpenAI image tools, Remotion/HyperFrames editing, FFmpeg compositing, and caption automation into a staged pipeline.

## Core Workflow

The skill follows five stages: **Intake** (gather requirements), **Script & shot list** (plan visuals with editorial jobs), **Asset generation** (render clips/images via providers), **Timeline assembly** (compose in Remotion/HyperFrames/FFmpeg), and **QC & export** (verify codec, duration, sync).

## Key Operating Principles

**Story-first design:** Every video defaults to "avatar-explainer" format—hook → disclosure → news beat → concrete example → source proof → action step → spoken CTA tail. The system avoids silent cards and plain slideshows.

**Disclosure requirements:** Synthetic presenters must be introduced via the avatar's own voice ("Quick note, this is the digital avatar of..."). If absent, a small rounded-pill badge appears during the opening 4 seconds. Every outro includes a permanent footer disclosure.

**Beat-locked visuals:** All b-roll, captions, and overlays sync to Whisper-transcribed word-level timestamps, never assumed timing.

**Layout discipline:** The system defines non-overlapping zones (top-left badge, top-right PiP, bottom-center captions, center b-roll) and forbids colliding overlays. Avatar PiP uses borderless 24px rounded corners with soft shadow.

**B-roll hierarchy:** Real screenshots > stock footage > generated stills, ordered by editorial honesty. Generated imagery must avoid "AI-slop" tells (floating objects, neon grids, symbolic abstractions) and default to documentary-realism framing.

## Provider Routing

- **Avatar:** HeyGen
- **Video b-roll:** Replicate Seedance 2.0
- **Images:** OpenAI (gpt-image-2, native 16:9 at 2048×1152)
- **Voice & music:** ElevenLabs
- **Timeline:** Remotion or HyperFrames
- **Final render:** FFmpeg + ffprobe

All results emit a JSON contract: `RESULT: {"status":"...","stage":"...","job_id":"..."}` for parsing downstream.

## Tool Reference

All tools live in `tools/` and are invoked directly:

```bash
python3 .agents/skills/super-video-maker/tools/heygen_client.py --script "..." --output out/avatar.mp4
python3 .agents/skills/super-video-maker/tools/replicate_video.py generate --prompt "..." --duration 7
python3 .agents/skills/super-video-maker/tools/image_provider.py generate --prompt "..." --size 2048x1152
python3 .agents/skills/super-video-maker/tools/video_captioner.py
python3 .agents/skills/super-video-maker/tools/screen_recorder.py
python3 .agents/skills/super-video-maker/tools/agent_browser_recorder.py
python3 .agents/skills/super-video-maker/tools/demo_video_composer.py
python3 .agents/skills/super-video-maker/tools/local_explainer_broll.py
python3 .agents/skills/super-video-maker/tools/broll_layout_qc.py clip1.mp4 clip2.png --job-dir tmp/video_jobs/foo
python3 .agents/skills/super-video-maker/tools/ffmpeg_qc.py output.mp4
python3 .agents/skills/super-video-maker/tools/music_provider.py local --path music.mp3
```

See `WORKFLOW_EXAMPLES.md` for complete end-to-end recipes and `FFMPEG_PLAYBOOK.md` for compositing commands.

## Job State Convention

Every job runs in `tmp/video_jobs/<job_id>/`. Create `job_state.json` at the start with canonical source URLs, beat map, and asset manifest. Update it after each stage.

## Cost Transparency

Before calling any paid provider (HeyGen, Replicate, ElevenLabs, OpenAI images), state the planned calls and ask for confirmation if the user has not pre-approved. Whisper transcription and local tools are free to call without asking.

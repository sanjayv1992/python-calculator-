# Workflow Examples

These examples show how an agent should combine the packaged tools. Adapt paths
inside a `tmp/video_jobs/<job_id>/` folder for real jobs.

## 1. Avatar over product screen recording

Use when the user wants a founder/tutorial presenter over a SaaS walkthrough.

Steps:

1. Write a short narration script.
2. Generate a HeyGen avatar clip on green screen.
3. Record the product workflow with event logging.
4. Compose avatar over the screen recording.
5. Add captions, music, and final QC.

Commands:

```bash
python3 .agents/skills/super-video-maker/tools/heygen_client.py
python3 .agents/skills/super-video-maker/tools/screen_recorder.py
python3 .agents/skills/super-video-maker/tools/demo_video_composer.py
python3 .agents/skills/super-video-maker/tools/ffmpeg_qc.py demo_videos/final_demo.mp4
```

Use `FFMPEG_PLAYBOOK.md` for chroma-key overlay if the avatar should appear
inside the demo composition rather than before/after it.

## 2. Faceless b-roll ad

Use when the user wants TikTok/Reels/Shorts style ads with generated clips,
voiceover, captions, and music.

Steps:

1. Create a 20-40 second hook-driven script.
2. Split script into 4-6 visual beats.
3. Generate one Seedance clip per beat.
4. Generate voiceover and music.
5. Concatenate clips, captions, and audio.
6. Export `9:16`, optionally `1:1` and `16:9`.

Seedance example:

```bash
python3 .agents/skills/super-video-maker/tools/replicate_video.py generate \
  --prompt "handheld UGC shot of a startup founder opening a laptop, fast-paced, natural light, realistic" \
  --duration 7 \
  --resolution 1080p \
  --aspect-ratio 9:16
```

## 3. Captioned talking head with b-roll

Use when the user already has a main talking-head MP4 and wants word captions
plus b-roll picture-in-picture windows.

Steps:

1. Put main video in `remotion-template/public/source/main.mp4`.
2. Put b-roll clips in `remotion-template/public/broll/`.
3. Build `public/render-props.json` from word timestamps and b-roll manifest.
4. Preview in Remotion Studio.
5. Render final MP4.

Commands:

```bash
cd .agents/skills/super-video-maker/remotion-template
npm install
npx remotion studio
npx remotion render src/index.ts CaptionedTalkingHead out/captioned.mp4 --props=public/render-props.json
```

## 4. HyperFrames HTML-native video

Use when the agent can define the whole video as HTML, especially for kinetic
text, simple product visuals, data visuals, and ad variants.

Steps:

1. Edit `hyperframes-template/compositions/demo.html`.
2. Preview in browser.
3. Render deterministic MP4.
4. Finish audio/captions with FFmpeg if needed.

Commands:

```bash
cd .agents/skills/super-video-maker/hyperframes-template
npm install
npx hyperframes preview compositions/demo.html
npx hyperframes render compositions/demo.html --output out/demo.mp4
```

## 5. Long video to vertical shorts

Use when the user has a podcast, tutorial, webinar, sales call, or YouTube
video and wants short social clips.

Steps:

1. Transcribe the full video once.
2. Pick segments and titles.
3. Render each vertical short with top title and karaoke captions.
4. QC each output.

Command:

```bash
python3 .agents/skills/super-video-maker/tools/video_captioner.py
```

The packaged script keeps simple hardcoded parameters near the bottom so the
user can edit the file and press run.

## 6. Generated thumbnail and video stills

Use OpenAI image generation/editing when the video needs a thumbnail, title
card, background plate, or storyboard image.

Suggested flow:

1. Generate three thumbnail concepts.
2. Pick the best one.
3. Edit for brand colors and exact title text.
4. Save as `thumbnail.png`.
5. Optionally extract a still from the final video and edit it.

The provider adapter should save images into the job folder and emit `RESULT:`
with `local_path`, `prompt`, `size`, and `provider`.

## 7. Final delivery package

For a complete job, return:

- `master_16x9.mp4` when relevant,
- `vertical_9x16.mp4` when relevant,
- `square_1x1.mp4` when relevant,
- caption file (`.srt` or `.ass`) if requested,
- thumbnail image,
- `job_state.json`,
- a short production summary.

Do not include temporary frames or provider caches in the final delivery list.

## 8. Story-driven SEO/news tutorial

Use when the user wants a news explainer that feels like a mini documentary,
not a slideshow.

Steps:

1. Write a story-first script:
   - hook,
   - transparent avatar disclosure,
   - news beat,
   - concrete example,
   - browser source proof,
   - action step.
2. Generate the HeyGen presenter with the matching avatar and matching voice.
3. Record coherent browser proof with `agent_browser_recorder.py`.
4. Generate 2-4 Seedance b-roll clips for the story/example beats.
5. If Seedance credits are unavailable, use `local_explainer_broll.py` as a temporary animated fallback.
6. Interweave browser proof and b-roll with FFmpeg or Remotion.
7. Add large punchy captions for key claims.

Commands:

```bash
python3 .agents/skills/super-video-maker/tools/agent_browser_recorder.py
python3 .agents/skills/super-video-maker/tools/replicate_video.py generate --prompt "original educational explainer metaphor..." --duration 7 --resolution 1080p --aspect-ratio 16:9
python3 .agents/skills/super-video-maker/tools/local_explainer_broll.py
```

Example transparency line after the hook:

```text
Quick note: this is <name>'s digital avatar walking you through the update.
```

## 9. Story-driven master with Whisper-locked beats and a unified b-roll set

This is the highest-coherence workflow used for the SEO news master video.

Pipeline:

1. Write a story-first script: hook -> casual avatar disclosure (in the avatar's own voice) -> news beat -> concrete example -> source proof -> action step. Do NOT plan a static disclaimer slide before the hook.
2. Render the HeyGen avatar with the matching avatar+voice IDs.
3. Extract the avatar audio with FFmpeg and Whisper-transcribe with word + segment timestamps.
4. Inspect Whisper segments and trim the avatar to the first unique pass if HeyGen duplicated the script.
5. Build a `storyboard.json` whose beats start and end on Whisper sentence boundaries. Map each beat to a layout (avatar fullscreen / b-roll PiP / browser PiP), a b-roll asset, a chapter title, and a lower-third source attribution.
6. Build a source deck and route every visual by editorial job (proof / mechanism / consequence / action / transition). Real screenshots, UI micro-stories, typographic cards, and real screen recordings come before generated b-roll. If generation is unavoidable, use `gpt-image-2` at `quality=high`, native 16:9 (`2048x1152`), documentary-realism prompts, and short 2-4s cuts.
7. For any beat that is longer than the natural b-roll clip, never loop. Choose one of: a complementary b-roll for the second half, `tpad=stop_mode=clone:stop_duration=N` to hold the final frame for ≤2 seconds, or a Ken Burns still as the continuation.
8. Record the agent-operated browser segments for the proof beats (`tools/agent_browser_recorder.py`) and slice them per beat.
9. Render an outro recap card (1920x1080) with the action steps and the digital-avatar disclosure. Skip the static title card.
10. Build a Hormozi-style ASS karaoke caption file from the Whisper words. Master offset is 0 (master timeline matches avatar timeline since there is no title pre-roll). Default captions are bottom-centered, so the avatar PiP belongs in the top-right.
11. Compose with FFmpeg in clean steps:
    - encode each timeline segment to 1920x1080 30fps yuv420p silent MP4,
    - concat into a single background track,
    - overlay the avatar PiP top-right as a borderless rounded card with soft drop shadow,
    - if the avatar's own audio does not include the disclosure, overlay a small top-left PNG badge during the first ~4.5 seconds,
    - burn the karaoke captions,
    - mux master audio (avatar audio + outro silence) with `loudnorm=I=-16:TP=-1.5:LRA=11`.
12. Sanity-check the timeline by sampling JPEG frames at every beat and reading them visually to verify the visual matches the audio at that moment.

## 10. Avatar Explainer (`avatar-explainer`) → 90-second master with editorial source deck + spoken CTA tail (CURRENT BEST PRACTICE)

Use this when the user wants a short trending-news master video with a natural
ending, clean professional overlays, and high-taste visual logic.

Pipeline:

1. **Pick the trend.** If X.com is gated, triangulate via Trends24 + WebSearch
   and confirm with at least two source pages (e.g. official blog post +
   Techmeme aggregation). Save canonical URLs in `job_state.json`.
2. **Build the source deck before writing the storyboard.** Each source asset
   needs a unique editorial job:
   - official announcement hero = proof / establishing receipt,
   - exact paragraph crop = proof of the technical claim,
   - feature section crop = mechanism,
   - byline/date crop = credibility receipt,
   - aggregator or outlet list = consequence / momentum,
   - UI/action surface = action step.
   Never plan "same website again, slightly different zoom" unless the second
   shot proves a different phrase or mechanism.
3. **Write the script with the mandatory CTA tail.** Hook → casual avatar
   disclosure → news beat → concrete story/example → source proof → 3-move
   action close → 6-8s spoken CTA tail ("If this kind of teardown is useful,
   hit follow over at <domain> for more <topic>. See you in the next one.").
   Keep the body around 75-85s and the master around 90-100s with the CTA.
4. **Render HeyGen** with the matching avatar+voice IDs from the user's
   `.env` (e.g. `HEYGEN_AVATAR_ID=<your_avatar_id>` paired with
   `HEYGEN_VOICE_ID=<your_voice_id>`).
5. **Extract audio + Whisper-transcribe** with word + segment timestamps. Note
   where the action close ends and where the CTA tail starts — the gap is
   where the outro card replaces the b-roll.
6. **Build a `storyboard.json`** with beats locked to Whisper sentence
   boundaries. For every shot include: narration, visual job (proof /
   mechanism / consequence / action / transition), surface, before state,
   cursor/action/motion, after state, source-deck asset, and reject list.
   Plan layout zones up front: hook fullscreen, body beats with PiP top-right
   + b-roll/browser-proof center, outro card during CTA tail.
7. **Pick visuals by beat purpose, not by prompt creativity.** For each
   non-hook beat, route through the table in `REFERENCE.md` ("B-roll design
   system") and the "Editorial taste system". Real visuals and UI micro-stories
   beat generated visuals every single time.
8. **Design story/example beats as micro-stories.** Example: for "Picture this,
   you're a founder who lives in Google Docs," do not show a founder at a
   laptop. Show a Google Docs-style launch plan with comments, TODOs, dates,
   thumbnails, a pasted chart, and cursor-driven action cards.
9. **Generate proof Ken Burns clips from real screenshots** at exact beat
   durations, but split any long screenshot beat into different roles/crops:
   establishing receipt, exact phrase crop, feature crop, and headline cluster.
10. **Record agent-operated browser proof when it adds evidence.** The recording
    should look like investigation: headline highlight, find-on-page, jump to
    feature, exact paragraph callout, tab switch to aggregator, outlet cluster
    zoom. Do not include slow filler scrolling.
11. **Run b-roll layout QC before composition.**

    ```bash
    python3 .agents/skills/super-video-maker/tools/broll_layout_qc.py \
      tmp/video_jobs/<job_id>/assets/v5_clips/*.mp4 \
      --job-dir tmp/video_jobs/<job_id>
    ```

    Mark every asset `pass`, `crop-edit`, `layout-edit`, `re-render`, or
    `replace`. Fix spacing problems before final composition.
12. **Render the disclosure badge once** with Pillow → `assets/disclosure_badge.png`.
13. **Render the outro recap card** (1920x1080) with the action steps and a
    permanent disclosure footer in the bottom-center.
14. **Build centered karaoke captions** from the Whisper words.
15. **Compose with FFmpeg** in one pass and **QC** by sampling JPEG frames at every beat.

Twelve lessons this workflow is built around (learned the hard way on v1 through v4):

- **Never overlap captions and lower-third.** Move the disclosure to a top-left PNG badge that fades before the PiP appears.
- **Captions must be centered.** Left-aligned looks amateur and forces asymmetric layouts.
- **Never end on silence.** The outro card needs spoken audio under it or the video feels broken.
- **PiP must be borderless with rounded corners and a soft drop shadow.**
- **Real visuals beat generated visuals.** AI-slop b-roll destroys credibility.
- **Use `gpt-image-2` at `quality=high`, not `gpt-image-1`.**
- **Generate at native 16:9 (`2048x1152`).** Padding on documentary photos screams "generated".
- **Cut every 2-4 s on AI stills, every 3-6 s on real screenshots.**
- **Every visual needs one editorial job.**
- **Screenshots are receipts, not wallpaper.**
- **Screen recordings must investigate.**
- **Story beats need working surfaces.**
- **B-roll needs its own layout QC/edit pass.**

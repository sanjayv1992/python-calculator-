"""Premium content-generation prompt specs for the AgroManch AI Content Factory.

Every spec turns verified agricultural context into a channel-ready asset via
Gemini, at professional agri-marketing quality. The shared system instruction
injects the permanent Brand Style Guide, the per-language writing directive, and
the target region; the shared user template injects the seasonal context, the
package's marketing angle, and the verified knowledge context.

Image/video specs output *generator-ready prompts* (subject, scene, style, aspect
ratio, negative prompts) for downstream Imagen/Veo — not the media itself.
"""

from __future__ import annotations

from agromanch_ai.prompts.spec import PromptSpec

# Shared system instruction: brand voice + language + region + grounding/safety.
_SYS = (
    "{brand_guide}\n\n"
    "LANGUAGE: Write in {language_name}. {language_directive}\n"
    "TARGET REGION: {target_region} — use its crops, seasons, mandis and realities.\n"
    "GROUNDING: Use ONLY the verified context provided. Never invent agronomic "
    "facts, doses, or scheme details; if the context does not cover something, say "
    "so plainly. For any agrochemical, defer to the registered label and the local "
    "KVK, and state a dose only if it appears in the verified context.\n"
    "OUTPUT: Final and publishable — no placeholders, no notes to the editor."
)

# Shared user template: knowledge + season + angle + the specific task.
_USER = (
    "{context_block}\n\n"
    "{seasonal_context}\n\n"
    "{content_angle}\n\n"
    "TOPIC: {topic}\n\n"
    "TASK: "
)


def _content(instruction: str, temperature: float = 0.7) -> PromptSpec:
    return PromptSpec(_SYS, _USER + instruction, temperature)


CONTENT_SPECS: dict[str, PromptSpec] = {
    "research_summary": _content(
        "Write a tight research brief of what the verified context establishes: "
        "6-8 bullet points of the key, accurate facts the content team needs "
        "(numbers, timings, thresholds), then one line flagging any important gap "
        "in the sources. Factual and citation-faithful — this seeds the package.",
        temperature=0.3,
    ),
    "instagram_carousel": _content(
        "Create a scroll-stopping Instagram carousel of 8 slides following the "
        "AgroManch structure Problem -> Cause -> Solution -> CTA:\n"
        "- SLIDE 1: a viral hook (max 8 words) that stops the scroll.\n"
        "- SLIDE 2: name the farmer's PROBLEM/pain vividly.\n"
        "- SLIDE 3: the real CAUSE (grounded in the context).\n"
        "- SLIDES 4-6: the SOLUTION, one clear idea per slide, concrete steps.\n"
        "- SLIDE 7: proof/result the farmer can expect (from the context).\n"
        "- SLIDE 8: a strong CTA to save, share and follow AgroManch.\n"
        "Each slide: a bold one-line headline + 2-3 short mobile-friendly lines. "
        "Then write a ready-to-post CAPTION (human, warm, first line hooks) and "
        "15-20 hashtags mixing niche + broad + local (region/crop) tags."
    ),
    "carousel_image_prompts": _content(
        "Write one image-generation prompt per carousel slide (8 total), optimized "
        "for Gemini image generation. For each: 'SLIDE n:' a detailed prompt — a "
        "realistic local farmer/scene from {target_region} agriculture (NOT generic "
        "stock-photo look), subject, composition, natural lighting, lens/mood, "
        "colour palette, 4:5 aspect ratio, and a short 'Negative:' line. Leave "
        "clean space for an overlay headline; keep any in-image text minimal.",
        temperature=0.85,
    ),
    "facebook_post": _content(
        "Write an engagement-first Facebook post (130-200 words): open with a "
        "question or bold local observation, tell a mini story a farmer relates to, "
        "give 3-4 practical tips as short emoji bullets, and close with a "
        "comment-bait question. Add 5-8 hashtags. Optimise for comments and shares."
    ),
    "whatsapp_broadcast": _content(
        "Write a forwardable WhatsApp broadcast (under 130 words) for farmer "
        "groups: warm greeting, one-line context, 3 numbered action points, and a "
        "short 'Team AgroManch' sign-off with a 1-tap CTA. Use *asterisks* for bold "
        "ONLY on the few most important keywords, at most 4 emoji, and short lines "
        "that read well on a small phone. It should be easy and tempting to forward."
    ),
    "youtube_shorts_script": _content(
        "Write a 45-60s YouTube Shorts script that tells a small story and builds "
        "curiosity: HOOK in the first 3 seconds (a pattern-interrupt line that "
        "creates an open loop), then retention beats every ~10s with the exact "
        "spoken line + a bracketed b-roll suggestion, a simple clear explanation, "
        "and a strong close = subscribe + AgroManch CTA. Energetic, farmer-friendly."
    ),
    "veo_video_prompt": _content(
        "Write a cinematic Veo text-to-video prompt for a vertical 9:16 clip "
        "optimized for a ~30-second reel, showing realistic farming action for this "
        "topic in {target_region}. Include: scene & subject (real local farmer), a "
        "specific camera movement, lens, lighting & time of day, mood/pacing, "
        "ambient detail, and a 'Negative:' line. Concrete and shootable; no "
        "on-screen text.",
        temperature=0.85,
    ),
    "voiceover_script": _content(
        "Write a natural voiceover narration (about 55-70 seconds read aloud) in "
        "the voice of an experienced, trusted agriculture expert: warm, clear, "
        "easy to understand, with natural pauses (use short line breaks to mark "
        "breaths). Plain spoken sentences only — no stage directions, timestamps, "
        "or speaker labels."
    ),
    "subtitle_srt": PromptSpec(
        system_instruction=_SYS
        + "\nYou output ONLY a valid SubRip (.srt) subtitle file and nothing else.",
        user_template=_USER
        + "Produce an SRT subtitle file for a ~60-second vertical video narration "
        "about this topic, grounded in the verified context. Sequential numbering, "
        "'HH:MM:SS,mmm --> HH:MM:SS,mmm' timecodes from 00:00:00,000, 1-2 short "
        "lines per cue (max ~7 words/line), covering ~60 seconds. Output only the "
        "SRT — no code fences, no commentary.",
        temperature=0.3,
    ),
    "seo_keywords": _content(
        "List SEO keywords (in Hindi/Hinglish for searchability, even if the rest "
        "of the package is Bhojpuri) under three headings: 'Primary' (10 keywords), "
        "'Long-tail' (10 phrases farmers actually search, incl. 'in Bihar/UP' and "
        "Hinglish variants), 'Questions' (5 question-style queries). One per line.",
        temperature=0.5,
    ),
    "blog": _content(
        "Write a highly readable 600-800 word blog (in Hindi/Hinglish even if the "
        "package language is Bhojpuri, for searchability): SEO title (<60 chars) on "
        "line 1, meta description (<155 chars) on line 2, then an engaging intro, "
        "short scannable paragraphs, clear H2 subheads, bulleted lists, **bolded** "
        "key takeaways, one practical checklist, a 3-Q&A FAQ, and a conclusion "
        "pointing to the AgroManch app for personalised advice."
    ),
    "podcast_script": _content(
        "Write a 3-4 minute podcast script as a warm dialogue between host RAVI and "
        "expert DR. MEERA: a cold-open question, 3 key learnings each with a real "
        "field example from {target_region}, and a recap outro. Speaker names in caps."
    ),
    "thumbnail_prompt": _content(
        "Write a high-CTR 16:9 YouTube thumbnail package: (1) the 3-4 word overlay "
        "text that sells the click (state it on its own line), (2) an image-"
        "generation prompt — real local farmer with clear expression/emotion, bold "
        "focal subject, {target_region} farm setting, high-contrast colours, space "
        "for the overlay, plus a 'Negative:' line. Optimized for Gemini image gen.",
        temperature=0.85,
    ),
    "story_prompt": _content(
        "Write a 3-frame Instagram/WhatsApp Story sequence (9:16) as image prompts "
        "with a problem -> solution -> CTA arc. For each: 'FRAME n:' a detailed "
        "Gemini image prompt (real local farmer, {target_region} setting, no stock "
        "look), a one-line caption/sticker suggestion, and a 'Negative:' line.",
        temperature=0.85,
    ),
    "image_prompt": _content(
        "Write one strong general-purpose 1:1 image-generation prompt optimized for "
        "Gemini: a realistic {target_region} farmer/scene for this topic (never "
        "generic stock), subject, composition, natural lighting, style, palette, and "
        "a 'Negative:' line.",
        temperature=0.85,
    ),
    "reel_video_prompts": _content(
        "Plan a 20-30s Instagram Reel (9:16) as a shot list of 5-6 shots with a "
        "3-second hook shot and a problem -> solution -> CTA arc. For each: 'SHOT "
        "n:' the visual as a video-generation prompt (real local farming action), "
        "duration in seconds, the on-screen text overlay, and a b-roll note. End "
        "with a suggested trending-audio style.",
        temperature=0.85,
    ),
    "hook": _content(
        "Write 7 scroll-stopping one-line hooks (max 10 words each), ranked "
        "strongest first, using proven formulas: curiosity gap, a number, "
        "loss-aversion, 'stop doing X', and local proof. In-language, punchy.",
        temperature=0.9,
    ),
    "cta": _content(
        "Write 5 psychology-driven, low-friction CTAs driving farmers to the "
        "AgroManch app/WhatsApp for personalised advice — one each for Instagram, "
        "Facebook, WhatsApp, YouTube, and a blog. Benefit-led, one line each, "
        "labelled by channel.",
        temperature=0.8,
    ),
}

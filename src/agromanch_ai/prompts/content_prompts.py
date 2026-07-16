"""Content-generation prompt specs for the AgroManch AI Content Factory.

Every spec turns verified agricultural context into a channel-ready asset via
Gemini. Shared rules baked into the system instructions:

- Audience: Indian smallholder farmers — simple, practical, respectful wording.
- Grounding: use ONLY the verified context; never invent agronomic facts; if the
  context is thin, say so rather than guessing.
- Safety: for any agrochemical mention, defer to the registered label and the
  local KVK; never state doses not present in the context.
- Language: write in {language_name}.

Image/video specs output *generator-ready prompts* (subject, scene, style,
aspect ratio, negative prompts) for downstream Imagen/Veo — not images.
"""

from __future__ import annotations

from agromanch_ai.prompts.spec import PromptSpec

# Common system preamble shared by every content spec.
_SYS = (
    "You are the senior content lead at AgroManch, creating high-quality "
    "agricultural content for Indian smallholder farmers. Write in "
    "{language_name}, in clear, simple, practical words. Use ONLY the verified "
    "context provided; do not invent agronomic facts, doses, or scheme details. "
    "If the context does not cover something, say so plainly. For any "
    "agrochemical, defer to the registered label and the local KVK. "
)

_USER = "{context_block}\n\nTOPIC: {topic}\n\nTASK: "


def _content(instruction: str, temperature: float = 0.7) -> PromptSpec:
    return PromptSpec(_SYS, _USER + instruction, temperature)


CONTENT_SPECS: dict[str, PromptSpec] = {
    "research_summary": _content(
        "Write a tight research summary of what the verified context establishes "
        "about this topic: 5-8 bullet points of the key, accurate facts a content "
        "team needs, then a one-line note on any important gap in the sources. "
        "This summary seeds the rest of the content, so keep it factual and "
        "citation-faithful.",
        temperature=0.3,
    ),
    "instagram_carousel": _content(
        "Create an Instagram carousel of 7 slides. For each: 'SLIDE n' — a bold "
        "hook line (max 8 words) then 2-3 short supporting lines. Slide 1 is the "
        "scroll-stopping hook; slide 7 is a clear call to action to follow "
        "AgroManch. End with 10 relevant hashtags (mix English + Hinglish)."
    ),
    "carousel_image_prompts": _content(
        "Write one image-generation prompt per carousel slide (7 total). For each: "
        "'SLIDE n:' then a detailed prompt — subject, setting (Indian farm "
        "context), composition, lighting, style (clean, vibrant, photoreal or "
        "flat-illustration), 4:5 aspect ratio, and a short 'Negative:' line. Keep "
        "text-in-image minimal and specify space for an overlay headline.",
        temperature=0.8,
    ),
    "facebook_post": _content(
        "Write a Facebook post of 120-180 words: a strong first line, 3-4 practical "
        "tips as short emoji bullets, and a closing question that invites farmer "
        "comments. Add 5 hashtags."
    ),
    "whatsapp_broadcast": _content(
        "Write a WhatsApp broadcast under 120 words for farmer groups: greeting, "
        "one-line context, 3 numbered action points, and a short 'Team AgroManch' "
        "sign-off. Use *asterisks* for bold keywords and at most 4 emoji; it must "
        "read well on a small phone screen."
    ),
    "youtube_shorts_script": _content(
        "Write a 45-60 second YouTube Shorts script: a HOOK in the first 3 seconds "
        "(one line), then timestamped beats every ~10 seconds with the exact spoken "
        "line and a bracketed b-roll suggestion, ending with a CTA to subscribe to "
        "AgroManch. Keep it energetic and farmer-friendly."
    ),
    "veo_video_prompt": _content(
        "Write a Veo text-to-video prompt for a 8-second vertical (9:16) clip that "
        "visualizes this topic on an Indian farm. Include: scene and subject, "
        "camera movement, lighting and time of day, mood, and a 'Negative:' line. "
        "Make it concrete and shootable; no on-screen text.",
        temperature=0.8,
    ),
    "voiceover_script": _content(
        "Write a natural voiceover narration script (about 55-70 seconds when read "
        "aloud) that matches the Shorts/Reel. Plain spoken sentences only — no "
        "stage directions, timestamps, or speaker labels. Warm, encouraging tone "
        "for a farmer audience."
    ),
    "subtitle_srt": PromptSpec(
        system_instruction=_SYS
        + "You output ONLY a valid SubRip (.srt) subtitle file and nothing else.",
        user_template=_USER
        + "Produce an SRT subtitle file for a ~60-second vertical video narration "
        "about this topic, grounded in the verified context. Use sequential "
        "numbering, 'HH:MM:SS,mmm --> HH:MM:SS,mmm' timecodes starting at "
        "00:00:00,000, and 1-2 short lines per cue (max ~7 words per line). Cover "
        "roughly 60 seconds. Output only the SRT, no code fences or commentary.",
        temperature=0.3,
    ),
    "seo_keywords": _content(
        "List SEO keywords for AgroManch web/video content under three headings: "
        "'Primary' (10 keywords), 'Long-tail' (10 phrases farmers actually search, "
        "include Hinglish variants), and 'Questions' (5 question-style queries). "
        "One per line.",
        temperature=0.5,
    ),
    "blog": _content(
        "Write a 600-800 word blog post: SEO title (<60 chars) on the first line, a "
        "meta description (<155 chars) on the second, then an engaging intro, clear "
        "H2 sections, one practical checklist, a short FAQ (3 Q&A), and a "
        "conclusion pointing readers to the AgroManch app for personalised advice."
    ),
    "podcast_script": _content(
        "Write a 3-4 minute podcast script as a friendly dialogue between host RAVI "
        "and expert DR. MEERA: a cold-open question, 3 key learnings each with a "
        "real field example, and a recap outro. Mark speaker names in caps."
    ),
    "thumbnail_prompt": _content(
        "Write a single image-generation prompt for a high-CTR 16:9 YouTube "
        "thumbnail: subject and expression, bold focal point, Indian farm setting, "
        "high-contrast colours, and space for a 3-4 word overlay (state the "
        "suggested overlay text separately). Add a 'Negative:' line.",
        temperature=0.8,
    ),
    "story_prompt": _content(
        "Write image-generation prompts for a 3-frame Instagram/WhatsApp Story "
        "sequence (9:16). For each frame: 'FRAME n:' a detailed visual prompt plus "
        "a one-line caption/sticker suggestion. Build a mini narrative: problem → "
        "solution → CTA. Add a 'Negative:' line for each.",
        temperature=0.8,
    ),
    "image_prompt": _content(
        "Write one strong, detailed general-purpose image-generation prompt (1:1) "
        "representing this topic for social posts: subject, Indian farm setting, "
        "composition, lighting, style, and a 'Negative:' line.",
        temperature=0.8,
    ),
    "reel_video_prompts": _content(
        "Write a shot list for a 20-30 second Instagram Reel (9:16): 4-6 shots. For "
        "each: 'SHOT n:' the visual (as a video-generation prompt), duration in "
        "seconds, and the on-screen text overlay. Keep a punchy problem→solution→CTA "
        "arc.",
        temperature=0.8,
    ),
    "hook": _content(
        "Write 5 scroll-stopping one-line hooks (max 10 words each) for this topic, "
        "ordered strongest first. Mix curiosity, benefit, and question styles.",
        temperature=0.9,
    ),
    "cta": _content(
        "Write 4 short calls-to-action driving farmers to the AgroManch app/WhatsApp "
        "for personalised advice — one each for Instagram, WhatsApp, YouTube, and a "
        "blog. One line each, labelled by channel.",
        temperature=0.8,
    ),
}

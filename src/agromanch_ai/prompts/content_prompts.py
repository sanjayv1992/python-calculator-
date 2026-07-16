"""Content-automation prompt templates for AgroManch channels.

Each template turns knowledge-base material on {topic} into a channel-ready
draft. All templates demand: grounding in notebook sources, {language_name}
output, and farmer-friendly wording. Citation references returned by
NotebookLM are attached separately by
:class:`~agromanch_ai.services.content_service.ContentService`.
"""

from __future__ import annotations

_BASE = (
    "You are the AgroManch content team. Use ONLY the documents in this "
    "notebook about {topic}. Write in {language_name}, in simple words an "
    "Indian farmer understands. "
)

CONTENT_PROMPTS: dict[str, str] = {
    "instagram_carousel": (
        _BASE
        + "Create an Instagram carousel of 7 slides.\n"
        "For each slide give: SLIDE n — a bold hook line (max 8 words), then "
        "2–3 short supporting lines. Slide 1 is the hook, slide 7 is a call "
        "to action to follow AgroManch. Add 10 relevant hashtags at the end."
    ),
    "facebook_post": (
        _BASE
        + "Write a Facebook post of 120–180 words: an attention-grabbing first "
        "line, 3–4 practical tips as short bullet lines with emoji, and a "
        "closing question that invites farmer comments. Add 5 hashtags."
    ),
    "whatsapp_broadcast": (
        _BASE
        + "Write a WhatsApp broadcast message under 120 words for farmer "
        "groups: greeting, 1-line context, 3 numbered action points, and a "
        "short sign-off from Team AgroManch. Use asterisks for *bold* "
        "keywords and at most 4 emoji. It must read well on a small phone "
        "screen."
    ),
    "youtube_shorts_script": (
        _BASE
        + "Write a 45–60 second YouTube Shorts script: HOOK (first 3 seconds, "
        "one line), then timestamped beats every ~10 seconds with the exact "
        "spoken line and a b-roll suggestion in brackets, ending with a CTA "
        "to subscribe to AgroManch."
    ),
    "youtube_description": (
        _BASE
        + "Write a YouTube video description: 2-sentence summary, 4–6 bullet "
        "chapter lines with timestamps as placeholders (00:00), and a final "
        "line linking viewers to the AgroManch app. Keep it under 150 words."
    ),
    "seo_keywords": (
        _BASE
        + "List SEO keywords for AgroManch web content: 10 primary keywords, "
        "10 long-tail phrases farmers actually search (include Hinglish "
        "variants), and 5 question-style queries. One per line, grouped under "
        "those three headings."
    ),
    "blog_outline": (
        _BASE
        + "Create a blog outline: SEO title (under 60 characters), meta "
        "description (under 155 characters), and H2/H3 section headings with "
        "one line on what each section covers. Include an FAQ section with 4 "
        "questions."
    ),
    "blog_draft": (
        _BASE
        + "Write a 600–800 word blog post with an engaging introduction, "
        "clear H2 sections, one practical checklist, and a conclusion that "
        "points readers to the AgroManch app for personalised advice."
    ),
    "podcast_script": (
        _BASE
        + "Write a 3–4 minute podcast script as a friendly dialogue between "
        "host RAVI and expert DR. MEERA: cold-open question, 3 key learnings "
        "with a real field example each, and a recap outro. Mark speaker "
        "names in caps."
    ),
    "faq": (
        _BASE
        + "Write 8 frequently asked questions with concise answers (2–4 "
        "sentences each), ordered from beginner to advanced. Format as "
        "'Q:' / 'A:' pairs."
    ),
    "farmer_education_notes": (
        _BASE
        + "Write one-page training notes for a village farmer meeting: 5 key "
        "points with a one-line explanation each, a do/don't table in "
        "markdown, and 3 discussion questions for the group."
    ),
}

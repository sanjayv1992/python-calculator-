# RUN PRODUCTION — Generating Real Content (After "Factory Ready")

Prerequisite: `python scripts/check_environment.py` ends with **Factory Ready**
(see `FIRST_RUN.md`). Every command below uses the **real Gemini API** grounded
in **NotebookLM-verified context** — grounding stays ON.

## 1. One full content package (the main workflow)

```bash
python examples/agromanch/content_factory.py --topic "धान में बैक्टीरियल लीफ ब्लाइट प्रबंधन"
```

What happens: NotebookLM retrieves verified context once → Gemini generates the
full 18-asset bundle (research summary, carousel + image prompts, Facebook,
WhatsApp, Shorts script, Veo prompt, voiceover, SRT, SEO, blog, podcast script,
thumbnail/story prompts, CTA, hooks, reel shot list) → multi-agent review scores
the hero asset and rewrites toward 95+ (`AGROMANCH_REVIEW=true`) → everything is
published to:

```
output/<topic>/
  assets/                    one .md per asset
  instagram/ facebook/ youtube_shorts/ whatsapp/ telegram/   per-platform post.md
  manifest.json              machine-readable handoff
  quality_report.txt         internal quality/confidence report
  review_report.txt          internal multi-agent review scores
  learning_snapshot.json     why this hook/angle/CTA was chosen
```

If a topic has no verified context, generation is **refused** (GroundingError) —
add sources to `knowledge/` and re-run `python scripts/index_knowledge.py`.

## 2. Single assets / advisory

```bash
python examples/agromanch/instagram_carousel_generator.py --topic "ड्रिप सिंचाई के फायदे"
python examples/agromanch/whatsapp_post_generator.py --topic "सुरक्षित कीटनाशक छिड़काव"   # hi + bho
python examples/agromanch/crop_doctor_assistant.py --crop rice --region "Bihar" --symptoms "पत्तियों पर पीली धारियां"
python examples/agromanch/farmer_chatbot.py        # interactive grounded Q&A
```

## 3. Language / persona / region (per run)

```bash
AGROMANCH_LANGUAGE=bho python examples/agromanch/content_factory.py --topic "..."
AGROMANCH_PERSONA=dairy_farmer python examples/agromanch/content_factory.py --topic "..."
```

(Defaults in `.env`: Hindi, small_farmer, Purvanchal/Bihar.)

## 4. Batch production (planner-driven)

```bash
python scripts/plan_content.py --days 7          # builds plan + queue + reports (offline)
# then run the factory for the top queue topics, e.g.:
python examples/agromanch/content_factory.py --topic "<topic from data/publishing_queue.json>"
```

## 5. Full production audit (30+ topics, scored)

```bash
python scripts/audit_content.py                  # REAL run now that credentials work
```

Writes `audit_out/AUDIT_REPORT.md` with top/weakest outputs and detected
problems. Review the weakest by hand before publishing at scale.

## 6. Close the learning loop (after publishing)

```bash
python scripts/record_performance.py --topic "..." --platform instagram \
  --hook-style number --reach 5000 --shares 120 --engagement-rate 0.06
```

Future generations automatically prefer the styles that performed best.

## Cost & safety notes

- One full bundle ≈ 18 Gemini calls (+ review calls). On free tier this can hit
  per-minute limits — the engine retries with backoff; enable billing for volume.
- **Human gate before publishing:** verify agrochemical doses, scheme claims and
  safety lines against the cited sources. Grounded ≠ publish-blind.

# TEST PRODUCTION — Verifying Every Layer (Real Credentials)

Run these **in order** on your local machine after `FIRST_RUN.md`. Each step has
a clear expected result; if a step fails, stop and check the matching
troubleshooting row (§7).

## 1. Gemini connection

```bash
python scripts/check_environment.py
```

Expected first lines:
```
[PASS] GEMINI_API_KEY exists — key: XXXX…XX
[PASS] Gemini request succeeds — model: <your model>
```

## 2. NotebookLM connection

Same command; expected:
```
[PASS] NotebookLM authentication works — N notebook(s) visible
[PASS] Notebook exists — ...
```
Standalone re-check anytime: `notebooklm auth check --test`

## 3. Grounded retrieval

Same command; expected:
```
[PASS] Retrieval succeeds — topic: 'Fall Armyworm in maize'
[PASS] Grounded context returned — N citation(s)
...
Factory Ready
```
Try another topic: `python scripts/check_environment.py --topic "गेहूं में पीला रतुआ"`

## 4. Content generation (one real bundle)

```bash
python examples/agromanch/content_factory.py --topic "Fall Armyworm control in maize"
```

Verify:
- Console shows `Produced 18 assets ... Grounded in N verified source(s)`
- `output/Fall_Armyworm_control_in_maize/assets/` has 18 `.md` files with real
  Hindi content (no placeholders, no "GENERATED" text)
- `manifest.json` has `"grounded": true` and a non-empty `sources` list

## 5. Review system

```bash
cat output/Fall_Armyworm_control_in_maize/review_report.txt
```

Verify: an `Overall Score: NN/100`, 8 category scores (Scientific Accuracy,
Marketing Impact, Farmer Readability, SEO, Emotional Hook, Virality, CTA,
Language Quality), rewrite attempts count, and a Recommendation line.
(If missing, confirm `AGROMANCH_REVIEW=true` in `.env`.)

## 6. Publishing bundle

```bash
ls output/Fall_Armyworm_control_in_maize/
cat output/Fall_Armyworm_control_in_maize/instagram/post.md | head -30
```

Verify: `instagram/ facebook/ youtube_shorts/ whatsapp/ telegram/` folders each
contain a `post.md`; internal reports (`quality_report.txt`,
`review_report.txt`) are at the **root only**, never inside platform folders.

## 7. Troubleshooting

| Failure | Meaning | Fix |
| --- | --- | --- |
| **Invalid API key** — `[FAIL] Gemini request` HTTP 401/403 | Key revoked/mistyped | New key at aistudio.google.com/apikey → update `.env` |
| **Quota exceeded** — HTTP 429 after retries | Free-tier per-minute/day cap | Wait 1–2 min; retry; enable billing for volume |
| **Notebook login expired** — `[FAIL] NotebookLM authentication` | Google rejected stored cookies | `notebooklm login` again; servers: `notebooklm auth refresh` |
| **Notebook ID not found** — `[FAIL] Notebook exists` | Stale/foreign `NOTEBOOK_ID` | Re-run `python scripts/index_knowledge.py`; paste printed ID into `.env` |
| **Model unavailable** — HTTP 404 | Model retired / not on this key | Engine auto-falls back (pro → 2.5-flash → flash-latest); or set `GEMINI_MODEL=gemini-flash-latest` |
| **Network timeout** — repeated retries then failure | Slow network / proxy | Raise `GEMINI_TIMEOUT` in `.env`; check connection |
| `GroundingError` on generation | No verified context for the topic | Add documents to `knowledge/<domain>/`; re-run indexer. **Do not** disable grounding |
| Empty/short model reply | Output-token cap on a thinking model | Don't set small `max_output_tokens` |

All green through §6 = the factory is verified end to end on real credentials.

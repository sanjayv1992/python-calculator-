# FIRST RUN — From Zero to "Factory Ready" (Local Machine)

Complete this **on your own computer** (a real browser is required for NotebookLM
login — it cannot be done in a cloud container).

## 1. Prerequisites

- Python **3.10+** (`python3 --version`)
- Git
- A Google account (for NotebookLM)
- A Gemini API key — free from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Chrome/Chromium (the `[browser]` extra installs Playwright's browser for login)

## 2. Installation

```bash
git clone https://github.com/sanjayv1992/python-calculator-.git
cd python-calculator-
git checkout claude/notebooklm-py-voth1d

python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev,browser]"
```

## 3. Guided setup (recommended — does steps 4–7 for you)

```bash
python scripts/setup.py
```

It walks you through: Gemini key (hidden input) → real key verification →
NotebookLM browser login → notebook selection → saving `.env` (key +
`AGROMANCH_NOTEBOOK_ID`, mode 600) → full validation ending in **Factory Ready**.
If you use it, skip to §8. The manual steps below do the same thing.

## 4. Gemini API setup (manual)

```bash
cp .env.example .env
```

Edit `.env` and set:

```
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-flash-latest
```

> Model note (learned from live testing): free-tier keys usually have **no
> quota for `gemini-2.5-pro`** (HTTP 429) and `gemini-2.5-flash` is **retired
> for new accounts** (HTTP 404). `gemini-flash-latest` works and the engine
> auto-falls back down the chain anyway. Enable billing later for pro-tier
> quality (see `docs/setup.md`).

## 5. NotebookLM authentication (browser login)

```bash
notebooklm login          # opens a Google sign-in window — log in once
notebooklm auth check --test
```

This stores a **reusable session** on disk; every later run reuses it. There is
no OAuth API — this stored session (or browser-cookie import / master token for
servers) is the real, supported mechanism. See `docs/setup.md` §2.

## 6. Build the knowledge base + get the Notebook ID

```bash
python scripts/index_knowledge.py
```

This creates the **"AgroManch Knowledge Base"** notebook, indexes `knowledge/`
(only catalog-approved docs), and **prints the Notebook ID**. Paste it in `.env`:

```
NOTEBOOK_ID=<printed id>
```

## 7. Environment validation

```bash
python scripts/check_environment.py
```

All six checks must PASS; the run ends with:

```
Gemini Connected
NotebookLM Connected
Grounded Retrieval Working
Factory Ready
```

**Do not generate anything until you see Factory Ready.**

## 8. First content generation

```bash
python examples/agromanch/content_factory.py --topic "Fall Armyworm control in maize"
```

Output lands in `output/<topic>/` — per-asset files, per-platform folders
(`instagram/`, `whatsapp/`, …), `manifest.json`, plus internal
`quality_report.txt` / `review_report.txt`. See `RUN_PRODUCTION.md` and verify
with `TEST_PRODUCTION.md`.

## 9. Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| `GEMINI_API_KEY is not set` | No key in `.env`/env | §4; get a key from AI Studio |
| **Invalid API key** (HTTP 401/403) | Key mistyped/revoked | Create a fresh key; update `.env` |
| **Quota exceeded** (HTTP 429 after retries) | Free-tier per-minute/day limit | Wait a minute; lower rate; or enable billing |
| **Model unavailable** (HTTP 404) | Model retired / not on your key | Engine auto-falls back; or set `GEMINI_MODEL=gemini-flash-latest` |
| **Notebook login expired** | Google rejected stored cookies | `notebooklm login` again (or `notebooklm auth refresh`) |
| **Notebook ID not found** | Wrong/foreign ID in `.env` | Re-run `python scripts/index_knowledge.py`; paste the printed ID |
| **Network timeout** | Slow network/proxy | Raise `GEMINI_TIMEOUT` in `.env`; check connectivity |
| Empty Gemini reply | Tiny `max_output_tokens` on a thinking model | Don't cap output tokens (validator already fixed) |
| `notebooklm: command not found` | `[browser]` extra not installed | `pip install "notebooklm-py[browser]"` |
| No grounded context for a topic | Knowledge base lacks documents on it | Add docs to `knowledge/<domain>/`, re-run indexer |

More detail: `docs/setup.md`.

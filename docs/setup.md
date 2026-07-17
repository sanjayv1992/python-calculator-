# Production Setup — Credentials & Runtime

Two credentials make the factory runnable: a **Gemini API key** (generation) and
a **NotebookLM session** (retrieval). Guided path:

```bash
pip install -e ".[dev,browser]"
python scripts/setup.py            # key → verify → login → pick notebook → save → validate
python scripts/check_environment.py   # re-check anytime
```

## 1. Gemini API key

1. Go to **[Google AI Studio → API keys](https://aistudio.google.com/apikey)**,
   sign in, and **Create API key** (choose/create a Google Cloud project).
2. Put it in `.env` in the repo root (or export it):

   ```bash
   GEMINI_API_KEY=your-key-here
   ```

   `.env` is loaded automatically (existing environment variables win) and is
   git-ignored. **Never commit or paste keys anywhere**; tools here always mask
   them (`AIza…Xy`).

### Enable billing (recommended)

Free-tier keys have small per-minute/per-day quotas that a full 15-asset bundle
can exhaust. In [Google Cloud Console](https://console.cloud.google.com/billing),
link a billing account to the key's project, then use the same key — limits rise
automatically (pay-as-you-go).

### Supported Gemini models

| Model | Use |
| --- | --- |
| `gemini-2.5-pro` | **Default** — maximum content quality |
| `gemini-2.5-flash` | **Automatic fallback** — fast/cheap; used when the key can't access pro |

Set `GEMINI_MODEL` to override. If the configured model returns 404 for your
key, the engine logs a warning and falls back to `gemini-2.5-flash` on its own.

## 2. NotebookLM authentication

**What's actually supported:** Google has **no public OAuth API for NotebookLM**.
Authentication is a **reusable authenticated session** (cookies in
`~/.notebooklm/profiles/<profile>/storage_state.json`) created once by
`notebooklm-py` via any of:

| Flow | Command | When |
| --- | --- | --- |
| Interactive browser login | `notebooklm login` | Default on a desktop |
| Browser cookie reuse | `notebooklm login --browser-cookies chrome` | Reuse an already-signed-in browser; no Playwright |
| Master token | `notebooklm login --master-token --account you@example.com` | Headless servers / CI |

Every run then reuses the stored session (`NotebookLMClient.from_storage()`).
Keep it alive on schedulers with `notebooklm auth refresh --quiet`. Expired or
revoked sessions are **detected with a real API call** and reported as a clear
"re-run `notebooklm login`" error — never a stack trace.

## 3. Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `GEMINI_API_KEY` | — (required) | Gemini auth (or `GOOGLE_API_KEY`) |
| `GEMINI_MODEL` | `gemini-2.5-pro` | Generation model (auto-fallback to flash) |
| `GEMINI_TEMPERATURE` | `0.7` | Default sampling temperature |
| `GEMINI_TIMEOUT` | `120` | Per-request timeout (seconds) |
| `AGROMANCH_NOTEBOOK_ID` | — | Pin the knowledge notebook (from `scripts/index_knowledge.py`) |
| `AGROMANCH_NOTEBOOK_NAME` | `AgroManch Knowledge Base` | Lookup name when ID unset |
| `AGROMANCH_PROFILE` | default | notebooklm-py auth profile |
| Other `AGROMANCH_*` | see `.env.example` | Language, region, persona, grounding, review |

## 4. Validation

`python scripts/check_environment.py` prints PASS/FAIL for: key exists → Gemini
request succeeds → NotebookLM auth works → notebook exists → retrieval succeeds →
grounded context returned; on success it ends with **Factory Ready**.

## Troubleshooting

| Symptom | Cause & fix |
| --- | --- |
| `GEMINI_API_KEY is not set` | Create a key in AI Studio; add to `.env`; re-run |
| **Invalid key** (`HTTP 401/403`) | Key revoked/mistyped or API not enabled on the project — create a fresh key |
| **Quota exceeded** (`HTTP 429`, retries exhausted) | Free-tier limit hit — wait, slow down, or enable billing (§1) |
| **Model unavailable** (`HTTP 404`) | Key can't access `GEMINI_MODEL`; engine auto-falls back to flash — or set `GEMINI_MODEL=gemini-2.5-flash` |
| **Authentication expired** (NotebookLM) | Google rejected stored cookies — `notebooklm login` again (or `notebooklm auth refresh` with a master token) |
| **Notebook not found** | Wrong `AGROMANCH_NOTEBOOK_ID` or empty account — run `python scripts/index_knowledge.py` to create + fill it, then pin the printed ID |
| No grounded context | Notebook lacks documents on the topic — add sources to `knowledge/` and re-index |
| Timeouts | Raise `GEMINI_TIMEOUT`; check network/proxy |

Security rules baked in: secrets are read only from env/`.env`, masked in every
log and message, never printed, and `.env` is git-ignored and written mode 600.

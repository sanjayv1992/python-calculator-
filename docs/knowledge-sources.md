# Trusted Agriculture Sources & Knowledge-Base Policy

AgroManch's answers are only as trustworthy as the documents behind them.
Because agricultural advice affects livelihoods, food safety, and the safe use
of agrochemicals, the knowledge base must be built **only** from authoritative,
verifiable sources.

## Trusted source categories

| Source | Use it for |
| ------ | ---------- |
| **ICAR** (Indian Council of Agricultural Research) and its institutes | Crop production technology, pest/disease management, post-harvest, contingency plans |
| **State Agricultural Universities (SAUs)** | Region-specific package of practices, fertilizer and pest recommendations |
| **Krishi Vigyan Kendras (KVKs)** | District-level advisories, demonstrations, local crop calendars |
| **Government scheme portals & notifications** | PM-KISAN, PMFBY, KCC, subsidies — eligibility, benefits, application processes |
| **CIB&RC registered labels** | Pesticide dose, target pests, spray volume, pre-harvest interval, safety |
| **Seed catalogues / variety notifications** | Recommended varieties, seed rate, duration |
| **Fertilizer labels & soil-test recommendations** | Nutrient contents, dose by soil-test value |
| **Crop production guides** | End-to-end cultivation practices |
| **IMD / Gramin Krishi Mausam Sewa bulletins** | Agromet advisories, weather-based operations |
| **Soil Health Card material & ICAR-IISS** | Soil sampling, interpretation, amelioration |

## How to add documents

1. Download the authoritative document (PDF preferred, or note its stable URL).
2. Place it in the matching `knowledge/<domain>/` folder:
   - PDFs / office files → drop the file in directly.
   - Web pages → add the URL to that folder's `urls.txt` (one per line).
   - Short notes → write a `.md`/`.txt` file.
3. Record provenance: keep the official title, publishing body, and year in the
   document (the sample `.md` files show the pattern).
4. Run `python scripts/index_knowledge.py` to index it (idempotent).

## Best practices for a verified knowledge base

- **Prefer primary sources.** Use the original ICAR/SAU/government document, not
  a second-hand blog summary.
- **Keep label/dose data exact.** Never paraphrase pesticide doses, PHIs, or
  safety statements — copy them verbatim from the registered label.
- **Record region and year.** Recommendations vary by state and get revised;
  note where and when each document applies.
- **Review before indexing.** A human should confirm each document is
  authoritative and current before it enters the knowledge base.
- **Refresh periodically.** Re-check schemes, MSP, mandi data, and label
  registrations on a schedule; remove superseded documents.
- **Let citations do their job.** Answers cite their sources — surface those
  citations to farmers and extension staff so advice is auditable.
- **Add a safety net.** For agrochemical and scheme answers, always advise the
  farmer to confirm with the printed label / official portal and the local KVK.

## What NOT to put in the knowledge base

- Unverified social-media claims or vendor marketing without technical backing.
- Outdated recommendations or de-registered pesticides.
- Personally identifiable farmer data (keep the KB about agronomy, not people).

# Lead Scout

An AI-powered lead generation pipeline that finds companies actively investing in AI, scores them for fit, tracks down a decision-maker, and drafts a personalised cold email — all in a single run. Results stream into the UI live as each company clears the pipeline.

Built by an AI Adoption Trainer who got tired of manually searching LinkedIn.

---

## What It Does

You select an industry and region, set a max card count, and click Scout. Lead Scout runs a five-stage pipeline and streams each qualified lead to the UI as a card — no waiting for the full run to complete.

Each card shows the company name, domain, score, AI signals, a detected industry label, a named contact with email, and a ready-to-send email draft tailored to whether the company is a potential client, employer, or peer in the space.

---

## Pipeline

### 1. Discovery — `pipeline/discovery.py`

Tavily API searches for companies matching the selected industry and region using hand-tuned query sets. Each industry has three targeted queries — Spanish/Valencia-region searches run in Spanish. Job boards, aggregator domains, and recruitment sites are filtered out before anything reaches the scoring stage. Companies are deduplicated by root domain, and display names are derived from the domain (not the page title).

### 2. Scoring — `pipeline/scoring.py`

Claude fetches and reads each company's public website content and returns a structured JSON assessment. Scoring rules applied:

- **HIGH (7–10):** AI adoption or the target sector is central to the company's day-to-day operations
- **MEDIUM (5–6):** Weak or indirect signals of internal AI adoption
- **LOW (1–4):** Broad consultancy, holding group, or publisher where AI is one of many service areas — or a conference, news site, or market research firm
- **Disqualified (score = 0):** Event organisers, job boards, aggregators, or any company with 1,000+ employees (unless they are a direct AI training competitor — those pass through for the employer/partner email angle)
- **Size penalty:** 500–1,000 employees → score reduced by 2 points
- **Finance & Banking hard reject:** Traditional banking, insurance, or financial services companies at enterprise scale are disqualified regardless of AI signals. Fintech companies are exempt.

Additional fields returned per company: `website_language` (spanish / german / english), `industry` label, `headcount_estimate`, `is_competitor`, `company_type` (client / employer / competitor).

Companies scoring below 6 are dropped and never shown.

### 3. Classification — `pipeline/classify.py`

Checks the scored company against a regional and role filter. Flags companies that fall outside the configured target geography.

### 4. Contact Discovery — `pipeline/contact.py`

Hunter.io domain search finds the best available decision-maker email — prioritising Head of People, HR Director, L&D, CTO, and similar titles. Results containing `linkedin.com` are rejected. Generic `info@` addresses are surfaced but flagged in the UI.

### 5. Email Drafting — `pipeline/email_draft.py`

Claude writes a short, warm, specific cold email using a detailed system prompt that encodes Chris's background, industry-to-experience mappings, and tone rules. The email angle branches automatically by `company_type`:

- **Client:** Outreach positioning Chris as an external AI adoption trainer
- **Competitor:** Job inquiry — curious whether they have room for someone with Chris's background
- **Employer:** Team-building inquiry about building internal AI capability

Email language matches the company's detected website language (Spanish, German, or English).

---

## Tech Stack

| Layer | Tool |
| --- | --- |
| Web framework | Flask |
| Company discovery | Tavily API |
| Website scraping | BeautifulSoup + requests |
| AI scoring + email drafting | Anthropic API (claude-sonnet-4-5) |
| Contact discovery | Hunter.io API |
| Live results | Server-Sent Events (SSE) |
| Config | python-dotenv |

---

## Project Structure

```text
lead-scout/
├── app.py                    # Flask app, routes, SSE streaming
├── pipeline/
│   ├── discovery.py          # Tavily search, domain filtering, name derivation
│   ├── scoring.py            # Claude scoring, size signals, competitor detection
│   ├── classify.py           # Region/role classification
│   ├── contact.py            # Hunter.io contact discovery
│   └── email_draft.py        # Claude email generation, language-aware, branched by type
├── templates/
│   └── index.html            # Single-page UI — dark theme, streaming cards
├── static/
│   ├── css/main.css
│   └── js/main.js
├── .env                      # API keys — never commit this
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Cuqui522/lead-scout.git
cd lead-scout
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Create a `.env` file in the project root

```env
ANTHROPIC_API_KEY=your_anthropic_key
TAVILY_API_KEY=your_tavily_key
HUNTER_API_KEY=your_hunter_key
```

All three keys are required. Anthropic and Tavily both have free tiers sufficient for testing. Hunter.io offers 25 free searches per month.

### 4. Run the app

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Constraints by Design

- **No LinkedIn scraping** — against their ToS, and the data is noisy anyway
- **No storing contacts** — GDPR. Contacts are surfaced per-session only, never written to disk
- **No auto-sending** — every draft is reviewed and sent manually
- **No fake emails** — Hunter.io results containing `linkedin.com` are rejected at the contact stage

---

## Portfolio Note

Lead Scout demonstrates an end-to-end AI pipeline: search → scrape → score → classify → enrich → generate, with live streaming results via SSE. The scoring layer uses structured JSON prompting with multi-rule logic applied partly in the LLM and partly in Python — keeping deterministic business rules (size penalties, hard rejects) out of the model. The email drafting layer uses a persona-encoded system prompt with dynamic branching by company type and detected language. The whole thing runs locally with no database, no cloud infrastructure, and no monthly SaaS bill.

---

## Author

**Chris Chester** — AI Adoption Trainer & Automation Specialist, Valencia, Spain.
Available remotely for EU and US companies. Available in-person for Valencia.

---

## Licence

MIT — use it, fork it, improve it.

# context.md — Lead Scout Project

## What This Is

A local Flask web app that finds companies likely to need an
AI Adoption Trainer / Automation Specialist, scores them by
AI-readiness signals, classifies their type, finds a contact,
and drafts a personalised cold email ready to send.

## Who It's For

Chris — AI Adoption Trainer and Automation Specialist based
in Valencia, Spain. 30 years teaching experience. Available
remotely for EU and US companies, in-person for Valencia only.

## Current Status

Fully operational and in active use/testing phase. Do not
reference any old scraper or v1 code — this is a clean architecture.

## Target Companies

- Size: 50–500 employees (sweet spot)
- Geography: EU remote, US remote, or Valencia in-person
- Signal: actively adopting or investing in AI internally
  (NOT companies that merely write or publish about AI)
- NOT large multinationals (500+ employees, e.g. Santander, BBVA,
  Deutsche Bank) — these are disqualified in favour of SMEs

## Tech Stack

- Flask (local web app)
- Tavily API (company discovery)
- BeautifulSoup (website content scraping)
- Anthropic API / claude-sonnet-4-5 (AI readiness scoring + email drafting)
- Hunter.io API (contact discovery)
- python-dotenv, requests, tavily-python

## API Keys (all in .env)

- ANTHROPIC_API_KEY
- HUNTER_API_KEY
- TAVILY_API_KEY
- FLASK_SECRET_KEY

## Pipeline Architecture

### Stage 1 — Company Discovery (pipeline/discovery.py)

Use Tavily API to find companies via targeted queries.
Queries use negative terms to filter out job boards and aggregators.
Deduplicates results by domain.
Filters out domains containing: linkedin, indeed, glassdoor,
builtin, workingnomads, remote.co, lever.co, greenhouse.io,
jobs, careers, recruit.

Industry-specific query sets:

- Fintech / Finance & Banking: startup/SME-focused fintech queries
- Valencia (In-person) / Spain Remote: bilingual queries in Spanish
  (empresa, automatización, inteligencia artificial, transformación digital)
  with location variants (Valencia, España, Comunitat Valenciana)

Region label mapping:

- "Valencia (In-person)" → "Valencia España"
- "Spain Remote" → "Spain"
- "EU Remote" → "Europe"
- "US Remote" → "United States"

### Stage 2 — AI Readiness Scoring (pipeline/scoring.py)

Visits each company's public website (/, /blog, /news, /about).
Feeds content to Claude with scoring instructions.
Supports multilingual content: Spanish, French, German, Dutch, Italian.
Looks for AI adoption signals in any language (automatización,
inteligencia artificial, transformación digital, aprendizaje automático, etc.)

Scoring rules:

- Score HIGH (7-10): real business actively adopting/deploying AI internally
- Score LOW (1-4): conferences, events, job boards, market research
  publishers, AI news sites — anything that writes ABOUT AI but
  doesn't USE it as a business
- Score MEDIUM (5-6): weak or uncertain signals

Disqualify rules (score forced to 0):

- Conferences, event organisers, market research firms, news aggregators, job boards
- Large multinationals with 500+ employees (e.g. major banks)
- Small fintech startups, scale-ups, and advisory firms are NOT disqualified

Returns: score, signals (list), fit_reason, disqualify, company_type.

company_type values:

- "client": real business adopting AI internally, could use Chris's services
- "competitor": sells AI consulting/automation/training as their core business
- "employer": relevant industry, might hire Chris internally

Only companies scoring 6+ proceed to Stage 3.

### Stage 3 — Region & Role Classification (pipeline/classify.py)

If a job posting URL is found:

- Classify role as: Remote / Hybrid / In-person
- Extract location
- Filter out in-person roles outside Valencia, Spain

If no job posting, classify as "Proactive outreach candidate".

### Stage 4 — Contact Discovery (pipeline/contact.py)

Uses Hunter.io Domain Search API as primary source.
Preferred titles (in order): Chief AI, Head of AI, CTO, CEO,
Founder, Head of Product, and similar decision-maker titles.
If email contains "linkedin.com" → reject, set email to None.
If Hunter returns no named contact, falls back
to info@domain as last resort.
Returns: contact dict with name, title, email.

### Stage 5 — Email Draft (pipeline/email_draft.py)

Uses Anthropic API (claude-sonnet-4-5).
System prompt positions Claude as Chris.

Email angle branches on company_type:

- "client": sales pitch — references fit reason and AI signal,
  mentions Chris works remotely with EU/US companies,
  soft CTA for a 20-minute call
- "competitor": job inquiry — frames Chris's 30 years of teaching
  experience and AI/automation skills, warm professional inquiry
  about whether they have room for someone with his background
- "employer": team inquiry — frames Chris as someone who could
  help them build AI capabilities internally

All emails: max 3 short paragraphs, warm/human tone, sign off: Chris.
Returns: email_draft string.

## Streaming Architecture

Flask uses Server-Sent Events (SSE) via stream_with_context.
Frontend opens an EventSource connection to /search.
Query params: industry, region, max_cards (default 10).
Event types: status, company, warning, error, done.
Cards stream in progressively as each company clears the pipeline.
Pipeline stops emitting cards once max_cards is reached.
Done event includes a count: "X lead(s) found."

## UI

- Single page Flask app (templates/index.html)
- Fonts: IBM Plex Mono (labels, badges, code) + IBM Plex Sans (body)
- Dark theme with teal-green accent (#00e0a0)
- Search controls: Industry dropdown + Region dropdown + Max Cards selector + Scout button
- Max Cards selector: pill buttons for 3 / 5 / 10 / 20 (default 10)
- Status bar with pulsing dot and live status text
- Results grid: cards animate in as they stream
- Card shows: company name, domain, score badge, region badge,
  type badge (colour-coded: green=client, amber=competitor, blue=employer),
  dismiss button, fit reason, signals tags
- Expandable "Contact & draft email" section per card:
  contact name/title/email, email draft, Copy button
- Copy button shows "Copied ✓" for 2 seconds

## Industry Dropdown Options

Healthcare, Finance & Banking, Fintech, Retail & E-commerce,
Manufacturing, Education, HR & People Ops, Legal,
Marketing & Media, Logistics & Supply Chain, All Industries

## Region Dropdown Options

All Regions, EU Remote, US Remote, Valencia (In-person), Spain Remote

## Known Limitations (to address in future sessions)

- Card titles sometimes show page titles instead of company names
- Hunter.io and Apollo.io coverage is thin for niche domains —
  named decision-maker contacts often not publicly available
- Manual LinkedIn lookup recommended as fallback for contact
  discovery when both APIs return generic results
- Occasional noise results still slip through despite disqualify flag

## Session Tracking

Chris is logging each Scout session in LeadScout_Session_Log.xlsx.
Columns: Date, Industry, Region, Results Count, Quality (1-5),
Noise Level (1-5), Contact Quality (1-5), Emails Sendable?,
Best Lead Company, Best Lead Domain, Notes.
This data will be used in a future tuning session to improve
query targeting and scoring by industry/region combo.

## Things to Avoid

- No LinkedIn scraping (ToS violation)
- No storing contact databases (GDPR)
- Reject any Hunter.io result with linkedin.com in the email
- Do not reuse v1 scraper logic
- Do not switch back to Google Custom Search API

## The Council — Pipeline Review System
Three-agent review system for periodic pipeline health checks.
Agent files and SOPs stored in project root (flat naming convention).

| Agent | Role | Trigger |
|---|---|---|
| Ra | Architecture & strategy | Major changes, monthly |
| Anubis | Code forensics & bugs | Known bugs, post-Ra |
| Horus | Session log patterns | Every 5 sessions |

Full process documented in COUNCIL_RUNBOOK.md.
Ra always runs twice and findings are merged before passing to Anubis.
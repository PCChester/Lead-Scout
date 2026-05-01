import json
import anthropic

_client = anthropic.Anthropic()

_BAD_KEYWORDS = [
    "crowdsourc", "freelanc", "upwork", "fiverr", "gig platform",
    "talent marketplace", "clickworker", "microwork", "appen",
    "remotask", "mturk", "mechanical turk", "task marketplace",
    "staffing agency", "recruitment agency",
]

_SYSTEM = """\
Decide if a company should be skipped for B2B AI-implementation sales outreach.
Flag (flagged=true) if: crowdsourcing/freelance marketplace, consumer app, job board,
recruitment agency, government body, charity/NGO, or a direct AI-services competitor.

Reply with ONLY valid JSON — no markdown fences, no extra text:
{"flagged": <bool>, "reason": "<short reason or empty string>"}\
"""


def classify(company: dict) -> dict:
    """Detect crowdsourcing / freelance platforms and other unwanted company types.

    Returns a dict with keys:
        flagged (bool)   True means skip this company
        reason  (str)    why it was flagged (empty string if not flagged)
    """
    combined = f"{company.get('name', '')} {company.get('domain', '')}".lower()
    for kw in _BAD_KEYWORDS:
        if kw in combined:
            return {"flagged": True, "reason": f"Keyword match: '{kw}'"}

    prompt = (
        f"Company: {company.get('name')}\n"
        f"Domain: {company.get('domain')}\n"
        f"Industry: {company.get('industry', 'Unknown')}\n"
        "Should we skip this company?"
    )

    msg = _client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        system=[{"type": "text", "text": _SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        return json.loads(msg.content[0].text)
    except (json.JSONDecodeError, IndexError):
        return {"flagged": False, "reason": ""}

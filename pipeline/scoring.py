import os
import re
import json
import requests
from bs4 import BeautifulSoup
import anthropic

_PATHS = ["/", "/blog", "/news", "/about"]
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}
_TEXT_LIMIT = 3000

_SYSTEM = "You are an AI readiness analyst. Analyse the website content and return ONLY valid JSON."


def fetch_website_text(domain: str) -> str:
    combined = ""
    for path in _PATHS:
        try:
            resp = requests.get(
                f"https://{domain}{path}",
                headers=_HEADERS,
                timeout=8,
            )
            if not resp.ok:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            combined += " " + soup.get_text(separator=" ", strip=True)
            if len(combined) >= _TEXT_LIMIT:
                break
        except Exception:
            continue
    return combined[:_TEXT_LIMIT]


def score_company(company: dict) -> dict:
    try:
        text = fetch_website_text(company["domain"])
        if not text.strip():
            return {**company, "score": 0, "signals": [], "fit_reason": ""}

        prompt = (
            f"Website content for {company['domain']}:\n\n{text}\n\n"
            "Analyse this website content and score this company as a potential client for Chris, "
            "an AI Adoption Trainer and Automation Specialist.\n\n"
            "IMPORTANT SCORING RULES:\n"
            "- Score HIGH (7-10) only if the company is a real business that appears to be actively "
            "adopting, deploying, or investing in AI tools internally\n"
            "- Score LOW (1-4) if the company is: a conference, event, job board, market research "
            "publisher, AI news site, or any site that writes ABOUT AI but doesn't USE it as a business\n"
            "- Score MEDIUM (5-6) if uncertain but there are weak signals of internal AI adoption\n\n"
            "Also add a \"disqualify\" boolean to your JSON — set it true if the company is a "
            "conference, event organiser, market research firm, news aggregator, or job board.\n\n"
            "Return ONLY valid JSON with keys: score (int), signals (list of strings, max 5), "
            "fit_reason (string), disqualify (boolean)"
        )

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        msg = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = msg.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
        result = json.loads(raw)

        score = 0 if result.get("disqualify") else int(result.get("score", 0))

        return {
            **company,
            "score":      score,
            "signals":    result.get("signals", []),
            "fit_reason": result.get("fit_reason", ""),
        }

    except Exception:
        return {**company, "score": 0, "signals": [], "fit_reason": ""}

import re
import json
import warnings
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

_client = anthropic.Anthropic()


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
            return {
                **company,
                "score": 0,
                "signals": [],
                "fit_reason": "",
                "company_type": "client",
                "website_language": "english",
                "industry": "",
                "headcount_estimate": "unknown",
                "is_competitor": False,
            }

        prompt = (
            f"Website content for {company['domain']}:\n\n{text}\n\n"
            "Analyse this website content and score this company as a potential client for Chris, "
            "an AI Adoption Trainer and Automation Specialist.\n\n"
            "IMPORTANT: The website content may be in any language including Spanish, French, German, "
            "Dutch, Italian or others. Identify AI adoption signals regardless of the language — "
            "look for concepts like automation, artificial intelligence, digital transformation, "
            "machine learning, and workflow tools in whatever language they appear. For example: "
            "automatización, inteligencia artificial, transformación digital, aprendizaje automático "
            "in Spanish. Location references may also appear in local form — Valencia, España, "
            "Comunitat Valenciana, or Spain are all valid location signals.\n\n"
            "IMPORTANT SCORING RULES:\n"
            "- Score HIGH (7-10) only if AI adoption or the target industry is CENTRAL to what "
            "the company actually does day-to-day — not just listed as one of many service areas\n"
            "- Score LOW (1-4) if the company is: a conference, event, job board, market research "
            "publisher, AI news site, or any site that writes ABOUT AI but doesn't USE it as a "
            "business — AND if the company's primary business is broad consultancy, government "
            "services, investment, or a general holding group where AI or the target sector is "
            "merely one of many areas they touch. Explain this clearly in fit_reason.\n"
            "- Score MEDIUM (5-6) if uncertain but there are weak signals of internal AI adoption\n\n"
            "Also add a \"disqualify\" boolean to your JSON — set it true if the company is a "
            "conference, event organiser, market research firm, news aggregator, or job board. "
            "Small fintech startups, scale-ups, and independent investment or advisory firms "
            "should NOT be disqualified.\n\n"
            "Also add a \"headcount_estimate\" field. Infer approximate company size from cues "
            "in the website content — explicit headcount or staff numbers, number of offices or "
            "locations, \"enterprise\" or \"Fortune 500\" self-description, customer scale, or "
            "similar signals. Set it to one of: \"under_500\", \"500_to_1000\", \"over_1000\", "
            "or \"unknown\" if there are no clear signals.\n\n"
            "Also add an \"is_competitor\" boolean. Set it to true if the company already offers "
            "AI adoption training, AI literacy programs, or change management consulting around AI "
            "as a CORE service — meaning this is central to their business, not a peripheral "
            "offering. When is_competitor is true, do NOT disqualify the company. Instead, set "
            "fit_reason to something like: \"Already operates in this space — potential employer "
            "or partner rather than client.\"\n\n"
            "Also add a \"company_type\" field to your JSON. Set it to one of three values:\n"
            "- \"competitor\" if the company sells AI consulting, automation consulting, AI adoption "
            "training, or digital transformation services as their core business (i.e. they do what "
            "Chris does, for clients)\n"
            "- \"client\" if the company is a real business actively adopting AI internally and could "
            "benefit from Chris's training and automation services\n"
            "- \"employer\" if the company is in a relevant industry and might need someone with "
            "Chris's skills as a team member but does not obviously need external training\n\n"
            "Also detect the primary language of the website content and set \"website_language\" "
            "to \"spanish\", \"german\", or \"english\" (use \"english\" as the default for any "
            "other language).\n\n"
            "Also set \"industry\" to a short label describing the company's core business — "
            "for example: \"retail\", \"manufacturing\", \"fintech\", \"logistics\", \"healthcare\", "
            "\"education\", \"real estate\", \"hospitality\", \"legal\", \"consulting\".\n\n"
            "Return ONLY valid JSON with keys: score (int), signals (list of strings, max 5), "
            "fit_reason (string), disqualify (boolean), headcount_estimate (string), "
            "is_competitor (boolean), company_type (string), website_language (string), "
            "industry (string)"
        )

        msg = _client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = msg.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
        result = json.loads(raw)

        company_type = result.get("company_type", "client")
        if company_type not in {"client", "employer", "competitor"}:
            warnings.warn(f"Unexpected company_type '{company_type}' for {company.get('domain')} — defaulting to 'client'")
            company_type = "client"

        headcount     = result.get("headcount_estimate", "unknown")
        is_competitor = result.get("is_competitor", False)
        detected_ind  = result.get("industry", "").lower()

        # 6c: Finance & Banking hard reject at enterprise scale
        finance_keywords = ("bank", "insurance", "financial services", "asset management")
        is_large_finance  = (
            any(kw in detected_ind for kw in finance_keywords)
            and headcount in ("500_to_1000", "over_1000")
            and "fintech" not in detected_ind
        )

        disqualify = (
            result.get("disqualify", False)
            or (headcount == "over_1000" and not is_competitor)
            or is_large_finance
        )

        raw_score = int(result.get("score", 0))
        if disqualify:
            score = 0
        elif headcount == "500_to_1000":
            score = max(0, raw_score - 2)
        else:
            score = raw_score

        return {
            **company,
            "score":              score,
            "signals":            result.get("signals", []),
            "fit_reason":         result.get("fit_reason", ""),
            "company_type":       company_type,
            "website_language":   result.get("website_language", "english"),
            "industry":           result.get("industry", ""),
            "headcount_estimate": headcount,
            "is_competitor":      is_competitor,
        }

    except Exception:
        return {
            **company,
            "score": 0,
            "signals": [],
            "fit_reason": "",
            "company_type": "client",
            "website_language": "english",
            "industry": "",
            "headcount_estimate": "unknown",
            "is_competitor": False,
        }
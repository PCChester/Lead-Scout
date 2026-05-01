import os
import requests

HUNTER_KEY = os.getenv("HUNTER_API_KEY")

_PRIORITY_TITLES = [
    "chief ai", "head of ai", "vp ai", "director of ai",
    "chief technology", "cto", "vp engineering", "head of engineering",
    "chief digital", "chief innovation", "head of innovation",
    "chief executive", "ceo", "founder", "co-founder",
    "head of product", "vp product",
]


def _title_priority(title: str) -> int:
    t = (title or "").lower()
    for i, kw in enumerate(_PRIORITY_TITLES):
        if kw in t:
            return i
    return len(_PRIORITY_TITLES)


def find_contact(company: dict) -> dict:
    """Find the best decision-maker contact at a company.

    Returns a dict with keys:
        name  (str)   full name
        title (str)   job title
        email (str)   email address or LinkedIn profile URL if no direct email found
    """
    domain = company.get("domain", "")
    if not domain:
        return {"name": "Hiring Team", "title": "", "email": ""}

    resp = requests.get(
        "https://api.hunter.io/v2/domain-search",
        params={"domain": domain, "api_key": HUNTER_KEY, "limit": 20},
        timeout=15,
    )

    if resp.status_code != 200:
        return {"name": "Hiring Team", "title": "", "email": f"info@{domain}"}

    emails = resp.json().get("data", {}).get("emails", [])
    if not emails:
        return {"name": "Hiring Team", "title": "", "email": f"info@{domain}"}

    best = min(emails, key=lambda e: _title_priority(e.get("position", "")))
    first = best.get("first_name", "")
    last = best.get("last_name", "")
    return {
        "name":  f"{first} {last}".strip() or "Hiring Team",
        "title": best.get("position", ""),
        "email": best.get("value", f"info@{domain}"),
    }

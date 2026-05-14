import json
import os
import requests

HUNTER_KEY = os.getenv("HUNTER_API_KEY")
APOLLO_KEY = os.getenv("APOLLO_API_KEY")

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


def _is_generic(contact: dict) -> bool:
    """Returns True if the contact is a generic fallback — no name or no email."""
    return not contact.get("email") or contact.get("name") == "Hiring Team"


def _apollo_fallback(domain: str) -> dict:
    """Try Apollo's organization_top_people endpoint for a named decision-maker."""
    if not APOLLO_KEY:
        return {"name": "Hiring Team", "title": "", "email": ""}

    try:
        resp = requests.post(
            "https://api.apollo.io/api/v1/mixed_people/organization_top_people",
            headers={"Content-Type": "application/json"},
            json={"api_key": APOLLO_KEY, "organization_domain": domain},
            timeout=15,
        )
        if resp.status_code != 200:
            return {"name": "Hiring Team", "title": "", "email": ""}

        people = resp.json().get("people", [])
        if not people:
            return {"name": "Hiring Team", "title": "", "email": ""}

        best = min(people, key=lambda p: _title_priority(p.get("title", "")))
        email = best.get("email", "")
        if "linkedin.com" in (email or ""):
            email = None

        first = best.get("first_name", "")
        last = best.get("last_name", "")
        return {
            "name":  f"{first} {last}".strip() or "Hiring Team",
            "title": best.get("title", ""),
            "email": email,
        }

    except Exception:
        return {"name": "Hiring Team", "title": "", "email": ""}


def find_contact(company: dict) -> dict:
    """Find the best decision-maker contact at a company.

    Returns a dict with keys:
        name  (str)   full name
        title (str)   job title
        email (str)   email address or None if no direct email found
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
        return _apollo_fallback(domain)

    try:
        emails = resp.json().get("data", {}).get("emails", [])
    except json.JSONDecodeError:
        return _apollo_fallback(domain)

    if not emails:
        return _apollo_fallback(domain)

    best = min(emails, key=lambda e: _title_priority(e.get("position", "")))
    first = best.get("first_name", "")
    last = best.get("last_name", "")
    email = best.get("value", "")
    if "linkedin.com" in (email or ""):
        email = None

    contact = {
        "name":  f"{first} {last}".strip() or "Hiring Team",
        "title": best.get("position", ""),
        "email": email,
    }

    if _is_generic(contact):
        return _apollo_fallback(domain)

    return contact
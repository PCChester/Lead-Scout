import os
import re
from tavily import TavilyClient

_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return _client


_REGION_LABEL = {
    "EU Remote":            "Europe",
    "US Remote":            "United States",
    "Valencia (In-person)": "Valencia Spain",
    "Spain Remote":         "Spain",
}

_NEGATIVE_TERMS = (
    "-site:linkedin.com -site:indeed.com -site:glassdoor.com "
    "-site:builtin.com -site:workingnomads.com -site:remote.co "
    "-site:weworkremotely.com -site:jobs.com"
)

_SKIP_DOMAIN_FRAGMENTS = [
    "linkedin", "indeed", "glassdoor", "builtin", "workingnomads",
    "remote.co", "lever.co", "greenhouse.io", "jobs", "careers", "recruit",
]


def _build_queries(industry: str, region: str) -> list[str]:
    ind = industry if industry and industry != "All Industries" else ""
    reg = _REGION_LABEL.get(region, region) if region and region != "All Regions" else ""

    def _q(*parts) -> str:
        tokens = [p for p in parts if p]
        return " ".join(tokens) + " " + _NEGATIVE_TERMS

    return [
        _q(ind, "company AI automation strategy", reg, "2024"),
        _q(ind, "company deploying AI tools employees", reg),
        _q(ind, "business AI adoption digital transformation", reg, "case study"),
    ]


def _root_domain(url: str) -> str:
    m = re.search(r"https?://(?:www\.)?([^/?#]+)", url)
    return m.group(1).lower() if m else ""


def _company_name(title: str, domain: str) -> str:
    for sep in (" - ", " | ", " — ", " · "):
        if sep in title:
            return title.split(sep)[0].strip()
    return domain.split(".")[0].replace("-", " ").title()


def _is_aggregator(domain: str) -> bool:
    return any(frag in domain for frag in _SKIP_DOMAIN_FRAGMENTS)


def discover(industry: str, region: str):
    """Yield company dicts matching the given industry and region.

    Expected keys per yielded dict:
        name     (str)   company name
        domain   (str)   e.g. "acme.com"
        industry (str)   industry label from the search filter
        region   (str)   matched region label
        role     (str)   job role that triggered discovery
    """
    queries = _build_queries(industry, region)
    client = _get_client()

    seen: set[str] = set()
    for query in queries:
        response = client.search(
            query=query,
            max_results=10,
            search_depth="basic",
        )
        for result in response.get("results", []):
            domain = _root_domain(result.get("url", ""))
            if not domain or domain in seen or _is_aggregator(domain):
                continue
            seen.add(domain)
            yield {
                "name":     _company_name(result.get("title", ""), domain),
                "domain":   domain,
                "industry": industry or "General",
                "region":   region or "All Regions",
                "role":     "AI / Technology",
            }

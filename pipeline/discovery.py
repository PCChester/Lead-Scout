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
    "Valencia (In-person)": "Valencia España",
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

    if industry == "Fintech":
        return [
            _q("fintech startup under 500 employees AI automation", reg, "2024"),
            _q("payments digital banking regtech insurtech AI tools", reg),
            _q("fintech scaleup AI adoption platform lending neobank", reg),
            _q("fintech company AI adoption case study press release", reg),
        ]

    if industry == "Finance & Banking":
        return [
            _q("financial services SME AI adoption digital transformation", reg, "2024"),
            _q("investment advisory wealth management AI tools", reg),
            _q("insurance asset management AI automation", reg),
            _q("financial services AI adoption case study press release", reg),
        ]

    if industry == "Language & Communication Training":
        return [
            _q("corporate language school AI content delivery L&D", reg, "2024"),
            _q("communication training provider AI tools e-learning", reg),
            _q("language learning company AI automation blended learning", reg),
            _q("language training company AI adoption case study press release", reg),
        ]

    if industry == "IT & AI Solutions":
        return [
            _q("IT consultancy AI solutions provider digital transformation", reg, "2024"),
            _q("IT services company AI tools internal adoption", reg),
            _q("technology consultancy AI implementation partner", reg),
            _q("IT company AI adoption case study press release", reg),
        ]

    if industry == "Film & Production":
        return [
            _q("film production company AI tools content creation", reg, "2024"),
            _q("video production studio AI automation post-production", reg),
            _q("media production company AI workflow digital", reg),
            _q("film production AI adoption case study press release", reg),
        ]

    if reg in ("Valencia España", "Spain", "España"):
        return [
            _q(ind, "empresa automatización inteligencia artificial Valencia España", "2024"),
            _q(ind, "empresa transformación digital IA herramientas", reg),
            _q(ind, "company AI automation digital transformation", reg),
            _q(ind, "empresa IA caso de éxito transformación digital", reg),
        ]

    return [
        _q(ind, "company AI automation strategy", reg, "2024"),
        _q(ind, "company deploying AI tools employees", reg),
        _q(ind, "business AI adoption digital transformation", reg, "case study"),
        _q(ind, "company AI adoption case study press release", reg),
    ]

def _root_domain(url: str) -> str:
    m = re.search(r"https?://(?:www\.)?([^/?#]+)", url)
    return m.group(1).lower() if m else ""


def _name_from_domain(domain: str) -> str:
    stem = domain.split(".")[0]          # "some-company" from "some-company.es"
    words = stem.split("-")
    if len(words) == 1 and len(stem) <= 5:
        return stem.upper()              # ainia → AINIA, bbva → BBVA
    return " ".join(w.capitalize() for w in words)  # some-company → Some Company


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
        try:
            response = client.search(
                query=query,
                max_results=20,
                search_depth="basic",
            )
        except Exception as e:
            print(f"[Discovery] Tavily query failed: {query!r} — {e}")
            continue

        for result in response.get("results", []):
            domain = _root_domain(result.get("url", ""))
            if not domain or domain in seen or _is_aggregator(domain):
                continue
            seen.add(domain)
            yield {
                "name":     _name_from_domain(domain),
                "domain":   domain,
                "industry": industry or "General",
                "region":   region or "All Regions",
                "role":     "AI / Technology",
            }

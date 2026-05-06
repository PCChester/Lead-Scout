import os
import anthropic

_SYSTEM = """You are drafting cold outreach emails on behalf of Chris Chester.

## Who Chris is
Chris Chester is an AI Adoption Trainer and Automation Specialist based in Valencia, Spain. He has 25+ years of experience helping people and organisations work more effectively — first through corporate communication and language training across Europe and the US, now bringing AI literacy and workflow automation into his training practice as the natural next step. He speaks English (native), Spanish (advanced), and German (advanced), and has lived and worked in Austria, Germany, New York, and Spain. He is available remotely for EU and US companies, and in-person for Valencia.

## Industry-to-experience mapping
Use this to select the ONE or TWO most relevant background points for the email. Weave them in naturally — do not list them all.

- Retail / FMCG / Food: Mercadona (trained managers and department heads across retail ops, product, marketing); Delibreads (Mercadona tortilla supplier — food manufacturing)
- E-commerce / IT / Tech (retail): Mercadona Online — separate IT and e-commerce focused subsidiary
- Automotive / Manufacturing / Engineering: SRG Global (automotive body parts, Liria — technical English for engineers and management); MAN Trucks Munich (corporate communication, major vehicle manufacturer); Siemens AG (global industrial/tech environment)
- Finance / Insurance / Banking: Munich RE (reinsurance — high-stakes financial communication training); CaixaBank (Spanish financial institution)
- Pharma / Life Sciences: Bayer AG (one of the world's largest pharma/chemical companies)
- Tech / Enterprise Software: Microsoft Munich European HQ (trained professionals in a global tech enterprise)
- Paints / Coatings / Manufacturing: Sherwin Williams
- Shipping / Logistics: MSC Shipping (CFO was a direct student — executive-level stakeholder relationship)
- Public Sector / Chambers / Associations: Valencia Chamber of Commerce (President was a direct student — strong local institutional credibility)
- Language / Education / Training: Worked across multiple language academies in Valencia and Germany — curriculum development, learning materials, staff training and recruitment, translations. Senior contributor, not owner.
- HR / People Ops: Consistent HR stakeholder relationships throughout career — needs analysis, aligning training to business goals, measuring outcomes. HR Specialist title at SRG Global.
- Cross-cultural / International: Lived and worked in 9 countries, visited 36. Trained teams across Austria, Germany, Spain, and the US in cross-cultural business communication.

## Human angle hook
Use this when no specific industry match exists:
"30 years teaching people in high-pressure, unfamiliar environments — ESL, scuba diving, boardroom negotiations — translates directly into AI adoption training. Same fear, same resistance, same method: calm them down, build confidence, make it stick."

## Standing rules
- Write warm, human, concise emails. Never sound salesy.
- Maximum 3 short paragraphs.
- End with a soft CTA for a 20-minute call.
- Sign off: Regards, Chris
- Do NOT claim Chris has years of AI adoption training experience — frame it as his natural next step combining deep training expertise with new AI skills.
- Return ONLY the email text, no subject line, no explanation.
"""


def draft_email(company: dict) -> dict:
    """Draft a cold outreach email and store it in company['email_draft'].

    Expects company to contain: name, domain, signals, fit_reason, contact,
    company_type, and optionally website_language ('spanish', 'german', or 'english').
    Returns the updated company dict.
    """
    try:
        contact = company.get("contact") or {}
        contact_name = contact.get("name", "")
        greeting = f"Hi {contact_name.split()[0]}," if contact_name and contact_name != "Hiring Team" else "Hi there,"

        signals = company.get("signals") or []
        signal_note = f'Specifically reference this signal found on their website: "{signals[0]}"' if signals else ""

        company_type = company.get("company_type", "client")

        lang = (company.get("website_language") or "english").lower().strip()
        if lang == "spanish":
            lang_instruction = "Write the entire email in Spanish."
        elif lang == "german":
            lang_instruction = "Write the entire email in German."
        else:
            lang_instruction = "Write the email in English."

        industry = company.get("industry", "")
        industry_note = f"Their industry: {industry}." if industry else ""

        if company_type == "competitor":
            prompt = (
                f"Write a cold email to the contact at {company.get('name')} ({company.get('domain')}).\n\n"
                f"Start with: {greeting}\n"
                f"Context: This company offers similar services to Chris — AI consulting, automation, "
                f"or digital transformation. The email angle is a job inquiry, not a sales pitch.\n"
                f"{industry_note}\n"
                f"{signal_note}\n\n"
                "Instructions:\n"
                "- Mention Chris is Valencia-based with deep teaching and training experience "
                "plus hands-on AI and automation skills\n"
                "- Frame the email as genuine curiosity about whether they have room for someone "
                "with Chris's background — not desperation, just a warm professional inquiry\n"
                f"- {lang_instruction}\n"
            )
        elif company_type == "employer":
            prompt = (
                f"Write a cold email to the contact at {company.get('name')} ({company.get('domain')}).\n\n"
                f"Start with: {greeting}\n"
                f"Context: This company may benefit from having someone with Chris's AI adoption "
                f"and training skills on their team.\n"
                f"{industry_note}\n"
                f"{signal_note}\n\n"
                "Instructions:\n"
                "- Mention Chris is Valencia-based with deep teaching and training experience "
                "plus hands-on AI and automation skills\n"
                "- Frame the email as an inquiry about whether they are building out AI capabilities "
                "internally and might need someone like Chris\n"
                f"- {lang_instruction}\n"
            )
        else:
            prompt = (
                f"Write a cold email to the contact at {company.get('name')} ({company.get('domain')}).\n\n"
                f"Start with: {greeting}\n"
                f"Why they're a fit: {company.get('fit_reason', '')}\n"
                f"{industry_note}\n"
                f"{signal_note}\n\n"
                "Instructions:\n"
                "- Mention Chris is Valencia-based and works remotely with EU and US companies\n"
                "- Use the industry mapping in your instructions to weave in the most relevant "
                "background point for this company's sector\n"
                f"- {lang_instruction}\n"
            )

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        msg = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )

        company["email_draft"] = msg.content[0].text.strip()

    except Exception:
        company["email_draft"] = "Could not generate email draft."

    return company

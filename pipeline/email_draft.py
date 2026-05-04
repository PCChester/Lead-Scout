import os
import anthropic

_SYSTEM = (
    "You are Chris, an AI Adoption Trainer and Automation Specialist based in Valencia, Spain. "
    "Write warm, human, concise emails. Never sound salesy."
)


def draft_email(company: dict) -> dict:
    """Draft a cold outreach email and store it in company['email_draft'].

    Expects company to contain: name, domain, signals, fit_reason, contact, company_type.
    Returns the updated company dict.
    """
    try:
        contact = company.get("contact") or {}
        contact_name = contact.get("name", "")
        greeting = f"Hi {contact_name.split()[0]}," if contact_name and contact_name != "Hiring Team" else "Hi there,"

        signals = company.get("signals") or []
        signal_note = f'Specifically reference this signal found on their website: "{signals[0]}"' if signals else ""

        company_type = company.get("company_type", "client")

        if company_type == "competitor":
            prompt = (
                f"Write a cold email to the contact at {company.get('name')} ({company.get('domain')}).\n\n"
                f"Start with: {greeting}\n"
                f"Context: This company offers similar services to Chris — AI consulting, automation, "
                f"or digital transformation. The email angle is a job inquiry, not a sales pitch.\n"
                f"{signal_note}\n\n"
                "Instructions:\n"
                "- Maximum 3 short paragraphs\n"
                "- Mention Chris is Valencia-based with 30 years of teaching and training experience "
                "plus hands-on AI and automation skills\n"
                "- Frame the email as genuine curiosity about whether they have room for someone "
                "with Chris's background — not desperation, just a warm professional inquiry\n"
                "- End with a soft CTA suggesting a 20-minute call\n"
                "- Sign off: Chris\n"
                "- Return ONLY the email text, no subject line, no explanation"
            )
        elif company_type == "employer":
            prompt = (
                f"Write a cold email to the contact at {company.get('name')} ({company.get('domain')}).\n\n"
                f"Start with: {greeting}\n"
                f"Context: This company operates in a relevant industry and may benefit from having "
                f"someone with Chris's AI adoption and training skills on their team.\n"
                f"{signal_note}\n\n"
                "Instructions:\n"
                "- Maximum 3 short paragraphs\n"
                "- Mention Chris is Valencia-based with 30 years of teaching and training experience "
                "plus hands-on AI and automation skills\n"
                "- Frame the email as an inquiry about whether they are building out AI capabilities "
                "internally and might need someone like Chris\n"
                "- End with a soft CTA suggesting a 20-minute call\n"
                "- Sign off: Chris\n"
                "- Return ONLY the email text, no subject line, no explanation"
            )
        else:
            prompt = (
                f"Write a cold email to the contact at {company.get('name')} ({company.get('domain')}).\n\n"
                f"Start with: {greeting}\n"
                f"Why they're a fit: {company.get('fit_reason', '')}\n"
                f"{signal_note}\n\n"
                "Instructions:\n"
                "- Maximum 3 short paragraphs\n"
                "- Mention Chris is Valencia-based and works remotely with EU and US companies\n"
                "- End with a soft CTA suggesting a 20-minute call\n"
                "- Sign off: Chris\n"
                "- Return ONLY the email text, no subject line, no explanation"
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

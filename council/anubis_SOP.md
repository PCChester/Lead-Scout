# SOP.md — Anubis, The Surgeon

## Rules of Engagement

### What triggers an Anubis session
- A known bug needs pinpointing to the exact stage and line
- Ra has flagged a strategic concern that needs forensic investigation
- A Scout session produced unexpected results and the cause is unknown
- Routine pipeline health check (monthly minimum)

### How to open an Anubis session in Claude Code
Paste the following at the start of the conversation:

```
Read council/anubis_AGENT.md and context.md. You are Anubis.
Here is the current state of the system: [paste context.md]
Here are Ra's strategic concerns: [paste Ra's findings if available]
Your task: conduct a forensic review of the Lead Scout pipeline code.
Follow your output format exactly.
```

Then paste the relevant pipeline files for Anubis to read.

### Which files to provide
Always provide all five pipeline files:
- pipeline/discovery.py
- pipeline/scoring.py
- pipeline/classify.py
- pipeline/contact.py
- pipeline/email_draft.py

### Anubis does not
- Redesign pipeline stages
- Analyse session log data
- Suggest new APIs or tools — refer those to Ra

### After Anubis reports
- Confirmed Issues → take to Chris for execution
- Fragile Points → log in context.md Known Limitations
- Referred to Ra → paste into Ra's session
- Referred to Horus → paste into Horus's session

### Fix length rule
Any fix Anubis suggests must be describable in 3 sentences or fewer.
If it takes more, it is Ra's territory — escalate.

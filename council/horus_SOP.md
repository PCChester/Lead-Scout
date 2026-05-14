# SOP.md — Horus, The Watchman

## Rules of Engagement

### What triggers a Horus session
- After every 5 Scout sessions logged in the session log
- When a specific industry/region combo feels like it's getting worse
- When Chris suspects signal quality is drifting but can't pinpoint why
- At the start of a full Council session (runs parallel to Ra)

### How to open a Horus session in Claude Code
Paste the following at the start of the conversation:

```
Read council/horus_AGENT.md and context.md. You are Horus.
Here is the current state of the system: [paste context.md]
Here is the session log data: [paste or attach LeadScout_Session_Log.xlsx]
Your task: analyse patterns across all logged Scout sessions.
Follow your output format exactly.
```

### How to provide session log data
Option A: Paste the log as a markdown table directly into the chat
Option B: Attach the .xlsx file if Claude Code supports it in context
Option C: Paste a CSV export of the log

### Horus does not
- Review pipeline code
- Make architectural decisions
- Flag patterns from fewer than 3 sessions (low confidence)

### After Horus reports
- Drift Alerts → share with Anubis for forensic investigation
- Hidden Opportunities → share with Chris for next Scout session planning
- Recommendations to the Council → share with Ra for strategic review

### Cadence rule
Run Horus at minimum once per month, or every 5 sessions —
whichever comes first. The log is only useful if it's being read.

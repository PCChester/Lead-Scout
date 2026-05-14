# SOP.md — Ra, The Architect

## Rules of Engagement

### What triggers a Ra session
- Before any major pipeline change
- When a new industry or region produces consistently poor results
- When the pipeline is being adapted for a new client or use case
- At the start of a full Council session

### How to open a Ra session in Claude Code
Paste the following at the start of the conversation:

```
Read council/ra_AGENT.md and context.md. You are Ra.
Here is the current state of the system: [paste context.md]
Your task: conduct a full architectural review of the Lead Scout pipeline.
Follow your output format exactly.
```

### Run Ra twice — always
Open two separate Claude Code chats and run the same Ra prompt in both.
Ra approaches the same system from a different angle each session —
one may think like an engineer, the other like a strategist.
Combine both reports before passing concerns to Anubis.

Rules for combining:
- Concerns that appear in both sessions = high priority, Ra is certain
- Concerns that appear in one session only = worth investigating, lower confidence
- Never discard single-session concerns — they caught real issues in testing

### Ra does not
- Write or suggest specific code fixes
- Review session log data directly
- Make decisions alone — Ra recommends, Chris decides

### After Ra reports (both sessions)
- Merge Strategic Concerns from both sessions into a single list
- Copy merged concerns into Anubis's session for forensic investigation
- Copy Ra's "Questions for the Council" into Horus's session for pattern analysis
- Return combined findings to Ra for final plan

### Plan length rule
Ra's recommended direction must fit in 10 sentences or fewer.
If it doesn't, Ra is over-engineering. Cut it.

### Anti-patterns to avoid
- Ra suggesting a full rebuild when a targeted fix will do
- Ra commenting on code syntax or style
- Ra producing a plan longer than the problem warrants

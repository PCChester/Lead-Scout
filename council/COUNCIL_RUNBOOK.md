# THE COUNCIL — Master Session Runbook
## Lead Scout / Egyptian Council System

---

## The Three Voices

| Agent | Role | Reviews | Thinks In |
|---|---|---|---|
| ⚡ Ra | The Architect | Pipeline design & strategy | Systems |
| 🔪 Anubis | The Surgeon | Pipeline code & bugs | Specifics |
| 👁️ Horus | The Watchman | Session log patterns | Time |

---

## Folder Structure

```
lead-scout/
├── council/
│   ├── ra_AGENT.md
│   ├── ra_SOP.md
│   ├── anubis_AGENT.md
│   ├── anubis_SOP.md
│   ├── horus_AGENT.md
│   ├── horus_SOP.md
│   └── COUNCIL_RUNBOOK.md
├── context.md          ← all three agents read this
├── agents.md
├── memory.md
├── skills.md
└── pipeline/
    ├── discovery.py
    ├── scoring.py
    ├── classify.py
    ├── contact.py
    └── email_draft.py
```

**File naming rule:** All council files use the flat `agentname_FILETYPE.md`
format everywhere — on your computer, in Claude Code, and in Claude Projects.
One name, one place, no confusion.

**Updating rule:** Edit the file on your computer in VS Code, save it,
then re-upload the updated file to Claude Projects. That's it.

---

## Running a Full Council Session

### Step 1 — Open Ra (Architecture Review) — run TWICE
Open two separate Claude Code chats. Paste the same prompt in both:
```
Read council/ra_AGENT.md and context.md. You are Ra.
[paste context.md]
Conduct a full architectural review. Follow your output format.
```
Save both outputs. Merge Strategic Concerns before proceeding.
Concerns appearing in both sessions = high priority.
Concerns appearing in one session only = lower confidence but don't discard.

### Step 2 — Open Horus (Pattern Review) — run in parallel with Ra
New Claude Code chat. Paste:
```
Read council/horus_AGENT.md and context.md. You are Horus.
[paste context.md]
[paste or attach session log data]
Analyse patterns across all logged sessions. Follow your output format.
```
Save Horus's full output.

### Step 3 — Open Anubis (Forensic Review)
New Claude Code chat. Paste:
```
Read council/anubis_AGENT.md and context.md. You are Anubis.
[paste context.md]
Ra's concerns: [paste Ra's Strategic Concerns]
Horus's drift alerts: [paste Horus's Drift Alerts]
[paste all 5 pipeline files]
Conduct a forensic review. Follow your output format.
```
Save Anubis's full output.

### Step 4 — Council Round (Synthesis)
Return to Ra's chat. Paste:
```
Anubis found: [paste Anubis's Confirmed Issues + Fragile Points]
Horus found: [paste Horus's Drift Alerts + Hidden Opportunities]
Build the recovery and improvement plan. Maximum 10 sentences.
```
Ra produces the final plan.

### Step 5 — Execute
Chris executes Ra's plan. Anubis's specific fixes go first.

### Step 6 — Update the Docs
Update these files before closing the session — never skip this step:
- `context.md` — log architectural changes, update Known Limitations,
  update pipeline stage descriptions if anything changed
- `memory.md` — log new decisions or corrections discovered
- `README.md` — update if pipeline stages, tech stack, or setup changed
- `COUNCIL_RUNBOOK.md` — update if the Council process itself improved

Then re-upload any changed files to Claude Projects.

### Step 7 — Log the Session
Add a row to LeadScout_Session_Log.xlsx noting it was a Council session.
Note which agent flagged the most valuable finding.

---

## Quick Reference — When to Trigger Each Agent

| Situation | Agent |
|---|---|
| Something feels architecturally wrong | Ra |
| Known bug, unknown location | Anubis |
| Results quality feels like it's slipping | Horus |
| Major change planned | Ra first, then Anubis |
| Every 5 Scout sessions | Horus |
| Monthly health check | Full Council |
| Adapting for a new client | Ra + Anubis |

---

## The Golden Rules
1. Ra recommends. Anubis finds. Horus watches. Chris decides.
2. No agent rewrites working logic without cause.
3. Plans must be short. If Ra's plan needs more than 10 sentences, cut it.
4. One Council session per month minimum — the log is only useful if it's being read.
5. When in doubt, run Horus first — the pattern usually points to the problem.
6. One source of truth — flat file names everywhere, update on your computer, re-upload to Claude Projects.

---

## Adapting for a New Client (Template Use)
1. Copy the entire `council/` folder into the new project
2. Replace `context.md` with the new client's pipeline description
3. Update `anubis_AGENT.md` with the new pipeline file names
4. Update `horus_AGENT.md` with the new session log column names
5. `ra_AGENT.md` and `horus_SOP.md` need no changes — they are universal
6. Run a full Council session before the first Scout run

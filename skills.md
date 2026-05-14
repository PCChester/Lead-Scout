# skills.md — Reusable SOPs & Skills

> These are reusable processes and standards Chris and Claude have agreed on. Reference these when starting new tasks to maintain consistency.

---

## Skill: Starting a New Session
1. Claude reads agents.md, memory.md, context.md, and skills.md from the project files
2. Claude confirms the project files are the latest versions (ask Chris if unsure)
3. Claude confirms understanding and asks: "Where are we picking up?"
4. No assumptions — check in before making changes

---

## Skill: Building a New Website Section
1. Agree on the section goal and content before writing any code
2. Keep tone warm, witty, and professional (see context.md)
3. Check in before choosing layout or design approach
4. Build mobile-first
5. Document decisions in context.md progress log

---

## Skill: Evaluating a Tool or Platform
1. Define the problem first
2. Ask: can this be solved with Claude Code alone?
3. If external data/integrations are needed, check for API access
4. Compare: custom build vs. subscription tool vs. API hybrid
5. Recommend based on: speed, cost, maintainability, and whether client needs to touch it

---

## Skill: Adding a New Project to Portfolio
1. Describe what the project does in plain English
2. Explain why this approach was chosen (tool selection rationale)
3. Note what problem it solves for the client/employer
4. Add to context.md projects list
5. Create a portfolio card with: title, description, tools used, outcome

---

## Skill: Updating Memory
When Claude learns something new:
- Correct a mistake → log in memory.md under "Corrections"
- Learn a preference → log under "Preferences Learned"
- Make a project decision → log in context.md "Progress Log"
- Always remind Chris to save in VS Code and re-upload to Claude Projects

---

## Skill: Lead Scout — Running a Scout Session
1. Select Industry and Region in the UI
2. Click Scout and monitor the streaming results
3. Review cards — dismiss noise results
4. For quality leads: expand card, review contact and email draft
5. Log the session in LeadScout_Session_Log.xlsx (Date, Industry, Region, Results Count, Quality 1-5, Noise Level 1-5, Contact Quality 1-5, Emails Sendable?, Best Lead, Notes)

---

## Skill: Lead Scout — Tuning & Debugging
1. Check context.md for known limitations before diagnosing
2. Identify which pipeline stage the issue originates in
3. Fix in the relevant pipeline file (discovery.py, scoring.py, classify.py, contact.py, email_draft.py)
4. Test with a single industry/region combo before broader testing
5. Log any architectural decisions in context.md

---

## Skill: File & Folder Management System

### Master Folder Structure

AI-Projects/
│
├── _MASTER/                  ← Originals, never edited directly
│   ├── agents.md             ← Permanent profile (rarely changes)
│   └── memory.md             ← Universal preferences & corrections
│
├── lead-scout/               ← Active project
│   ├── agents.md             ← Copy from master (reference only)
│   ├── memory.md             ← Copy from master
│   ├── context.md            ← Unique to this project
│   ├── skills.md             ← Relevant skills for this project
│   └── (code files)
│
├── portfolio-website/        ← Paused project
│   └── ...

### Rules
- `_MASTER` is the source of truth — never edit directly during a project
- Each project gets its own folder with copies of the master files
- `context.md` and `skills.md` are updated within the project folder as work progresses
- If `memory.md` gets a universal update (new preference, correction) → copy it back to `_MASTER`
- `agents.md` only changes if Chris's profile, goals, or working style changes
- Always save in VS Code before uploading to Claude Projects

### Starting a New Project Chat
1. Open the relevant project folder in VS Code
2. Confirm all files are saved
3. Upload/replace files in Claude Projects
4. Claude reads all four files and confirms: "Where are we picking up?"

---

## Notes
- More skills to be added as we build and encounter repeatable tasks
- Each skill should be simple enough to trigger with a short prompt
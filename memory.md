# memory.md — Chris's Persistent Memory File

> **Instruction for Claude:** When Chris corrects you, changes a preference, or you learn something new about how he works or what he wants, update this file. This creates a self-improving loop across sessions.

## Preferences Learned
- Chris prefers voice/conversational input — he often uses voice transcription, so expect informal phrasing
- Chris thinks strategically before diving in — he likes to clarify concepts before building
- Chris has a great sense of humour — lean into it, it builds rapport and trust
- Chris values understanding the "why" behind decisions, not just the "what"
- Chris is family-oriented — stability and income security matter when making recommendations
- Chris saves files in VS Code before uploading to Claude Projects — always confirm the project file is the latest version at session start

## Corrections & Adjustments
- Google Custom Search API no longer allows new app registrations — replaced with Tavily API
- claude-sonnet-4-5 is the correct model string for Lead Scout's Anthropic API calls
- VS Code auto-save is not always reliable — confirm files are saved before uploading to Claude Projects
- Apollo.io added as Hunter.io fallback in contact.py (free tier, 900 credits/year)
- Tavily max_results increased from 10 to 20 per query
- Fourth query added per industry/region set targeting case studies and press coverage
- Exception handler in scoring.py was returning incomplete dict — now fixed with all required fields

## Decisions Made
- Portfolio website tone: warm, professional, witty — not corporate
- Build approach: Claude Code preferred over no-code platforms for Chris's own projects
- Audit-first philosophy confirmed: always assess client needs before recommending tools
- Context files (agents.md, memory.md, context.md, skills.md) adopted as project management system
- Lead Scout v2 built from scratch — do not reference v1 scraper logic
- Tavily API chosen for company discovery (replaces Google CSE)
- Session logging adopted: Chris tracks each Scout run in LeadScout_Session_Log.xlsx
- Portfolio website project paused — Lead Scout is the active project
- The Council system adopted: Ra, Anubis, Horus agents for pipeline review
- Ra always run twice per session — findings merged before passing to Anubis
- Manual LinkedIn lookup accepted as human-in-the-loop step for contact discovery
- Fintech/EU established as standing benchmark combo — run first to calibrate quality
- Apollo.io free tier sufficient for Lead Scout usage — Basic plan deferred until freelance work justifies it
- Outreach Engine concept documented but deferred — fix contact quality first
- Apollo.io dropped as backup to Hunter.io as yielded no results over multiple sessions

## Things to Avoid
- Don't over-explain technical concepts unless asked
- Don't assume Chris wants the most complex solution — simpler is often better
- Don't skip check-ins on big decisions
- Don't reference old v1 scraper or Google CSE architecture
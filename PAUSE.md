# Paused — 2026-04-11

## Apply Tomorrow
Need to submit an application. Resume may need tailoring before then.

## Notion Drafts (not yet in sections/)
The following experience bullets are drafted in Notion and need to be added to `sections/experiences.txt` before they can be used in resume generation:
- **Experiences** (general)
- **APS** (likely a role/project)
- **Project Director** (likely a role/project)

Pull these into `sections/experiences.txt` before the next session so the AI can use them.

## Where We Left Off
Working through setting up this repo. Completed:
- [x] `CLAUDE.md` — instructions for AI (WHO pattern, writing style, file rules, action verb table)
- [x] `scripts/save.ps1` — saves `draft.tex` to `saved/(N)name.tex`, compiles, renames PDF

Still to do:
- [ ] `README.md` — project overview for humans/collaborators (was mid-discussion when paused)

## README Notes (collected so far)
- `saved/` — finalized resumes: `(1)main`, `(2)swe`, `(3)ds`; future company/role-specific ones follow the same `(N)name` pattern
- `sections/` — master experience data (education, experiences, orgs, skills, volunteering, context)
- `applications/` — history of application writing (essays, prompts, notes) for future reference
- `draft.tex` — single active working file for the current application
- `build/` — LaTeX output directory for `draft.tex`
- `saved/build/` — compiled PDFs for finalized resumes
- `scripts/rename-pdf.ps1` — renames built PDF to `Alessandro_Felici_Resume[_SWE|_DS].pdf`
- `scripts/save.ps1` — new: copies draft → saved, compiles, renames in one command
- `.agent/rules/general.md` — legacy AI rules (superseded by `CLAUDE.md`)

### Two Workflows
1. **Write a bullet** — give a rough sentence or context, AI uses WHO pattern + action verbs to form the best version
2. **Tailor to a job** — paste a job URL or description, AI selects and adapts bullets from `sections/` to match

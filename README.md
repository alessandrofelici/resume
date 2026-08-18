# Resume

A personal resume system for tailoring and maintaining multiple versions of a LaTeX resume, driven by a master experience library and AI assistance.

---

## Project Structure

```
resume/
├── draft.tex               # Active working file — current application in progress
├── master_doc.tex          # Comprehensive, non-tailored master resume (every entry from
│                            # sections/, not constrained to one page) — the source to pull
│                            # from when assembling/tailoring draft.tex
├── build/                  # LaTeX output for draft.tex / master_doc.tex (auto-generated, not committed)
├── sections/                # Master experience library
│   ├── experiences.md      # Work history and internships
│   ├── organizations.md    # Clubs, teams, leadership roles
│   ├── education.md        # Degree, coursework
│   ├── projects.md
│   ├── technical-skills.md
│   └── volunteering.md
├── saved-resumes/          # Finalized resume versions
│   ├── (1)main.tex         # General-purpose resume
│   ├── (2)swe.tex          # Software engineering tailored
│   ├── (3)ds.tex           # Data science tailored
│   ├── (N)company-role.tex # Company or role-specific
│   └── build/              # Compiled PDFs for saved resumes
├── applications/           # Application history (essays, prompts, notes)
│   ├── GeorgiaTech.md      # Example: GT Trading Competition essay
│   ├── ICER.md
│   ├── HackMIT.md
│   ├── MHacks25.md
│   └── MHacks26.md
├── scripts/
│   ├── save.ps1            # Save draft → saved-resumes/, compile, rename PDF
│   └── rename-pdf.ps1      # Rename compiled PDF to clean filename
├── CLAUDE.md               # AI instructions (writing rules, WHO pattern, verb list)
└── .agent/rules/general.md # Legacy AI rules (superseded by CLAUDE.md)
```

---

## Workflows

### 1. Tailor to a Job Posting
Give the AI a job URL or paste the description. It reads `sections/` and selects the most relevant bullets, adapting them to match the role.

### 2. Write or Improve a Bullet
Give a rough sentence or context. The AI applies the **WHO pattern** (What → How → Outcome) and rewrites it using strong action verbs and a quantified result. Rewritten lines will show an astrisk, to mark it for review.

### 3. Save a Finalized Resume
When `draft.tex` is ready to be saved as a named version:

```powershell
./scripts/save.ps1 swe          # saves as saved-resumes/(N)swe.tex
./scripts/save.ps1 google-swe   # saves as saved-resumes/(N)google-swe.tex
```

This copies the draft, compiles it, and renames the PDF in `saved-resumes/build/`.

---

## Saved Resume Naming

Saved resumes follow the `(N)name` convention where `N` is auto-incremented:

| File | Purpose |
|---|---|
| `(1)main.tex` | General / default |
| `(2)swe.tex` | Software engineering |
| `(3)ds.tex` | Data science |
| `(N)company-role.tex` | Company or role-specific |

---

## Applications Folder

`applications/` is a history of application writing — essays, personal statements, short answers. Not resume content, but useful as reference when applying to similar programs or companies in the future.

---

## AI Rules

Resume generation follows the rules in `CLAUDE.md`:
- One page, fills the page without overflow
- Bold metrics and significant numbers
- WHO pattern: **What** (action verb) → **How** (method/tool) → **Outcome** (bold metric)
- No fabricated statistics — ask before adding implied metrics
- Drafted sentences marked with `*` — do not change without user approval
- The master doc is for visualization. Change hierarchy should always reference the markdown file for the respective section.

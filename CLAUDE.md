# Resume Project Instructions

## File Editing Rules
- Do NOT edit any files under `./saved/` or `./sections/`. Only edit `draft.tex`.

## Project Purpose
Generate a tailored resume `.tex` file (`draft.tex`) for a given computer science internship URL. The resume should be customized to the job posting using the user's information stored in `./sections/`.

## Resume Formatting
- **One page only.** Fill the page as much as possible without exceeding one page.
- Bold significant numbers (e.g. metrics, percentages, counts).
- Use standard text characters only — no emojis or special characters.
- Do not use LaTeX packages not already installed. Check with `pdflatex --version`.

## Bold Formatting Convention
Bold markers must be preserved when moving bullets between `sections/` files and `draft.tex`:
- In `.txt` section files: mark bold text with `**text**`
- In `draft.tex`: render as `\textbf{text}`
- When pulling a bullet from sections into the draft, convert `**text**` → `\textbf{text}`
- When writing a bullet back to a sections file, convert `\textbf{text}` → `**text**`

## Writing Style
- Use strong action verbs and quantify achievements whenever possible.
- Make sentences concise and impactful.
- Each sentence should fill its full line without extending only a few words into the next line. Do not forcefully extend a sentence to achieve this.

## Statistics & Accuracy
- Do NOT fabricate statistics. Use "N/A" or "Not Applicable" if unknown.
- If a statistic is implied by the sentence or required by the job description, ask the user before including it.

## Draft Review
- Mark drafted sentences with an asterisk (`*`).
- Consult the user before changing any asterisk-marked sentence.
- Do NOT remove the asterisk — only the user should remove it.

## Bullet Point Structure (WHO Pattern)
Each resume bullet should follow the **What → How → Outcome** pattern:
- **What**: the action taken — open with a strong action verb (per Writing Style)
- **How**: the method, tool, or approach used
- **Outcome**: the quantified result or impact — bold the metric (per Resume Formatting)

Example structure: `[Action verb] + [what you did] + [how you did it] + [bold outcome/metric]`

- If a bullet is missing an outcome and a metric can be inferred from context, ask the user before adding it (per Statistics & Accuracy).
- Drafted bullets should be marked with `*` and follow this pattern (per Draft Review).

### Action Verb Reference
Use **present tense** for current roles, **past tense** for past roles.

| Category | Verbs |
|---|---|
| Achievement | accelerated, accomplished, achieved, activated, attained, competed, earned, effected, elicited, executed, expanded, expedited, generated, improved, increased, insured, marketed, mastered, obtained, produced, reduced, reorganized, reproduced, restructured, simplified, sold, solicited, streamlined, succeeded, upgraded |
| Administrative | arranged, channeled, charted, collected, collated, coordinated, dispensed, distributed, established, executed, implemented, installed, maintained, offered, outlined, performed, prepared, processed, provided, purchased, recorded, rendered, served, serviced, sourced, supported, translated |
| Communication | addressed, arbitrated, articulated, briefed, communicated, conducted, contacted, conveyed, corresponded, delivered, demonstrated, entertained, interviewed, informed, lectured, mediated, negotiated, persuaded, presented, promoted, proposed, publicized, reported, represented, responded, suggested, translated, wrote |
| Creative | authored, changed, conceived, constructed, created, developed, devised, drafted, established, formulated, founded, illustrated, influenced, invented, introduced, launched, originated, revamped, revised, staged, updated, visualized |
| Financial | allocated, analyzed, appraised, audited, balanced, budgeted, calculated, compiled, computed, controlled, disbursed, estimated, figured, financed, forecasted, projected, reconciled, tabulated |
| Lead/Manage | acquired, administered, approved, assigned, chaired, contracted, controlled, decided, delegated, directed, enlisted, governed, handled, initiated, instilled, employed, managed, motivated, recruited, retained, reviewed, selected |
| Plan/Organize | allocated, anticipated, arranged, catalogued, categorized, classified, collected, consolidated, convened, edited, eliminated, grouped, monitored, planned, regulated, scheduled, structured |
| Help/Teach | advised, clarified, coached, collaborated, consulted, counseled, educated, explained, facilitated, guided, instructed, modeled, taught, trained, tutored |
| Research/Analytical | assessed, compared, critiqued, defined, derived, detected, determined, discovered, evaluated, examined, explored, found, inspected, interpreted, investigated, located, measured, observed, rated, recommended, reviewed, searched, studied, surveyed |
| Technical | adapted, adjusted, applied, built, computed, constructed, designed, diagnosed, engineered, maintained, modified, operated, prescribed, programmed, proved, reinforced, repaired, resolved, restored, solved, specified, systematized, tested |

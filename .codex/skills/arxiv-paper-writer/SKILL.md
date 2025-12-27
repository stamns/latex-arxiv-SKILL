---
name: arxiv-paper-writer
description: >
  Write LaTeX ML/AI review articles for arXiv using the IEEEtran template
  and verified BibTeX citations.
compatibility: >
  Python 3.8+ for scripts. Web browsing/search for citation verification.
  LaTeX is required (pdflatex + bibtex or latexmk).
metadata:
  short-description: ML/AI review papers (IEEEtran template) with verified citations
---

# ML/AI Review Paper Workflow (IEEEtran template)

## When to Use
- ML/AI review papers for arXiv (main text ~6-10 pages; references excluded)
- LaTeX + BibTeX workflow with verified citations
- Citation validation/repair on existing LaTeX projects

## When NOT to Use
- Novel experimental research papers (this is a review workflow)
- Non-academic documents

## Inputs
- Topic description (required)
- Constraints: venue, page limit, author/affiliations (optional)
- Existing project path for citation validation (optional)

## Outputs
- `main.tex` (LaTeX source)
- `ref.bib` (verified BibTeX entries)
- `IEEEtran.cls`
- `plan/<timestamp>-<slug>.md`, `issues/<timestamp>-<slug>.csv`
- Figures/tables; `main.pdf`
- `notes/literature-notes.md` (optional per-citation notes)

---

## Gated Workflow

> Tip: Treat scripts as black boxes; run `python3 scripts/<script>.py --help` before use.
> Open reference files only when a step calls them out.

### Non-Negotiable Rules
1. **No prose in `main.tex`** until plan approved AND issues CSV exists.
2. First deliverable: research snapshot + outline + clarification questions + draft plan.
3. **Use plan + issues tracking for all new papers; do not opt out.**
4. Issues CSV is the execution contract; update `Status` and `Verified_Citations` per issue.
5. **Template is fixed**: use IEEEtran two-column layout (`assets/template/IEEEtran.cls`).
   Treat two-column width as a layout constraint (use two-column floats when needed).

### Gate 0: Research Snapshot + Draft Plan
1. Confirm constraints (venue, page limit, author block, date range).
2. Translate the topic into search keywords and run a light discovery pass:
   10-20 key papers (see `references/research-workflow.md`).
3. Propose 2-4 candidate titles aligned to the topic.
4. Scaffold the project folder and draft plan:
   ```bash
   python3 scripts/bootstrap_ieee_review_paper.py --stage kickoff --topic "<topic>"
   ```
   This copies LaTeX templates from `assets/template/` and plan/issues templates from `assets/`.
5. Create a **framework skeleton** in `main.tex`
   (section headings + 2-4 bullets per section + seed citations; **no prose**).
6. Update the plan file to reflect the framework, proposed titles, and section/subsection plan.
7. Compile early to surface LaTeX errors:
   `python3 scripts/compile_paper.py --project-dir <paper>`
   - After compiling, scan `main.log` for `Overfull \hbox` warnings and fix them (e.g., switch to `figure*`/`table*` for wide content, size to `\textwidth` instead of `\columnwidth`, or adjust table column widths / `\tabcolsep`).
8. Return to user:
    - Proposed outline (5-8 sections, 2-4 bullets each)
    - Planned visualizations (5+) mapped to sections (see `references/visual-templates.md`)
    - Clarification questions
9. **STOP** until user approves.

### Gate 1: Create Issues CSV (after approval)
1. Check kickoff gate in plan: `- [x] User confirmed scope + outline in chat`.
2. Create issues CSV (script refuses if gate unchecked):
   ```bash
   python3 scripts/bootstrap_ieee_review_paper.py --stage issues --topic "<topic>" --with-literature-notes
   ```
3. Validate:
   ```bash
   python3 scripts/validate_paper_issues.py <paper>/issues/<timestamp>-<slug>.csv
   ```
4. If literature notes are enabled, keep short summaries and (optional) abstract snippets to avoid re-search.
5. The plan may evolve; update the issues CSV accordingly and re‑validate it regularly.

### Phase 2: Per-Issue Writing Loop
For each writing issue in the CSV:
1. **Research**: 8-12 section-specific papers.
2. **Write**: Never 3 sentences without citations; varied paragraph rhythm
   (see `references/writing-style.md`).
   For section intent and structure, use `references/template-usage.md`.
3. **Visualize**: Match content triggers (see `references/visual-templates.md`).
   Prioritize two-column sizing; use double-column spans only when necessary to avoid overflow.
   - Plots/diagrams: start with `figure` + `width=\columnwidth`; switch to `figure*` + `width=\textwidth` if labels/legends or content density won’t fit.
   - Tables: start with `table` sized to `\columnwidth`; switch to `table*` when column count/headers/notes don’t fit. Prefer tuning `p{...}` widths / `\tabcolsep` over `\resizebox` (last resort).
   - Long equations: prefer line-breaking (`split`, `multline`, `aligned`, `IEEEeqnarray`); if still too wide, use a two-column span (e.g., `strip` from `cuted`, if available) rather than shrinking illegibly.
   If a figure includes externally sourced content (nodes, labels, data), add in-text citations.
4. **Verify**: Web search + open source page (and PDF if available) before adding to `ref.bib`.
5. **Update**: Mark issue `DONE` with `Verified_Citations` count.
6. Compile after meaningful changes to catch LaTeX errors early.
   - Treat `Overfull \hbox` warnings as a layout bug to fix before marking an issue `DONE`.

### Phase 3: QA Gate
1. Run internal QA checklist (see `references/quality-report.md`).
2. Compile the paper and resolve errors.
   - Ensure there are no `Overfull \hbox` warnings in the final `main.log`.
3. Deliver `main.tex`, `ref.bib`, figures, and `main.pdf`.

---

## Existing Paper Workflow (No Re-Scaffold)
If a paper folder already exists, do NOT rerun scaffold:
```bash
# Create plan
python3 scripts/create_paper_plan.py --topic "<topic>" --stage plan --output-dir <paper>
# STOP for approval, then check kickoff gate box
# Create issues (use timestamp/slug from plan filename/frontmatter)
python3 scripts/create_paper_plan.py --topic "<topic>" --stage issues --timestamp "<TS>" --slug "<slug>" --output-dir <paper> --with-literature-notes
```

## Citation-Validation Variant
1. Treat provided path as LaTeX project root.
2. Follow `references/citation-workflow.md`.
3. Use `references/bibtex-guide.md` for BibTeX rules if entries need repair.
4. Deliver validation report and corrected `ref.bib` if requested.

---

## Verification & Success Criteria

**Compilation**:
```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```
- Exit 0, no "Citation undefined" warnings, page count within limit.
Alternative: `python3 scripts/compile_paper.py --project-dir <paper>`

**Quality Metrics**:
- 6-10 pages of main text (references excluded)
- 60-80 total citations (8+ per section)
- 100% citation verification rate
- 70%+ citations from last 3 years
- 5+ visualization types
- All issues `DONE` or `SKIP`

---

## Safety & Guardrails
- **Never fabricate** citations or results; add TODO and ask user if evidence missing.
- **Verify every citation** via web search + source page (and PDF if available) before adding to `ref.bib`.
- **Confirm before** large literature searches.
- **Do not overwrite** user files without confirmation.
- **Issues CSV** is the contract; mark `DONE` only when criteria met.
- **No submission bundles** unless user requests.

---

## Manual Script Usage (advanced)
For finer control than `bootstrap_ieee_review_paper.py`:
```bash
# Plan only
python3 scripts/create_paper_plan.py --topic "<topic>" --stage plan --output-dir "<folder>"
# Issues only (after approval)
python3 scripts/create_paper_plan.py --topic "<topic>" --stage issues --timestamp "<TS>" --slug "<slug>" --output-dir "<folder>" --with-literature-notes
```

---

## Issues CSV Schema (default template)
| Phase | Issues |
|-------|--------|
| Research | Rx: discovery, scaffolding, framework, viz planning |
| Writing | Wx: each section with target citations and visualization |
| QA | Qx: citation verification, QA checklist, compilation, final review |

Status flow: `TODO` -> `DOING` -> `DONE`

Validate with: `python3 scripts/validate_paper_issues.py <csv>`

> Note: Paper-specific schema (Phase, Target_Citations, Verified_Citations, Visualization);
> use `validate_paper_issues.py` as source of truth.
> Add or remove section rows as needed; keep IDs consistent.

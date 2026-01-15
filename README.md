# Research Project Template

## Manifesto
This directory structure is designed for **Agentic Research**. It separates "Ideation/Context" from "Formal Theory" and "Execution".

### Directory Guide
- **`literature/`**: 
  - `papers/`: PDF storage.
  - `reviews/`: Markdown summaries (`CiteKey.md`). **Agents: Read these to understand prior work.**
  - `bibliography.bib`: Single source of truth.
- **`context/`**:
  - `glossary.md`: **CRITICAL**. Defines symbols ($v$ vs $u$) and terms.
  - `hypotheses.md`: List of scientific claims and their status.
  - `notes/`: Raw human notes (scans, PDFs).
- **`theory/`**: Formal derivations (Notebooks, Mathematica).
- **`simulation/`**:
  - `src/`: Code.
  - `runs/`: Structured logs (`YYMMDD_Hash`).
- **`manuscript/`**: LaTeX source.

## Project State & Memory
**For Agents Starting Fresh:**
1.  **Read History**: `context/RESEARCH_LOG.md` (What have we done?)
2.  **Read Theory**: `theory/Theory_Structure.md` (What are we building?)
3.  **Read Plan**: `simulation/Detailed_Plan.md` (What is the next task?)

## Agent Instructions
1.  **Context First**: Before suggesting code or theory, read `context/glossary.md` and `context/hypotheses.md`.
2.  **Logs**: When running simulations, ALWAYS create a new subdirectory in `simulation/runs/` with `config.json` and `results.json`.
3.  **Citations**: Use `literature/bibliography.bib` keys.

## Agent Cluster
This project is architected for a multi-agent workflow. The Main Agent (Antigravity) orchestrates specialized personas defined in `context/AGENTS.md`.

### The Team
1.  **The Theorist** (`context/prompts/theorist.md`): Critical thinking, derivation, rigor.
2.  **The Simulator** (`context/prompts/simulator.md`): Efficient Python code, logging, PDF plotting.
3.  **The Reviewer** (`context/prompts/literature_review.md`): Literature analysis.
4.  **The Writer** (`context/prompts/academic_writer.md`): Manuscript drafting.

## Autonomous Research Tools
### Literature Review
**Find Papers**:
```powershell
py utils/research_assistant.py --query "Topic" --max 3
```
*   Downloads PDFs to `literature/papers/`.
*   Updates `literature/bibliography.bib`.
*   Creates stubs in `literature/reviews/`.

**Review Papers**:
*   "Antigravity, review `paper.pdf` using the literature prompt."

## Commands
### Option A: Makefile (if installed)
- `make install`, `make sim`, `make paper`

### Option B: PowerShell (Recommended for Windows)
- `.\manage.bat install`
- `.\manage.bat sim`
- `.\manage.bat paper`

> Note: `manage.bat` automatically bypasses PowerShell execution restrictions.

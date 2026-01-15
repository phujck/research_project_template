# Agent Registry

This file defines the specialized agents available in this project.
The Main Agent (Antigravity) uses this to route user requests.

## 1. The Theorist
*   **Trigger**: "Derive", "Check math", "Hypothesize", "Explain theory"
*   **Persona File**: `context/prompts/theorist.md`
*   **Role**: The Creative Core. Prioritizes clarity, pedagogy, and mathematical rigour.

## 2. The Reviewer
*   **Trigger**: "Review this paper", "Find papers on X", "Summarize"
*   **Persona File**: `context/prompts/literature_review.md`
*   **Role**: Critical analysis of literature, data extraction.

## 3. The Simulator
*   **Trigger**: "Write code", "Simulate", "Optimize", "Plot"
*   **Persona File**: `context/prompts/simulator.md`
*   **Role**: Implementation, efficiency, logging, plotting (PDFs).

## 4. The Writer
*   **Trigger**: "Draft", "Write section", "Edit manuscript"
*   **Persona File**: `context/prompts/academic_writer.md`
*   **Role**: Synthesis of results and reviews into academic LaTeX.

## 5. The Archivist
*   **Trigger**: "Update log", "Clean up", "Where were we?", "Organize"
*   **Persona File**: `context/prompts/archivist.md`
*   **Role**: Project Oracle. Tracks history (`RESEARCH_LOG.md`) and maintains order.

# Approach

Companion hands-on lab for reading Martin Kleppmann's *Designing Data-Intensive Applications*. The goal isn't just notes — it's building real judgment: knowing what options exist for a given problem and being able to weigh them against constraints (cost, latency, scale, ops burden, failure modes), not just recognizing the vocabulary.

## Structure

- One folder per chapter: `chapter1/`, `chapter3/`, etc. **The user creates these as they progress** — don't create a new chapter folder unprompted.
- Inside each chapter folder:
  - `summary.md` — a **precise, targeted revision sheet** for the chapter's concepts (definitions, comparison tables, decision checklists) — meant to be re-read quickly to refresh before moving on. Not a chronological log/journal of what was done, no dates, no narration of the session — just the distilled knowledge, with a one-line pointer to the relevant task PDF for hands-on reference.
  - Small practical/mini-project pieces tied to concepts from that chapter. These can be a subdirectory or just loose files — whatever fits the size of the exercise. No fixed layout is imposed (e.g. `chapter3/simplest_db.sh` + `chapter3/database` is a toy key-value store, just two files, no subdir needed).
  - Task PDFs, filed within the chapter they belong to.

## Practical task workflow

When the user hits a concept they understand abstractly but can't yet apply — can't enumerate the real options, or can't judge which constraints should decide between them — they'll flag it (a term, a design question, a "why X over Y" moment). No fixed schedule; they set the pace.

In response: build a short, practical, hands-on task — not another explainer — that forces comparing at least two real options against concrete constraints and making a call, then reveals the tradeoffs. Save it as a PDF inside the relevant chapter folder.

Don't pre-pick topics or force a menu of terms on the user before they've asked.

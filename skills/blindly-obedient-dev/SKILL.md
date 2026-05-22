---
name: blindly-obedient-dev
description: Review any procedural documentation — tutorial, README, install guide, quickstart, CONTRIBUTING, onboarding docs — by following it literally as a first-time user, executing every step for real, and reporting every friction where the docs are wrong, incomplete, contradictory, or block the reader. Use when asked to QA/review a tutorial or getting-started guide, validate that documentation actually works end-to-end, check that a README/setup guide can be followed, or to "dérouler un tutoriel / une doc" and remonter les frictions.
---

# Blindly Obedient Dev

QA **procedural documentation** by *being the developer who reads it for the
first time and obeys it literally* — no prior knowledge, no shortcuts. Follow it
to the letter, run every command for real, and report every friction.

## Scope — when this skill applies

Applies to any doc the reader is meant to **execute step by step**: tutorials,
`README`, install/setup guides, quickstarts, `CONTRIBUTING.md`, onboarding docs,
how-to recipes — whether or not it is labelled "tutorial" or split into "parts".

Does **not** apply to purely **reference** docs (API reference, config tables)
or **conceptual** docs (architecture, "core concepts") — there is no procedure
to walk. At most you can spot-check individual claims there; that is a different
exercise.

Below, "the doc" means whatever procedural doc is under review, "a step" means
any instruction to perform, and "a section" means any unit the doc is split into
(a tutorial part, a README heading, a numbered step…).

## Golden rules

1. **The documentation is the only source of truth.** Do not read the project's
   source code to figure out how things work — a real first-time reader can't.
2. **Read source code only when blocked**, or to back up a friction report with a
   root cause. Note explicitly that you had to.
3. **Execute everything.** Don't assume a step works — run the command, open the
   URL, check the output, the exit code, the rendered page.
4. **Copy snippets verbatim first.** If a snippet, applied literally, breaks or
   overwrites something — that *is* the friction. Report it, then apply the
   sensible fix to continue.
5. If genuinely stuck even after reading the code, **ask the user**.

## Workflow

1. **Map the doc.** Fetch the landing page, extract the table of contents or
   the list of sections. For a single-page doc (a `README`), just read it top to
   bottom. Use `scripts/fetchdoc.py <url>` for web docs — it handles self-signed
   certs and converts HTML → readable markdown (keeps code blocks & tables).
2. **Set up a report folder**, e.g. `.scratch/<doc>-review/` with a `README.md`
   index and one numbered note per friction.
3. **Do the prerequisites** (install / bootstrap / run the stack) — these are
   part of the doc; frictions here count.
4. **For each section, in order:** apply every step literally → verify it works
   → log frictions as you hit them. Never skip ahead.
5. **Compile the report** (see below).

## What counts as a friction

- A command that doesn't exist / is misspelled / has wrong flags.
- A snippet that, copied verbatim, **overwrites** existing config or **breaks**
  something (missing attribute, wrong import).
- A URL / endpoint / path that differs from what the doc claims.
- A missing step or missing file (e.g. an `__init__.py` never mentioned).
- An instruction that is ambiguous for the real environment (e.g. "set the env
  var" when the app runs in Docker).
- The page **contradicts another page** (reference doc, or its own snippet).
- An incomplete diagram / structure block.
- Anything that silently does the wrong thing (no error, wrong result).

Also flag, separately, **what deserves to be added/expanded** in the doc
(undocumented mechanisms, missing wiring steps), and **what you could not
verify** (coverage gaps).

## One note per friction

```md
# Friction NN — <short title>

**Page concernée :** <doc page / section>
**Sévérité :** Élevée | Moyenne | Faible

## Ce que dit la doc
<quote / snippet>

## Ce qui se passe réellement
<observed behavior, exact error, exit code>

## Cause (si vérifiée dans le code)
<file:line + explanation — only if you had to dig>

## Correctif recommandé
<concrete doc fix; A/B options if relevant>
```

## The report (`README.md`)

- Verdict global (1–2 sentences: does it work end-to-end? does it block?).
- Frictions table grouped by severity (🔴 bloquant/destructif, 🟠 doc
  fausse/incomplète, 🟡 confusion), each linking its note.
- A "déroulé" table: one row per section → ✅ / ⚠️ + which friction.
- Cross-cutting recommendation if several frictions share a root cause.

## Severity guide

- 🔴 **Élevée** — blocks the reader, or destroys/loses configuration if followed.
- 🟠 **Moyenne** — it works, but the doc is factually wrong or incomplete.
- 🟡 **Faible** — confusing, but no blockage and no data loss.

## Persona discipline

Stay in character. Phrase findings as "a developer following this would…".
Browse the docs like a real reader would (follow links, check the reference
pages the doc points to — contradictions between them are prime frictions).

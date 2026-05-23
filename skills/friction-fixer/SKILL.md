---
name: friction-fixer
description: Consume a documentation friction report (produced by the blindly-obedient-dev skill) and apply the recommended fixes to the documentation only — never to application code — then open a pull request. Use when asked to fix/apply/act on a doc review or friction report, to patch documentation based on QA findings, or to turn a `.scratch/<doc>-review/` folder into actual doc corrections. Pairs with blindly-obedient-dev, which diagnoses; this skill repairs.
---

# Friction Fixer

`blindly-obedient-dev` QAs documentation and produces a **friction report** — it
diagnoses but changes nothing. This skill is the next step: it reads that report
and **applies the recommended fixes to the documentation**, then opens a pull
request.

Hard boundary: **this skill never modifies application code.** Frictions whose
fix lives in the code are surfaced to the user, not fixed here — the user has
other tools for that.

## Required inputs — gather these before doing anything else

Confirm both before starting. If either is missing or ambiguous, **stop and ask
the user** — do not guess.

1. **Report folder** (mandatory) — the path to the friction report produced by
   `blindly-obedient-dev`, e.g. `.scratch/<doc>-review/`. It holds a `README.md`
   index and one numbered note per friction.
2. **Documentation source** (mandatory) — the local files to edit. If the doc
   was reviewed from a remote URL and no local source exists, ask the user for
   the **repo URL** and `git clone` it into a working directory first.

Note explicitly which inputs you were given vs. had to ask for.

## If the report is missing or partial

- **Absent or invalid path** — stop, explain, and tell the user to run
  `blindly-obedient-dev` first. Do **not** invoke it yourself: these skills are
  deliberately decoupled.
- **Partial** (review interrupted, no index, some notes missing) — proceed
  best-effort: process every note file that *is* present, and state in the PR
  that the report looked incomplete.
- **No doc-fixable frictions** — produce no PR; just report a short summary.

## The core rule — what you may and may not edit

For **every** friction note, decide from its `## Recommended fix`:

- The fix is fully achievable inside documentation files → **apply it.**
- The fix requires touching real application code → **do not touch anything.**
  Route it to the *"to handle in code"* section of the PR.

The `## Cause` section is only a hint, not the deciding factor — a friction with
no `## Cause` can still be code-caused, and vice versa.

### Files you may edit

- ✅ Prose doc pages, `README`, `CONTRIBUTING`, guides, and code snippets
  **embedded inside** those files.
- ✅ **Example / sample code shipped with the docs** — files the tutorial has
  the reader copy or run as teaching material (typically under `examples/`,
  `samples/`, or `docs/`). This is documentation material.
- ❌ Real application or library source code — files imported and run by the
  product itself.

When unsure whether a file is example material or real code, treat it as
**code** (the conservative choice) and route the friction to "to handle in
code". Heuristic for "example code": it lives in an `examples/`-style location
or under `docs/`, and the doc presents it as something to copy/run — it is not
imported by the application itself.

## Ambiguous fixes

- The `## Recommended fix` offers **A/B options** → pick the safest, most
  doc-only option, apply it, and justify the choice in the PR description.
- The fix is **too vague or absent** to apply with confidence → do not touch it;
  list it under *"not applied — needs a decision"* in the PR.
- **Never block interactively** per friction — the PR review is the checkpoint.

## Workflow

0. **Confirm inputs.** Report folder + documentation source (clone the repo if
   the doc has no local source — see "Required inputs").
1. **Read the report.** Read the `README.md` index, then every friction note.
   Build a list: for each, the page concerned, the recommended fix, and your
   classification — *doc-fixable*, *needs a decision*, or *to handle in code*.
2. **Create a branch.** `friction-fixer/<doc>-doc-fixes` off the current branch.
   Never commit directly to the default branch.
3. **Apply the doc-fixable frictions.** One at a time. Edit the doc file(s) per
   the recommended fix. **One commit per friction**, message referencing the
   note, e.g. `Fix friction 03 — wrong install flag in quickstart`.
4. **Sanity-check each edit (static only).** Confirm the edit is well-formed —
   links resolve, snippet syntax is valid, no contradiction introduced with the
   rest of the doc, document structure preserved. **Do not** rebuild or re-run
   the project: end-to-end validation means re-running `blindly-obedient-dev` on
   the corrected doc, which is the user's separate step.
5. **Open the PR** (see below). If there were no doc-fixable frictions, skip the
   PR and report a summary instead.

## The pull request

One PR for the whole report. Title: short summary of the doc fixes. The
description has four sections — always all four, even if a section is empty:

1. **Frictions fixed** — one row per applied fix: friction `NN` (link to the
   note), the doc file(s) changed, a one-line summary.
2. **A/B decisions** — every friction where the recommended fix offered options:
   which option you picked and why.
3. **Not applied — needs a decision** — frictions whose fix was too vague or
   ambiguous to apply safely. Quote the note; explain what is missing.
4. **To handle in code** — frictions whose real fix is in application code,
   out of scope for this skill. List them so they are not lost (they can feed a
   separate issue-tracking step).

## Scope discipline

- You are a **doc repair** tool, not a QA tool and not a code-fixing tool. Do
  not re-review the doc, do not second-guess the friction report — trust its
  findings and act on them.
- Apply the *recommended fix*; do not invent a different or larger change. If
  the recommended fix seems wrong, that is a "needs a decision" case — flag it,
  do not improvise.
- Every change must be reviewable: small, scoped commits, one per friction,
  each traceable back to its note.
- Mode-agnostic: friction notes share one format regardless of whether
  `blindly-obedient-dev` ran in Walkthrough or Mission mode.

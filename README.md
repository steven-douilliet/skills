# Skills For Me

## Quickstart (30-second setup)

1. Run the skills.sh installer:

```
npx skills@latest add steven-douilliet/skills
```

## Skills

- [blindly-obedient-dev](skills/blindly-obedient-dev/SKILL.md) — QA a project's documentation as a first-time developer using only the docs: either walk through a procedural doc (tutorial, README, install guide) literally, or attempt a concrete goal with the docs alone — and report every friction.

  Example usage:

  - **Walkthrough mode** — *"Review the getting-started tutorial at https://docs.example.com/tutorial — follow it step by step and report every friction."* The agent obeys each step literally and flags anything wrong, missing, or contradictory.
  - **Mission mode** — *"Use this framework to build a contact manager, relying only on the docs in ./docs (clone https://github.com/acme/framework if needed)."* The agent plays a first-time developer, navigates the docs to reach the goal, and reports wherever the docs fail.

  To let this skill verify a web UI in a real browser, set up the optional `chrome-devtools` MCP server — see [docs/chrome-devtools-mcp-setup.md](docs/chrome-devtools-mcp-setup.md) (Ubuntu install procedure).

- [friction-fixer](skills/friction-fixer/SKILL.md) — Consume a friction report produced by `blindly-obedient-dev` and apply the recommended fixes to the documentation only — never to application code — then open a pull request. Where `blindly-obedient-dev` diagnoses, this skill repairs.

  Example usage:

  - *"Apply the fixes from the doc review in `.scratch/tutorial-review/` — the docs live in ./docs."* The agent reads each friction note, edits the documentation per the recommended fix, opens a PR with one commit per friction, and lists any code-caused frictions separately for the user to handle.

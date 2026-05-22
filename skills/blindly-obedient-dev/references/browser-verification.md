# Verifying the real result in a browser

When the doc under review produces a **web UI or web app served on a URL**,
opening the URL is not enough — a page can return HTTP 200 and still be blank,
throw JavaScript errors, or silently fail to save. This file describes how to
drive a real browser to verify the *actual* result, using the
[`chrome-devtools` MCP server](https://github.com/ChromeDevTools/chrome-devtools-mcp).

This is an extension of golden rule 3 (*execute everything*): verifying the
rendered page **is** executing the doc to its end.

## Prerequisite — and what to do without it

This needs the `chrome-devtools` MCP server configured (tools named
`mcp__chrome-devtools__*`). It is an **optional** prerequisite.

**Setting it up is the user's job, not yours.** Do not attempt to install the
MCP server, Node.js, or Chrome — that means modifying the user's system, which
is out of scope for this skill. Just check whether the `mcp__chrome-devtools__*`
tools are available and act accordingly.

If those tools are **not available**, degrade gracefully:

- Fall back to the previous behaviour — `curl`/HTTP check that the URL responds.
- Continue the review; do not block on it.
- Record the gap in the report's *"what I could not verify"* section: the real
  rendered result (console errors, runtime behaviour) was **not** inspected.
- Tell the user that real browser verification is available if they set up the
  server, and point them to `docs/chrome-devtools-mcp-setup.md` — let them
  decide whether to install it.

## When to drive the browser

Whenever following the doc results in a web UI reachable at a URL (typically a
local dev server: `http://localhost:<port>`). This applies in **both** modes.
If the doc never produces a served web UI, skip this entirely.

The dev server must stay running while you drive the browser — start it as a
background process, then inspect, then clean up.

## The inspection workflow

For every page the doc tells you to open (or that the goal requires):

1. **Navigate** — `navigate_page` to the URL the doc gives.
2. **Wait for load** — `wait_for` the content the doc says should appear.
3. **Capture evidence** — `take_snapshot` (DOM, drives interactions) and
   `take_screenshot` (visual proof for the report).
4. **Read the console** — `list_console_messages`. Any `error` is a friction
   if it came from following the doc verbatim.
5. **Check the network** — `list_network_requests`. Failed requests (4xx/5xx,
   blocked, CORS) are frictions — a missing asset or a broken API call the doc
   never warned about.

A page that is blank, errors in the console, or has failed network requests —
**after the doc was followed literally** — is a friction. The doc led the
reader to a broken result: a step is missing, a snippet is wrong, or wiring
went undocumented.

## Mission mode — prove the goal functionally

In **Mission** mode the goal *is* the verification. Loading the page without
errors is not enough — reproduce the **minimal user journey that proves the
goal was reached**:

- Goal "build a contact manager" → fill the "add contact" form
  (`fill` / `fill_form`), submit (`click`), then confirm the contact actually
  appears (`take_snapshot` / `wait_for`).
- If the journey breaks (form does nothing, item never appears) → friction,
  even when the console and network are clean.

Only reproduce the journey **the doc describes or implies** for the goal. If
the doc is silent on a step the goal needs, that silence is itself the friction
(consistent with Mission-mode rules in `SKILL.md`).

In **Walkthrough** mode, stay at the inspection workflow above — only reproduce
an interaction if the doc explicitly tells the reader to perform it.

## Turning observations into frictions

No new friction format — use the standard note from `SKILL.md`. The browser
observation is the **evidence**:

- *What actually happens* — the observed behaviour, plus the exact console
  error / failed request, and a link to the screenshot.
- Save screenshots into the report folder, e.g.
  `.scratch/<doc>-review/screenshots/NN-<short>.png`, and link them from the
  friction note.

Severity follows the usual guide: a blank page or broken core journey is 🔴; a
console error that does not block is 🟠/🟡 depending on impact.

In the report's **journey** section, note which pages were verified for real in
a browser vs. only checked over HTTP.

## Cleanup

When the review is done, `close_page` any pages you opened and stop the
background dev server.

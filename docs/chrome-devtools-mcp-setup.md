# Setting up the chrome-devtools MCP server (Ubuntu)

The `blindly-obedient-dev` skill can drive a real browser to verify the actual
result of a doc that produces a web UI (see
[browser-verification.md](../skills/blindly-obedient-dev/references/browser-verification.md)).
That capability needs the [`chrome-devtools` MCP
server](https://github.com/ChromeDevTools/chrome-devtools-mcp). It is an
**optional** prerequisite — without it the skill degrades gracefully to an
HTTP-only check.

This guide covers the install on **Ubuntu**.

## 1. Node.js (LTS)

The server runs through `npx`. Check the version:

```bash
node --version   # must be >= 20 LTS (22 recommended)
```

If missing or too old:

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## 2. Chrome — required, not downloaded automatically

The server does **not** fetch Chrome itself. Google Chrome (or Chrome for
Testing) must already be installed — Ubuntu's `chromium` package is not
officially supported.

```bash
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
google-chrome --version   # verify
```

This also adds Google's apt repository, so Chrome updates with `apt upgrade`.

## 3. The MCP server

```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

- `--scope user` makes it available across all projects.
- `chrome-devtools-mcp@latest` keeps it on the newest version.
- `claude mcp list` confirms the entry.

The tools (`mcp__chrome-devtools__*`) appear after the session restarts. The
server launches Chrome on first use and stores profiles in
`~/.cache/chrome-devtools-mcp/`.

Equivalent manual config in `~/.claude.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## Display: desktop vs. headless

This is the key Ubuntu decision.

- **Ubuntu desktop (graphical environment)** — nothing extra; Chrome opens
  normally.
- **Ubuntu server / WSL / SSH with no display** — use **headless mode**. Add
  the flag when registering the server:

  ```bash
  claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest --headless --isolated
  ```

Even in headless mode Chrome's system libraries must be present. On a minimal
Ubuntu install they may be missing — if Chrome fails to launch:

```bash
sudo apt-get install -y libnss3 libatk-bridge2.0-0 libdrm2 libgbm1 \
  libasound2t64 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgtk-3-0
```

For containerised / sandboxed environments, pass Chrome arguments via
`--chrome-arg` (e.g. `--chrome-arg=--no-sandbox`).

## Verifying it works

After a session restart, `claude mcp list` should show `chrome-devtools`, and
the `mcp__chrome-devtools__*` tools become available to the
`blindly-obedient-dev` skill.

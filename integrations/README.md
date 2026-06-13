# Using this with other AI tools (Codex, Cursor, Gemini CLI)

The main `/aso-screenshot-prep` skill is built for **Claude Code**. These adapter files let you run the
**same workflow** in other agents as a slash command. They don't change anything about the Claude flow.

**How they work:** each adapter is a tiny command that tells the agent to read `SKILL.md` from your
local clone of this repo and follow it (running `compose.py` from the same repo). One brain
(`SKILL.md`), several front doors.

## Prerequisite (all tools)

1. Clone this repo somewhere on your machine and remember the path:
   ```bash
   git clone https://github.com/aleembhd/aso-screenshot-prep.git ~/aso-screenshot-prep
   ```
2. Install the one dependency:
   ```bash
   pip3 install Pillow      # or: pip3 install --break-system-packages Pillow
   ```

When the agent asks "where is the aso-screenshot-prep repo?", answer with that path (e.g.
`~/aso-screenshot-prep`).

---

## Codex CLI

Copy the adapter into Codex's prompts folder:
```bash
mkdir -p ~/.codex/prompts
cp ~/aso-screenshot-prep/integrations/codex/aso-screenshot-prep.md ~/.codex/prompts/
```
Start a new Codex session, then run: **`/aso-screenshot-prep`**
(Codex loads prompts from `~/.codex/prompts/*.md` on session start.)

---

## Cursor

Copy the adapter into Cursor's commands folder — global (all projects) or per-project:
```bash
# global:
mkdir -p ~/.cursor/commands
cp ~/aso-screenshot-prep/integrations/cursor/aso-screenshot-prep.md ~/.cursor/commands/

# or per-project (run inside the project):
mkdir -p .cursor/commands
cp ~/aso-screenshot-prep/integrations/cursor/aso-screenshot-prep.md .cursor/commands/
```
In Cursor's Agent input, type **`/`** and pick **aso-screenshot-prep** (Cursor 1.6+).

---

## Gemini CLI

Copy the TOML adapter into Gemini's commands folder — global or per-project:
```bash
# global:
mkdir -p ~/.gemini/commands
cp ~/aso-screenshot-prep/integrations/gemini/aso-screenshot-prep.toml ~/.gemini/commands/

# or per-project:
mkdir -p .gemini/commands
cp ~/aso-screenshot-prep/integrations/gemini/aso-screenshot-prep.toml .gemini/commands/
```
In Gemini CLI run `/commands reload` (or restart), then: **`/aso-screenshot-prep`**

---

## Notes

- The final image step is still done by **you** in ChatGPT (or any image model) — these adapters only
  produce the scaffolds + prompts, exactly like the Claude skill. No image API is ever called.
- If a tool can't find `compose.py`, it's because the repo path wasn't given — just tell the agent the
  folder you cloned into.
- Tested mechanisms (Jun 2026): Codex `~/.codex/prompts/`, Cursor `.cursor/commands/`, Gemini CLI
  `.gemini/commands/`. If a tool changes its command location, only the copy destination changes — the
  adapter content stays the same.

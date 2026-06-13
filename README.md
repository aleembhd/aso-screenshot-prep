# ASO Screenshot Prep — Play Store & App Store

A [Claude Code](https://claude.com/claude-code) **skill** that turns your raw app screenshots into
**titled, framed "scaffold" images** plus a **ready-to-paste prompt for each one** — so you generate
the final, polished store screenshots yourself in **ChatGPT** (or any image model). Supports **Google
Play Store** (Android frame), **Apple App Store** (iPhone frame), or **both at once** from the same
screenshots.

It does the parts an AI is genuinely good at — analyzing your app, writing high-converting ASO titles,
and laying out a clean device mockup — and **deliberately stops before image generation**. No image
API, no API keys, nothing to fail or bill you. You stay in control of the final render.

> **Why this exists:** automated image-generation pipelines are expensive and unreliable. This skill
> keeps the free, high-value 90% (titles + layout + tailored prompts) and lets you do the last 10%
> in the chat tool you already trust.

---

## What you get

For each store you pick, in an `aso-output/` folder inside your project:

```
aso-output/
├── play/                       ← Google Play Store set (Android frame, 1080×1920)
│   ├── scaffolds/
│   │   ├── 01-track.png        ← your screenshot, in an Android frame, with the ASO title on top
│   │   └── 02-organize.png
│   └── prompts/
│       ├── README.md           ← index: which scaffold ↔ which prompt ↔ which title
│       ├── 01-track.md         ← the exact prompt to paste into ChatGPT for 01
│       └── 02-organize.md
└── appstore/                   ← Apple App Store set (iPhone frame, 1290×2796) — only if chosen
    ├── scaffolds/ …
    └── prompts/ …
```

You then: **attach a scaffold image + paste its prompt into ChatGPT → download the polished
screenshot → upload to Play Console.**

---

## Setup from zero (first-timer friendly — follow top to bottom)

No prior experience needed. Every command goes into your **Terminal** app.

> **Open the Terminal:**
> - **macOS:** press `Cmd + Space`, type **Terminal**, press Enter.
> - **Windows:** install [WSL](https://learn.microsoft.com/windows/wsl/install) or use Git Bash, then open it.
> - **Linux:** open your **Terminal** app.
> You type a command, press **Enter**, and wait for it to finish before the next one.

### Step 1 — Install the things this needs (one time)

1. **Claude Code** — the app this skill runs inside. Install it from
   **https://claude.com/claude-code** and sign in.
2. **Python 3** — check if you already have it:
   ```bash
   python3 --version
   ```
   If you see a version number (e.g. `Python 3.12`), you're good. If it says "command not found",
   install it from **https://www.python.org/downloads/** (or `brew install python3` on macOS).
3. **Pillow** — the one library the script needs:
   ```bash
   pip3 install Pillow
   ```
   If that errors with "externally-managed-environment" (common on macOS), run:
   ```bash
   pip3 install --break-system-packages Pillow
   ```
4. **ChatGPT** (or any image-capable chat) — for the final image step. A normal account is fine.

### Step 2 — Install this skill (one time)

A Claude Code "skill" is just a folder. Installing it = copying this repo into a special folder Claude
looks in. Copy-paste this exactly:

```bash
git clone https://github.com/aleembhd/aso-screenshot-prep.git ~/.claude/skills/aso-screenshot-prep
```

> `~` means your home folder. So this lands in `~/.claude/skills/aso-screenshot-prep`, which Claude
> Code automatically reads. (Want it in just one project instead of everywhere? Clone into that
> project's `.claude/skills/aso-screenshot-prep` folder instead.)

### Step 3 — Turn it on

**Close Claude Code completely and open it again.** (It only notices new skills on restart.)

To confirm it worked, type `/` in Claude Code and look for **`aso-screenshot-prep`** in the list — or
just type `/aso-screenshot-prep`. If it's there, setup is done. ✅

> There is **no** `claude install-skill` command — the `git clone` in Step 2 *is* the install.

---

## Usage

1. **Take screenshots** of the app features you want to showcase (on a phone or emulator). Aim for
   ≥ 1080px wide, clean status bar, screens full of realistic content (not empty/login/settings).
2. Put them in a folder in your project, e.g. `screenshots/`.
3. In Claude Code, from your project, run:
   ```
   /aso-screenshot-prep
   ```
4. Follow the conversation:
   - Give it the **screenshots folder path**.
   - Tell it **which store(s)**: Play Store, App Store, or both.
   - It reads your project + screenshots and asks a few **follow-up questions**.
   - It proposes a **title for each screenshot** and asks you to **confirm or change** them.
   - On approval, it builds the **scaffolds** and writes a **prompt file per image** into
     `aso-output/play/` and/or `aso-output/appstore/`.
5. **Generate the finals in ChatGPT:** new chat → attach `aso-output/play/scaffolds/01-*.png` → paste
   the matching `aso-output/play/prompts/01-*.md` → download. (For App Store, use the `appstore/`
   folders.) Do #1 first; for the rest, also attach your finished #1 so the set stays visually consistent.
6. **(Optional) Normalize the set** to one size — see below.
7. **Upload:** Play Console → Main store listing → Phone screenshots (2–8, in order), and/or App Store
   Connect → your app → Screenshots (up to 10).

---

## Optional: resize finals to a uniform size

ChatGPT's portrait images are ~1024×1536 (already valid). To normalize a set, set the target for the
store and point it at the folder where you saved your finished images:

- **Play Store:** `TARGET_W=1080 TARGET_H=1920`
- **App Store (iPhone 6.7"):** `TARGET_W=1290 TARGET_H=2796`

**macOS:**
```bash
TARGET_W=1080 && TARGET_H=1920          # ← change per store
SRC="aso-output/play/finished"          # ← folder where you saved ChatGPT downloads
mkdir -p aso-output/final
for INPUT in "$SRC"/*; do
  [ -e "$INPUT" ] || continue
  OUT="aso-output/final/$(basename "${INPUT%.*}").png"
  cp "$INPUT" "$OUT"
  W=$(sips -g pixelWidth  "$OUT" | tail -1 | awk '{print $2}')
  H=$(sips -g pixelHeight "$OUT" | tail -1 | awk '{print $2}')
  CW=$(python3 -c "print(min($W, round($H*$TARGET_W/$TARGET_H)))")
  CH=$(python3 -c "print(min($H, round($W*$TARGET_H/$TARGET_W)))")
  sips --cropToHeightWidth $CH $CW "$OUT" >/dev/null
  sips -z $TARGET_H $TARGET_W "$OUT" >/dev/null
done
```

**Linux (ImageMagick):**
```bash
for f in aso-output/play/finished/*; do
  convert "$f" -resize 1080x1920^ -gravity center -extent 1080x1920 \
    "aso-output/final/$(basename "${f%.*}").png"
done
```

---

## Store screenshot specs (what the output targets)

**Google Play:** JPEG or 24-bit PNG (no transparency); each side 320–3840px; longest side ≤ 2× shortest
(up to 2:1 portrait); 2–8 phone screenshots; first 3–4 are most-seen. Default output **1080×1920**.

**Apple App Store:** exact sizes only — iPhone 6.7" **1290×2796**, 6.5" **1242×2688**, 6.9"
**1320×2868**; up to 10 per size. Default output **1290×2796**.

---

## How it works (under the hood)

| Step | Tool | Cost |
|------|------|------|
| Analyze app + write titles | Claude (the skill's instructions) | your normal Claude usage |
| Stamp title + phone frame onto screenshot | `compose.py` (Pillow, local) | free |
| Write a tailored prompt per image | Claude | your normal Claude usage |
| Generate the final polished screenshot | **you, in ChatGPT** | your ChatGPT plan |

The repo contains:
- `SKILL.md` — the instructions Claude follows
- `compose.py` — builds the scaffold (title + phone frame + screenshot); `--platform android|ios`
- `generate_frame.py` — regenerates the Android + iPhone device frame assets
- `assets/` — the bundled font (Archivo Black, OFL) and both device frames

---

## Use it in Codex, Cursor, or Gemini CLI too

The native skill is for Claude Code, but **the same `/aso-screenshot-prep` command works in Codex CLI,
Cursor, and Gemini CLI** via ready-made adapter files in **[`integrations/`](integrations/)**. They
reuse the same `SKILL.md` brain and `compose.py` — nothing about the Claude flow changes.

Quick version (full per-tool steps in [`integrations/README.md`](integrations/README.md)):

```bash
# 1. clone the repo somewhere and install Pillow
git clone https://github.com/aleembhd/aso-screenshot-prep.git ~/aso-screenshot-prep
pip3 install Pillow

# 2. copy the adapter for your tool, then run /aso-screenshot-prep in it:
cp ~/aso-screenshot-prep/integrations/codex/aso-screenshot-prep.md   ~/.codex/prompts/        # Codex
cp ~/aso-screenshot-prep/integrations/cursor/aso-screenshot-prep.md  ~/.cursor/commands/      # Cursor
cp ~/aso-screenshot-prep/integrations/gemini/aso-screenshot-prep.toml ~/.gemini/commands/     # Gemini CLI
```

When the agent asks where the repo is, give it the clone path (e.g. `~/aso-screenshot-prep`). The
`compose.py` script and the prompts are plain Python + text, so they're portable to any assistant —
these adapters just make it a one-word command in each tool.

---

## Customizing

- **Background colour / title:** the skill picks these with you, but you can re-run `compose.py`
  manually with different `--bg`, `--verb`, `--desc` to regenerate any scaffold.
- **Different font:** drop a `.ttf`/`.otf` into `assets/` and update `FONT_PATH` in `compose.py`.
- **Platform:** the skill asks you to pick Play Store, App Store, or both — it never assumes. Under the
  hood `compose.py --platform android|ios` swaps the device frame; both frames ship in `assets/`.

---

## License

MIT for the code. The bundled **Archivo Black** font is licensed under the
[SIL Open Font License](https://openfontlicense.org/).

*Built with [Claude Code](https://claude.com/claude-code).*

---
description: Prepare ASO store screenshots — titles + framed scaffolds + per-image prompts (no image API)
---

You are running the **ASO Screenshot Prep** workflow.

Goal: turn the user's raw app screenshots into (1) titled, framed "scaffold" images and (2) a
ready-to-paste image prompt per screenshot, for Google Play Store and/or Apple App Store. You do NOT
generate the final images, and you NEVER call any image-generation API or tool.

Steps:
1. Locate the `aso-screenshot-prep` repository on this machine (it contains `SKILL.md`, `compose.py`,
   and `assets/`). If you don't know its path, ask the user where they cloned it. Treat that absolute
   path as `$SKILL_DIR`.
2. Read `$SKILL_DIR/SKILL.md` and follow its phases EXACTLY:
   - ask for the screenshots folder path,
   - ask which store(s): Play Store, App Store, or both (never assume both),
   - analyze the project + screenshots, ask a short round of follow-up questions,
   - propose a title per screenshot and get the user's confirmation/changes,
   - run `python3 "$SKILL_DIR/compose.py"` (with `--platform android` and/or `--platform ios`) to build
     the scaffolds into `aso-output/`,
   - write one tailored prompt file per image into `aso-output/<store>/prompts/`.
3. Stop after scaffolds + prompts. Tell the user to finish each image in ChatGPT (attach the scaffold,
   paste its prompt; do image 1 first, then attach it as a style reference for the rest).

Hard rule: the ONLY program you run is `compose.py` (local, free). Never call any image-generation
tool/API. If Python's Pillow is missing, tell the user to run `pip3 install Pillow`.

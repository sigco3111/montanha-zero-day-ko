# Montanha: Zero Day — Korean Edition (unofficial)

*He went to rescue Gle. Now she's coming for him.*

An unofficial Korean edition of **Montanha: Zero Day**, the cyberpunk action platformer built with vanilla JS and a canvas. The game code, art and sound are exactly the original's; this repository only **overwrites the on-screen text and dialogue with a Korean dictionary**.

| | |
|---|---|
| Play (deployed) | https://sigco3111.github.io/montanha-zero-day-ko/ |
| Original | **tiagovilasboas/montanha-zero-day** — https://github.com/tiagovilasboas/montanha-zero-day |
| Original demo (Portuguese) | https://tiagovilasboas.github.io/montanha-zero-day/ |
| This repository | https://github.com/sigco3111/montanha-zero-day-ko |
| Glossary (fixed terms) | [docs/glossary.md](docs/glossary.md) |

## About the game

**Neo-Sampa, 2099.** The invading AI **LEGIÃO NULL** has taken the planet's network. Its general **TITAN** has released malware drones into the streets, and **Gle** has been kidnapped and locked in an encrypted capsule.

- **Stage 1 — Cecapão Rooftops.** You play **Montanha**: jetpack, the **H4X** hacking watch and the robot **BYTE**, running across the rooftops. At the end he finds Gle in her capsule, but TITAN's claw snatches him away and Gle breaks free.
- **Stages 2 and 3 — Sublevel 404: Sunken Server and Kernel Panic: the Core.** Now you play **Gle**, with the golden gauntlet, the light boots and a pink BYTE, going after Montanha. The Core adds pulse beams that switch on and off in rhythm, a climb over lasers, a turret gauntlet and the boss **TITAN** with a firewall phase.
- **Ending.** After the boss, Gle takes TITAN's key and opens Montanha's cell deep in the Core.

Game elements: three kinds of terminal hacking puzzles (sequence, binary, node grid), turrets you can turn to your side, an EMP pulse, a landscape-only UI with touch controls, and a per-stage soundtrack.

## What the Korean edition adds

| Item | Detail |
|---|---|
| Dictionary entries | `KO.ui` **111** (every UI string) and `KO.lines` **57** (56 dialogue and hint lines plus the equipment label `BOTAS`). **168 entries in total** |
| Language switch | One button on the title screen cycles **Korean → Portuguese → English → Korean** |
| Button label | The button shows the *next* language (Korean shows `Português`, Portuguese shows `English`, English shows `한국어`) |
| Default language | With no saved choice, the game starts in **Korean when the browser language is Korean**; otherwise the original rule applies (Brazil timezone plus Portuguese → Portuguese, everything else → English) |
| Saved choice | `localStorage` key `mzd-lang` |
| Strings missing from the dictionary | Fall back to the English original; the game keeps running |
| Fonts | The pixel webfonts have no Korean glyphs, so Korean is drawn with the system Korean font (see "Removed features") |
| Text baked into art | Lettering inside images (logo, signs) is original art and stays as it is (all rights reserved, not editable) |

## How the translation is wired

The original's language system is used as-is. The English source (`UI.en`) and the Portuguese source (`LINES`) are **left untouched**; a Korean dictionary file is added and only the values are overridden.

- **`js/i18n.ko.js`** — the Korean dictionary. `KO.ui` (111 keys, the same keys as the original `UI.en`) plus `KO.lines` (57 entries whose keys are the Portuguese original sentences). Dialogue is replaced sentence by sentence using the original as the key, so a changed line simply falls back to the original.
- **`js/i18n.js`** — ten patch points that attach the `ko` language: `import { KO }`, `UI.ko = KO.ui`, the Korean table for `LINES`, the `ko` branch in `tr()`, `browserIsKorean()`, the saved-choice handling (`mzd-lang`), the `ko` branch of `detectLang()`, `<html lang="ko">` in `applyDom()`, the three-way `toggleLang()` and the language-button label.
- **`tools/ko_build.py`** — the build script that fetches the original code and re-applies those patches.
- **`docs/glossary.md`** — fixed terms for names, gear and puzzles, plus the style rules (short noun buttons, the original's friendly informal tone, `BYTE`/`TITAN`/`EP`/`XP`/`LV` kept as written, one original sentence always maps to the same Korean).

## Images and sound are loaded from the original Pages

The original author holds **all rights to the artwork, characters, names and story** (all rights reserved). So this repository **does not copy a single original image, icon or audio file**.

- `ASSET_BASE` in `js/assets.js` points at `https://tiagovilasboas.github.io/montanha-zero-day/`, and while the game runs it pulls `assets/*.webp` and the animation metadata `assets/anims.json` straight from there.
- Neither the repository nor the deployed output contains any rights-reserved file. Only the MIT-licensed code is here.
- As of 2026-11 the original Pages sends `access-control-allow-origin: *`, so both the cross-origin `fetch(anims.json)` and the `<img>` loads work. All 33 asset URLs answered 200 to a HEAD check (`docs/build-report.txt`).
- The canvas never reads pixels back (no `getImageData`), so cross-origin images do not taint it.
- **Limitation**: if the original site goes away or moves its asset paths, the game keeps its logic but **loses the pictures**. Fixing that is a one-line `ASSET_BASE` change.
- **Sound** is synthesized live in the browser with WebAudio by the original code. There are no audio files, so there is nothing to load remotely.

## Removed features and why

- **Google Fonts links** (`fonts.googleapis.com` / `fonts.gstatic.com`) — removed so the page does not call an outside server. The cost is that the original pixel webfonts are no longer downloaded, so text falls through to the next family in the CSS and canvas stacks (for Korean, the system Korean font).
- **Service worker / PWA offline cache** — `sw.js`, `manifest.webmanifest` and `icons/` are not shipped, and the registration call in `js/main.js` is switched off. An offline cache would replicate the original's rights-reserved assets onto this repository's origin, which conflicts with the rights handling above. The "install app" button therefore never appears.
- **Analytics, statistics, telemetry** — the original has none, so there was nothing to strip; this edition sends nothing either.
- **Persistence** lives only in browser `localStorage` (`montanha-zero-day-v1`).

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | `←` `→` or `A` `D` | direction pad on the left |
| Jump | `Z`, `Space`, `↑`, `W` | `JUMP` |
| Hover (jetpack / light boots) | hold jump in the air | hold `JUMP` |
| Shoot | `X` or `J` (hold to charge, release for a piercing shot) | `SHOOT` |
| Hack | `C` or `K` | `HACK` |
| Pause | `Esc` or `P` | `II`, top right |
| Advance dialogue | `Enter`, jump or shoot | tap the buttons |

Hacking near a red turret flips it to your side, at a yellow terminal opens its puzzle, and away from everything fires an EMP pulse. On phones the game is landscape-only: held upright, it shows a "rotate your phone" screen and stays paused.

## Run it locally

It is a static site with no build step. Opening it over `file://` blocks ES modules and `fetch`, so serve the folder:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

The art comes from the original Pages, so an internet connection is required.

## Rebuilding

```bash
python3 tools/ko_build.py
```

It fetches only the code files from the original repository (currently upstream commit `d11866be57ff770ce88680eb87c73458764604f6`, 26 files), re-applies the Korean patches and records patch and asset results in `docs/build-report.txt`. A patch that no longer applies is written as `MISS` in that report.

`index.html` is the file the original generates with `build.py`, taken as-is with the external links removed, so this repository never runs the original `build.py` (which needs Pillow).

## Checked / not checked

**Checked**

- On the deployed page, the title screen (start, sound and language buttons, tagline, key hint) displays in Korean (verified 2026-11-15). In-game dialogue and the opening cutscene were not seen in this check.
- Clicking the language button really cycles **Korean → Portuguese → English → Korean**, and the button label changes to the next language name.
- Dictionary size: `KO.ui` 111 entries and `KO.lines` 57 entries, counted in `js/i18n.ko.js`.
- All 33 original asset URLs answer 200, CORS is `*`, there are no root-absolute references and no local asset paths (`docs/build-report.txt`).

**Not checked**

- **Finishing the boss fight and the ending.** The action is canvas-driven, so automated input could not carry play to the end; the late stage-2/3 dialogue and the boss firewall hints were never seen on screen.
- **Touch input on a real phone.** The touch pad, rotation screen and full-screen button were verified in code only.
- **The Esc pause hint overlapping.** The keyboard hint can sit partly over the dialogue box, so on small screens the hint may overlap the dialogue text.

## Credits

- **Original game, code, story and art**: **Tiago Vilas Boas** — https://github.com/tiagovilasboas/montanha-zero-day
- **Art production**: made with **Artlist** from the author's prompts and reference photos — Nano Banana 2 for images, Seedance 1.5 and 2.0 for animation clips.
- **Development help**: the original author credits Claude Opus 5.5 (Cowork).
- **Music and sound effects**: synthesized live in the browser with WebAudio; there are no audio files.
- **Libraries used**: none. The original is vanilla JS plus canvas with no package manager and no bundler (`package.json`, `node_modules` and bundlers are absent), and this repository is the same. The external font links were removed too, so there is no font-licence dependency.
- **Korean translation and build**: sigco3111
- In game, the title screen and the ending show "made by Tiago Vilas Boas", and the ending credits screen lists game, art, music, tooling and support entries.

## Licence and attribution

- **Code**: MIT License, Copyright (c) 2026 Tiago Vilas Boas. The full text is kept verbatim in [`LICENSE`](LICENSE).
- **Artwork, characters, names and story**: `assets/`, `icons/`, `docs/screenshots/`, and Montanha, Gle and BYTE themselves are © 2026 Tiago Vilas Boas, **all rights reserved**. This repository neither copies nor redistributes them; it only loads them from the original Pages.
- **Translation text**: distributed as data appended to MIT-licensed code; rights in the original dialogue and names remain with the original author.
- **Takedown**: if the original author asks for it, this repository and the deployed page come down immediately.

This is an unofficial fan translation, unaffiliated with the original author.

## Changes other than translation

1. `js/assets.js`: added the `ASSET_BASE` constant and pointed image and `anims.json` paths at the original Pages.
2. `js/i18n.js`: added the `ko` language (the ten patch points above).
3. `js/main.js`: removed the service-worker registration call.
4. `css/style.css`: Korean fallbacks in `--font-display`/`--font-body`, plus an `html[lang="ko"]` block.
5. `js/*.js`: Korean fallbacks in the canvas font strings (`ctx.font`), one file.
6. `index.html`: dropped the Google Fonts links, the manifest link and the icon links.
7. Not taken from the original: `build.py`, `game.html`, `sw.js`, `manifest.webmanifest`, `icons/`, `assets/`, `docs/screenshots/`, `README.pt-BR.md`, the dev.to articles and the art-generation tools.

## Verification log

- 2026-11-14 build: 26 code files taken from upstream commit `d11866be57ff770ce88680eb87c73458764604f6`; 18 patch checks `OK`; the icon-link removal (`drop-icon-links`) was logged as `MISS(2/1)` (2 matches against 1 expected), and the report's `FAILED PATCHES` count is 0.
- 2026-11-14 asset check: 33 URLs HEAD-checked, 0 problems, `access-control-allow-origin: *` present; `sw.js`, `manifest.webmanifest`, `build.py` and `game.html` confirmed absent from the repository.
- 2026-11-15 deployed page: Korean title screen displayed, three-way language cycle (ko→pt→en→ko) working.
- 2026-11-15 dictionary count: `KO.ui` 111 entries, `KO.lines` 57 entries.

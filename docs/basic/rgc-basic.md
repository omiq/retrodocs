# RGC BASIC — overview

**RGC BASIC** (Retro Game Coders BASIC) is a **modern, cross-platform BASIC interpreter** written in C. It takes inspiration from **Commodore BASIC V2** (line numbers, `POKE`/`PEEK` idioms, PETSCII) but adds structured syntax, user-defined functions, real file I/O, graphics, and more — so you can use `GOTO` when you want it, or write in a more structured style when you do not.

You can run it in **five** complementary ways:

| Where | What you get |
|--------|----------------|
| **[Web IDE (WASM)](rgc-basic/web-ide.md)** | Same interpreter in the browser — instant share, no install |
| **Terminal** (`basic`) | Scripting, pipes, `ARG$` / `SYSTEM` / `EXEC$`, PETSCII→ANSI |
| **Graphics** (`basic-gfx`) | [Raylib](https://www.raylib.com/) window — 40×25 PETSCII, `POKE` screen RAM, AMOS-class 2-D primitives (RECT/CIRCLE/ELLIPSE/TRIANGLE/POLYGON/FLOODFILL/DRAWTEXT + all fills), PNG sprites with rotation and multi-instance stamping, array-driven `TILEMAP DRAW`, 1bpp blitter (`IMAGE NEW/LOAD/GRAB/COPY/SAVE`), `KEYDOWN`/`KEYPRESS`, atomic `VSYNC` frame commit, scroll, gamepad |
| **Windows / macOS / Linux** | [Prebuilt binaries](https://github.com/omiq/rgc-basic/releases) for all three |

This documentation set includes a **full [language reference](rgc-basic/language.md)** (statements, intrinsics, meta directives, system variables, host matrix), deep **[Terminal & PETSCII](rgc-basic/terminal-petscii.md)** and **[Web IDE](rgc-basic/web-ide.md)** pages, and a **complete [graphics](rgc-basic/graphics-raylib.md)** chapter (Graphics 1.0 — bitmap primitives, PNG sprites with rotation and stamping, tilemaps, 1bpp blitter with PNG/BMP I/O, VSYNC pipeline, keyboard intrinsics, scroll, gamepad) — so routine API detail lives here, not only in the [GitHub README](https://github.com/omiq/rgc-basic/blob/main/README.md). The repo remains the **source of truth** for every edge case and version note; we link to it where it helps.

## Quick links

| Topic | Page |
|--------|------|
| **Brand new? Start here** — install, hello world, frame loop, sprites in 30 lines, common gotchas | [Getting started](rgc-basic/getting-started.md) |
| Download, build, releases, macOS Gatekeeper | [Install & platforms](rgc-basic/install.md) |
| Full statement & function reference, operators, `TI` / `ST`, reserved words, recently added detailed reference | [Language reference](rgc-basic/language.md) |
| CLI flags, PETSCII/ANSI, terminal scripting, `COLOR` / `LOCATE` | [Terminal & PETSCII](rgc-basic/terminal-petscii.md) |
| `basic-gfx`, screen modes 0..4 (text / 1bpp / RGBA / indexed / hi-RGBA), bitmap primitives, **sprites (full API + STAMP)**, tilemaps, 1bpp + RGBA blitter (`IMAGE NEW`/`CREATE`/`BLEND`/`DRAW`), HUD `OVERLAY`, `LOADSCREEN`, palette load/save, `KEYDOWN`/`VSYNC`, scroll zones, multi-buffer `SCREEN`, mouse, gamepad, sound, music | [Graphics (Raylib)](rgc-basic/graphics-raylib.md) |
| RGC IDE, `HTTP$`, `PLATFORM$()`, WASM vs native | [Web IDE (WASM)](rgc-basic/web-ide.md) |
| `HTTP$` / `HTTPFETCH` / `BUFFER*` slot-based file-backed HTTP, binary I/O (`PUTBYTE` / `GETBYTE` / `EOF`), CORS notes | [Network & buffers](rgc-basic/network-and-buffers.md) |
| `MAPLOAD` / `MAPSAVE` JSON tilemaps, BASIC-builder vs JSON | [Level authoring](rgc-basic/level-authoring.md) |
| Object types (loot, weapons, spells, traps, McGuffins), enemy AI presets, attack patterns, boss phases — Zelda-class RPG vocabulary | [RPG tutorial](rgc-basic/rpg-tutorial.md) |

## Project links

- **Repository:** [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic)
- **Releases:** [github.com/omiq/rgc-basic/releases](https://github.com/omiq/rgc-basic/releases) (stable) and [**nightly**](https://github.com/omiq/rgc-basic/releases/tag/nightly) (automated builds from `main`)
- **Examples:** [`examples/`](https://github.com/omiq/rgc-basic/tree/main/examples) in the repo — demos for trek, PETSCII viewers, gfx games, scripting, etc. Many of the same **`*.bas`** files are bundled in the **[Web IDE](rgc-basic/web-ide.md)** RGC BASIC preset — open directly, e.g. [petscii-data.bas](https://ide.retrogamecoders.com/?file=petscii-data.bas&platform=rgc-basic), [trek.bas](https://ide.retrogamecoders.com/?file=trek.bas&platform=rgc-basic), [gfx_game_shell.bas](https://ide.retrogamecoders.com/?file=gfx_game_shell.bas&platform=rgc-basic).

## How this relates to other docs here

- **[Commodore BASIC V2](commodore-basic-v2.md)** — the ROM dialect on real C64/VIC/PET hardware in emulators inside the IDE.
- **RGC BASIC** — its *own* interpreter and language; not a C64 emulator, but familiar syntax and PETSCII-oriented features.

When you outgrow “toy” snippets and want **real files, JSON, shell glue, or Raylib games**, RGC BASIC is aimed at that — locally or in the IDE.

## Suggested learning path

1. Read **[Getting started](rgc-basic/getting-started.md)** — pick a runtime, run hello world, see the frame-loop pattern.
2. Open **[Web IDE](rgc-basic/web-ide.md)** or install **[binaries](rgc-basic/install.md)**.
3. Skim **[Language reference](rgc-basic/language.md)** for keywords you need; revisit the *Recently added — detailed reference* appendix for `BUFFER*`, `OVERLAY`, `IMAGE CREATE/BLEND/DRAW`, `LOADSCREEN`, `MAPSAVE`, `PUTBYTE`/`GETBYTE`.
4. For colourful terminal output or pipes, read **[Terminal & PETSCII](rgc-basic/terminal-petscii.md)**.
5. For games, sprites, sound, palette tricks, scroll zones — read **[Graphics (Raylib)](rgc-basic/graphics-raylib.md)** and run the repo `examples/gfx_*.bas` / `tutorial_gfx_*.bas` files. Open the same basenames in the **[Web IDE](rgc-basic/web-ide.md)** ([example](https://ide.retrogamecoders.com/?file=gfx_poke_demo.bas&platform=rgc-basic)).
6. For HTTP, binaries, large responses, level loading — read **[Network & buffers](rgc-basic/network-and-buffers.md)** and **[Level authoring](rgc-basic/level-authoring.md)**.

---

*Documentation aligned with RGC BASIC **1.9.0** (2026-04-18, "Graphics 1.0" milestone). Next major is **2.0** when sound lands. For exact behaviour per release, see [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md) and the [1.9.0 announcement](https://github.com/omiq/rgc-basic/blob/main/docs/release-graphics-1.0.html).*

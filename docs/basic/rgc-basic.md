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
| Download, build, releases, macOS Gatekeeper | [Install & platforms](rgc-basic/install.md) |
| Full statement & function reference, operators, `TI`/`ST`, reserved words | [Language reference](rgc-basic/language.md) |
| CLI flags, PETSCII/ANSI, terminal scripting, `COLOR` / `LOCATE` | [Terminal & PETSCII](rgc-basic/terminal-petscii.md) |
| `basic-gfx`, virtual memory, bitmap primitives + fills, **sprites (full API + STAMP)**, tilemaps, blitter surfaces, `KEYDOWN`/`VSYNC`, `INKEY$`, `TI`, scroll, gamepad | [Graphics (Raylib)](rgc-basic/graphics-raylib.md) |
| RGC IDE, **`HTTP$`**, **`PLATFORM$()`**, WASM vs native | [Web IDE (WASM)](rgc-basic/web-ide.md) |

## Project links

- **Repository:** [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic)
- **Releases:** [github.com/omiq/rgc-basic/releases](https://github.com/omiq/rgc-basic/releases) (stable) and [**nightly**](https://github.com/omiq/rgc-basic/releases/tag/nightly) (automated builds from `main`)
- **Examples:** [`examples/`](https://github.com/omiq/rgc-basic/tree/main/examples) in the repo — demos for trek, PETSCII viewers, gfx games, scripting, etc. Many of the same **`*.bas`** files are bundled in the **[Web IDE](rgc-basic/web-ide.md)** RGC BASIC preset — open directly, e.g. [petscii-data.bas](https://ide.retrogamecoders.com/?file=petscii-data.bas&platform=rgc-basic), [trek.bas](https://ide.retrogamecoders.com/?file=trek.bas&platform=rgc-basic), [gfx_game_shell.bas](https://ide.retrogamecoders.com/?file=gfx_game_shell.bas&platform=rgc-basic).

## How this relates to other docs here

- **[Commodore BASIC V2](commodore-basic-v2.md)** — the ROM dialect on real C64/VIC/PET hardware in emulators inside the IDE.
- **RGC BASIC** — its *own* interpreter and language; not a C64 emulator, but familiar syntax and PETSCII-oriented features.

When you outgrow “toy” snippets and want **real files, JSON, shell glue, or Raylib games**, RGC BASIC is aimed at that — locally or in the IDE.

## Suggested learning path

1. Open **[Web IDE](rgc-basic/web-ide.md)** or install **[binaries](rgc-basic/install.md)**.
2. Run a tiny `PRINT` / `FOR` program, then skim **[Language reference](rgc-basic/language.md)** for keywords you need.
3. For colourful terminal output or pipes, read **[Terminal & PETSCII](rgc-basic/terminal-petscii.md)**.
4. For games, sprites, and `.seq` art, read **[Graphics (Raylib)](rgc-basic/graphics-raylib.md)** (full sprite/bitmap API) and run the repo `examples/gfx_*.bas` / `tutorial_gfx_*.bas` files — or open the same basenames in the **[Web IDE](rgc-basic/web-ide.md)** ([example](https://ide.retrogamecoders.com/?file=gfx_poke_demo.bas&platform=rgc-basic)).

---

*Documentation aligned with RGC BASIC **Graphics 1.0** (unreleased post-v1.8; full feature set landed in the Unreleased section of the CHANGELOG). For exact behaviour per release, see [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md).*

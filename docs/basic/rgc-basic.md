# RGC BASIC — overview

**RGC BASIC** (Retro Game Coders BASIC) is a **modern, cross-platform BASIC interpreter** written in C. It takes inspiration from **Commodore BASIC V2** (line numbers, `POKE`/`PEEK` idioms, PETSCII) but adds structured syntax, user-defined functions, real file I/O, graphics, and more — so you can use `GOTO` when you want it, or write in a more structured style when you do not.

You can run it in **five** complementary ways:

| Where | What you get |
|--------|----------------|
| **[Web IDE (WASM)](rgc-basic/web-ide.md)** | Same interpreter in the browser — instant share, no install |
| **Terminal** (`basic`) | Scripting, pipes, `ARG$` / `SYSTEM` / `EXEC$`, PETSCII→ANSI |
| **Graphics** (`basic-gfx`) | [Raylib](https://www.raylib.com/) window — 40×25 PETSCII, `POKE` screen RAM, sprites, gamepad |
| **Windows / macOS / Linux** | [Prebuilt binaries](https://github.com/omiq/rgc-basic/releases) for all three |

This documentation is the **friendly entry point**: concepts, workflows, and tables so you are not forced to read only the [GitHub README](https://github.com/omiq/rgc-basic/blob/main/README.md), [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md), or example sources. The repo remains the **source of truth** for every edge case; we link to it where it helps.

## Quick links

| Topic | Page |
|--------|------|
| Download, build, releases, macOS Gatekeeper | [Install & platforms](rgc-basic/install.md) |
| Statements, functions, variables, `#INCLUDE`, `#OPTION` | [Language reference](rgc-basic/language.md) |
| CLI flags, PETSCII/ANSI, terminal scripting, `COLOR` / `LOCATE` | [Terminal & PETSCII](rgc-basic/terminal-petscii.md) |
| `basic-gfx`, virtual memory, bitmap, sprites, `INKEY$`, `TI` | [Graphics (Raylib)](rgc-basic/graphics-raylib.md) |
| RGC IDE integration, URLs, keyboard focus | [Web IDE (WASM)](rgc-basic/web-ide.md) |

## Project links

- **Repository:** [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic)
- **Releases:** [github.com/omiq/rgc-basic/releases](https://github.com/omiq/rgc-basic/releases) (stable) and [**nightly**](https://github.com/omiq/rgc-basic/releases/tag/nightly) (automated builds from `main`)
- **Examples:** [`examples/`](https://github.com/omiq/rgc-basic/tree/main/examples) in the repo — demos for trek, PETSCII viewers, gfx games, scripting, etc.

## How this relates to other docs here

- **[Commodore BASIC V2](commodore-basic-v2.md)** — the ROM dialect on real C64/VIC/PET hardware in emulators inside the IDE.
- **RGC BASIC** — its *own* interpreter and language; not a C64 emulator, but familiar syntax and PETSCII-oriented features.

When you outgrow “toy” snippets and want **real files, JSON, shell glue, or Raylib games**, RGC BASIC is aimed at that — locally or in the IDE.

## Suggested learning path

1. Open **[Web IDE](rgc-basic/web-ide.md)** or install **[binaries](rgc-basic/install.md)**.
2. Run a tiny `PRINT` / `FOR` program, then skim **[Language reference](rgc-basic/language.md)** for keywords you need.
3. For colourful terminal output or pipes, read **[Terminal & PETSCII](rgc-basic/terminal-petscii.md)**.
4. For games and `.seq` art, move to **[Graphics (Raylib)](rgc-basic/graphics-raylib.md)** and the repo `examples/gfx_*.bas` files.

---

*Documentation aligned with RGC BASIC **v1.5.x**-class features described in the upstream README; for exact behaviour per release, see [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md).*

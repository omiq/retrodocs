---
title: Getting started with the IDE
description: Overview of the Retro Game Coders web IDE — workflow, shortcuts, and platforms.
---

# Getting started with the IDE

The **[Retro Game Coders IDE](https://ide.retrogamecoders.com/)** is a browser-based environment for 8-bit development.

!!! note "Living product"
    The IDE gains features over time. This page summarizes behaviour described in the public help and common workflows; your running version may include **more** options (platforms, compilers, UI). When in doubt, use the in-app help and the **platform / language** dropdowns.

## Overview

- Pick a **platform** (C64, VIC-20, NES, …) and a **language / toolchain**.
- Edit source in the **editor**; build and run in the **emulator** (or compile-only flows where applicable).
- Use **auto-compile** for fast feedback, or turn it off for long editing sessions and build manually when ready.

## What’s avilable

The RGC IDE is contantly being developed or improved with things such as:

- Extra **platforms** (e.g. VIC-20, BBC Micro, enhanced C64 BASIC paths).
- **Auto-compile** toggle with clear on/off status.
- **Manual build** when auto-compile is off.
- Stronger **emulator controls** (reset, pause, resume) where the core supports them.
- **Keyboard shortcuts** for compile, debug, and editor actions (see below).

Exact availability depends on **platform + toolchain**.

## Supported languages & compilers (summary)

| Area | Examples in the IDE |
|------|---------------------|
| **C** | cc65, z88dk, CMOC, and platform-specific C runtimes |
| **BASIC** | Commodore BASIC (C64, VIC, PET), BBC BASIC, Color BASIC, AppleSoft, ugBASIC, batari BASIC, FastBasic, **XC-BASIC 3**, **[RGC BASIC](../basic/rgc-basic.md)** (WASM), … |
| **Assembly** | 6502 family: DASM, KickAss, ACME, cc65’s assembler; **Z80** / **6809** / **ARM** via dedicated tool modules |
| **Other** | Verilog flows, remote/external tools, Markdown/BASIC-only “notebook” style platforms |

See also the dedicated docs: **[Commodore BASIC v2](../basic/commodore-basic-v2.md)**, **[XC-BASIC 3](../basic/xc-basic-3.md)**, **[RGC BASIC](../basic/rgc-basic.md)**, **[6502 assembly](../assembly/6502.md)**, **[Z80 assembly](../assembly/z80.md)**, **[cc65 / C](../c/cc65.md)**.

## Auto-compile

| Action | How |
|--------|-----|
| Toggle auto-compile | Lightning (⚡) control, or **Ctrl+Alt+C** (Windows/Linux); adjust for macOS if your build maps differently |
| Status | Look for **Auto-Compile: ON/OFF** (often colour-coded) |
| Manual build | When auto-compile is **off**, use **Build and Run** (▶) or **Ctrl+Alt+M** |

**Tips**

- Turn **off** auto-compile while making large refactors to avoid constant rebuilds.
- Turn **on** when learning or iterating for immediate feedback.
- Use **manual build** for a final check before sharing or recording.

## Keyboard shortcuts (reference)

### Build & run

| Action | Shortcut (typical) |
|--------|---------------------|
| Toggle auto-compile | Ctrl+Alt+C |
| Manual build and run | Ctrl+Alt+M |
| Reset and run | Ctrl+Alt+R |

### Debug (where supported)

| Action | Shortcut |
|--------|----------|
| Pause | Ctrl+Alt+, |
| Resume | Ctrl+Alt+. |
| Reset (debug) | Ctrl+Alt+E |

### Editor

| Action | Windows / Linux | macOS |
|--------|------------------|--------|
| Select all | Ctrl+A | Cmd+A |
| Start / end of file | Ctrl+Home / Ctrl+End | Cmd+Home / Cmd+End (or Cmd+↑ / Cmd+↓) |
| Word left / right | Ctrl+← / → | Alt+← / → |
| Undo / redo | Ctrl+Z / Ctrl+Shift+Z or Ctrl+Y | Cmd+Z / Cmd+Shift+Z |
| Indent / outdent | Ctrl+] / Ctrl+[ | Cmd+] / Cmd+[ |
| Find | Ctrl+F | Cmd+F |
| Replace | Ctrl+Shift+F | Cmd+Shift+F | 
| Find next / prev | Ctrl+G / Ctrl+Shift+G | Cmd+G / Cmd+Shift+G |

!!! tip
    Browsers and OS keyboard layouts can steal shortcuts. If something doesn’t fire, try clicking the emulator canvas first or check the in-app shortcut list.

## Quick start workflow

1. **Choose a platform** from the platform selector.
2. **Load an example** if you want a known-good starting point.
3. **Edit** your source. With auto-compile on, fixes often run as you type.
4. **Watch the emulator** (or build output) for behaviour and errors.
5. **Debug** if the platform exposes pause/step/reset tools.

## Troubleshooting (common)

- **Auto-compile seems off** — Confirm the status line says ON; fix syntax errors that block the toolchain.
- **No manual build button** — Manual build appears when auto-compile is **disabled**.
- **Emulator buttons missing** — Some cores don’t support pause/resume; the UI hides unsupported controls.
- **RGC BASIC** — Click the emulator canvas before keyboard input (`GET` / `INKEY$`). Use project download/export options if you ship a standalone HTML package.
- **BBC / VIC quirks** — BBC BASIC loading and VIC memory limits are platform-specific; see platform notes in examples.

## Credits

- **Retro Game Coders IDE** — [Chris Garrett](https://retrogamecoders.com/) and contributors.
- **Original 8bitworkshop IDE** — [Steven E. Hugg](https://github.com/sehugg/8bitworkshop).
- **Community** — [retrogamecoders.com/community](https://retrogamecoders.com/community/)
- Licence: GPL-3.0 (see project `LICENSE` where applicable).

---



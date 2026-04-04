---
title: Commodore BASIC V2
description: Commodore 6502 BASIC (V2) in the RGC IDE — C64, VIC-20, PET, and related platforms.
---

# Commodore BASIC V2

**Commodore BASIC V2** is the built-in interpreter ROM on many Commodore 6502 machines (most famously the **Commodore 64**, also **VIC-20**, **PET**, early **C128** in C64 mode, etc.). In the IDE it usually appears when you choose a Commodore platform and a **BASIC** (or “C64 BASIC”) preset.

## What you’re programming

- **Line numbers** or **labels** depending on the project template.
- **Tokens** stored as single bytes in classic LIST output; the editor may show **keywords spelled out** for clarity.
- **POKE / PEEK** for hardware registers; **SYS** to call machine code.
- **String and array** limits depend on **RAM** after BASIC overhead (especially tight on **VIC-20** and small **PET** configs).

## In the RGC IDE

1. Select a **Commodore** family platform (C64, VIC-20, PET, …).
2. Pick the **BASIC** workflow for that platform (naming varies by preset).
3. Use **auto-compile** or **manual build** to tokenize/run in the emulated BASIC environment.

!!! note "Tokenizer and control codes"
    The RGC fork has improved **tokenizer** behaviour and **control-code** handling for C64-style BASIC in several paths. If something differs from hardware, check the **console** and try a minimal one-liner to isolate tokenizer vs. runtime issues.

## Core concepts worth teaching

| Topic | Notes |
|-------|--------|
| **PRINT, INPUT, GET, INKEY$** | Text I/O; some keys differ on real hardware vs. emulator focus |
| **FOR / NEXT, IF / GOTO** | Classic control flow |
| **POKE 53280, n** etc. | Border/background on C64 — values are platform-specific |
| **USR, SYS** | Bridge to machine code; requires correct load address and register conventions |
| **Memory** | `FRE(0)`, program vs. variable space — important on small machines |

## Links

- [IDE getting started](../ide/getting-started.md) — shortcuts and workflow
- [6502 assembly](../assembly/6502.md) — when BASIC calls ML via `SYS`
- [Main site — RGC BASIC](https://retrogamecoders.com/) — browser/WASM BASIC projects where relevant

## Expand this page

Add **lesson-sized** snippets: first `PRINT`, then loops, then a `POKE` border colour demo, then a `SYS` stub. Keeping examples **short** matches how people learn in the IDE.

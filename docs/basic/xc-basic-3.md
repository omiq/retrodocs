---
title: XC-BASIC 3
description: XC-BASIC 3 cross-compiler for Commodore targets in the Retro Game Coders IDE.
---

# XC-BASIC 3

**XC-BASIC 3** is a **BASIC-like language** that **cross-compiles** to efficient 6502 machine code for Commodore-class targets. In the IDE it is listed among **specialized BASICs** alongside dialects like batariBASIC and FastBasic.

Typical targets include **Commodore 64**, **VIC-20**, and **PET** (exact presets depend on your IDE version).

## How it differs from Commodore ROM BASIC

| Aspect | Commodore BASIC V2 | XC-BASIC 3 |
|--------|-------------------|------------|
| Execution | Interpreted in ROM | Compiled to **machine code** ahead of time |
| Performance | Slower, predictable | Much faster for game loops |
| Syntax | Microsoft BASIC dialect | Modernized syntax; see **official XC-BASIC docs** |
| Debugging | `STOP`, `CONT`, `LIST` | Use compiler errors + emulator; patterns differ |

## In the RGC IDE

1. Choose a platform that lists **XC-BASIC 3** (or the closest preset name in your build).
2. Create or open an example project; the template shows **file layout** and **entry conventions**.
3. Build with the same **auto-compile / manual build** workflow as other languages ([getting started](../ide/getting-started.md)).

!!! warning "Compiler vs. interpreter"
    Errors you see are usually **compile-time** from the XC-BASIC toolchain, not tokenization errors like ROM BASIC. Read the first error line carefully.

## Official resources

- **XC-BASIC 3** language and compiler documentation live with the **XC-BASIC** project (search for “XC-BASIC 3” and your target). Link the canonical URL here when you standardize on one version in the IDE.

## What to add here later

- **Minimal “Hello”** program that matches your IDE template.
- **Memory map** notes for C64 vs VIC vs PET for that XC-BASIC version.
- **Calling assembly** or **inline** patterns if your toolchain exposes them.

## See also

- [Commodore BASIC V2](commodore-basic-v2.md) — ROM BASIC for comparison
- [6502 assembly](../assembly/6502.md) — mixing ML with compiled BASIC ecosystems

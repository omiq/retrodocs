---
title: RGC BASIC
description: Retro Game Coders BASIC — WebAssembly interpreter integrated in the RGC IDE.
---

# RGC BASIC

**RGC BASIC** is a BASIC dialect with a **WebAssembly (WASM) interpreter** built for the [Retro Game Coders web IDE](https://ide.retrogamecoders.com/). Programs run **in the browser** — no separate emulator binary — with fast edit-run cycles for learning and experimenting.

Source code and development history live in the public repository:

**[github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic)**

## Open in the IDE

Choose the **RGC BASIC** platform in the IDE, or open a direct link with the `platform` and optional `file` query parameters:

**[ide.retrogamecoders.com/?platform=rgc-basic&file=petscii-data.bas](https://ide.retrogamecoders.com/?platform=rgc-basic&file=petscii-data.bas)**

You can change `file=` to another example shipped with the IDE, or start from the default template after selecting the platform.

## How it fits in

| Aspect | Notes |
|--------|--------|
| **Execution** | WASM interpreter embedded in the IDE |
| **Use case** | Teaching, prototyping, and PETSCII/data-oriented examples without targeting a specific 8-bit ROM BASIC |
| **Compared to other BASICs here** | Unlike [Commodore BASIC V2](commodore-basic-v2.md) or [Color BASIC](color-basic.md), RGC BASIC is not tied to a particular machine’s ROM — it is the platform |

## See also

- [Getting started with the IDE](../ide/getting-started.md) — workflows, shortcuts, and build/run behaviour
- [BASIC dialects index](index.md) — other BASIC options in the IDE
- [Platforms overview](../platforms/index.md) — hardware-oriented presets (C64, Spectrum, etc.)

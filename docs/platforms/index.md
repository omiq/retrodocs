---
title: Platforms
description: Supported platforms in the Retro Game Coders IDE — quick reference for each machine.
---

# Platforms

The Retro Game Coders IDE supports a wide range of 8-bit (and some 16-bit) computers and consoles. Each platform page covers the machine's hardware, available languages in the IDE, a quick start workflow, and key things to know before you start coding.

## 6502-based platforms

These machines all use the MOS 6502 or a close variant. Core assembly knowledge transfers between them, though the hardware — video, sound, I/O — is completely different per machine.

| Platform | Languages in IDE | Notes |
|----------|-----------------|-------|
| [Commodore 64](c64.md) | CC65 C, Commodore BASIC V2, KickAss assembly | The most popular home computer of all time |
| [VIC-20](vic20.md) | CC65 C, Commodore BASIC V2 | C64's little sibling; tight on RAM |
| [BBC Micro](bbc-micro.md) | CC65 C, BBC BASIC | Sophisticated BASIC with inline assembler |
| [NES](nes.md) | ca65 / DASM assembly | Console; no OS, strict timing requirements |
| [Atari 8-bit](atari8.md) | CC65 C, 6502 assembly | ANTIC/GTIA give it exceptional graphics hardware |

## Z80-based platforms

These machines use the Zilog Z80. The Z80 has more registers and a richer instruction set than the 6502 — and very different I/O conventions per machine.

| Platform | Languages in IDE | Notes |
|----------|-----------------|-------|
| [ZX Spectrum](zx-spectrum.md) | Z88DK C, ZX BASIC (Boriel), Z80 assembly | Iconic British micro; simple memory map |

## Choosing a platform to start with

If you're new to retro programming, the **Commodore 64** is a great first machine:

- Huge community, tutorials, and example code
- Well-documented hardware
- Several language options in the IDE
- The emulator (Vice) is battle-tested and accurate

If you're interested in the **ZX Spectrum**, its simplicity (especially the 48K model) makes it very approachable. ZX BASIC (Boriel) lets you write compiled code with minimal friction.

For **console development**, the **NES** is the most documented console of the 8-bit era, though it requires assembly or careful C — there's no OS to help you.

## See also

- [6502 assembly](../assembly/6502.md) — common to all 6502 platforms
- [Z80 assembly](../assembly/z80.md) — common to all Z80 platforms
- [IDE getting started](../ide/getting-started.md)

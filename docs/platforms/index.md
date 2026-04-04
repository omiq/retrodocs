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
| [Commodore PET](pet.md) | CC65 C, Commodore BASIC V2, 6502 assembly | Commodore's first computer; monochrome character display |
| [BBC Micro](bbc-micro.md) | CC65 C, BBC BASIC | Sophisticated BASIC with inline assembler |
| [NES / Famicom](nes.md) | ca65 / DASM assembly | Console; no OS, strict timing requirements |
| [Atari 8-bit](atari8.md) | CC65 C, 6502 assembly | ANTIC/GTIA give it exceptional graphics hardware |
| [Apple II](apple2.md) | CC65 C, AppleSoft BASIC, 6502 assembly | Soft-switched graphics; non-linear HIRES layout |

## Z80-based platforms

These machines use the Zilog Z80. The Z80 has more registers and a richer instruction set than the 6502 — and very different I/O conventions per machine.

| Platform | Languages in IDE | Notes |
|----------|-----------------|-------|
| [ZX Spectrum](zx-spectrum.md) | Z88DK C, ZX BASIC (Boriel), Z80 assembly | Iconic British micro; simple memory map |
| [ZX81](zx81.md) | Z80 assembly | 1KB RAM; FAST/SLOW display modes |
| [Amstrad CPC6128](cpc.md) | Z80 assembly | 4 MHz Z80, Gate Array, no memory contention |
| [MSX](msx.md) | Z88DK C, Z80 assembly | BIOS + libCV; slot-based memory system |
| [Sega Master System / Game Gear](sega.md) | Z80 assembly | VDP via I/O ports; ROM header required |

## 6809-based platforms

The Motorola 6809 is a more advanced architecture than the 6502 or Z80 — two stacks, two accumulators, multiply instruction, and powerful indexed addressing.

| Platform | Languages in IDE | Notes |
|----------|-----------------|-------|
| [Dragon 32 / TRS-80 CoCo 2](dragon-coco.md) | CMOC C, Color BASIC, 6809 assembly | MC6847 VDG graphics; Color BASIC built in |
| [Vectrex](vectrex.md) | CMOC C, 6809 assembly | Vector display — no pixels, no raster; unique BIOS |

## x86 / DOS

| Platform | Languages in IDE | Notes |
|----------|-----------------|-------|
| [x86 / DOSBox](x86.md) | NASM assembly | DOS 6.22 environment; COM programs; Mode 13h VGA |

## Choosing a platform to start with

If you're new to retro programming, the **Commodore 64** is a great first machine — huge community, multiple language options, and well-documented hardware.

For **Z80 systems**, the **ZX Spectrum 48K** is the most approachable: a simple memory map, a single ULA chip to understand, and ZX BASIC (Boriel) to ease you in before diving into assembly.

For something **unusual**, the **Vectrex** is unlike anything else — it draws actual vectors on screen, not pixels, and its BIOS makes it surprisingly easy to get something moving.

For **DOS nostalgia**, the **x86/DOSBox** preset drops you into Mode 13h and INT 21h — the world of early PC games.

## See also

- [6502 assembly](../assembly/6502.md) — common to all 6502 platforms
- [Z80 assembly](../assembly/z80.md) — common to all Z80 platforms
- [6809 assembly](../assembly/6809.md) — common to Dragon/CoCo and Vectrex
- [IDE getting started](../ide/getting-started.md)

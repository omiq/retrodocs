---
title: Commodore PET
description: Commodore PET platform guide — 6502, Commodore BASIC, and CC65 C in the RGC IDE.
---

# Commodore PET

The **Commodore PET** (Personal Electronic Transactor, 1977) was Commodore's first computer and one of the first successful personal computers ever sold. It predates the Apple II and TRS-80 by only months and established Commodore as a serious computing company.

The PET uses a **MOS 6502** CPU and runs **Commodore BASIC 2.0** (or 4.0 on later models) — the same BASIC family that descended into the VIC-20 and C64. The machines are characterised by their all-in-one design (keyboard, screen, and cassette tape in one unit) and their distinctive green phosphor display.

## Languages in the IDE

| Language | Notes |
|----------|-------|
| **Commodore BASIC V2** | Built-in ROM BASIC — line-numbered, interpreted |
| **CC65 C** | C cross-compiler with PET target |
| **6502 assembly** | ca65 assembler |

## Quick start

1. Select **Commodore PET** as the platform.
2. Choose your language preset.
3. The IDE loads a PET emulator — you'll see the familiar `READY.` prompt.
4. Build and run.

!!! tip "Which PET?"
    The IDE emulates a specific PET model (check the preset). Common targets are the **PET 2001** (original, 40-column) and **PET 8032** (80-column business machine). Screen width and RAM differ between models.

## Hardware overview

### CPU — MOS 6502 at 1 MHz

Standard 6502 — see [6502 assembly](../assembly/6502.md) for the full instruction set. The PET runs the 6502 at 1 MHz, the same as the C64.

### Video — 6545 CRTC

The PET uses a **Motorola 6845/6545 CRTC** (the same chip as the Amstrad CPC) to drive its built-in monitor. The display is character-based only — no bitmap graphics mode on most PETs.

| Model | Screen | Notes |
|-------|--------|-------|
| PET 2001/3000 series | 40×25 characters | 1 KB video RAM |
| PET 4000 series | 40×25 characters | BASIC 4.0, disk commands |
| PET 8000 series | 80×25 characters | Business machine |

### Memory map (PET 2001 / 32K)

| Range | Contents |
|-------|----------|
| $0000–$00FF | Zero page |
| $0100–$01FF | Stack |
| $0200–$03FF | OS work area |
| $0400–$0FFF | Video RAM (1 KB at $8000 on early models) |
| $1000–$7FFF | User RAM (up to 32 KB) |
| $8000–$8FFF | Video RAM (later models) |
| $9000–$9FFF | I/O (VIA chips, CRTC) |
| $A000–$BFFF | BASIC ROM |
| $C000–$DFFF | BASIC ROM (continued) |
| $E000–$FFFF | Kernal ROM + editor ROM |

!!! note "Video RAM location varies"
    Early PET 2001 models have video RAM at $8000. Later models moved it. Always check which model your preset targets before hard-coding screen addresses.

### VIA chips — I/O

Two **MOS 6522 VIA** chips handle keyboard, IEEE-488 bus (for disk drives and printers), cassette, and the speaker.

The keyboard is read as a matrix via VIA 1 (port B = column select, port A = row readback).

## Commodore BASIC on the PET

The PET runs essentially the same BASIC V2 as the C64 — see [Commodore BASIC V2](../basic/commodore-basic-v2.md) for the full guide. Key differences:

**No colour** — the PET display is monochrome (green or white phosphor). POKE addresses for colour don't apply.

**No sprites** — the PET has no sprite hardware.

**PETSCII characters** — the same character set as the C64. Block graphics characters (codes 160–223) provide crude graphics.

**Screen RAM location** — not at $0400 like the C64. Check your model:

```basic
10 REM PET 2001 early: screen at $8000 = 32768
20 POKE 32768, 1    : REM Block character top-left
30 REM PET 4000/8000: check model documentation
```

**No SID chip** — the PET has a simple speaker driven by a VIA timer. You can produce beeps but not the rich sound of the C64.

A simple PET BASIC program:

```basic
10 PRINT CHR$(147)        : REM Clear screen
20 FOR Y=0 TO 24
30   FOR X=0 TO 39
40     PRINT CHR$(INT(RND(1)*5)+160);  : REM Random block char
50   NEXT X
60 NEXT Y
70 GOTO 20
```

## CC65 C on the PET

CC65 has a `pet` target. Basic usage:

```c
#include <peekpoke.h>
#include <conio.h>
#include <stdio.h>

int main(void) {
    clrscr();
    gotoxy(10, 5);
    printf("HELLO FROM CC65!\n");

    /* Write directly to screen RAM */
    POKE(0x8000, 0x01);   /* Block character, top-left (PET 2001) */

    return 0;
}
```

The cc65 `pet.h` and `conio.h` headers handle screen addressing differences between PET models for the standard I/O functions.

## PET graphics — block characters

Without a graphics mode, PET programmers use the PETSCII block graphic characters to draw shapes. The block set provides characters that fill different portions of a character cell:

| Code range | Description |
|------------|-------------|
| 160–175 | Solid and partial blocks |
| 176–191 | Diagonal and special shapes |
| 224–254 | More block graphics |

By combining these characters you can produce surprisingly detailed graphics — many PET games are pure character graphics.

## IEEE-488 — disk and printer I/O

The PET uses the **IEEE-488** (GPIB) bus for storage and printing rather than the serial bus used by the C64. This is faster but the devices (disk drives, printers) were expensive. The Kernal provides OPEN/CLOSE/GET/PUT routines for IEEE-488 access just like the C64 does for its devices.

```basic
10 OPEN 1,8,0,"MYFILE,S,R"   : REM Open file on disk drive 8
20 INPUT#1, A$                : REM Read a line
30 CLOSE 1
```

## Kernal routines (call via SYS / JSR)

| Address | Name | Action |
|---------|------|--------|
| $FFD2 | CHROUT | Print character in A |
| $FFE4 | GETIN | Get character from keyboard |
| $FF9C | CLALL | Close all files |
| $FFB4 | OPEN | Open a file |
| $FFC0 | CLOSE | Close a file |
| $FFA5 | CHKIN | Set input device |
| $FFA8 | CHKOUT | Set output device |

These are the same Kernal entry points as the C64 — deliberate design continuity across the Commodore line.

## Tips

**Use CHR$(147) to clear** — `PRINT CHR$(147)` clears the screen via the PETSCII control code (same as on C64). `CLR` only clears variables.

**PETSCII vs ASCII** — the PET uses PETSCII throughout, not ASCII. Many special characters are in different positions. `ASC("A")` = 65 in PETSCII and ASCII, but lowercase letters differ.

**64K PET** — some PET models have 64 KB RAM and use a different memory map. The upper 32 KB is accessed by banking out the BASIC ROM.

**The PET is the ancestor** — the C64's Kernal, BASIC structure, and many hardware conventions trace directly back to the PET. If you understand the PET, you understand the whole Commodore 8-bit family.

## See also

- [Commodore BASIC V2](../basic/commodore-basic-v2.md) — the same BASIC as the C64
- [cc65 / C](../c/cc65.md) — CC65 toolchain reference
- [6502 assembly](../assembly/6502.md) — 6502 language reference
- [C64 platform guide](c64.md) — the PET's famous descendant
- [IDE getting started](../ide/getting-started.md)

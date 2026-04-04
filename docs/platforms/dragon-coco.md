---
title: Dragon 32 / TRS-80 CoCo 2
description: Dragon 32 and TRS-80 Color Computer 2 platform guide — 6809, Color BASIC, and CMOC C in the RGC IDE.
---

# Dragon 32 / TRS-80 Color Computer 2

The **Dragon 32** (1982, Wales) and the **TRS-80 Color Computer 2** (CoCo 2, 1983, USA) are closely related machines — both built around the **Motorola 6809** CPU and the **MC6847** Video Display Generator, with similar ROM BASICs and nearly identical hardware. The Dragon was designed and built by Dragon Data in South Wales; the CoCo was made by Tandy/Radio Shack and sold through their stores.

The 6809 is a remarkable CPU — see the [6809 assembly guide](../assembly/6809.md) for why it's considered the most elegant 8-bit processor ever made.

## Languages in the IDE

| Language | Notes |
|----------|-------|
| **Color BASIC** | Built-in ROM BASIC — line-numbered, interpreted |
| **CMOC C** | Cross-compiler producing 6809 machine code |
| **6809 assembly** | LWASM assembler — maximum control |

## Quick start

1. Select **Dragon 32** or **TRS-80 CoCo 2** as the platform.
2. Choose your language preset.
3. Build and run in the emulator.

!!! tip "Dragon vs CoCo differences"
    The Dragon 32 and CoCo 2 are similar but not identical. Key differences: the Dragon uses a slightly different memory map, different SAM (Synchronous Address Multiplexer) chip, and the BASIC ROM has minor differences. The IDE emulates each separately — pick the right one for your target.

## Hardware overview

### CPU — Motorola 6809E at ~0.89 MHz

The 6809 is a 16-bit capable 8-bit processor — two accumulators (A and B), a combined 16-bit D register, two 16-bit index registers (X and Y), two stack pointers (S and U), and a direct page register. See [6809 assembly](../assembly/6809.md) for the full story.

Both machines run at approximately 0.89 MHz (the 3.58 MHz colour burst oscillator divided by 4). This is slower than the BBC Micro or ZX Spectrum, but the 6809's efficiency more than compensates.

### MC6847 — Video Display Generator

The **MC6847 VDG** generates the video signal with no CPU involvement once configured. It reads directly from RAM and produces the display. Graphics modes:

| Mode | Command | Resolution | Colours |
|------|---------|------------|---------|
| Text | `TEXT` | 32×16 chars | 2 (green/black or white/black) |
| Graphics 1C | `GR(0)` | 64×64 | 4 |
| Graphics 2C | | 128×64 | 4 |
| Graphics 3C | | 128×96 | 4 |
| Graphics 6C | `HGR(0)` | 128×192 | 4 |
| Graphics 6R | `HGR(1)` | 256×192 | 2 |

The MC6847 has a fixed colour palette based on an NTSC phosphor palette — greens, yellows, blues, reds — without the custom colour mixing of the C64's VIC-II or Spectrum's ULA.

### SAM — Synchronous Address Multiplexer

The **MC6883 SAM** manages memory and video timing. It controls which RAM area the VDG reads from, the CPU clock rate, and the VDG mode. SAM registers are write-only and live at $FFC0–$FFDF.

### Sound

Both machines have a single-bit DAC connected to the cassette port — basic but capable of reasonable music with careful timing. The CoCo also has a 6-bit DAC via the MC6821 PIA.

### Memory map (Dragon 32 / CoCo 2)

| Range | Contents |
|-------|----------|
| $0000–$001F | Direct page / system variables |
| $0020–$007F | More system variables |
| $0080–$00FF | More system area |
| $0100–$7FFF | User RAM (up to ~32 KB) |
| $8000–$BFFF | Cartridge ROM slot |
| $A000–$BFFF | Extended Color BASIC ROM (CoCo) |
| $C000–$DFFF | Color BASIC ROM |
| $E000–$FFFF | Color BASIC ROM / OS |

VDG screen RAM is configurable via the SAM — by default it starts at $0400 (Dragon) or $0400 (CoCo).

### PIA — I/O

Two **MC6821 PIAs** handle:
- PIA 0: Keyboard matrix, joystick comparators, cassette, horizontal sync
- PIA 1: 6-bit DAC (sound), VDG mode bits, vertical sync, motor control

## Color BASIC

Color BASIC on both machines is a Microsoft-licensed BASIC very similar to other Microsoft BASICs of the era. See the dedicated [Color BASIC guide](../basic/color-basic.md) for a full reference.

Quick overview:

```basic
10 CLS             : REM Clear screen (green on black in text mode)
20 PRINT "HELLO, DRAGON!"
30 FOR I=1 TO 10
40   PRINT I
50 NEXT I
60 POKE &H1000, 0  : REM POKE in hex (& prefix)
70 X = PEEK(&H1000)
80 PLAY "CDEFGAB"  : REM Play musical notes!
90 JOYSTK(0)       : REM Read joystick 0 (0-63)
```

Color BASIC includes `PLAY` for music, `DRAW` for graphics primitives, `GET` and `PUT` for sprite-style graphics, and `MOTOR` to control the cassette motor — a nicely featured BASIC for its era.

## CMOC C

**CMOC** is a C cross-compiler that targets the 6809 — it takes a subset of C and produces 6809 assembly via LWASM. See [CMOC guide](../c/cmoc.md) for full details.

```c
#include <cmoc.h>

int main() {
    // Clear screen
    cls();

    // Print text
    printf("HELLO FROM CMOC!\n");

    // Hardware access
    byte *screen = (byte *) 0x0400;
    *screen = 0xBF;   /* Block graphic character */

    return 0;
}
```

CMOC supports `printf`, `malloc`, basic string functions, and inline assembly — enough for real games.

## 6809 assembly quick reference

The 6809's powerful addressing modes make it particularly pleasant for Dragon/CoCo programming:

```asm
; Dragon 32 — write a character to the screen
; Screen RAM at $0400 (32 cols × 16 rows text mode)

        ORG $7E00

start:
        LDX #$0400      ; Screen RAM start
        LDA #$C1        ; 'A' in MC6847 semi-graphics set
        STA ,X          ; Write to top-left
        RTS

        END start
```

Call from BASIC with `EXEC &H7E00`.

### Key differences from 6502/Z80

- **No zero page** (but moveable Direct Page — set DP register)
- **16-bit registers** throughout — index registers, stack, and D are all 16-bit
- **Two stacks** — use U freely as a second stack or frame pointer
- **MUL instruction** — 8×8=16 bit multiply in one opcode
- **LEA instructions** — Load Effective Address (like a 68000-style `LEA`)

```asm
LEAX 5,X        ; X = X + 5  (no memory access — just address arithmetic)
LEAY D,X        ; Y = X + D  (very useful for table lookups)
LEAS -4,S       ; Allocate 4 bytes on stack (move SP down)
```

## Joystick input

Both machines have two analog joysticks (0–63 range) read through the PIA's comparator:

```basic
10 X = JOYSTK(0)   : REM Left joystick horizontal (0-63)
20 Y = JOYSTK(1)   : REM Left joystick vertical
30 PRINT X, Y
```

In assembly, joystick reading involves the PIA's comparator and a DAC — the BASIC ROM's `JOYSTK` routine handles the timing. Calling it via JSR is the easiest approach.

## Practical tips

**Dragon vs CoCo BASIC compatibility** — the two BASICs are very similar but have subtle differences in some PLAY/DRAW command syntax and a few POKE addresses. Always test on the target machine.

**The 6809 DP register** — both machines use $00 as the Direct Page on startup (same as 6502 zero page). You can change it, but ROM routines expect DP=$00.

**Screen RAM and SAM** — the SAM chip controls where the VDG reads screen data from. If you need a custom screen address, you must program the SAM as well as use that address in your code.

**Cassette/tape format** — the Dragon and CoCo use the same basic tape encoding. Programs saved from one can sometimes be loaded on the other, depending on BASIC version compatibility.

**Extended BASIC** — the CoCo's Extended Color BASIC (in the separate $A000–$BFFF ROM) adds `DRAW`, `PAINT`, `GET`/`PUT`, and other graphics commands not in the base Dragon BASIC.

## See also

- [6809 assembly](../assembly/6809.md) — full 6809 language reference
- [Color BASIC](../basic/color-basic.md) — BASIC language guide
- [CMOC C for 6809](../c/cmoc.md) — C compilation for Dragon/CoCo/Vectrex
- [Vectrex platform guide](vectrex.md) — another 6809-based system
- [IDE getting started](../ide/getting-started.md)

---
title: Apple II
description: Apple II platform guide — 6502, AppleSoft BASIC, and CC65 C in the RGC IDE.
---

# Apple II

The **Apple II** (1977) was one of the first mass-market personal computers and one of the longest-lived — the Apple II line remained in production until 1993. Designed by Steve Wozniak, it introduced many features that became standard: colour graphics, a built-in BASIC interpreter, expansion slots, and a floppy disk drive.

The IDE supports the **Apple ][+** and **Apple //e** models, which are the most common targets for homebrew development.

## Languages in the IDE

| Language | Notes |
|----------|-------|
| **CC65 C** | C cross-compiler with Apple II target library |
| **6502 assembly** | ca65 assembler (part of the cc65 suite) |
| **AppleSoft BASIC** | Built into ROM — available at the `]` prompt |

## Quick start

1. Select **Apple ][+** or **Apple //e** as the platform.
2. Choose your language preset.
3. The IDE loads an Apple II emulator (typically based on AppleWin or a JS emulator).
4. Build and run.

!!! tip "The ] prompt"
    The Apple II boots directly to AppleSoft BASIC — the `]` prompt. Machine code programs are called from BASIC using `CALL address` or from the monitor with `address G`. The IDE template handles this automatically.

## Hardware overview

### CPU — MOS 6502 at 1 MHz

The Apple II uses the same 6502 as the C64 and BBC Micro, running at 1.023 MHz. See [6502 assembly](../assembly/6502.md) for the full instruction set.

The **Apple //e** uses the 65C02 (an enhanced 6502) — same instruction set plus a handful of new instructions (`STZ`, `TRB`, `TSB`, `PHX`, `PHY`, etc.). CC65 and ca65 support both.

### Video — Woz's Video Hardware

Apple II video is driven by cleverly timing the CPU's memory accesses. It supports several modes:

| Mode | Resolution | Colours | Notes |
|------|------------|---------|-------|
| **Text** | 40×24 characters | Green/amber/white on black | ROM character set |
| **Lo-Res** | 40×48 "blocks" | 16 colours | Chunky pixels from text page |
| **Hi-Res** | 280×192 pixels | 6 colours* | Famous "HIRES" mode |
| **Double Hi-Res** (//e) | 560×192 | 16 colours | Requires 80-col card |

*Hi-Res colour is quirky — colour depends on the horizontal position of pixels, not just the byte value. Pairs of pixels form colour dots. This leads to Apple II's characteristic colour-fringing look.

### Memory map

| Range | Contents |
|-------|----------|
| $0000–$00FF | Zero page |
| $0100–$01FF | Stack |
| $0200–$02FF | Input buffer |
| $0300–$03FF | System vectors and I/O |
| $0400–$07FF | Text page 1 / Lo-Res page 1 |
| $0800–$0BFF | Text page 2 / Lo-Res page 2 |
| $2000–$3FFF | Hi-Res page 1 (8 KB) |
| $4000–$5FFF | Hi-Res page 2 (8 KB) |
| $6000–$95FF | Free RAM (on 48K machine) |
| $C000–$C0FF | Soft switches (I/O) |
| $C100–$CFFF | Peripheral card ROMs |
| $D000–$DFFF | DOS / ProDOS area |
| $E000–$FFFF | ROM (BASIC, Monitor) |

### Soft switches

The Apple II uses **soft switches** — memory addresses in $C000–$C0FF that toggle hardware modes when read or written:

| Address | Action |
|---------|--------|
| $C050 | Graphics mode on |
| $C051 | Text mode on |
| $C052 | Full-screen graphics |
| $C053 | Mixed mode (text at bottom) |
| $C054 | Display page 1 |
| $C055 | Display page 2 |
| $C056 | Lo-Res mode |
| $C057 | Hi-Res mode |
| $C000 | Read keyboard (bit 7 = key ready) |
| $C010 | Clear keyboard strobe |

```asm
; Switch to Hi-Res page 1, full screen
STA $C057       ; Hi-Res
STA $C050       ; Graphics
STA $C052       ; Full screen
STA $C054       ; Page 1
```

### Keyboard

The Apple II keyboard is polled, not interrupt-driven:

```asm
wait_key:
    LDA $C000       ; Read keyboard — bit 7 set when key is ready
    BPL wait_key    ; Loop until bit 7 is set
    AND #$7F        ; Mask off the strobe bit (key is ASCII + $80)
    STA $C010       ; Clear keyboard strobe
    ; A now contains the ASCII key code
```

### Speaker

The Apple II speaker is toggled by reading or writing $C030. Each access flips the speaker membrane:

```asm
; Click the speaker (one flip)
STA $C030

; Simple tone — toggle rapidly in a loop
    LDX #tone_period
tone_loop:
    STA $C030       ; Toggle speaker
    DEX
    BNE tone_loop
```

Generating music means carefully timed toggles in tight assembly loops — a genuine skill on the Apple II.

## Hi-Res graphics

The Apple II Hi-Res screen is at $2000. The layout is non-linear (similar to the ZX Spectrum but with a different pattern):

```asm
; Address of pixel row Y (0-191) in Hi-Res page 1:
; Addr = $2000 + (Y & 7)*$0400 + ((Y >> 3) & 7)*$80 + (Y >> 6)*$28
```

Each byte in HIRES controls 7 pixels (bit 7 is a colour palette selector). Pixels are arranged left-to-right, bits 0–6.

The colour rules:
- On an NTSC screen, adjacent "on" pixels produce colour (orange, green, blue, violet)
- The exact colour depends on horizontal position (even/odd column) and bit 7 of the byte

Most Apple II graphics programmers use lookup tables for row addresses and shape data rather than calculating from scratch.

## AppleSoft BASIC quick reference

```basic
]HOME               : REM Clear screen
]PRINT "HELLO"
]GR                 : REM Switch to Lo-Res graphics
]HGR                : REM Switch to Hi-Res graphics
]COLOR= 12          : REM Set Lo-Res colour (0-15)
]PLOT X,Y           : REM Plot Lo-Res block at (X,Y)
]HCOLOR= 3          : REM Set Hi-Res colour (0-7)
]HPLOT X,Y          : REM Plot Hi-Res pixel
]HPLOT TO X2,Y2     : REM Draw line
]CALL -936          : REM Clear screen (via ROM)
]CALL address       : REM Call machine code
]PEEK(addr)         : REM Read memory byte
]POKE addr, val     : REM Write memory byte
```

AppleSoft BASIC variables follow the same 2-significant-character rule as Commodore BASIC. Integers use `%` suffix, strings use `$`.

## CC65 C on the Apple II

CC65 provides an `apple2` (Apple ][+) and `apple2enh` (Apple //e) target with platform headers:

```c
#include <apple2.h>
#include <conio.h>
#include <stdio.h>

int main(void) {
    /* Clear screen */
    clrscr();

    /* Print at position */
    gotoxy(10, 5);
    cputs("HELLO FROM CC65!");

    /* Switch to Lo-Res graphics */
    /* Use soft switches via POKE-equivalent */
    *(volatile char*)0xC050 = 0;   /* Graphics on */
    *(volatile char*)0xC056 = 0;   /* Lo-Res */
    *(volatile char*)0xC052 = 0;   /* Full screen */

    return 0;
}
```

The `apple2enh.h` header adds //e-specific extras like 80-column text and double hi-res graphics.

## Common mistakes

**Hi-Res colour fringing** — the Apple II's colour system means that a solid block of "on" bits produces alternating colours, not a solid colour. Use established colour byte patterns from reference tables rather than guessing.

**Non-linear HIRES layout** — like the ZX Spectrum, Hi-Res rows are stored non-linearly. Always use a lookup table.

**Speaker timing** — generating a clean tone requires very precise loop timing. A loop that does other work will produce a buzzing, uneven sound. Keep speaker-toggle loops tight and pure.

**Soft switch read vs write** — some soft switches care whether you read or write them; others respond to either. In assembly use `STA` (write) for most; in situations where you're checking a switch state, `LDA` (read). The cc65 Apple II headers abstract this for common operations.

**40 vs 80 columns** — the base Apple II is 40 columns. The Apple //e with an 80-column card supports 80 columns. CC65's `conio.h` targets 40 columns by default; use `apple2enh.h` for 80-column support.

## See also

- [6502 assembly](../assembly/6502.md) — full 6502 language reference
- [cc65 / C](../c/cc65.md) — CC65 toolchain reference
- [IDE getting started](../ide/getting-started.md)

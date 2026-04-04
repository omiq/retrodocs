---
title: Atari 8-bit
description: Atari 8-bit platform guide — ANTIC, GTIA, POKEY, and programming with CC65 in the RGC IDE.
---

# Atari 8-bit

The **Atari 8-bit family** (400, 800, XL, XE — 1979 onwards) is built around a 1.79 MHz **MOS 6502B** CPU, but its real strength lies in the custom chips alongside it: **ANTIC** (graphics), **GTIA** (display), **POKEY** (sound + keyboard), and **PIA** (I/O). Together they give the Atari 8-bit hardware capabilities that rival the C64.

The Atari 8-bit machines are well-documented, have an active community, and offer some genuinely unique features — particularly ANTIC's Display List, which allows multiple graphics modes to be mixed on the same screen.

## Languages in the IDE

| Language | Use for |
|----------|---------|
| **CC65 C** | Structured programs targeting the Atari 8-bit |
| **6502 assembly** | Low-level hardware access and maximum performance |

## Quick start

1. Select **Atari 8-bit** (or the specific model) as the platform.
2. Choose **C / cc65** or **Assembly**.
3. The IDE loads an Atari emulator (Altirra-based or similar) with your program.

## Hardware overview

### The custom chips

Unlike the C64, the Atari 8-bit doesn't map everything through one or two chips. Four custom chips each handle different roles:

**ANTIC** ($D400–$D41F) — the display processor. It reads a **Display List** from RAM and drives the electron beam independently of the 6502. The CPU can set up the Display List and then let ANTIC handle the video with minimal intervention.

**GTIA** ($C000–$C0FF) — the colour/priority chip. It translates ANTIC's output into colours, handles player/missile (sprite) priorities, and supports several colour interpretation modes.

**POKEY** ($D200–$D21F) — handles sound (4 channels), the keyboard, serial I/O (SIO bus), and timer interrupts. The 4-channel sound hardware is very capable.

**PIA** ($D300–$D3FF) — joystick ports and some I/O.

### The Display List

ANTIC's **Display List** is a table in RAM that tells ANTIC what to draw on each line of the screen. Each entry is one byte (a mode command) or three bytes (a mode command + address of the data to display). ANTIC reads this table at 1.79 MHz while the CPU is doing something else.

This is powerful: you can mix text and graphics modes on the same screen, change the colour of different parts of the screen by inserting wait-for-line-blank (DLI) instructions, or do raster effects without tying up the CPU.

A minimal Display List:

```asm
; Display List for a 40-column text screen
display_list:
    .byte $70, $70, $70     ; 3 × 8 blank lines
    .byte $42               ; Mode 2 text + LMS (Load Memory Scan)
    .word screen_ram        ; Address of first text line
    .byte $02, $02, $02     ; Remaining text lines (24 total)
    .byte $02, $02, $02
    .byte $02, $02, $02
    .byte $02, $02, $02
    .byte $02, $02, $02
    .byte $02, $02, $02
    .byte $02, $02, $02
    .byte $41               ; Jump and wait for VBlank
    .word display_list      ; Loop back to start
```

### Graphics modes

ANTIC supports multiple text and graphics modes, each with different resolutions and colour depths. The OS adds extra modes on top.

From BASIC, modes are selected with `GRAPHICS n`:

| GRAPHICS # | ANTIC mode | Pixels | Colours |
|------------|-----------|--------|---------|
| 0 | 2 | 40×24 text | 2+bg |
| 8 | F | 320×192 | 2 |
| 7 | D | 160×96 | 4 |
| 15 | F | 160×192 | 4 (MultiColor) |

Graphics modes 1–6 and 9–15 offer various resolutions and colour depths. The GTIA can also apply three additional colour interpretation modes to ANTIC's output, creating the "GTIA modes" with unusual colour/resolution tradeoffs.

### Memory map

| Range | Contents |
|-------|----------|
| $0000–$00FF | Zero page (OS uses some — check the OS manual) |
| $0100–$01FF | Stack |
| $0200–$02FF | OS page 2 |
| $0300–$03FF | OS page 3 |
| $0400–$04FF | OS page 4 (floating point) |
| $0600–$BFFF | Free RAM (varies by model and cart) |
| $C000–$CFFF | GTIA registers |
| $D000–$D0FF | (Reserved) |
| $D200–$D2FF | POKEY registers |
| $D300–$D3FF | PIA registers |
| $D400–$D4FF | ANTIC registers |
| $D800–$DFFF | Floating point ROM |
| $E000–$FFFF | OS ROM |

### Key hardware registers

**ANTIC:**

| Address | Register | Purpose |
|---------|---------|---------|
| $D400 | DMACTL | DMA enable, display width |
| $D402/$D403 | DLISTL/H | Display List address |
| $D407 | PMBASE | Player/Missile base address |
| $D40A | WSYNC | Write to halt CPU until end of scanline |
| $D40B | VCOUNT | Current scanline counter |
| $D40C | PENH | Light pen horizontal |
| $D40E | NMIEN | NMI enable (VBlank and DLI) |

**GTIA:**

| Address | Register | Purpose |
|---------|---------|---------|
| $C000–$C003 | M0PF–M3PF | Missile/player collisions |
| $C010–$C017 | COLPM0–COLPF3 | Player and playfield colours |
| $C018 | COLBK | Background colour |
| $C01F | CONSOL | Console keys (Start/Select/Option) |

**POKEY:**

| Address | Register | Purpose |
|---------|---------|---------|
| $D200/$D201 | AUDF1/AUDC1 | Channel 1 frequency/control |
| $D202/$D203 | AUDF2/AUDC2 | Channel 2 |
| $D204/$D205 | AUDF3/AUDC3 | Channel 3 |
| $D206/$D207 | AUDF4/AUDC4 | Channel 4 |
| $D208 | AUDCTL | Audio control (frequency base, poly clocks) |
| $D209 | STIMER | Start timers |
| $D20E | IRQEN | IRQ enable |
| $D20F | SKCTL | Serial/keyboard control |

## Players and Missiles (sprites)

Atari 8-bit "hardware sprites" are called **Players** (wide) and **Missiles** (narrow):

- **4 Players**: each 8 pixels wide, 128/192/256 scanlines tall (selectable height), one colour per player
- **4 Missiles**: each 2 pixels wide, associated with a player's colour, or combined into a 5th player

Players and Missiles are defined as vertical byte strips in RAM, starting at the address specified by PMBASE. The horizontal position is set in GTIA registers.

```asm
; Position Player 0 at X=100
LDA #100
STA $D000       ; HPOSP0 — Player 0 horizontal position

; Enable Player 0 DMA
LDA #$0E        ; DMACTL: enable PM DMA, wide display
STA $D400
```

## Programming with cc65 C

cc65 includes an `atari` platform target with headers for all the hardware chips:

```c
#include <atari.h>
#include <stdio.h>
#include <conio.h>

int main(void) {
    /* Change background colour */
    GTIA_WRITE.colbk = 0x94;    /* Blue-ish */

    /* Enable graphics mode 0 (text) */
    /* In cc65, use the OS screen() function or direct GTIA */

    printf("Hello, Atari!\n");

    /* Read joystick 0 (PORTA on PIA) */
    unsigned char joy = PIA.porta;
    /* Bits 0-3: Up/Down/Left/Right (active low) */
    if (!(joy & 0x01)) {
        /* Joystick up */
    }

    return 0;
}
```

## BASIC quick reference

In Atari BASIC (accessed via the OS ROM):

```basic
10 GRAPHICS 7+16     : REM Mode 7, no text window (+16)
20 SETCOLOR 2,4,6    : REM Set playfield colour 2: hue 4, lum 6
30 COLOR 1           : REM Set drawing colour register 1
40 PLOT 80,48        : REM Plot pixel at (80, 48)
50 DRAWTO 100,80     : REM Draw line to (100, 80)
60 STICK(0)          : REM Read joystick 0 (15=centre, bits for directions)
70 STRIG(0)          : REM Read fire button 0 (1=not pressed, 0=pressed)
```

## Display List Interrupts (DLI)

DLIs are a powerful feature — the ANTIC chip can trigger an NMI on specific scanlines, allowing you to change colours, scroll positions, or switch modes mid-screen.

```asm
; Simple DLI — change background colour on a specific scanline
dli_handler:
    PHA                 ; Save A
    LDA #$28            ; New background colour (orange)
    STA $C018           ; COLBK (WSYNC isn't needed here but helps timing)
    PLA
    RTI

; Set DLI handler address
    LDA #<dli_handler
    STA $0200           ; VDSLST (Display List IRQ vector, low byte)
    LDA #>dli_handler
    STA $0201           ; VDSLST high byte
    LDA #$80            ; Enable DLI NMI
    STA $D40E           ; NMIEN
```

Add `$80` to a Display List entry to trigger the DLI on that line.

## Tips

**Use WSYNC for timing** — writing any value to $D40A (WSYNC) halts the CPU until the end of the current scanline. This is the easiest way to time hardware accesses precisely.

**Use the OS SIO for storage** — the Atari's Serial I/O (SIO) bus handles disk drives, cassette, and other peripherals through a clean OS interface. Don't bit-bang the hardware if you don't have to.

**Collision detection is hardware** — GTIA tracks collisions between players, missiles, and playfields automatically. Read the collision registers ($C000–$C00F) for zero-cost collision data.

**POKEY has built-in serial** — the SIO bus uses POKEY for clocking. If you're writing custom SIO-compatible hardware, POKEY handles the timing.

## See also

- [cc65 / C](../c/cc65.md) — C compilation targeting the Atari 8-bit
- [6502 assembly](../assembly/6502.md) — 6502 assembly language reference
- [IDE getting started](../ide/getting-started.md)

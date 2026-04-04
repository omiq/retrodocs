---
title: Amstrad CPC6128
description: Amstrad CPC6128 platform guide — Z80 assembly in the RGC IDE.
---

# Amstrad CPC6128

The **Amstrad CPC** (Colour Personal Computer) line was launched in 1984 by Alan Sugar's Amstrad company. The **CPC6128** (1985) is the most capable model — **128 KB of RAM**, a built-in **3-inch disk drive**, and a **Z80 at 4 MHz**. It came bundled with a monitor (either green screen or colour), making it a self-contained computing package at a competitive price.

The CPC was hugely successful in the UK, France, and Spain, and has a strong retro homebrew community today.

## Languages in the IDE

| Language | Notes |
|----------|-------|
| **Z80 assembly** | Primary development language for the CPC |

## Quick start

1. Select **Amstrad CPC6128** as the platform.
2. Choose the Assembly preset.
3. The IDE emulates the CPC — you'll see the familiar blue BASIC screen.
4. Build and your program loads automatically.

!!! tip "AMSDOS and BASIC"
    The CPC boots into Locomotive BASIC with AMSDOS (the disk operating system). Machine code programs are typically loaded with `LOAD "file.bin"` and called with `CALL address`. The IDE template handles this.

## Hardware overview

### CPU — Z80A at 4 MHz

The CPC's Z80A runs at **4 MHz** — faster than most Z80 machines of the era (ZX Spectrum runs at 3.5 MHz, MSX at 3.58 MHz). See [Z80 assembly](../assembly/z80.md) for the full instruction set.

Unlike the Spectrum, the CPC has **no memory contention** — the Z80 runs at full speed all the time.

### Gate Array — Video

The **Amstrad Gate Array** (a custom ASIC) controls:
- Screen mode and resolution
- Palette (colour selection from 27 possible colours)
- ROM/RAM switching
- CPU interrupt timing

Three screen modes:

| Mode | Resolution | Colours | Notes |
|------|------------|---------|-------|
| **Mode 0** | 160×200 | 16 | Chunky, colourful |
| **Mode 1** | 320×200 | 4 | Good balance — most games use this |
| **Mode 2** | 640×200 | 2 | High resolution, monochrome |

The CPC palette can show any 16 colours from a fixed set of 27 (from a 3-level RGB system — each channel can be off, half, or full).

### CRTC 6845 — Screen Timing

The **Motorola MC6845 CRTC** controls screen timing, scroll position, and screen start address. This chip is the key to many CPC demo effects:

- Change `CRTC R12/R13` (start address) mid-frame to implement hardware scrolling
- Write to CRTC mid-scanline for split-screen effects
- Reprogram the display timings for custom resolutions

### AY-3-8912 — Sound

The **AY-3-8912 PSG** provides 3 tone channels, 1 noise channel, and envelope control. On the CPC it's accessed via the PPI (8255 chip):

```asm
; Select AY register (via PPI port A)
LD BC, $F4xx        ; BC = AY register select (xx = register number)
OUT (C), A          ; Select register

; Write to AY register
LD BC, $F600        ; PPI control
OUT (C), A
```

In practice, most CPC programmers use BIOS sound routines or a known working AY driver rather than programming the chip directly.

### Memory map

| Range | Contents |
|-------|----------|
| $0000–$3FFF | Lower ROM (BASIC/AMSDOS) or RAM (bank-switchable) |
| $4000–$7FFF | RAM |
| $8000–$BFFF | RAM |
| $C000–$FFFF | Upper ROM or RAM (bank-switchable) |

The **Gate Array** controls ROM banking. By default, both ROMs are visible. To access all 128 KB of RAM, you bank out the ROMs.

The CPC6128 has 8 × 16 KB RAM banks, switched via Gate Array port $7F00.

### I/O port map

| Port | Device | Notes |
|------|--------|-------|
| $7F00 | Gate Array | Mode, palette, RAM banking |
| $BC00 | CRTC (select register) | |
| $BD00 | CRTC (read/write register) | |
| $F400 | PPI port A (AY data) | |
| $F500 | PPI port B (cassette, screen refresh, joystick) | |
| $F600 | PPI port C (AY register select, motor control) | |
| $F700 | PPI mode control | |

## Setting screen mode and palette

```asm
; Set Mode 1 (320x200, 4 colours) via Gate Array
LD BC, $7F8D        ; Gate Array port ($7F00), value $8D = Mode 1 + IRQ reset
OUT (C), C

; Set palette colour 0 to bright white (ink 26 in CPC notation)
LD BC, $7F00        ; Gate Array
LD A, $40           ; "Set colour" command: $40 | pen number
OUT (C), A          ; Set pen 0
LD A, $40 + 26      ; Colour value: 26 = bright white
OUT (C), A
```

CPC colour values (the 27 palette colours are indexed 0–26 in a specific order — use a reference table; the numbering is non-obvious).

## Screen RAM layout

The CPC screen is at a configurable address (set via CRTC). The default address is **$C000** for a full-screen display.

In **Mode 1** (320×200, 4 colours), each byte holds 4 pixels (2 bits per pixel). The pixel packing is:

```
Byte bit layout (Mode 1):
Pixel 0: bits 7,3  (bit 7 = high bit, bit 3 = low bit)
Pixel 1: bits 6,2
Pixel 2: bits 5,1
Pixel 3: bits 4,0
```

This interleaved bit pattern is the CPC's biggest quirk — it differs from straightforward packed pixels. Writing `$F0` to a Mode 1 byte gives you pixels `(1,1,0,0)` not `(1,1,1,1)`.

Use a lookup table mapping colour index pairs to byte values:

```asm
; mode1_byte(c0, c1, c2, c3) lookup — use precalculated table
; or use the BIOS plot routines which handle this for you
```

## Reading the joystick

On the CPC, joystick data is read from **PPI port B** (`$F500`):

```asm
IN A, ($F500)
; Bit 6: Joystick 0 UP    (0 = pressed)
; Bit 7: Joystick 0 FIRE2
; (Other bits: Joystick 0 directions in bits 0-5 via different read)
```

Actually the joystick is spread across two reads — port B for up and fire2, and a keyboard matrix scan for the remaining directions. The CPC BIOS provides a cleaner interface:

```asm
; BIOS: Read joystick 0
LD A, $03
CALL $BB24          ; KM READ CHAR — reads input
```

## BIOS calls

The CPC Firmware (BIOS) provides extensive routines. A selection:

| Address | Name | Action |
|---------|------|--------|
| $BB06 | TXT OUTPUT | Output character in A |
| $BB57 | SCR SET MODE | Set screen mode (A=0/1/2) |
| $BB5A | SCR SET BORDER | Set border colour |
| $BB5D | SCR SET INK | Set ink colour |
| $BB75 | SCR DOT POSITION | Plot a pixel |
| $BB7E | SCR HORIZONTAL | Draw horizontal line |
| $BB8A | GRA LINE ABSOLUTE | Draw line to absolute coords |
| $BB24 | KM READ CHAR | Read keyboard character |
| $BB1E | KM WAIT CHAR | Wait for a keypress |
| $BCCE | MC WAIT FLYBACK | Wait for VBlank |

```asm
; Clear screen and set mode 1
LD A, 1
CALL $BB57          ; SCR SET MODE

; Print a character
LD A, 'A'
CALL $BB06          ; TXT OUTPUT
```

## Minimal working program

```asm
; CPC6128 — Hello World via firmware
; Load at $4000, call with CALL &4000 from BASIC

        ORG $4000

start:
        LD A, 1
        CALL $BB57          ; SCR SET MODE 1

        LD HL, message
print_loop:
        LD A, (HL)
        CP 0
        RET Z
        CALL $BB06          ; TXT OUTPUT
        INC HL
        JR print_loop

message:
        DEFM "HELLO, CPC!", 13, 10, 0

        END start
```

From BASIC: `LOAD "HELLO.BIN"` then `CALL &4000`.

## CPC Locomotive BASIC quick reference

```basic
10 MODE 1              : REM Set mode (0, 1, or 2)
20 BORDER 0            : REM Set border colour
30 INK 1,24            : REM Set ink 1 to colour 24
40 PAPER 0             : REM Set paper colour
50 PEN 1               : REM Set current text colour
60 PRINT "HELLO"
70 LOCATE 10,5         : REM Move text cursor to col 10, row 5
80 MOVE 100,100        : REM Move graphics cursor
90 DRAW 200,100        : REM Draw line
90 CIRCLE 160,100,50   : REM Draw circle
100 JOY(0)             : REM Read joystick (bit field)
```

## Demo effects — what the CPC is famous for

The CPC demo scene produces extraordinary effects by manipulating the CRTC mid-frame:

**Hardware scrolling**: change CRTC R12/R13 each frame to scroll the display without copying RAM.

**Raster colour changes**: change Gate Array palette registers each scanline for rainbow effects. Time your code against the CRTC's hsync signal.

**Mode switching**: switch between modes mid-screen for mixed-resolution displays.

**Overscan**: reprogram CRTC timing to display beyond the normal borders.

Most of these require cycle-exact timing knowledge — see the CPC wiki for detailed CRTC programming.

## Common mistakes

**Mode 1 pixel bit packing** — the interleaved bit layout catches everyone out. `$FF` is NOT 4 white pixels in Mode 1 — it's 4 pixels of colour 3. Use a lookup table for pixel-to-byte conversion.

**Gate Array palette numbering** — CPC colour codes (0–26) don't correspond to a simple RGB ordering. Use the standard CPC colour chart.

**Forgetting ROM banking** — if you try to write to $0000–$3FFF or $C000–$FFFF and nothing happens, you're probably writing to ROM. Bank it out via the Gate Array first.

**CRTC address** — the default screen address ($C000) is set by the BIOS. If you reprogram CRTC R12/R13, remember the value is in terms of CRTC character units (each = 2 bytes in Mode 1 or Mode 2, 4 bytes in Mode 0).

## See also

- [Z80 assembly](../assembly/z80.md) — full Z80 language reference
- [MSX platform guide](msx.md) — another Z80 machine with AY sound
- [IDE getting started](../ide/getting-started.md)

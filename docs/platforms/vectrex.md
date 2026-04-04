---
title: Vectrex
description: Vectrex platform guide — vector graphics, 6809 assembly, and CMOC C in the RGC IDE.
---

# Vectrex

The **Vectrex** (1982, General Consumer Electronics / Milton Bradley) is unlike any other home console: it draws graphics using **vector beams** on its built-in CRT monitor, not raster pixels. There are no pixels at all — the electron beam traces lines and dots directly onto the screen. The result is sharp, flicker-free graphics that look nothing like any other home system of the era.

It uses a **Motorola 6809** CPU at 1.5 MHz and an **AY-3-8912** sound chip. Its BIOS (built into a 8 KB ROM) provides a rich library of vector drawing routines that make programming it surprisingly accessible.

## Languages in the IDE

| Language | Notes |
|----------|-------|
| **6809 assembly** | Primary language — LWASM assembler |
| **CMOC C** | C cross-compiler targeting 6809 + Vectrex BIOS |

## Quick start

1. Select **Vectrex** as the platform.
2. Choose Assembly or C.
3. The template includes the correct ROM header and BIOS call setup.
4. Build — the IDE loads the cartridge image into the Vectrex emulator.

!!! tip "The BIOS is your friend"
    The Vectrex BIOS ROM provides dozens of high-level drawing, sound, and controller routines. Using them is much easier than programming the hardware directly, and they're what all commercial Vectrex games use.

## Hardware overview

### CPU — Motorola 6809 at 1.5 MHz

The 6809 runs at 1.5 MHz — see [6809 assembly](../assembly/6809.md) for the full language reference. The Vectrex's 6809 is the same chip as the Dragon/CoCo, but running slightly faster and with different peripherals.

### The vector display system

Instead of a framebuffer, the Vectrex has:

- An **X/Y DAC** (Digital-to-Analogue Converter) that controls the beam position
- A **Z-axis signal** (beam-on/beam-off) controlled by another DAC
- A **ramp generator** (MC3001) that moves the beam in a straight line at controlled speed

To draw a line, you:
1. Position the beam at the start point
2. Set the beam intensity (Z-axis)
3. Tell the ramp generator the direction and speed — it moves the beam steadily
4. After the right time, turn the beam off

This is all handled for you by the BIOS routines — you just provide a list of vectors.

### Vector list format

The BIOS draws shapes from a **vector list** — a sequence of `(scale, y, x)` triples:

```asm
my_shape:
        DB $00          ; End of list marker

; A simple square (relative coordinates):
my_square:
        DB $80, $50, $00    ; Move to (+80, 0) — no draw
        DB $00, $50, $50    ; Draw to (+80, +80)  (wait, see note below)
        DB $FF              ; End of list
```

The BIOS interprets each byte group as a move or draw command. The actual format is documented in the Vectrex BIOS reference — use the template as your starting point.

### AY-3-8912 — Sound

The **AY-3-8912** Programmable Sound Generator provides 3 tone channels plus a noise channel, accessed via a pair of I/O addresses. It's the same chip family used in the Amstrad CPC and MSX, and produces a characteristic "beepy" sound well-suited to arcade-style games.

```asm
; Write to AY-3-8912
; First: write register number to address $C800 (via 6522 VIA)
; Then: write value to $C900

AY_ADDR EQU $C800
AY_DATA EQU $C900

        LDA #7          ; AY register 7 = mixer
        STA AY_ADDR
        LDA #$38        ; Enable all tone channels, no noise
        STA AY_DATA
```

### Memory map

| Range | Contents |
|-------|----------|
| $0000–$7FFF | Cartridge ROM (your game) |
| $C800 | AY-3-8912 address latch |
| $C900 | AY-3-8912 data |
| $D000–$D7FF | 6522 VIA (I/O — controller, sound sync) |
| $E000–$FFFF | BIOS ROM (8 KB) |
| $F000–$F7FF | BIOS RAM area |
| $C000–$C7FF | RAM (1 KB) |

### 6522 VIA — I/O

The **6522 Versatile Interface Adapter** handles the controller, synchronises the sound chip, and coordinates the beam timing. Most of this is managed by the BIOS routines.

## The BIOS

The Vectrex BIOS ROM at $E000–$FFFF is the star of the show. It provides:

- **Drawing routines**: draw dot lists, line lists, patterns
- **Controller reading**: digital and analogue joystick
- **Sound**: note tables, ADSR envelopes, jingle playback
- **Maths**: multiply, divide, sine/cosine tables
- **Calibration**: automatic beam intensity calibration on startup

### Key BIOS calls

| Address | Routine | Action |
|---------|---------|--------|
| $F2EB | `Wait_Recal` | Wait for VBlank, recalibrate beam — **call every frame** |
| $F3AE | `Moveto_d` | Move beam to position in D (no draw) |
| $F406 | `Draw_Line_d` | Draw a line |
| $F5A4 | `Read_Btns` | Read controller buttons into A |
| $F5F2 | `Read_Joys_1_2` | Read joystick axes |
| $F160 | `Print_Str_hwyx` | Print a text string |
| $F956 | `Sound_Byte_raw` | Send byte to AY sound chip |

### Minimal working program

```asm
; Vectrex — draw a dot in the centre every frame
; LWASM syntax

        ORG $0000

; Cartridge header
        DB $67          ; Magic byte
        DB $00          ; Music data (none)
        DB $F8, $50     ; Height / width
        DB $00, $00     ; Relative Y/X position
        DB $00          ; End of header

title:  DB "MY GAME", $80   ; Title string ($80 = end)

start:
frame_loop:
        JSR $F2EB       ; Wait_Recal — MUST call every frame
                        ; Also recalibrates beam and reads controllers

        ; Move beam to centre (coordinates are signed, 0,0 = centre)
        LDA #$00
        LDB #$00
        JSR $F3AE       ; Moveto_d

        ; Draw a bright dot
        LDA #$7F        ; Intensity (0=off, $7F=full)
        JSR $F3DF       ; Dot_d (or equivalent dot draw routine)

        JMP frame_loop

        END start
```

!!! warning "Call Wait_Recal every frame"
    `Wait_Recal` (`$F2EB`) synchronises your game to the Vectrex's display cycle and recalibrates the beam. **If you don't call it every frame, the beam will drift off-screen.** This is the most important rule of Vectrex programming.

## Reading the controller

```asm
; Read buttons — result in A
        JSR $F5A4       ; Read_Btns
        ; Bit 0: Button 1 (0 = pressed)
        ; Bit 1: Button 2
        ; Bit 2: Button 3
        ; Bit 3: Button 4
        BIT #$01        ; Test button 1
        BEQ btn1_pressed

; Read analogue joystick axes
        JSR $F5F2       ; Read_Joys_1_2
        ; Results stored in system RAM locations:
        ; VIA_joy_1_x, VIA_joy_1_y (signed bytes, ~-128 to +127)
```

## Drawing text

```asm
; Print "SCORE" at position (y=50, x=-60) with scale 2
        LDA #2          ; Scale
        LDB #$32        ; Y position
        LDX #$C4        ; X position (negative = $C4 as signed byte)
        JSR $F160       ; Print_Str_hwyx — expects string pointer in...
                        ; (check BIOS docs for exact calling convention)
        DB "SCORE:", $80   ; $80 terminates string
```

## Coordinate system

Vectrex coordinates are **signed** with (0,0) at the **centre** of the screen:

- X increases to the **right** (range roughly -128 to +127)
- Y increases **upward** (range roughly -128 to +127)

This is different from raster machines where (0,0) is top-left. Bear in mind when positioning objects.

## Tips for Vectrex programming

**Intensity matters** — unlike raster machines where everything is either on or off, the Vectrex beam has a variable intensity (brightness). Drawing slower = brighter; drawing faster = dimmer. The BIOS routines handle this automatically for most calls.

**Flicker is a feature** — the beam can only be in one place at once, so complex scenes flicker. Managing draw time per frame is a key skill. Simple scenes with fewer/shorter vectors flicker less.

**Scale everything** — the BIOS drawing routines accept a scale parameter. Design your shapes at a convenient coordinate size and scale at runtime.

**No sprites — think differently** — there's no sprite engine. Everything is a list of vectors drawn each frame. Think of your objects as vector lists, not bitmaps.

**Sound is separate from display timing** — unlike raster machines, there's no VBlank-linked sound update. The BIOS's `Wait_Recal` does synchronise sound DMA, but you generally queue sound via BIOS calls rather than doing it manually.

## Official resources

- **[Vectrex Programming Manual](http://vide.malban.de/)** — VIDE IDE documentation includes BIOS reference
- **[Vectrex BIOS source](https://github.com/jamesirv/vectrex-game-development)** — community documentation of all BIOS calls

## See also

- [6809 assembly](../assembly/6809.md) — full 6809 language reference
- [CMOC C for 6809](../c/cmoc.md) — C on Vectrex
- [Dragon 32 / CoCo platform guide](dragon-coco.md) — other 6809 machines
- [IDE getting started](../ide/getting-started.md)

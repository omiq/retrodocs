---
title: MSX
description: MSX platform guide — Z80, TMS9918 VDP, and Z80 assembly in the RGC IDE.
---

# MSX

**MSX** (1983) was a standardised home computer architecture created by Microsoft and ASCII Corporation and adopted by manufacturers across Japan, Europe, and Brazil — Panasonic, Sony, Philips, Toshiba, and many others all made MSX machines. The idea was that software written for one MSX machine would run on any other, a novelty at the time.

The standard is built on a **3.58 MHz Zilog Z80** CPU, the **TMS9918A** Video Display Processor (the same chip used in the TI-99/4A and later the Sega Master System's predecessor), and the **AY-3-8910** Programmable Sound Generator.

## Languages in the IDE

| Preset | Language / toolchain |
|--------|---------------------|
| **MSX (BIOS)** | Z80 assembly using MSX BIOS calls |
| **MSX (libCV)** | Z80 assembly / C using ColecoVision-compatible libraries |

## Quick start

1. Select **MSX (BIOS)** or **MSX (libCV)** as the platform.
2. Load the Assembly template — it shows the ROM header and startup code.
3. Build and run in the MSX emulator.

!!! note "BIOS vs libCV presets"
    **MSX (BIOS)** targets the MSX BIOS directly — portable across all MSX machines. **MSX (libCV)** uses libraries originally written for the ColecoVision (which shares the TMS9918A and AY-3-8910 chips) — useful for cross-development between the two platforms.

## Hardware overview

### CPU — Z80 at 3.58 MHz

Standard Zilog Z80 — see [Z80 assembly](../assembly/z80.md) for the full instruction set. The MSX runs the Z80 at 3.58 MHz, the same speed as most arcade Z80 boards.

### VDP — TMS9918A Video Display Processor

The **TMS9918A** is a dedicated video chip with its own 16 KB of VRAM (completely separate from the main Z80 address space). The CPU communicates with it via two I/O ports:

| Port | Direction | Purpose |
|------|-----------|---------|
| $98 | Write | VRAM data write |
| $98 | Read | VRAM data read |
| $99 | Write | VDP control (register write / VRAM address set) |
| $99 | Read | VDP status register |

The TMS9918A supports several video modes:

| Mode | Resolution | Sprites | Notes |
|------|------------|---------|-------|
| **Mode 0** (Text) | 40×24 text | No sprites | 2 colours only |
| **Mode 1** (Graphics I) | 32×24 tiles | 32 sprites | 16 colours, 256 tiles |
| **Mode 2** (Graphics II) | 256×192 pixels | 32 sprites | Per-tile colour, full bitmap |
| **Mode 3** (Multicolour) | 64×48 blocks | 32 sprites | 4×4 colour blocks |

**Graphics II (Mode 2)** is what most MSX games use — it gives a full 256×192 pixel display with per-8-pixel-row colour control.

### PSG — AY-3-8910

The **AY-3-8910** Programmable Sound Generator (same family as the Spectrum 128K's AY chip) provides 3 tone channels, 1 noise channel, and envelope control. On MSX, it's accessed via the PPI (Programmable Peripheral Interface) — not directly via Z80 I/O ports.

### MSX slot system

MSX uses a **slot** system for memory: the 64 KB address space is divided into four 16 KB pages, each of which can be mapped to any of up to four hardware slots (ROMs, RAM, cartridges). The BIOS manages this, but understanding it matters for cartridge development.

The main RAM is typically in slot 3; the BIOS ROM is in slot 0.

### Memory map (typical MSX1)

| Range | Contents |
|-------|----------|
| $0000–$7FFF | BIOS ROM + cartridge ROMs (slot-dependent) |
| $8000–$9FFF | Cartridge ROM page 2 (if present) |
| $A000–$BFFF | Cartridge ROM / BASIC ROM |
| $C000–$FFFF | RAM (16–64 KB depending on model) |

System variables and the BASIC work area are in RAM starting around $F380.

## Using the MSX BIOS

The MSX BIOS provides a standardised set of routines accessible via `CALL` at fixed addresses:

| Address | Name | Action |
|---------|------|--------|
| $00C | DOSCAL | Invoke MSX-DOS |
| $0090 | ERAFNK | Erase function key display |
| $009F | DSPFNK | Display function key names |
| $00A2 | TOTEXT | Switch to TEXT mode |
| $00CF | CHPUT | Output character in A to screen |
| $00D2 | POSIT | Move cursor to (H=row, L=col) |
| $00D5 | FNKSB | Check function key input |
| $00D8 | ERAFNK | Erase function key line |
| $00DB | DSPFNK | Display function key line |

```asm
; Print 'A' to screen via BIOS CHPUT
LD A, 'A'
CALL $00CF          ; CHPUT
```

### Writing to the VDP

Setting a VRAM write address and writing data:

```asm
VDP_DATA    EQU $98
VDP_CTRL    EQU $99

; Set VRAM write address to $1800 (Name Table in Graphics I mode)
LD A, $00           ; Low byte of address
OUT (VDP_CTRL), A
LD A, $58           ; High byte | $40 (write bit)
OUT (VDP_CTRL), A   ; Two writes set the address

; Write tile index 5 to first cell
LD A, 5
OUT (VDP_DATA), A
```

### Reading VDP status

```asm
IN A, (VDP_CTRL)    ; Read VDP status
BIT 7, A            ; Bit 7 = VBlank flag (1 = in VBlank)
JR Z, not_vblank
```

## Minimal working program

```asm
; MSX — Hello World using BIOS CHPUT
; Assemble and load as a binary, call from BASIC with BLOAD"file",R

        ORG $C000       ; Load into RAM

start:
        LD HL, message
print_loop:
        LD A, (HL)
        CP 0
        RET Z           ; Return when we hit the null terminator
        CALL $00CF      ; BIOS CHPUT — print character in A
        INC HL
        JR print_loop

message:
        DEFM "HELLO, MSX!", 13, 10, 0

        END start
```

From MSX BASIC:
```basic
BLOAD "HELLO.BIN",R
```

## MSX Cartridge ROM header

For cartridge development (the IDE preset uses this format):

```asm
        ORG $4000       ; Cartridge ROM starts here

; ROM header
header:
        DB 'A', 'B'     ; Magic bytes — identifies this as a ROM cartridge
        DW start        ; INIT address (called on startup)
        DW 0            ; STATEMENT address (0 = none)
        DW 0            ; DEVICE address (0 = none)
        DW 0            ; TEXT address (0 = none)
        DS 6, 0         ; Reserved

start:
        ; Your code here
        RET
```

## MSX-BASIC quick reference

MSX BASIC is Microsoft BASIC — similar to Commodore BASIC V2 and Color BASIC but with MSX-specific extensions:

```basic
10 SCREEN 2           : REM Graphics II mode (256x192, 16 colours)
20 COLOR 15,1,1       : REM Ink=white, background=black, border=black
30 CLS
40 LINE (0,0)-(255,191),15  : REM Draw a line in colour 15 (white)
50 CIRCLE (128,96),50,12    : REM Draw a circle, colour 12
60 PSET (128,96),14         : REM Plot a pixel, colour 14
70 STRIG(0)                 : REM Read trigger button (1=pressed)
80 STICK(0)                 : REM Read joystick direction (1-8, 0=centre)
```

## Tips for MSX development

**VRAM is separate from RAM** — the TMS9918A has its own 16 KB of VRAM accessed only through I/O ports, not via the Z80 address space. All tile data, sprite data, colour tables, and name tables live in VRAM.

**Mode 2 colour works per-8-pixel-row** — in Graphics II mode, each 8-pixel row of a tile has its own foreground and background colour. This gives per-row colour control, unlike the 6502 machines where colour is often per character cell.

**32 sprites on screen, 4 per scanline** — the TMS9918A supports up to 32 sprites but only shows 4 per scanline. If you have more than 4 sprites on the same horizontal line, the lowest-numbered 4 take priority.

**Use the BIOS for I/O** — the MSX BIOS standardises hardware access across all MSX machines. Using BIOS calls instead of direct I/O means your program runs on every MSX, regardless of manufacturer.

**Slot access** — if you need more than 64 KB or access to multiple ROMs simultaneously, you need to manage the slot system. The BIOS provides `ENASLT` and related routines for this.

## See also

- [Z80 assembly](../assembly/z80.md) — full Z80 language reference
- [Z88DK C for Z80](../c/z88dk.md) — z88dk supports MSX as a target
- [Amstrad CPC platform guide](cpc.md) — another AY-3-891x sound chip machine
- [IDE getting started](../ide/getting-started.md)

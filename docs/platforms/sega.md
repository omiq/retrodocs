---
title: Sega Master System & Game Gear
description: Sega Master System and Game Gear platform guide — Z80 assembly in the RGC IDE.
---

# Sega Master System & Game Gear

The **Sega Master System** (1985 in Japan as the Sega Mark III) and the **Sega Game Gear** (1990) are closely related Z80-based platforms. The Game Gear is essentially a portable Master System with a smaller, backlit colour screen and a slightly different memory layout.

Both machines use a **3.58 MHz Zilog Z80** and the **Sega VDP** (Video Display Processor, based on the Texas Instruments TMS9918A with enhancements). They're well-documented, have a growing homebrew scene, and the Z80 assembly knowledge transfers almost completely between the two.

## Languages in the IDE

| Language | Notes |
|----------|-------|
| **Z80 assembly** | Primary language for both platforms |

## Quick start

1. Select **Sega Master System** or **Sega Game Gear** as the platform.
2. The Assembly preset loads a template with the correct ROM header and startup code.
3. Build — the IDE loads the ROM into the emulator.

!!! tip "Start with the template"
    The ROM header (including the SEGA magic string and checksum) must be present and correct or the BIOS will refuse to run your program. The template handles this for you — don't delete it.

## Hardware overview

### CPU — Z80 at 3.58 MHz

Standard Z80 — see the [Z80 assembly guide](../assembly/z80.md) for the full instruction set. The Master System Z80 runs at 3.58 MHz (NTSC) or 3.55 MHz (PAL).

### VDP — Video Display Processor

The **VDP** is the heart of the graphics system. It manages:

- **Background (Name Table)**: 32×28 tiles of 8×8 pixels, from VRAM
- **Sprites**: up to 64 sprites (8×8 or 8×16 pixels), 8 per scanline
- **Palette**: 32 colours total (16 for backgrounds, 16 for sprites), chosen from 64 possible colours (6-bit RGB, 2 bits per channel)
- **Scrolling**: hardware X and Y scroll for the background

The VDP sits at I/O ports $BE (data) and $BF (control/status):

```asm
; Write to VDP control port
LD A, value
OUT ($BF), A

; Write to VDP data port
LD A, data
OUT ($BE), A
```

**Always access the VDP via the I/O ports — never via memory-mapped addresses on the SMS.**

### PSG — Sound

The **SN76489** Programmable Sound Generator provides 3 square-wave channels and 1 noise channel, accessed via port $7E:

```asm
; Set channel 0 frequency (lower nibble of tone register)
LD A, %10000000     ; Latch, channel 0, tone
OUT ($7E), A
LD A, low_byte      ; Frequency low 4 bits
OUT ($7E), A

; Set channel 0 volume (0=max, 15=silent)
LD A, %10010000     ; Latch, channel 0, volume
OR volume           ; OR in the 4-bit volume value
OUT ($7E), A
```

### Memory map (Master System)

| Range | Contents |
|-------|----------|
| $0000–$03FF | ROM slot 0 first 1 KB (always mapped — contains ROM header) |
| $0000–$3FFF | ROM slot 0 (16 KB) |
| $4000–$7FFF | ROM slot 1 (16 KB) |
| $8000–$BFFF | ROM slot 2 (16 KB, or cartridge RAM) |
| $C000–$DFFF | RAM (8 KB) |
| $E000–$FFFF | RAM mirror |
| $FFFC–$FFFF | Memory control registers (paging) |

I/O ports:

| Port | Device |
|------|--------|
| $7E | PSG (write), V counter (read) |
| $7F | PSG (write), H counter (read) |
| $BE | VDP data |
| $BF | VDP control / status |
| $DC | I/O port A (joystick 1, joystick 2 partial) |
| $DD | I/O port B (joystick 2 partial, misc) |

### Memory map (Game Gear)

The Game Gear is mostly compatible with the Master System at the hardware level, with these differences:

- Screen resolution: **160×144** pixels (vs SMS 256×192)
- Palette: **12-bit colour** (4 bits per channel, 4096 colours) vs SMS 6-bit
- Palette registers at ports $00–$01 (GG) vs VDP internal (SMS)
- Start button at port $00 bit 7

## The ROM header

Every Master System/Game Gear ROM must have a valid header at $7FF0:

```asm
        ORG $7FF0

header:
        DB "TMR SEGA"       ; Magic string (8 bytes)
        DW $0000            ; Reserved
        DW $0000            ; Checksum
        DB $00, $00, $00    ; Product code (3 digits BCD)
        DB $00              ; Version
        DB $05              ; Region / size ($05 = SMS export, 32KB)
```

The template in the IDE includes a correct header — always build from the template.

## Startup code

```asm
        ORG $0000

; Interrupt handlers
        DI                  ; Disable interrupts
        IM 1                ; Set interrupt mode 1 (RST $38 on IRQ)
        LD SP, $DFF0        ; Set stack pointer to top of RAM

; Clear RAM
        LD HL, $C000
        LD BC, $2000
        XOR A
        CALL clear_mem      ; Fill BC bytes at HL with A

; Initialise VDP
        CALL init_vdp

; Enable interrupts and enter main loop
        EI
        JP main

clear_mem:
        LD (HL), A
        INC HL
        DEC BC
        LD A, B
        OR C
        LD A, $00
        JR NZ, clear_mem
        RET
```

## VDP — Writing to VRAM

Setting the VRAM write address:

```asm
SET_VRAM_ADDR: MACRO addr
        LD A, LOW(addr)
        OUT ($BF), A
        LD A, HIGH(addr) | $40  ; $40 = write mode
        OUT ($BF), A
        ENDM
```

Writing tile data to VRAM:

```asm
; Write a single 4bpp tile (32 bytes) to VRAM at address $0000
        SET_VRAM_ADDR $0000
        LD HL, tile_data
        LD B, 32
write_tile:
        LD A, (HL)
        OUT ($BE), A
        INC HL
        DJNZ write_tile
```

## Setting the palette

```asm
; Write to palette (CRAM) via VDP
; First set CRAM write address
        LD A, $00
        OUT ($BF), A
        LD A, $C0           ; $C0 = CRAM write mode
        OUT ($BF), A

; Write colour: SMS format = %00BBGGRR (2 bits per channel)
        LD A, %00000011     ; Red (max R, no G, no B)
        OUT ($BE), A
```

## Reading the joypad

```asm
READ_JOY:
        IN A, ($DC)         ; Read port A
        ; Bit 0: P1 Up    (0=pressed)
        ; Bit 1: P1 Down
        ; Bit 2: P1 Left
        ; Bit 3: P1 Right
        ; Bit 4: P1 Button 1
        ; Bit 5: P1 Button 2
        ; Bit 6: P2 Up
        ; Bit 7: P2 Down
        CPL                 ; Invert (now 1=pressed)
        LD (joy_state), A
        RET
```

## Minimal hello world

```asm
; SMS — set background colour and write a tile to name table
        ORG $0000

INIT:
        DI
        IM 1
        LD SP, $DFF0

        ; Set VDP register 1 — enable display
        LD A, $A0           ; Display on, frame IRQ on
        OUT ($BF), A
        LD A, $81           ; Register 1
        OUT ($BF), A

        ; Set background colour (palette entry 0) to dark blue
        LD A, $00           ; CRAM address 0
        OUT ($BF), A
        LD A, $C0           ; CRAM write mode
        OUT ($BF), A
        LD A, %00110000     ; Blue
        OUT ($BE), A

LOOP:
        JP LOOP             ; Spin forever (interrupt-driven game loop goes here)
```

## Game Gear differences

If targeting Game Gear specifically:

- Use **12-bit palette** — each colour entry is 2 bytes: `%0000BBBB` then `%GGGGRRRR`
- The **visible area** is 160×144 (centred in the VDP's 256×192 buffer)
- Read the **Start button** from port $00 bit 7 (active low)
- The **power LED** and battery status are also accessible via I/O

Most Master System code runs on Game Gear with palette and viewport adjustments.

## Common mistakes

**Missing or wrong ROM header** — the BIOS checks the "TMR SEGA" magic string and the checksum. A wrong header means a blank screen (BIOS refuses to run your code).

**Accessing VDP during active display** — on real hardware, accessing VRAM during the active display area causes graphical glitches. Write to VRAM only during VBlank (in the VDP interrupt handler).

**Forgetting to latch VDP address** — `OUT ($BF)` must be done **twice** (low byte then high byte with mode bits) before each VRAM access. A single write changes the VDP's internal register, not the address.

**8 sprites per scanline limit** — only 8 sprites can be visible on any one scanline. If you have more, the extras (those with the highest sprite numbers) are dropped.

## See also

- [Z80 assembly](../assembly/z80.md) — full Z80 language reference
- [ZX Spectrum platform guide](zx-spectrum.md) — another Z80 machine with different hardware
- [MSX platform guide](msx.md) — yet another Z80 platform
- [IDE getting started](../ide/getting-started.md)

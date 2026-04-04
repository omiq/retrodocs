---
title: NES / Famicom
description: NES platform guide — PPU, APU, cartridge layout, and 6502 assembly in the RGC IDE.
---

# NES / Famicom

The **Nintendo Entertainment System** (NES, 1983 in Japan as Famicom, 1985 in North America) is the most documented 8-bit console of all time. It uses a **Ricoh 2A03** CPU — essentially a 6502 at 1.79 MHz with the decimal mode disabled — paired with dedicated **PPU** (graphics) and **APU** (audio) chips.

Unlike home computers, the NES has **no OS** and **no BASIC interpreter**. Your cartridge ROM is everything — it supplies the reset vector, the interrupt handlers, and all the code. This makes NES programming more demanding than C64 or Spectrum programming, but also gives you complete control.

## Languages in the IDE

| Language | Use for |
|----------|---------|
| **6502 / ca65 assembly** | Primary language — most NES code is assembly |
| **cc65 C (with NES target)** | Higher-level structure, with caveats (see below) |

!!! note "C on the NES"
    The NES has strict timing requirements (PPU must be driven in sync with the TV) and limited RAM. While cc65 supports an NES target, most production NES code is assembly. C is useful for game logic but assembly is typically needed for rendering code.

## Quick start

1. Select **NES** as the platform and **Assembly** as the language.
2. Load the example — it shows the iNES header, startup code, and a minimal game loop structure.
3. Build; the IDE loads the resulting `.nes` ROM into an NES emulator.

!!! tip "The NES has strict timing"
    The NES PPU requires that you don't access VRAM outside of VBlank. Most beginner crashes are caused by reading/writing PPU registers at the wrong time. Read the template comments carefully.

## Hardware overview

### CPU — Ricoh 2A03 (modified 6502) at 1.79 MHz (NTSC)

The 2A03 is a 6502 with the decimal mode instruction (`SED`/`CLD` still exist, but ADC/SBC don't use BCD). It's otherwise identical — same registers, same addressing modes, same instruction timings.

The 2A03 also includes the **APU** (Audio Processing Unit) built directly into the CPU chip.

### PPU — Picture Processing Unit

The **PPU** ($2000–$3FFF in the CPU address space) generates the video signal independently of the CPU. It has its own 2 KB of VRAM and a 256-byte Object Attribute Memory (OAM) for sprite data.

PPU features:
- **Background**: Tile-based, 32×30 tiles of 8×8 pixels each (256×240 pixels total)
- **Sprites**: Up to 64 hardware sprites (8×8 or 8×16 pixels), 8 per scanline
- **Scrolling**: Hardware scroll in X and Y
- **Palettes**: 4 background palettes × 4 colours, 4 sprite palettes × 3 colours + transparent

The **TV safe area** is roughly 256×224 pixels (NTSC loses the top and bottom 8 rows).

### Key PPU registers

| Address | Register | Purpose |
|---------|---------|---------|
| $2000 | PPUCTRL | NMI enable, sprite size, VRAM increment, base nametable |
| $2001 | PPUMASK | Rendering enable, colour emphasis |
| $2002 | PPUSTATUS | VBlank flag, sprite 0 hit |
| $2003 | OAMADDR | OAM address to write |
| $2004 | OAMDATA | OAM data write |
| $2005 | PPUSCROLL | Background scroll X/Y |
| $2006 | PPUADDR | VRAM address (write twice: high then low) |
| $2007 | PPUDATA | VRAM data read/write |
| $4014 | OAMDMA | Trigger DMA copy of 256 bytes to OAM |

**Never read/write $2006/$2007 (VRAM) outside of VBlank** — the PPU is rendering from VRAM during the visible frame, and accessing it causes graphical corruption.

### APU — Audio Processing Unit

The APU (mapped to $4000–$4017 in the CPU address space) has 5 channels:

| Channel | Addresses | Waveform |
|---------|-----------|---------|
| Pulse 1 | $4000–$4003 | Square wave with variable duty cycle |
| Pulse 2 | $4004–$4007 | Square wave |
| Triangle | $4008–$400B | Triangle wave (no volume control) |
| Noise | $400C–$400F | Pseudo-random noise |
| DMC | $4010–$4013 | Delta PCM (sampled audio) |

## Memory map

| Range | Contents |
|-------|----------|
| $0000–$07FF | 2 KB internal RAM (mirrored to $1FFF) |
| $0000–$00FF | Zero page |
| $0100–$01FF | Stack |
| $0200–$02FF | Often used for OAM shadow buffer |
| $2000–$2007 | PPU registers (mirrored every 8 bytes to $3FFF) |
| $4000–$4017 | APU and I/O registers |
| $4020–$5FFF | Cartridge expansion (mapper-dependent) |
| $6000–$7FFF | Cartridge WRAM / SRAM (optional) |
| $8000–$BFFF | PRG ROM bank 0 (or switchable) |
| $C000–$FFFF | PRG ROM bank 1 (or fixed) |
| $FFFA/$FFFB | NMI vector |
| $FFFC/$FFFD | RESET vector |
| $FFFE/$FFFF | IRQ/BRK vector |

## The game loop — VBlank timing

NES programs are structured around the **VBlank NMI** (Non-Maskable Interrupt) — a signal the PPU sends to the CPU at the start of each vertical blanking period (~1/60 second on NTSC).

A standard NES program structure:

```asm
    ; Minimal NES startup (ca65 syntax)
    .segment "HEADER"
    .byte "NES", $1A    ; iNES magic
    .byte 2             ; 2x 16KB PRG ROM banks
    .byte 1             ; 1x 8KB CHR ROM bank
    .byte 0, 0          ; Mapper 0 (NROM), flags

    .segment "CODE"

RESET:
    SEI                 ; Disable IRQs
    CLD                 ; Clear decimal mode
    LDX #$FF
    TXS                 ; Set stack pointer

    ; Wait for PPU to warm up (2 VBlanks)
    BIT $2002
wait1:
    BIT $2002
    BPL wait1
wait2:
    BIT $2002
    BPL wait2

    ; Clear RAM
    LDA #0
    LDX #0
clear_ram:
    STA $0000,X
    STA $0100,X
    STA $0200,X
    STA $0300,X
    STA $0400,X
    STA $0500,X
    STA $0600,X
    STA $0700,X
    INX
    BNE clear_ram

    ; Enable NMI, set sprite table to $0000, BG to $1000
    LDA #%10001000
    STA $2000           ; PPUCTRL

    ; Enable rendering
    LDA #%00011110
    STA $2001           ; PPUMASK

main_loop:
    ; Game logic goes here (runs every frame, CPU side)
    ; Wait for NMI to signal VBlank completion
    LDA nmi_done
    BEQ main_loop       ; Wait until NMI sets this flag
    LDA #0
    STA nmi_done

    JMP main_loop

NMI:
    ; VBlank handler — PPU update happens here
    ; Copy OAM shadow to PPU
    LDA #$02
    STA $4014           ; DMA from $0200 to OAM (takes 513 cycles)

    ; Update scroll
    LDA #0
    STA $2005           ; X scroll
    STA $2005           ; Y scroll

    LDA #1
    STA nmi_done        ; Signal main loop that VBlank is done
    RTI

IRQ:
    RTI                 ; Unused

    .segment "VECTORS"
    .word NMI
    .word RESET
    .word IRQ

    .segment "CHARS"
    .res 8192           ; 8KB CHR ROM (tile data)
```

## Sprites (OAM)

The PPU has 256 bytes of **Object Attribute Memory (OAM)** — 4 bytes per sprite, 64 sprites total:

| OAM byte | Purpose |
|----------|---------|
| 0 | Y position (top of sprite, subtract 1 for display position) |
| 1 | Tile index |
| 2 | Attributes (palette bits 0–1, priority bit 5, flip H bit 6, flip V bit 7) |
| 3 | X position |

The fastest way to update sprites is to maintain a **256-byte shadow OAM** at $0200 in RAM and use the DMA transfer:

```asm
LDA #$02        ; High byte of $0200
STA $4014       ; Trigger OAM DMA — takes 513 CPU cycles
```

This copies all 256 bytes (64 sprites) to the PPU's OAM in one operation, during VBlank.

## Controllers

NES controllers are read via shift registers at $4016 (player 1) and $4017 (player 2):

```asm
ReadController:
    LDA #1
    STA $4016           ; Latch buttons
    LDA #0
    STA $4016           ; Release latch

    ; Read 8 buttons: A, B, Select, Start, Up, Down, Left, Right
    LDX #8
.read_loop:
    LDA $4016           ; Read one bit
    AND #1              ; Bit 0 = button state
    ; Store the bit (common pattern: shift into a byte)
    ROR buttons_p1      ; Rotate into accumulator from carry
    DEX
    BNE .read_loop
    RTS
```

Button order in the result byte (bit 7 to bit 0): A, B, Select, Start, Up, Down, Left, Right.

## Common mistakes for NES beginners

**Accessing VRAM outside VBlank** — the most common beginner error. Always confine $2006/$2007 writes to your NMI handler.

**Not waiting for PPU warm-up** — the PPU takes ~2 frames to initialise after power-on. The reset handler must wait for 2 VBlanks before touching the PPU.

**Stack overflow** — the NES only has 256 bytes of stack ($0100–$01FF). Deep subroutine nesting or many nested interrupts can overflow it.

**Sprite 0 hit without sprite 0 on screen** — the sprite 0 hit flag in $2002 only triggers if sprite 0's opaque pixels overlap the background. If sprite 0 is off-screen or all transparent, the flag never fires.

**Forgetting RTI in the NMI** — if your NMI handler returns with `RTS` instead of `RTI`, the status register won't be restored and the CPU will misbehave.

## See also

- [6502 assembly](../assembly/6502.md) — the core language for NES development
- [cc65 / C](../c/cc65.md) — C compilation with the cc65 NES target
- [IDE getting started](../ide/getting-started.md)

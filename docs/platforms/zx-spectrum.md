---
title: ZX Spectrum
description: ZX Spectrum platform guide — hardware, memory, screen layout, and languages in the RGC IDE.
---

# ZX Spectrum

The **ZX Spectrum** (1982) is one of the most beloved home computers ever made. Designed by Sir Clive Sinclair and launched at just £125, it put computing into hundreds of thousands of British homes. The 48K model with its rubber keys remains a cultural icon.

It uses a **3.5 MHz Zilog Z80** CPU, has **48 KB of RAM** (on the 48K model), and a distinctive colour scheme based on "attributes" — a system that gives the Spectrum its look and its infamous **colour clash**.

## Languages in the IDE

| Language | Preset | Use for |
|----------|--------|---------|
| **ZX BASIC (Boriel)** | ZX Spectrum ZX BASIC | Compiled BASIC — fast, modern syntax |
| **Z88DK C** | ZX Spectrum C | C for Z80 — powerful, full standard library |
| **Z80 assembly** | ZX Spectrum Assembly | Maximum performance and direct hardware access |

## Quick start

1. Select **ZX Spectrum** as the platform.
2. Choose your language.
3. The IDE uses a JavaScript Spectrum emulator — you'll see the familiar loading screen.
4. Build and your program runs automatically.

!!! tip "Spectrum keyboard in the emulator"
    The Spectrum has unusual key mappings — symbols are accessed via CAPS SHIFT and SYMBOL SHIFT. The emulator typically maps these to your keyboard's modifier keys. For BASIC keywords, Spectrum BASIC normally auto-inserts them on key press — but in the IDE you're editing source text, so just type the keywords out.

## Hardware overview

### CPU — Zilog Z80 at 3.5 MHz

The Z80 runs at 3.5 MHz on the 48K Spectrum. It's an 8/16-bit processor with a rich instruction set, alternate register sets, and powerful block-move instructions (`LDIR`, `LDDR`). See [Z80 assembly](../assembly/z80.md) for the full picture.

The CPU is **contended** — it shares the bus with the ULA (the video chip), which slows it down by stealing memory cycles during the display period. Code running during the display area is slower than code running during the border or blanking period.

### ULA — Video and I/O

The **ULA** (Uncommitted Logic Array) is the Spectrum's custom chip — it handles video output, keyboard scanning, and the tape interface.

The screen is **256×192 pixels** in a **32×24** character grid. It's unusual in two ways:

**Pixel data and colour data are stored separately:**

- Pixel RAM: $4000–$57FF (6144 bytes)
- Attribute RAM: $5800–$5AFF (768 bytes — one byte per 8×8 character cell)

**Pixel rows are stored non-linearly** — the order within each third of the screen is scrambled. This was a hardware quirk that saved Sinclair the cost of more video RAM chips.

### The attribute system

Each 8×8 character cell has one attribute byte controlling colour:

```
Bit 7: FLASH (alternates ink/paper)
Bit 6: BRIGHT (brighter colours)
Bits 5–3: PAPER colour (0–7)
Bits 2–0: INK colour (0–7)
```

Spectrum colour palette (same index for ink and paper):

| Index | Normal | Bright |
|-------|--------|--------|
| 0 | Black | Black |
| 1 | Blue | Bright Blue |
| 2 | Red | Bright Red |
| 3 | Magenta | Bright Magenta |
| 4 | Green | Bright Green |
| 5 | Cyan | Bright Cyan |
| 6 | Yellow | Bright Yellow |
| 7 | White | Bright White |

**Colour clash** happens when two objects that are different colours share the same 8×8 attribute cell — one colour overwrites the other's attribute. This is the Spectrum's most distinctive limitation. Smart game design works around it by using one colour per character cell deliberately.

### Sound

The Spectrum has a **1-bit beeper** — a single piezo speaker controlled by toggling bit 4 of port $FE. This sounds like a severe limitation, but talented programmers have produced remarkably rich music from it using rapid pulse-width modulation techniques.

In ZX BASIC:
```basic
BEEP 0.5, 0   ' 0.5 seconds, note 0 (middle C)
BEEP 0.25, 12 ' 0.25 seconds, one octave up
```

## Memory map (48K)

| Range | Contents |
|-------|----------|
| $0000–$3FFF | ROM (16 KB — BASIC interpreter and routines) |
| $4000–$57FF | Screen pixel data (6144 bytes) |
| $5800–$5AFF | Screen attribute data (768 bytes) |
| $5B00–$5BFF | Print buffer |
| $5C00–$5CBF | System variables |
| $5CB6–$FFFF | Free RAM (BASIC program starts here) |

Your machine code programs typically load above the BASIC program and the BASIC stack — often around $7530 or higher. Use `CLEAR address` from BASIC to reserve space before loading.

## The non-linear pixel layout

The 48K Spectrum stores pixel rows in a scrambled order — this catches everyone out at least once.

For a pixel at row Y (0–191), column X (0–31 — each byte is 8 horizontal pixels):

```
Address = $4000
        + ((Y & 7) << 8)        ; row within character
        + ((Y >> 3) & 7) << 5   ; character row within third
        + (Y >> 6) << 11        ; which third (0, 1, or 2)
        + X                     ; column
```

In C (z88dk):
```c
unsigned char *pixel_row(int y, int x) {
    return (unsigned char*)0x4000
        + ((y & 7) << 8)
        + ((y & 0x38) << 2)
        + ((y >> 6) << 11)
        + x;
}
```

Most people use a lookup table of 192 pre-calculated row addresses.

## Attribute address

The attribute for character row R, column C is simply:

```
Attribute address = $5800 + R * 32 + C
```

This is much more straightforward than the pixel address.

## Keyboard scanning

The Spectrum keyboard is a 5×8 matrix scanned through port $FE. The high byte of the I/O address selects the row; bits 0–4 of the result indicate the five keys in that row (0 = pressed):

| Port high byte | Row | Keys (bit 0→4) |
|---------------|-----|----------------|
| $FE | 0 | CAPS, Z, X, C, V |
| $FD | 1 | A, S, D, F, G |
| $FB | 2 | Q, W, E, R, T |
| $F7 | 3 | 1, 2, 3, 4, 5 |
| $EF | 4 | 0, 9, 8, 7, 6 |
| $DF | 5 | P, O, I, U, Y |
| $BF | 6 | ENTER, L, K, J, H |
| $7F | 7 | SPACE, SYM SHIFT, M, N, B |

In Z80 assembly:
```asm
    LD A, $FE
    IN A, ($FE)     ; Read row 0 (CAPS Z X C V)
    BIT 0, A        ; Test CAPS SHIFT
    JR Z, caps_pressed
```

In ZX BASIC (Boriel):
```basic
IF MULTIKEYS(32) THEN   ' Space bar
    ' ...
END IF
```

## 128K Spectrum

The later **128K Spectrum** (and +2/+3 models) added:

- **128 KB RAM** (paged in 16 KB banks via port $7FFD)
- **AY-3-8912 sound chip** — 3 channels, proper envelope control
- Second ROM with 128 BASIC editor

The 128K machines are mostly compatible with 48K software. For new programs, the AY sound chip is a huge upgrade over the beeper.

## Port $FE — border and sound

Port $FE is a busy port on the Spectrum:

```
Write:
  Bits 2–0: Border colour (0–7)
  Bit 3: MIC output (tape)
  Bit 4: EAR/speaker output (for beeper sound)

Read:
  Bits 4–0: Keyboard row data
  Bit 6: EAR input (tape loading)
```

So setting the border colour is just an `OUT` instruction:
```asm
LD A, 2         ; Red
OUT ($FE), A
```

## Tips for Spectrum programming

**Plan around attribute clash** — the most successful Spectrum games work with the attribute system rather than against it. Use one colour scheme per character cell, or monochrome sprites with a coloured background.

**Use LDIR for fast fills and copies** — the Z80's `LDIR` block copy instruction is invaluable for clearing the screen or copying sprite data.

**Know the contention map** — code running at $4000–$7FFF is subject to ULA contention (slower access). Put time-critical code in RAM above $8000 if possible.

**ROM routines are your friend** — the Spectrum ROM has well-documented print, input, and maths routines. Using them saves code space and avoids reimplementing the wheel.

**Two-colour sprites avoid attribute clash** — monochrome sprites that use only ink colour (or only paper) don't cause clash because they don't change the attribute byte. Many Spectrum games use this approach.

## See also

- [ZX BASIC (Boriel)](../basic/zx-basic.md) — compiled BASIC for the Spectrum
- [Z88DK / C for Z80](../c/z88dk.md) — C compilation for the Spectrum
- [Z80 assembly](../assembly/z80.md) — Z80 language reference
- [IDE getting started](../ide/getting-started.md)

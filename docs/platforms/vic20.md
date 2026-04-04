---
title: VIC-20
description: Commodore VIC-20 platform guide — hardware, memory, and programming in the RGC IDE.
---

# VIC-20

The **Commodore VIC-20** (1980) was Commodore's first million-seller and the little sibling of the C64. It uses the same **MOS 6502** CPU, runs the same **Commodore BASIC V2**, and uses a similar Kernal — but the hardware is quite different, and RAM is *very* tight without expansion.

Don't underestimate it. The VIC-20 has a passionate community, and its constraints make programming it a genuine puzzle worth solving.

## Languages in the IDE

| Language | Use for |
|----------|---------|
| **Commodore BASIC V2** | Quick experiments, small programs |
| **CC65 C** | Structured programs with cc65's VIC-20 target |

## Hardware overview

### CPU — MOS 6502A at 1.108 MHz

Essentially the same 6502 as the C64, running slightly faster. The same assembly instructions work on both — but the hardware around it is completely different.

### VIC chip — Video

The **MOS 6560/6561** (the "VIC" chip the machine is named after) is simpler than the C64's VIC-II:

- **Text mode**: 22 columns × 23 rows of characters (not 40×25)
- **Graphics mode**: accessible via the VIC chip's registers
- **Colour**: 8 colours + 8 bright variants for foreground; 8 for background
- **No hardware sprites** — sprites must be software-drawn
- Sound: 3 square wave channels + 1 noise channel (built into the VIC chip)

Key VIC registers at $9000–$900F:

| Address | Register |
|---------|---------|
| $9000 | Interlace, screen origin X |
| $9001 | Screen origin Y |
| $9002 | Video columns (bits 0–6), screen memory bit 8 (bit 7) |
| $9003 | Video rows (bits 1–6), double height (bit 0) |
| $9005 | Screen and charset memory address |
| $900E | Auxiliary colour and sound volume |
| $900F | Screen colour and border colour |

### RAM — the tight part

**Unexpanded VIC-20**: only **5 KB of RAM total**, of which BASIC gets about **3.5 KB** after system overhead.

That sounds brutal, but people have written impressive games in 3.5 KB. With memory expansion:

| Expansion | Free BASIC RAM |
|-----------|---------------|
| None | ~3.5 KB |
| 3K expansion | ~6.5 KB |
| 8K expansion | ~11.5 KB |
| 16K+ expansion | ~27+ KB |

The IDE emulates the unexpanded machine by default. Check your preset's settings if you need expansion RAM.

## Memory map (unexpanded)

| Range | Contents |
|-------|----------|
| $0000–$00FF | Zero page |
| $0100–$01FF | Stack |
| $0200–$03FF | System workspace |
| $0400–$07FF | **Unmapped** (colour RAM mirrors here) |
| $1000–$1DFF | **User RAM** (main BASIC area, ~3.5 KB) |
| $1E00–$1FFF | Screen character RAM (22×23) |
| $8000–$8FFF | Character ROM |
| $9000–$93FF | VIC chip registers |
| $9400–$97FF | Colour RAM |
| $A000–$BFFF | BASIC ROM |
| $C000–$FFFF | Kernal ROM |

Notice that the user RAM starts at $1000 — not $0800 like the C64. And the screen is at $1E00, not $0400.

## Screen differences from C64

| Feature | C64 | VIC-20 |
|---------|-----|--------|
| Character columns | 40 | 22 |
| Character rows | 25 | 23 |
| Screen RAM | $0400 | $1E00 |
| Colour RAM | $D800 | $9400 |
| Border/bg colour | $D020/$D021 | $900F (combined byte) |

The border and background colour share one register on the VIC-20:

```basic
POKE 36879, 27   : REM BORDER=WHITE (high nibble), BG=BLUE (low nibble)
                 : REM High nibble 0-7 + bright: 8*bright + colour
```

The combined byte format: bits 7–4 = border colour, bits 3–0 = background colour.

## Writing to the screen

With only 22 columns, the calculation changes:

```basic
RO% = 5 : CO% = 3
POKE 7680 + RO%*22 + CO%, 65    : REM 7680 = screen RAM base ($1E00)
POKE 38400 + RO%*22 + CO%, 7    : REM 38400 = colour RAM base ($9600)
```

Wait — the colour RAM base address ($9600 = 38400) is different from most references. The VIC-20's colour RAM is at $9400, but the *accessible* colour RAM for the default screen position starts at $9600. Always verify with your specific memory configuration.

## Sound

The VIC chip includes a simple sound section: 3 square-wave channels and 1 noise channel. Volume is controlled by the low nibble of $900E.

```basic
10 POKE 36878, 15   : REM MAX VOLUME ($900E bits 0-3)
20 POKE 36876, 200  : REM VOICE 3 FREQUENCY (high freq channel)
30 FOR I=1 TO 500 : NEXT
40 POKE 36876, 0    : REM VOICE 3 OFF
```

The VIC chip's sound is much simpler than the C64's SID — but it has its own charm.

## Programming tips for the VIC-20

**Save every byte** — with 3.5 KB, every `REM` statement costs memory. Delete them from finished programs (not while developing, though!).

**Use short variable names** — in Commodore BASIC V2, only the first two characters of a variable name matter anyway. `S%` not `SCORE%`.

**Use integer variables everywhere** — `%` variables use 2 bytes; float variables use 7 bytes. On a 3.5 KB machine, the difference matters.

**Watch the column count** — 22 columns means printing calculations are different. `TAB(23)` wraps to the next line.

**Expansion RAM opens the machine up** — if you can emulate or use an 8K expansion cart, the VIC-20 becomes far more capable.

## See also

- [Commodore BASIC V2](../basic/commodore-basic-v2.md) — the same BASIC as the C64
- [cc65 / C](../c/cc65.md) — cc65 supports VIC-20 as a target
- [6502 assembly](../assembly/6502.md) — same CPU as the C64
- [C64 platform guide](c64.md) — for comparison
- [IDE getting started](../ide/getting-started.md)

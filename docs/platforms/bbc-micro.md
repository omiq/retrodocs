---
title: BBC Micro
description: BBC Micro platform guide — hardware, modes, BBC BASIC, and CC65 C in the RGC IDE.
---

# BBC Micro

The **BBC Micro** (1981) was built by Acorn Computers for the BBC Computer Literacy Project — an initiative to bring computing to British homes and schools. It has a 2 MHz **MOS 6502A** CPU, excellent engineering, and one of the best BASICs ever written for an 8-bit machine.

The BBC Micro punches above its weight. Its graphics modes are flexible, its BASIC is sophisticated, and its OS provides useful services that make bare-metal programming less of a chore than on the C64 or Spectrum.

## Languages in the IDE

| Language | Preset | Use for |
|----------|--------|---------|
| **BBC BASIC** | BBC BASIC | The natural choice — powerful, fast, with inline asm |
| **CC65 C** | BBC Micro C | C compilation targeting the BBC's memory layout |

## Quick start

1. Select **BBC Micro** as the platform.
2. Choose your language (BBC BASIC or C).
3. The template loads — the BBC Micro uses the JSBeeb emulator in the IDE.
4. Build and run.

!!! tip "BBC Micro keyboard in JSBeeb"
    The JSBeeb emulator maps your keyboard to the BBC's layout. Some keys differ — `£` and `@` are in different places. If BASIC gives you unexpected characters, check the JSBeeb key mapping.

## Hardware overview

### CPU — MOS 6502A at 2 MHz

The BBC runs at **2 MHz** — twice the speed of the standard C64. This gives BBC assembly code a noticeable advantage in raw throughput, though the graphics hardware is simpler.

### Video — CRTC 6845

The BBC Micro uses a **Motorola 6845 CRTC** (Cathode Ray Tube Controller) for video timing, paired with custom Acorn video logic. Unlike the VIC-II, there are no hardware sprites — everything is drawn into framebuffer memory.

Available modes:

| MODE | Pixels | Colours | Screen RAM size | Notes |
|------|--------|---------|----------------|-------|
| 0 | 640×256 | 2 | 20 KB | High-res, monochrome |
| 1 | 320×256 | 4 | 20 KB | Good balance |
| 2 | 160×256 | 16 | 20 KB | Full colour, lower res |
| 3 | 80-col text | 2 | 16 KB | No graphics |
| 4 | 320×256 | 2 | 10 KB | Half the RAM of mode 1 |
| 5 | 160×256 | 4 | 10 KB | Most common for games |
| 6 | 40-col text | 2 | 8 KB | Least RAM |
| 7 | Teletext | 8+flash | 1 KB | Teletext character display |

Mode 5 (160×256, 4 colours) is popular for games — it leaves more RAM free than modes 1 and 2, and four colours is enough for many games.

### Sound — SN76489

The BBC Micro uses the **Texas Instruments SN76489** for sound: 3 square-wave channels and 1 noise channel. In BBC BASIC, sound is accessed through the `SOUND` and `ENVELOPE` commands.

### Memory

The BBC Micro has **32 KB of RAM** on the Model B, with a sophisticated ROM paging system for languages and filing systems.

| Range | Contents |
|-------|----------|
| $0000–$00FF | Zero page (OS uses some — be careful!) |
| $0100–$01FF | Hardware stack |
| $0400–$07FF | OS workspace (**do not use**) |
| $0E00–$7FFF | User RAM (about 29 KB in MODE 7; less in graphical modes) |
| $8000–$BFFF | Sideways ROM (paged — can be RAM on BBC Master) |
| $C000–$DFFF | OS workspace, OS ROM |
| $E000–$FFFF | OS ROM |

Screen RAM lives at the **top of user RAM** — its address moves depending on the MODE selected. In MODE 5, screen RAM is at $5800. Your program should load below the screen start.

## OS calls — the MOS API

The BBC Micro OS (**MOS** — Machine Operating System) provides a clean API via software interrupts (`SWI` on ARM later, but on the 6502 it's `JSR` to specific Kernal addresses or `OSBYTE`/`OSWORD` calls):

```asm
; Write character in A to screen
JSR $FFEE       ; OSWRCH

; Read character from keyboard (blocks)
JSR $FFE0       ; OSRDCH

; Print zero-terminated string at (XY)
LDA #string_lo
LDX #string_hi
JSR $FFDB       ; GS_READ — for BBC OS string calls
```

In BBC BASIC, VDU codes give you many OS services directly:

```basic
VDU 7           : REM Bell
VDU 12          : REM Form feed (CLS)
VDU 19,0,4,0,0,0 : REM Set logical colour 0 to physical colour 4
VDU 23,1,0;0;0;0; : REM Hide cursor
```

## Graphics in CC65 C

When using CC65 C targeting the BBC Micro, the cc65 BBC Micro library gives you access to BASIC-style VDU calls:

```c
#include <bbc.h>
#include <stdio.h>

int main(void) {
    /* Set MODE 5 */
    bbc_mode(5);

    /* VDU codes for colour */
    bbc_vdu(19); bbc_vdu(1); bbc_vdu(2); /* Logical 1 = red */
    bbc_vduw(0); bbc_vduw(0);

    /* Plot a pixel at (100, 100) */
    bbc_plot(BBC_PLOT_DOT, 100, 100);

    /* Draw a line to (200, 200) */
    bbc_plot(BBC_DRAW_LINE, 200, 200);

    printf("Hello from CC65 on BBC!\n");
    return 0;
}
```

## BBC BASIC inline assembly

BBC BASIC's inline assembler is a killer feature — 6502 assembly directly embedded in your BASIC program:

```basic
10 DIM code% 30         : REM Allocate 30 bytes for machine code
20 P% = code%           : REM Set assembler program counter
30 [
40 OPT 2                : REM Assemble with listing (OPT 0=quiet, 2=list)
50 .start
60 LDA #7               : REM Load yellow colour (palette index 7)
70 JSR &FFEE            : REM OSWRCH — write character
80 RTS
90 ]
100 CALL code%          : REM Execute the assembled code
```

The `[...]` block is the assembler. `OPT` controls listing/error behaviour. Labels use `.name` syntax. You can access BBC BASIC variables from the assembler.

## A practical BASIC example — draw a bouncing ball

```basic
10  MODE 5              : REM 160x256 4-colour mode
20  VDU 23,1,0;0;0;0;  : REM Hide cursor
30  bx%=80 : by%=128   : REM Ball position
40  dx%=4 : dy%=4       : REM Ball velocity

100 REM ---- MAIN LOOP ----
110 GCOL 0,0 : PLOT 69,bx%*8,by%*8  : REM Erase (background colour)
120 bx%=bx%+dx% : by%=by%+dy%
130 IF bx%<2 OR bx%>158 THEN dx%=-dx%
140 IF by%<2 OR by%>254 THEN dy%=-dy%
150 GCOL 0,1 : PLOT 69,bx%*8,by%*8  : REM Draw in colour 1
160 GOTO 100
```

Note: BBC BASIC graphics use a 1280×1024 virtual coordinate space — multiply pixel positions by 8 to get MOVE/PLOT coordinates for a 160×256 mode.

## Tips for BBC Micro programming

**Avoid $0400–$07FF** — the OS uses this area heavily. Writing here will corrupt the system.

**Screen size varies by mode** — always check how much user RAM is available in your chosen mode. The OS tells you the top of user RAM in the `TOP` variable (in BASIC), or via OSWORD call.

**BBC BASIC's `ENVELOPE` command** — it provides real ADSR envelopes for `SOUND`, making the BBC's audio much more capable than its simple chip suggests.

**`CALL` vs `USR`** — `CALL addr` jumps to machine code and doesn't return a value. `USR(addr)` calls it and returns the value in A (with X in the next byte). Use `USR` when you need a result back in BASIC.

**The `?` and `!` operators** — BBC BASIC has shorthand for PEEK and POKE:
```basic
X = ?&8000       : REM Same as X = PEEK(&8000)
?&8000 = 65      : REM Same as POKE &8000, 65
X = !&8000       : REM Read 4-byte integer at &8000
!&8000 = 12345   : REM Write 4-byte integer
```

## See also

- [BBC BASIC](../basic/bbc-basic.md) — detailed language reference
- [cc65 / C](../c/cc65.md) — C compilation with the cc65 BBC Micro target
- [6502 assembly](../assembly/6502.md) — 6502 assembly, same CPU as the BBC
- [IDE getting started](../ide/getting-started.md)

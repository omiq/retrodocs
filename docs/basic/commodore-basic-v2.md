---
title: Commodore BASIC V2
description: Commodore 6502 BASIC (V2) in the RGC IDE — C64, VIC-20, PET, and related platforms.
---

# Commodore BASIC V2

**Commodore BASIC V2** is the built-in interpreter ROM on many Commodore 6502 machines — most famously the **Commodore 64**, and also the **VIC-20**, **PET**, early **C128** in C64 mode, and others. If you've ever typed `10 PRINT "HELLO"` on a C64, you already know BASIC V2.

It's not fast. It's not elegant. But it's immediately accessible, runs in ROM on the real hardware, and has an enormous community of tutorials, books, and examples stretching back to 1982. It's also a natural gateway to 6502 machine code — you'll soon find yourself using `POKE` and `SYS` to call your own assembly routines from BASIC.

In the IDE, select a Commodore platform (C64, VIC-20, PET) and choose the **BASIC** preset to get a BASIC environment with the emulator running in the background.

!!! note "Tokeniser and control codes"
    The RGC IDE has improved tokeniser behaviour and control-code handling for C64-style BASIC. If something differs from real hardware, check the build console and try a minimal one-liner to isolate the issue.

## The basics of BASIC

Commodore BASIC V2 programs use **line numbers**. Every statement starts with a number; `GOTO` and `GOSUB` jump to those numbers.

```basic
10 PRINT "HELLO, WORLD!"
20 PRINT "I AM A C64"
30 END
```

Type `RUN` and press Enter to execute.

## Variables

Commodore BASIC V2 has three variable types:

| Type | Suffix | Example | Notes |
|------|--------|---------|-------|
| **Float** | (none) | `X = 3.14` | Default; slow for game loops |
| **Integer** | `%` | `X% = 100` | Faster; range -32768 to 32767 |
| **String** | `$` | `N$ = "CHRIS"` | Up to 255 characters |

Variable names can only be **two significant characters** (plus the type suffix). `SCORE` and `SCUM` are both treated as `SC`. Keep variable names short and document them in `REM` statements.

```basic
10 REM -- VARIABLES --
20 SC% = 0        : REM SCORE (INTEGER)
30 LV% = 1        : REM LEVEL
40 NM$ = "PLAYER" : REM NAME
```

## Control flow

### IF / THEN

```basic
10 IF X% > 10 THEN PRINT "BIG"
20 IF X% < 0 THEN X% = 0 : GOTO 100
```

BASIC V2 has no `ELSE` keyword — use a second `IF` or restructure with `GOTO`.

### FOR / NEXT

```basic
10 FOR I% = 1 TO 10
20   PRINT I%
30 NEXT I%
```

Use `STEP` for non-1 increments:

```basic
10 FOR I% = 0 TO 255 STEP 5
20   POKE 53280, I%    : REM CYCLE BORDER COLOUR
30 NEXT I%
```

### GOTO and GOSUB / RETURN

```basic
100 GOSUB 500      : REM CALL SUBROUTINE AT LINE 500
110 GOTO 100       : REM LOOP FOREVER

500 REM SUBROUTINE
510 PRINT "IN SUBROUTINE"
520 RETURN
```

## Input and output

### PRINT

```basic
10 PRINT "SCORE:"; SC%       : REM SEMICOLON = NO SPACE/NEWLINE BETWEEN
20 PRINT "NAME: " + NM$
30 PRINT                      : REM BLANK LINE
40 PRINT TAB(10); "INDENTED" : REM MOVE TO COLUMN 10
```

### INPUT

```basic
10 INPUT "ENTER YOUR NAME: "; NM$
20 INPUT "ENTER A NUMBER: "; X%
```

### GET (non-blocking keypress)

```basic
10 GET K$
20 IF K$ = "" THEN GOTO 10   : REM WAIT FOR A KEY
30 PRINT "YOU PRESSED: "; K$
```

`GET` reads one character from the keyboard buffer without waiting. Use it in game loops:

```basic
100 GET K$
110 IF K$ = "W" THEN Y% = Y% - 1  : REM UP
120 IF K$ = "S" THEN Y% = Y% + 1  : REM DOWN
130 IF K$ = "A" THEN X% = X% - 1  : REM LEFT
140 IF K$ = "D" THEN X% = X% + 1  : REM RIGHT
```

## POKE and PEEK — talking to hardware

`POKE address, value` writes a byte to memory. `PEEK(address)` reads one. This is how you access the C64's hardware chips directly from BASIC.

### Screen and colour (C64)

```basic
10 POKE 53280, 0    : REM BLACK BORDER
20 POKE 53281, 6    : REM BLUE BACKGROUND
```

C64 colour palette:

| Index | Colour | Index | Colour |
|-------|--------|-------|--------|
| 0 | Black | 8 | Orange |
| 1 | White | 9 | Brown |
| 2 | Red | 10 | Light red |
| 3 | Cyan | 11 | Dark grey |
| 4 | Purple | 12 | Grey |
| 5 | Green | 13 | Light green |
| 6 | Blue | 14 | Light blue |
| 7 | Yellow | 15 | Light grey |

### Writing to screen RAM

Screen RAM on the C64 starts at $0400 (1024 decimal). Each cell is one byte — the Petscii character code:

```basic
10 POKE 1024, 65       : REM PETSCII 65 = "A" AT TOP LEFT
20 POKE 55296, 7       : REM COLOUR RAM: YELLOW INK FOR THAT CELL
```

To write at a specific row/column position (0-based, 40 columns wide):

```basic
10 RO% = 5 : CO% = 10
20 POKE 1024 + RO%*40 + CO%, 65   : REM "A" AT ROW 5, COL 10
30 POKE 55296 + RO%*40 + CO%, 2   : REM RED INK
```

### Useful C64 hardware addresses

| Address | Purpose |
|---------|---------|
| 53280 ($D020) | Border colour |
| 53281 ($D021) | Background colour 0 |
| 1024–2023 ($0400–$07E7) | Screen character RAM (40×25) |
| 55296–56295 ($D800–$DBE7) | Colour RAM |
| 56320 ($DC00) | CIA1 port A — joystick 2, keyboard columns |
| 56321 ($DC01) | CIA1 port B — joystick 1, keyboard rows |
| 54272 ($D400) | SID register base |

### Reading the joystick (C64)

Joystick 2 is on CIA1 port A. Bits are **active low** — 0 means the direction is pressed:

```basic
10 J% = PEEK(56320)
20 IF (J% AND 1) = 0 THEN PRINT "UP"
30 IF (J% AND 2) = 0 THEN PRINT "DOWN"
40 IF (J% AND 4) = 0 THEN PRINT "LEFT"
50 IF (J% AND 8) = 0 THEN PRINT "RIGHT"
60 IF (J% AND 16) = 0 THEN PRINT "FIRE"
```

## SYS and USR — calling machine code

`SYS address` jumps to a machine code routine at the given memory address and returns when it hits `RTS`. This is the primary bridge from BASIC to fast ML routines.

```basic
10 FOR I%=0 TO 5
20   READ B%
30   POKE 49152+I%, B%   : REM STORE ML AT $C000
40 NEXT I%
50 SYS 49152             : REM JUMP TO $C000
60 END

100 REM MACHINE CODE: LDA #2, STA $D020, RTS
110 DATA 169,2,141,32,208,96
```

The DATA bytes decode as: `LDA #2` (169, 2), `STA $D020` (141, 32, 208), `RTS` (96). The border turns red.

## String functions

```basic
10 A$ = "HELLO WORLD"
20 PRINT LEN(A$)              : REM  11
30 PRINT LEFT$(A$, 5)         : REM  HELLO
40 PRINT RIGHT$(A$, 5)        : REM  WORLD
50 PRINT MID$(A$, 7, 5)       : REM  WORLD
60 PRINT ASC("A")             : REM  65
70 PRINT CHR$(65)             : REM  A
```

## Math functions

```basic
10 PRINT INT(3.7)         : REM  3
20 PRINT ABS(-5)          : REM  5
30 PRINT SQR(16)          : REM  4
40 PRINT INT(RND(1)*6)+1  : REM  Random 1 to 6
```

## A minimal game loop

```basic
1  REM *** SIMPLE MOVER — MOVE * WITH WASD ***
5  POKE 53280,0 : POKE 53281,0   : REM BLACK SCREEN
10 X%=20 : Y%=12

100 REM ---- MAIN LOOP ----
110 POKE 1024 + Y%*40 + X%, 32   : REM ERASE (SPACE)

120 GET K$
130 IF K$="W" AND Y%>0  THEN Y%=Y%-1
140 IF K$="S" AND Y%<24 THEN Y%=Y%+1
150 IF K$="A" AND X%>0  THEN X%=X%-1
160 IF K$="D" AND X%<39 THEN X%=X%+1

170 POKE 1024 + Y%*40 + X%, 42   : REM DRAW * (PETSCII 42)
180 POKE 55296 + Y%*40 + X%, 7   : REM YELLOW INK
190 GOTO 100
```

## Performance tips

BASIC V2 is slow by nature — a simple loop does only a few hundred iterations per second. To get more speed:

- **Use integer variables** (`%` suffix) — roughly 3× faster than floats for arithmetic.
- **Keep line numbers low** — the interpreter searches from line 1 each `GOTO`; lower line numbers are found faster.
- **Put hot code early** — frequently-called `GOSUB` targets at low line numbers.
- **Avoid `PRINT` in game loops** — each `PRINT` goes through the Kernal. Use `POKE` to write to screen RAM directly.
- **Use `SYS` for anything timing-critical** — even a small machine code routine for collision detection is 50–100× faster than BASIC.

## VIC-20 differences

The VIC-20 runs the same BASIC V2, but memory is tight and the screen is smaller:

| Item | C64 | VIC-20 |
|------|-----|--------|
| Screen size | 40×25 | 22×23 |
| Free RAM | ~38 KB | ~3.5 KB (unexpanded) |
| Screen RAM | $0400 | $1E00 |
| Border/background | $D020/$D021 | $900F (combined) |

With expansion RAM (3K, 8K, or more) the VIC-20 becomes much more useful for games.

## See also

- [6502 assembly](../assembly/6502.md) — calling ML routines from BASIC via `SYS`
- [XC-BASIC 3](xc-basic-3.md) — compiled BASIC-like language, much faster output
- [C64 platform guide](../platforms/c64.md)
- [VIC-20 platform guide](../platforms/vic20.md)
- [IDE getting started](../ide/getting-started.md)

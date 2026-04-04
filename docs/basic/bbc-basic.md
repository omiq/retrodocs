---
title: BBC BASIC
description: BBC BASIC in the RGC IDE — programming the BBC Micro in its native language.
---

# BBC BASIC

**BBC BASIC** is the native BASIC interpreter on the **BBC Micro** — and it's a cut above most other 8-bit BASICs. Designed by Sophie Wilson at Acorn, it includes inline 6502 assembly, named procedures and functions, `REPEAT...UNTIL` and `WHILE...ENDWHILE` loops, local variables, and a proper `ELSE` clause. It feels surprisingly modern compared to Commodore BASIC V2 or Spectrum BASIC.

In the IDE, select the **BBC Micro** platform and the **BBC BASIC** preset to get a JSBeeb-powered emulator running in your browser.

## The basics

BBC BASIC programs use **line numbers**, like most 8-bit BASICs. But the structured control flow means you use them far less than on the C64.

```basic
10 PRINT "HELLO FROM BBC BASIC!"
20 PRINT "THE YEAR IS ";1982
30 END
```

!!! tip "Run it in the emulator"
    After building in the IDE, the BBC Micro emulator boots and runs your program automatically. You can type at the BASIC prompt in the emulator for quick tests.

## Variables

BBC BASIC has a more flexible type system than Commodore BASIC V2:

| Type | Suffix | Example | Notes |
|------|--------|---------|-------|
| **Float** | (none) | `X = 3.14` | Default numeric type |
| **Integer** | `%` | `X% = 100` | Faster; 32-bit range |
| **String** | `$` | `N$ = "CHRIS"` | Variable length |
| **Integer array** | `%()` | `A%(10)` | Declared with DIM |

Unlike Commodore BASIC, BBC BASIC integers are **32-bit** — very handy for scores and coordinates without overflow worries.

## Control flow

### IF / THEN / ELSE

```basic
10 IF score% > 100 THEN PRINT "HIGH" ELSE PRINT "LOW"

20 IF lives% = 0 THEN
30   PRINT "GAME OVER"
40   END
50 ENDIF
```

### FOR / NEXT

```basic
10 FOR I% = 1 TO 10
20   PRINT I%
30 NEXT I%

40 FOR I% = 0 TO 255 STEP 16
50   COLOUR I% MOD 8
60 NEXT I%
```

### REPEAT / UNTIL

```basic
10 REPEAT
20   REM ... game loop ...
30 UNTIL quit% = TRUE
```

### WHILE / ENDWHILE

```basic
10 WHILE lives% > 0
20   PROC_game_loop
30 ENDWHILE
```

### CASE ... OF (BBC BASIC V)

```basic
10 CASE key$ OF
20   WHEN "W" : y% = y% - 1
30   WHEN "S" : y% = y% + 1
40   WHEN "A" : x% = x% - 1
50   WHEN "D" : x% = x% + 1
60   OTHERWISE : REM No key
70 ENDCASE
```

## Procedures and functions

This is where BBC BASIC really shines. You can define proper named subroutines with local variables:

```basic
100 DEF PROC_draw_score
110   LOCAL col%
120   col% = score% MOD 7 + 1   : REM Colour cycles with score
130   COLOUR col%
140   PRINT TAB(0,0);"SCORE: ";score%
150 ENDPROC

200 DEF FN_clamp(val%, lo%, hi%)
210 IF val% < lo% THEN = lo%
220 IF val% > hi% THEN = hi%
230 = val%
```

`PROC_` prefix by convention for procedures; `FN_` prefix for functions that return values. `LOCAL` variables are scoped to the procedure — a huge improvement over global-only BASIC V2.

## Screen and graphics

The BBC Micro has several graphics modes, selectable with `MODE`:

| Mode | Resolution | Colours | Characters |
|------|------------|---------|------------|
| 0 | 640×256 | 2 | 80×32 |
| 1 | 320×256 | 4 | 40×32 |
| 2 | 160×256 | 16 | 20×32 |
| 4 | 320×256 | 2 | 40×32 |
| 5 | 160×256 | 4 | 20×32 |
| 7 | Teletext | 8+flash | 40×25 |

```basic
10 MODE 2          : REM 160x256, 16 colours
20 CLS             : REM Clear screen
30 COLOUR 3        : REM Set text colour (3 = yellow in mode 2)
40 PRINT "HELLO"
```

### Graphics primitives

BBC BASIC has built-in graphics commands — no POKE required:

```basic
10 MODE 1          : REM 320x256, 4 colours
20 GCOL 0, 3       : REM Set graphics colour to 3
30 DRAW 320, 256   : REM Draw line to (320, 256)
40 MOVE 0, 0       : REM Move graphics cursor
50 PLOT 69, 160, 128  : REM Plot filled triangle vertex

60 CLG             : REM Clear graphics area
```

Graphics coordinates in BBC BASIC use a 1280×1024 virtual grid regardless of mode — the hardware scales for you.

```basic
10 MODE 2
20 FOR angle = 0 TO 360 STEP 5
30   x% = 640 + 400 * COS(RAD(angle))
40   y% = 512 + 400 * SIN(RAD(angle))
50   GCOL 0, angle MOD 8
60   PLOT 69, x%, y%
70 NEXT angle
```

## Input

### Reading the keyboard

```basic
10 k$ = INKEY$(0)    : REM Non-blocking — returns "" if no key
20 IF k$ = "W" THEN y% = y% - 1

30 k$ = GET$         : REM Blocking — waits for keypress
```

`INKEY$` with a timeout of 0 is equivalent to Commodore BASIC's `GET` — non-blocking, perfect for game loops.

You can also check specific keys by their scan code:

```basic
IF INKEY(-105) THEN PRINT "SPACE PRESSED"  : REM -105 = Space
IF INKEY(-58)  THEN PRINT "Z PRESSED"
```

### Reading the joystick / ADC

```basic
ADVAL(1)   : REM Joystick 1 X axis (0-65520)
ADVAL(2)   : REM Joystick 1 Y axis
ADVAL(3)   : REM Joystick 2 X axis
ADVAL(4)   : REM Joystick 2 Y axis
ADVAL(0)   : REM Fire buttons (bit field)
```

## Inline 6502 assembly

One of BBC BASIC's killer features — you can write assembly inline with `[`:

```basic
10 DIM code% 20          : REM Reserve 20 bytes for ML code
20 P% = code%            : REM Set assembler PC to start of buffer
30 [
40 OPT 2                 : REM Assemble + list
50 LDA #2
60 STA &D020             : REM Not valid on BBC — this is C64 syntax, just for demo
70 RTS
80 ]
90 CALL code%            : REM Execute the assembled code
```

`CALL address` executes machine code. `USR(address)` calls it and returns the value in A (and X in the high byte). The assembler is built right into BBC BASIC — no separate tool needed.

## Sound

```basic
10 SOUND 1, -15, 53, 20    : REM Channel, amplitude, pitch, duration
20 SOUND 1, -15, 101, 10
30 ENVELOPE 1, 3, 1, -1, -1, 5, 5, 5, 126, 0, 0, -126, 126, 0
```

BBC BASIC's `SOUND` and `ENVELOPE` commands give you direct access to the BBC Micro's 4-channel sound chip (SN76489). `ENVELOPE` defines ADSR envelopes for more interesting tones.

## A minimal game loop

```basic
1  REM ** SIMPLE MOVER **
5  MODE 4 : VDU 23,1,0;0;0;0;   : REM Mode 4, hide cursor
10 x% = 320 : y% = 128

100 REM ---- MAIN LOOP ----
110 GCOL 0, 0 : PLOT 69, x%, y% : REM Erase (plot in background colour)
120 k$ = INKEY$(0)
130 IF k$ = CHR$(136) THEN x% = x% - 8  : REM Cursor left
140 IF k$ = CHR$(137) THEN x% = x% + 8  : REM Cursor right
150 IF k$ = CHR$(138) THEN y% = y% - 8  : REM Cursor down
160 IF k$ = CHR$(139) THEN y% = y% + 8  : REM Cursor up
170 x% = FN_clamp(x%, 0, 1280)
180 y% = FN_clamp(y%, 0, 1024)
190 GCOL 0, 3 : PLOT 69, x%, y% : REM Draw in colour 3
200 GOTO 100

1000 DEF FN_clamp(v%, lo%, hi%)
1010 IF v% < lo% THEN = lo%
1020 IF v% > hi% THEN = hi%
1030 = v%
```

## Common mistakes

**Forgetting `ENDPROC`** — every `DEF PROC_...` must end with `ENDPROC`. Missing it gives a `No ENDPROC` error.

**`FN_` functions return with `= value`** — there's no `RETURN value` syntax. The last executed `= expression` is the return value.

**Graphics coordinates vs text coordinates** — `PRINT TAB(x,y)` uses text column/row coordinates; `MOVE x,y` and `DRAW x,y` use the 1280×1024 graphics coordinate system. They're independent.

**`LOCAL` variable scope** — local variables in a `PROC` are only visible inside that procedure. You can't read them from the calling code. This is a feature, not a bug — use it to avoid name collisions.

## See also

- [6502 assembly](../assembly/6502.md) — BBC BASIC's inline assembler uses 6502
- [BBC Micro platform guide](../platforms/bbc-micro.md) — hardware reference
- [IDE getting started](../ide/getting-started.md)

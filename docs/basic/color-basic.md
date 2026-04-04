---
title: Color BASIC
description: Color BASIC for the Dragon 32 and TRS-80 Color Computer (CoCo) in the RGC IDE.
---

# Color BASIC

**Color BASIC** is the Microsoft-licensed BASIC interpreter built into the **Dragon 32**, **Dragon 64**, and **TRS-80 Color Computer** (CoCo) family. It's closely related to other Microsoft BASICs of the era — if you know Commodore BASIC V2, you'll recognise the structure immediately, though the keywords and hardware POKEs are different.

The CoCo extended its BASIC with an **Extended Color BASIC** ROM (on later models and the CoCo 2/3), which adds graphics, sound, and joystick commands.

## Quick start in the IDE

1. Select **Dragon 32** or **TRS-80 CoCo 2** as the platform.
2. Choose the **BASIC** preset.
3. Write your program in the editor and **Build** — it loads into the emulated machine.

## The basics

Like all Microsoft 8-bit BASICs, Color BASIC uses **line numbers** and **GOTO/GOSUB** for flow control:

```basic
10 CLS
20 PRINT "HELLO, DRAGON!"
30 FOR I=1 TO 5
40   PRINT "LINE"; I
50 NEXT I
60 END
```

`CLS` clears the screen — on the Dragon/CoCo it produces a distinctive green-on-black display in text mode.

## Variables

| Type | Suffix | Example | Notes |
|------|--------|---------|-------|
| **Float** | (none) | `X = 3.14` | Default — slow |
| **Integer** | `%` | `X% = 100` | Faster; -32768 to 32767 |
| **String** | `$` | `N$ = "HELLO"` | Variable length |

Variable names can be longer than 2 characters (unlike Commodore BASIC V2), though only the first 2 characters are significant on many versions.

Hex constants use `&H` prefix: `&H1000` = 4096.

## Control flow

```basic
10 IF X% > 10 THEN PRINT "BIG" ELSE PRINT "SMALL"
20 FOR I=1 TO 10 STEP 2
30   PRINT I
40 NEXT I
50 GOSUB 500
60 GOTO 10

500 PRINT "IN SUBROUTINE"
510 RETURN
```

## Screen and text

```basic
10 CLS               : REM Clear screen (default colour)
20 CLS 2             : REM Clear screen to colour 2 (background colour)
30 PRINT "HELLO"
40 PRINT @32, "COL 0, ROW 1"  : REM Print at screen position 32
                               : REM (screen is 32 cols, so pos 32 = row 1, col 0)
```

`PRINT @position` is the Dragon/CoCo equivalent of Commodore's POKE to screen RAM — it positions the cursor at a specific character position. Position 0 = top-left, 511 = bottom-right of the 32×16 text screen.

## Graphics

Color BASIC's graphics commands work in semi-graphic modes overlaid on the text display:

```basic
10 PMODE 4,1         : REM Set graphics mode 4 (256x192, 2 colour), page 1
20 PCLS 0            : REM Clear graphics screen (colour 0)
30 SCREEN 1,1        : REM Show graphics screen
40 PSET (128,96),1   : REM Plot pixel at (128,96) in colour 1
50 PRESET (128,96)   : REM Clear pixel at (128,96)
60 LINE (0,0)-(255,191),1      : REM Draw a line
70 LINE (0,0)-(255,191),1,BF   : REM Draw a filled box
80 CIRCLE (128,96),50,1        : REM Draw a circle
```

Graphics mode table (Extended Color BASIC):

| PMODE | Resolution | Colours |
|-------|------------|---------|
| 0 | 128×96 | 2 (from 4-colour set) |
| 1 | 128×96 | 4 |
| 2 | 128×192 | 2 |
| 3 | 128×192 | 4 |
| 4 | 256×192 | 2 |

```basic
10 PMODE 3,1 : SCREEN 1,1 : PCLS 0
20 FOR A=0 TO 360 STEP 5
30   X = 128 + 80*COS(A*3.14159/180)
40   Y = 96 + 60*SIN(A*3.14159/180)
50   PSET (X,Y), 1
60 NEXT A
```

## Sound — the PLAY command

One of Color BASIC's best features is the `PLAY` command — a music macro language built right into BASIC:

```basic
10 PLAY "CDEFGAB"    : REM Play a C major scale
20 PLAY "T2 L4 O2 CEGCE2"  : REM Tempo 2, quarter notes, octave 2
30 PLAY "MF"         : REM Music foreground (wait to finish)
40 PLAY "MB"         : REM Music background (continue while playing)
```

PLAY syntax:

| Letter | Meaning |
|--------|---------|
| A–G | Musical notes |
| O n | Set octave (1–5) |
| L n | Set note length (1=whole, 4=quarter, 8=eighth, …) |
| T n | Set tempo (1=slow, 255=fast) |
| V n | Set volume (1–31) |
| P n | Pause (length same as note) |
| MF | Music foreground (blocking) |
| MB | Music background (non-blocking) |

```basic
10 PLAY "T4 L4 O3 CEGCE"   : REM Simple arpeggio, foreground
20 PLAY "T8 MB L8 CDECCDEC" : REM Fast background melody
30 FOR I=1 TO 100 : NEXT I  : REM Do other work while music plays
```

## Joystick input

```basic
10 X = JOYSTK(0)    : REM Left joystick X axis (0-63, centre=31)
20 Y = JOYSTK(1)    : REM Left joystick Y axis
30 X2 = JOYSTK(2)   : REM Right joystick X axis
40 Y2 = JOYSTK(3)   : REM Right joystick Y axis
50 IF STRIG(0) THEN PRINT "LEFT FIRE"   : REM Fire button
60 IF STRIG(2) THEN PRINT "RIGHT FIRE"
```

The joystick axes return 0–63, with 31 at centre. `STRIG(n)` returns -1 (TRUE) if the button is pressed, 0 if not.

```basic
10 CLS
20 X=20 : Y=10
30 PRINT @Y*32+X, "*"     : REM Draw player
40 PRINT @Y*32+X, " "     : REM Erase (overwrite with space)
50 JX = JOYSTK(0) - 31    : REM Joystick -31 to +31
60 JY = JOYSTK(1) - 31
70 IF JX > 10 THEN X=X+1
80 IF JX < -10 THEN X=X-1
90 IF JY > 10 THEN Y=Y+1
100 IF JY < -10 THEN Y=Y-1
110 X = X - (X<0)*X : X = X - (X>31)*(X-31)  : REM Clamp X 0-31
120 Y = Y - (Y<0)*Y : Y = Y - (Y>15)*(Y-15)  : REM Clamp Y 0-15
130 GOTO 30
```

## POKE and PEEK — hardware access

```basic
10 POKE &H1000, 255  : REM Write to memory address $1000
20 X = PEEK(&H1000)  : REM Read from $1000
```

Hex addresses use `&H` prefix. Some useful addresses:

| Address | Purpose |
|---------|---------|
| $FF00 | PIA 0-A (keyboard row, DAC bit 7) |
| $FF01 | PIA 0-A control |
| $FF02 | PIA 0-B (joystick comparator, cassette) |
| $FF20 | PIA 1-A (6-bit DAC, cassette output) |
| $FF22 | PIA 1-B (VDG mode bits) |

## Calling machine code

```basic
10 FOR I=0 TO 5
20   READ B
30   POKE &H7E00+I, B  : REM Load 6809 ML at $7E00
40 NEXT I
50 EXEC &H7E00          : REM Call it

100 DATA 134,0,183,255,34,57  : REM CLRA, STA $FF22, RTS
```

`EXEC address` calls machine code (6809 `JSR` to that address). The code above stores 0 into the VDG mode register and returns.

## Extended Color BASIC extras (CoCo 2 and later Dragon models)

- **DRAW** — turtle-style drawing: `DRAW "U50;R50;D50;L50"` draws a square
- **PAINT** — flood fill: `PAINT (X,Y), colour`
- **GET / PUT** — sprite-style block graphics capture and restore
- **HSCREEN** — extended high-res graphics modes
- **HSET / HRESET / HPSET / HPRESET** — high-res pixel plotting

## Performance tips

- **Use integer variables** (`%`) — 4× faster than floats for arithmetic
- **EXEC machine code** for timing-critical loops — even short 6809 routines are 50–100× faster than BASIC
- **POKE directly to screen** instead of PRINT — `POKE &H0400+pos, charcode` is faster
- **Background music with MB** — let `PLAY "MB..."` run sound while your game loop continues

## See also

- [Dragon 32 / CoCo platform guide](../platforms/dragon-coco.md)
- [6809 assembly](../assembly/6809.md) — calling ML from BASIC via EXEC
- [CMOC C for 6809](../c/cmoc.md) — compiled C alternative
- [IDE getting started](../ide/getting-started.md)

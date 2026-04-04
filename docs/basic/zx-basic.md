---
title: ZX BASIC (Boriel)
description: ZX BASIC (Boriel's compiler) for the ZX Spectrum in the RGC IDE — compiled BASIC with modern syntax.
---

# ZX BASIC (Boriel)

**ZX BASIC** (sometimes called **Boriel's ZX BASIC** or **ZX Basic Compiler**) is a modern BASIC compiler for the **ZX Spectrum**. It takes BASIC-like source code and compiles it to fast Z80 machine code — giving you the approachability of BASIC with performance far beyond the Spectrum's built-in interpreter.

In the IDE, select the **ZX Spectrum** platform and the **ZX BASIC** preset to use this compiler.

## Why ZX BASIC instead of Spectrum BASIC?

| Aspect | ZX Spectrum BASIC | ZX BASIC (Boriel) |
|--------|-------------------|-------------------|
| Execution | Interpreted in ROM | Compiled to Z80 machine code |
| Speed | Very slow | ~10–50× faster |
| Line numbers | Required | Optional — can use labels |
| Structured code | Limited | `WHILE`, `FOR`, `DO`, `FUNCTION`, `SUB` |
| Arrays | 1-indexed, limited | Modern, flexible |
| Inline assembly | No | Yes — `ASM` blocks |

If you want to write a real game for the Spectrum and still use BASIC syntax, ZX BASIC is the tool to reach for.

## Quick start in the IDE

1. Select **ZX Spectrum** and the **ZX BASIC** toolchain.
2. The template loads a starter program — run it first to confirm the emulator is working.
3. Edit the source and **Build**. Errors are compiler errors (file and line number), not runtime errors.

!!! tip "Output is a .TAP file"
    ZX BASIC compiles your code to a `.TAP` tape image. The IDE loads this automatically into the Spectrum emulator. You can also download the `.TAP` to run on real hardware via a tape interface or SD card.

## Hello, ZX BASIC

```basic
' ZX BASIC — Hello World

PRINT "HELLO FROM ZX BASIC!"
PRINT "COMPILED AND FAST!"
```

No line numbers required. `'` is the comment character. Build it and it runs immediately in the Spectrum emulator.

## Variables

```basic
DIM score AS INTEGER    ' 16-bit signed integer
DIM lives AS UBYTE      ' 8-bit unsigned (0-255)
DIM name AS STRING      ' Variable-length string
DIM x AS LONG           ' 32-bit integer (use sparingly)
DIM flag AS BOOLEAN     ' TRUE or FALSE
```

Common types:

| Type | Size | Range |
|------|------|-------|
| `UBYTE` | 1 byte | 0–255 |
| `BYTE` | 1 byte | -128–127 |
| `UINTEGER` | 2 bytes | 0–65535 |
| `INTEGER` | 2 bytes | -32768–32767 |
| `ULONG` | 4 bytes | 0–4,294,967,295 |
| `LONG` | 4 bytes | ±2 billion |
| `STRING` | variable | Text |

**Use `UBYTE` and `UINTEGER` wherever possible** — unsigned arithmetic is faster on the Z80 than signed.

## Control flow

### IF / THEN / ELSE / END IF

```basic
IF score > 100 THEN
    PRINT "HIGH SCORE!"
ELSE
    PRINT "KEEP GOING"
END IF
```

### FOR / NEXT

```basic
FOR i AS UBYTE = 0 TO 9
    PRINT i; " "
NEXT i
```

Declaring the loop variable inline (`i AS UBYTE`) is good practice — it scopes the variable to the loop.

### WHILE / END WHILE

```basic
WHILE lives > 0
    ' game loop here
WEND
```

### DO / LOOP

```basic
DO
    ' game loop
LOOP UNTIL quit = TRUE
```

### SELECT CASE

```basic
SELECT CASE key$
    CASE "w", "W": y = y - 1
    CASE "s", "S": y = y + 1
    CASE "a", "A": x = x - 1
    CASE "d", "D": x = x + 1
END SELECT
```

## Subroutines and functions

```basic
' Subroutine (no return value)
SUB draw_score()
    PRINT AT 0, 0; "SCORE: "; score
END SUB

' Function with return value
FUNCTION clamp(val AS INTEGER, lo AS INTEGER, hi AS INTEGER) AS INTEGER
    IF val < lo THEN RETURN lo
    IF val > hi THEN RETURN hi
    RETURN val
END FUNCTION

' Calling them
CALL draw_score()
x = clamp(x, 0, 31)
```

## Screen and colours

The ZX Spectrum's screen is **256×192 pixels** in a **32×24** character grid. Colours are controlled through **attributes** — one colour byte per 8×8 character cell.

### Text output

```basic
PRINT "HELLO"               ' Print at cursor position
PRINT AT 5, 10; "HELLO"    ' Print at row 5, column 10

' Colour control sequences
PRINT INK 2; PAPER 7; "RED ON WHITE"
```

Spectrum colour constants:

| Value | Colour | Value | Colour |
|-------|--------|-------|--------|
| 0 | Black | 4 | Green |
| 1 | Blue | 5 | Cyan |
| 2 | Red | 6 | Yellow |
| 3 | Magenta | 7 | White |

Add `BRIGHT 1` for bright colours, `FLASH 1` for flashing.

### Border colour

```basic
BORDER 2    ' Red border
```

### Pixel graphics

```basic
PLOT 128, 96        ' Plot a pixel at (128, 96)
DRAW 50, 0          ' Draw line 50 pixels to the right
CIRCLE 128, 96, 40  ' Draw circle at (128,96) radius 40
```

Spectrum pixel coordinates: (0,0) is **bottom-left**, (255,175) is **top-right** (unusual — y increases upward).

## Keyboard input

```basic
' INKEY$ — non-blocking, returns "" if no key pressed
DIM k AS STRING
k = INKEY$
IF k = "w" THEN y = y - 1

' Read specific keys by code
IF MULTIKEYS(32) THEN ' Space bar
    ' space pressed
END IF
```

`MULTIKEYS` lets you check if a specific key is held down — useful for smooth movement in games.

## Inline Z80 assembly

One of ZX BASIC's most powerful features:

```basic
' Inline assembly block
ASM
    ld a, 2
    out (254), a    ; Set border to red
END ASM

' Access ZX BASIC variables in assembly
DIM border_color AS UBYTE
border_color = 3    ' Magenta

ASM
    ld a, (_border_color)   ; Load ZX BASIC variable (prefix with _)
    out (254), a
END ASM
```

ZX BASIC variables are accessible in assembly with a `_` prefix on the name.

## Working with Spectrum memory directly

```basic
' POKE and PEEK — direct memory access
POKE 23624, 56      ' Set border colour via system variable BORDCR
DIM val AS UBYTE = PEEK(23624)

' Clear screen attributes to white-on-black
DIM i AS UINTEGER
FOR i = 22528 TO 23295
    POKE i, 56      ' 56 = white paper (7), black ink (0), no bright
NEXT i
```

Key Spectrum memory addresses:

| Address | Purpose |
|---------|---------|
| 16384 ($4000) | Screen pixel data (6144 bytes) |
| 22528 ($5800) | Screen attribute data (768 bytes) |
| 23552 ($5C00) | System variables |
| 23624 | BORDCR — border colour |

## A minimal game loop

```basic
' ZX BASIC — Simple character mover

DIM x AS UBYTE = 15
DIM y AS UBYTE = 11
DIM k AS STRING

BORDER 0
CLS

DO
    ' Erase old position
    PRINT AT y, x; " "

    ' Read input
    k = INKEY$
    IF k = "q" THEN x = x - 1 : IF x > 31 THEN x = 31
    IF k = "w" THEN x = x + 1 : IF x > 31 THEN x = 31
    IF k = "o" THEN y = y - 1 : IF y > 23 THEN y = 23
    IF k = "p" THEN y = y + 1 : IF y > 23 THEN y = 23

    ' Draw new position
    PRINT AT y, x; INK 6; "*"

LOOP UNTIL k = " "   ' Exit on Space

PRINT AT 12, 12; "DONE!"
```

## Common mistakes

**Pixel Y axis is inverted** — `PLOT x, y` has (0,0) at the *bottom-left*, not the top-left. `PRINT AT row, col` has (0,0) at the *top-left*. They use different coordinate systems.

**Attribute clash** — the Spectrum's 8×8 colour cells mean any two things sharing a cell share the same ink and paper colour. This is a hardware limitation. Plan your layout around it.

**Type overflow** — if you declare `DIM x AS UBYTE` and assign -1 or 256, the value wraps silently. Use the right type for your range.

**String concatenation in loops** — building strings by appending in a loop is slow. Prepare strings before the loop if possible.

## Official resources

- **[ZX Basic Compiler documentation](https://zxbasic.readthedocs.io/)** — language reference and examples
- **[Boriel's ZX BASIC GitHub](https://github.com/boriel/zxbasic)** — source and issue tracker

## See also

- [Z80 assembly](../assembly/z80.md) — going lower-level on the Spectrum
- [Z88DK / C for Z80](../c/z88dk.md) — C compilation for Z80 platforms
- [ZX Spectrum platform guide](../platforms/zx-spectrum.md)
- [IDE getting started](../ide/getting-started.md)

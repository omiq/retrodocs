---
title: XC-BASIC 3
description: XC-BASIC 3 cross-compiler for Commodore targets in the Retro Game Coders IDE.
---

# XC-BASIC 3

**XC-BASIC 3** is a **BASIC-like language** that **cross-compiles** to 6502 machine code for Commodore-class targets. It gives you a familiar BASIC syntax while producing programs that run dramatically faster than interpreted Commodore BASIC V2 — making it an excellent choice for games and demos.

Supported targets include the **Commodore 64**, **VIC-20**, and **PET** (exact presets depend on your IDE build).

## How it differs from Commodore ROM BASIC

| Aspect | Commodore BASIC V2 | XC-BASIC 3 |
|--------|-------------------|------------|
| Execution | Interpreted in ROM at runtime | Compiled to 6502 machine code |
| Speed | Slow — a few hundred ops/sec | Fast — machine code speed |
| Syntax | Microsoft BASIC (line numbers required) | Modernised — labels, structured loops, no line numbers |
| Debugging | `STOP`, `CONT`, `LIST` in the BASIC prompt | Compiler errors + emulator; no live BASIC environment |
| Memory | ROM BASIC overhead always present | No ROM BASIC needed; compiler handles runtime |

Think of it as: *BASIC syntax, assembly performance.*

## Quick start in the IDE

1. Choose a **Commodore** platform preset that lists **XC-BASIC 3**.
2. The template gives you a working starter program — read it through before editing.
3. **Build** — errors come from the XC-BASIC compiler, not a tokeniser. Read the first error carefully.
4. Run in the emulator.

!!! warning "Compiler errors are not BASIC errors"
    XC-BASIC 3 errors appear at compile time, before anything runs. They look like C compiler errors (file, line, message). Fix the first error and rebuild — later errors are often cascading from the first.

## Hello, XC-BASIC 3

```basic
' XC-BASIC 3 — Hello World on C64

program hello

    print "HELLO FROM XC-BASIC 3!", nl
    print "MUCH FASTER THAN ROM BASIC!", nl

end program
```

Notice: no line numbers, `'` for comments (not `REM`), and `nl` for newline. It looks more like modern BASIC dialects than Commodore BASIC V2.

## Language overview

### Variables

XC-BASIC 3 uses typed variables with explicit declarations:

```basic
dim score as integer    ' 16-bit signed integer
dim lives as byte       ' 8-bit unsigned (0-255)
dim name as string * 20 ' Fixed-length string, max 20 chars
dim x as float          ' Floating point (use sparingly — slow)
```

### Constants

```basic
const BORDER = $D020    ' Hex address constant
const MAX_LIVES = 5
```

### Control flow

```basic
' IF / THEN / ELSE / END IF
if score > 100 then
    print "HIGH SCORE!", nl
else
    print "KEEP GOING", nl
end if

' FOR / NEXT
for i = 1 to 10
    print i, nl
next i

' FOR with STEP
for i = 0 to 255 step 16
    poke BORDER, i      ' Cycle border colour
next i

' WHILE / WEND
while lives > 0
    call game_loop()
wend

' DO / LOOP (infinite, exit with EXIT DO)
do
    call update()
    if quit_flag then exit do
loop
```

### Subroutines and functions

```basic
' Subroutine (no return value)
sub draw_score()
    locate 0, 0
    print "SCORE: ", score, nl
end sub

' Function (returns a value)
function clamp(val as integer, lo as integer, hi as integer) as integer
    if val < lo then return lo
    if val > hi then return hi
    return val
end function

' Calling them
call draw_score()
x = clamp(x, 0, 39)
```

### Hardware access — POKE and PEEK

POKE and PEEK work just like Commodore BASIC V2:

```basic
poke $D020, 0       ' Black border
poke $D021, 6       ' Blue background

dim val as byte
val = peek($DC00)   ' Read CIA1 port A (joystick 2)
```

### Screen operations

```basic
' Clear screen
cls

' Position cursor
locate col, row     ' 0-based, column first

' Print at position
locate 10, 5
print "HELLO"

' Print without newline
print "SCORE: ", score
```

### Inline assembly

Drop into 6502 assembly for maximum-speed operations:

```basic
asm {
    lda #2
    sta $D020       ; Red border
}
```

You can read and write XC-BASIC variables from inline assembly — see the XC-BASIC 3 documentation for the calling convention.

## A minimal game loop

```basic
program mover
    ' Move a character around with WASD

    dim x as byte
    dim y as byte
    dim k as byte

    x = 20 : y = 12
    poke $D020, 0 : poke $D021, 0   ' Black screen

    do
        ' Erase
        poke 1024 + y * 40 + x, 32

        ' Read keyboard (PETSCII codes)
        k = getkey()
        if k = asc("W") and y > 0  then y = y - 1
        if k = asc("S") and y < 24 then y = y + 1
        if k = asc("A") and x > 0  then x = x - 1
        if k = asc("D") and x < 39 then x = x + 1

        ' Draw * at new position
        poke 1024 + y * 40 + x, 42
        poke 55296 + y * 40 + x, 7  ' Yellow ink
    loop

end program
```

## Performance compared to ROM BASIC

Because XC-BASIC 3 compiles to machine code, the performance difference is substantial. A loop that iterates 1000 times takes:

- **Commodore BASIC V2**: several seconds
- **XC-BASIC 3**: milliseconds

This makes XC-BASIC 3 suitable for real-time games with smooth movement, whereas ROM BASIC games typically need careful tricks and `SYS` calls to achieve acceptable speed.

## Tips

**Use `byte` for small values** — 8-bit arithmetic is faster than 16-bit on the 6502. Declare loop counters, colour values, and coordinates as `byte` when they fit in 0–255.

**Use `integer` for scores and larger counts** — 16-bit arithmetic is well-supported and far faster than `float`.

**Avoid `float`** — floating point on a 6502 is slow even in compiled code. Use fixed-point integers if you need fractional values.

**Inline `asm {}` for hot paths** — if a subroutine is called every frame, consider rewriting the inner loop in inline assembly.

**The compiler catches type errors** — unlike Commodore BASIC V2, XC-BASIC 3 will tell you at compile time if you assign a string to an integer variable. Pay attention to these — they're real bugs.

## Official resources

- **[XC-BASIC 3 documentation](https://xc-basic.net/)** — language reference, compiler usage, examples
- **[XC-BASIC GitHub](https://github.com/neilsf/xc-basic3)** — source code and issue tracker

## See also

- [Commodore BASIC V2](commodore-basic-v2.md) — the ROM BASIC for quick, interpreted programs
- [6502 assembly](../assembly/6502.md) — going lower-level when you need maximum speed
- [cc65 / C](../c/cc65.md) — full C compilation for Commodore targets
- [C64 platform guide](../platforms/c64.md)
- [IDE getting started](../ide/getting-started.md)

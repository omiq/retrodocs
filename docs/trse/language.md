---
title: The TRSE language
description: A practical introduction to Turbo Rascal Syntax Error — the Pascal-like language at the heart of the TRSE IDE.
---

# The TRSE language

TRSE programs are written in **Turbo Rascal** — a structured, Pascal-flavoured language that compiles directly to native machine code for your target platform. If you've seen Pascal or Delphi before you'll feel right at home. If not, don't worry: the syntax is clean and readable.

!!! note "Desktop IDE only"
    This section covers the **TRSE desktop IDE** and its Turbo Rascal language. The web IDE at [ide.retrogamecoders.com](https://ide.retrogamecoders.com) uses separate toolchains (cc65, z88dk, CMOC, etc.) — see the [Platforms](../platforms/index.md) and [C](../c/index.md) / [Assembly](../assembly/index.md) sections for those.

---

## File types

| Extension | Purpose |
|-----------|---------|
| `.ras` | Main program file — contains the `program` declaration and `begin...end.` block |
| `.tru` | Unit file — a reusable library of variables and procedures, declared with `unit` |

---

## Program structure

Every TRSE program starts with a `program` declaration, optional `@use` directives to import units, a `var` section for variables, and a main `begin...end.` block.

```pascal
program HelloWorld;

@use "screen/screen"       // import the built-in screen unit
@use "system/memory"       // import the memory utility unit

var
    i, j : byte;
    x     : byte = 0;      // initialised to 0

begin
    Screen::Clear(#Screen::screen0, key_space);
    Screen::Clear(#Screen::color, yellow);
    Screen::PrintString(cstring("HELLO WORLD"), 10, 12, #Screen::screen0);

    while (true) do
    begin
        Screen::WaitForVerticalBlank();
        i += 1;
    end;
end.
```

Note the `.` at the end of `end.` — this marks the end of the entire program.

---

## Variables and types

Declare all variables in the `var` section before `begin`.

```pascal
var
    x, y       : byte;              // 8-bit unsigned (0–255)
    speed      : byte = 5;          // initialised
    score      : integer;           // 16-bit signed
    ptr        : pointer;           // generic pointer
    typed_ptr  : ^byte;             // pointer to byte
    name       : cstring = "CHRIS"; // compile-time string
    data       : array[8] of byte = ($01, $02, $03, $04, $05, $06, $07, $08);
    table      : array[256] of byte;
```

### Type summary

| Type | Size | Notes |
|------|------|-------|
| `byte` | 8-bit | Unsigned, 0–255. The most common type. |
| `integer` | 16-bit | Signed. Use sparingly — 16-bit ops are slower on 8-bit CPUs. |
| `pointer` | 16-bit | An address; can be indexed like an array (`ptr[i]`). |
| `^byte` | 16-bit | Typed pointer to byte. |
| `cstring` | compile-time | String literal embedded in code. Length known at compile time. |
| `string` | runtime | Null-terminated string in RAM. |
| `array[n] of T` | n × sizeof(T) | Fixed-size array. |

### Constants

```pascal
const maxSprites : byte = 8;
const screenBase : byte = $04;    // hi-byte of $0400
```

Constants are substituted at compile time — they don't use any RAM.

---

## Compiler directives

Directives start with `@` and are processed at compile time.

```pascal
@use "screen/screen"          // import a unit by path
@define charsetLoc $1400      // named compile-time value
@export "src.flf" "out.bin" 256  // convert an asset file
```

| Directive | Purpose |
|-----------|---------|
| `@use "path/unit"` | Import a `.tru` unit — makes its procedures and variables available |
| `@define NAME value` | Declare a compile-time constant. Reference it as `@NAME` elsewhere |
| `@export "in" "out" n` | Convert a TRSE asset (image, font, …) to a binary during build |

---

## The `#` address operator

In TRSE, `#variable` means *the address of* that variable — equivalent to `&` in C. This is how you pass pointers to procedures.

```pascal
Screen::Clear(#Screen::screen0, key_space);
//            ^ address of the screen0 variable defined in the Screen unit
```

You will see `#` used constantly when passing arrays, strings, and memory locations to built-in methods.

---

## Control flow

### while loop

```pascal
while (true) do
begin
    // game loop
end;
```

### for loop

```pascal
for i := 0 to 39 do
begin
    screenmemory[i] := key_space;
end;
```

### if / then / else

```pascal
if (x > 39) then x := 0;

if (health = 0) then
begin
    GameOver();
end
else
begin
    inc(health);
end;
```

### case

```pascal
case direction of
    0: MoveUp();
    1: MoveDown();
    2: MoveLeft();
    3: MoveRight();
end;
```

---

## Procedures

Procedures are subroutines with no return value. Define them before `begin` (or in a unit).

```pascal
procedure ClearRow(y : byte);
begin
    moveto(0, y, #Screen::screen0);
    for i := 0 to 39 do
        screenmemory[i] := key_space;
end;
```

Call them like built-in methods:

```pascal
ClearRow(12);
```

### The `global` keyword

By default, procedure parameters are local copies. Using `global` tells TRSE to reuse the global variable of the same name rather than making a copy — this saves RAM and stack space, which is precious on 8-bit machines.

```pascal
procedure DrawBox(x, y, w, h : global byte);
begin
    // x, y, w, h refer directly to the global variables
end;
```

!!! warning
    With `global` parameters, don't call procedures that use the same global variables nested inside each other — the outer call's values will be overwritten.

---

## Units

A unit is a `.tru` file that groups related variables and procedures. Units are the TRSE equivalent of a library or module.

```pascal
unit MyUnit;

var
    score : integer = 0;
    lives : byte    = 3;

procedure ResetGame();
begin
    score := 0;
    lives := 3;
end;

end.
```

Import it in your `.ras` file:

```pascal
@use "myunit"
```

Then access its contents with the `UnitName::` prefix:

```pascal
MyUnit::ResetGame();
MyUnit::lives -= 1;
```

---

## Working with memory

### Pointers and indexing

A `pointer` variable holds a 16-bit address. You can index it like an array to read and write memory:

```pascal
var
    ptr : pointer;

begin
    ptr := $D800;          // point to C64 colour RAM
    ptr[0] := red;         // set first byte to red
    ptr[1] := white;       // second byte to white
    ptr += screen_width;   // advance by 40 bytes
end.
```

### `incbin` — embedding binary data

Include pre-built binary files (graphics, sound, level data) at a fixed address:

```pascal
var
    charset : incbin("resources/charset.bin", $2000);
    image   : incbin("resources/image.bin",   $4000);
```

The data is assembled into the output binary at the address you specify.

---

## Built-in tables and values

TRSE pre-generates useful lookup tables for you. On 8-bit CPUs, table lookups are far faster than computing values at runtime.

| Table / constant | Description |
|-----------------|-------------|
| `sine[n]` | 256-entry sine table, values –128 to +127. `sine[n+64]` gives cosine. |
| `screen_width` | Columns on the current platform's text screen (e.g. 40 for C64). |
| `screen_height` | Rows on the current platform's text screen (e.g. 25 for C64). |
| `screenmemory` | Pointer to the current screen write position (set by `moveto`). |

Colour constants (`black`, `white`, `red`, `yellow`, …) and key constants (`key_space`, `key_return`, …) are also available, with platform-appropriate values.

---

## Operators

```pascal
x := 10;       // assignment
x += 1;        // increment
x -= 1;        // decrement
x := x * 2;   // multiply
x := x / 2;   // divide
x := x & $0F; // bitwise AND
x := x | $80; // bitwise OR
x := x ^ $FF; // bitwise XOR (NOT all bits)
x := (x + 3) & 15;  // wrap 0–15
```

---

## Comments

```pascal
// This is a single-line comment

/* This is a
   multi-line comment */

/**
    This is a doc comment — it appears in the in-IDE help
    when you hover over the next procedure.
**/
procedure MyProc();
```

---

## A minimal game loop

This is the pattern almost every TRSE program uses — wait for vertical blank, update game state, repeat forever.

```pascal
program MinimalGame;
@use "screen/screen"
var
    x, y, dx : byte;

begin
    Screen::border     := black;
    Screen::background := black;
    Screen::Clear(#Screen::screen0, key_space);
    Screen::Clear(#Screen::color, white);

    x  := 20;
    y  := 12;
    dx := 1;

    while (true) do
    begin
        Screen::WaitForVerticalBlank();

        // Erase old position
        Screen::PrintChar(key_space, x, y, #Screen::screen0);

        // Move
        x += dx;
        if (x > 38) then dx := -1;
        if (x = 0)  then dx :=  1;

        // Draw new position
        Screen::PrintChar($51, x, y, #Screen::screen0);   // ● character
    end;
end.
```

---

## Common mistakes

**Forgetting `begin`/`end` braces around multi-line blocks.**
If an `if` or `for` body has more than one statement, you must wrap it in `begin`/`end`. A missing `begin` will silently execute only the first line.

**Using `integer` when `byte` is enough.**
16-bit operations on 8-bit CPUs require multiple instructions. Use `byte` wherever 0–255 is sufficient.

**Indexing past the end of an array.**
TRSE doesn't add bounds checks. An out-of-range index will silently corrupt adjacent variables or code.

**Passing a value where an address is expected.**
Built-in methods that take memory addresses expect `#variable` (address-of), not `variable` (value). A missing `#` is one of the most common compile errors.

---

## Next steps

- **[Methods reference](reference/methods-index.md)** — complete listing of all built-in TRSE methods with parameters and platform compatibility
- **[Platforms](../platforms/index.md)** — hardware-specific memory maps, constants, and screen/sound addresses
- **[Tutorials](https://retrogamecoders.com/)** — example projects in the TRSE repository under `Publish/tutorials/`

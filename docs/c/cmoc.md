---
title: C with CMOC
description: CMOC — C cross-compiler for the 6809 CPU targeting Dragon 32, TRS-80 CoCo, and Vectrex in the RGC IDE.
---

# C with CMOC

**CMOC** is a cross-compiler for a subset of C that targets the **Motorola 6809** processor. It was created by Pierre Sarrazin and produces efficient 6809 assembly via the **LWASM** assembler (part of LWTOOLS). It supports the **Dragon 32**, **TRS-80 Color Computer** (CoCo), and **Vectrex** platforms.

Think of CMOC as the 6809 equivalent of cc65 — it lets you write readable, structured C code for machines that would otherwise require assembly, while still giving you access to inline assembly for performance-critical sections.

## What CMOC supports

CMOC implements a practical subset of C — enough for real games and applications:

- Basic types: `char`, `int`, `unsigned`, `long`, pointers
- `struct` and `union`
- `for`, `while`, `do...while`, `if/else`, `switch`
- Function calls and recursion
- Inline assembly with `asm { }`
- Standard library subset: `printf`, `malloc`, `memcpy`, `memset`, string functions
- Platform-specific headers for Dragon/CoCo/Vectrex hardware

What it doesn't support: `float` (no hardware FPU — use fixed-point), `long long`, the full C standard library.

## Quick start in the IDE

1. Select **Dragon 32**, **TRS-80 CoCo 2**, or **Vectrex** as the platform.
2. Choose the **C / CMOC** preset.
3. The template gives you a working `main.c` — read through it before editing.
4. **Build** — CMOC errors appear first, then LWASM/linker messages.

!!! tip "Start from the template"
    The startup code (setting up the C stack, calling `main`, and defining the entry point for the target platform) is in the template's assembly stub. Don't delete it.

## Hello, Dragon 32

```c
#include <cmoc.h>

int main(void) {
    // Clear screen and print
    cls();
    printf("HELLO FROM CMOC!\n");
    return 0;
}
```

Build and run — `printf` goes through CMOC's built-in runtime, which uses the platform's ROM print routines.

## Types and sizes

| Type | Size | Range |
|------|------|-------|
| `char` / `unsigned char` | 1 byte | -128–127 / 0–255 |
| `int` / `unsigned int` | 2 bytes | -32768–32767 / 0–65535 |
| `long` / `unsigned long` | 4 bytes | ±2 billion |
| pointer | 2 bytes | 16-bit |

**Use `unsigned char` for small values and loop counters** — the 6809 has efficient 8-bit operations. `unsigned int` is fine for 16-bit values (the 6809's D register is 16-bit). Avoid `long` in hot paths.

## Hardware access

### Direct memory access with pointers

```c
/* Write to Dragon 32 VDG mode register */
unsigned char *vdg_mode = (unsigned char *) 0xFF22;
*vdg_mode = 0x00;       /* Text mode */

/* Write to screen RAM (Dragon 32 text mode at $0400) */
unsigned char *screen = (unsigned char *) 0x0400;
screen[0] = 0xBF;       /* Block graphic character */
screen[1] = 0xC1;       /* 'A' in PETSCII-like Dragon charset */
```

### Platform-specific headers

CMOC provides platform headers with named constants and helper functions:

```c
#include <cmoc.h>
#include <dragon.h>     /* Dragon 32 specifics */

int main(void) {
    /* Clear screen */
    cls();

    /* Set graphics mode via Dragon register */
    setVDGMode(MODE_G6R);   /* 256x192, 2 colours */

    return 0;
}
```

(Exact header names and function names depend on your CMOC version — check the template.)

## Common patterns

### Screen output

```c
#include <cmoc.h>

/* Print string */
printf("Score: %u\n", score);

/* Print at position (Dragon/CoCo) */
/* Screen = 32 cols × 16 rows, base at $0400 */
unsigned char *screen = (unsigned char *) 0x0400;
screen[row * 32 + col] = char_code;
```

### Reading the joystick (Dragon 32)

The Dragon's joystick is read via the PIA comparator — a somewhat involved process that CMOC's library may abstract:

```c
#include <cmoc.h>

unsigned char joy_x = joystick(0);   /* X axis, 0-63 */
unsigned char joy_y = joystick(1);   /* Y axis, 0-63 */
unsigned char fire  = joystick_button(0);  /* 0 or 1 */
```

If the library doesn't provide joystick functions, read the PIA directly:

```c
/* Dragon: Fire button on PIA0-B bit 0 */
unsigned char *pia0b = (unsigned char *) 0xFF02;
if (!(*pia0b & 0x01)) {
    /* Fire pressed */
}
```

### Inline 6809 assembly

Drop into assembly for tight loops or hardware-specific code:

```c
void set_border_colour(unsigned char colour) {
    asm {
        lda     colour          ; Load the colour parameter
        sta     0xFF22          ; Write to VDG mode register
    }
}
```

Variables declared in C are accessible by name in the `asm {}` block. Check the CMOC documentation for the exact calling convention for parameters.

### Mixing C and separate assembly files

For larger assembly routines, write a `.asm` file and call it from C:

```c
/* Declare external assembly function */
extern void fast_clear_screen(void);

fast_clear_screen();    /* Call it */
```

In the `.asm` file:
```asm
; fast_clear.asm
    EXPORT _fast_clear_screen

_fast_clear_screen:
    ; ... 6809 code ...
    RTS
```

The CMOC convention prepends an underscore to C function names in assembly, like cc65.

## Vectrex-specific CMOC

For the Vectrex, CMOC includes headers that wrap the Vectrex BIOS calls:

```c
#include <cmoc.h>
#include <vectrex.h>

int main(void) {
    while (1) {
        Wait_Recal();           /* BIOS: wait for VBlank, recalibrate */

        /* Read controller */
        Read_Btns();
        if (Vec_Btn_State & 0x01) {
            /* Button 1 pressed */
        }

        /* Draw something */
        Moveto_d(0, 0);         /* Move beam to centre */
        Draw_Line_d(50, 50);    /* Draw line */
    }
}
```

The Vectrex BIOS functions are available as C-callable wrappers — you get the power of the BIOS with C syntax.

## Performance tips

**Avoid `long` in loops** — 32-bit arithmetic on the 6809 requires multiple instructions. Use `int` wherever 16 bits suffice.

**Use `unsigned` for counters** — unsigned comparisons often generate slightly better 6809 code than signed.

**Prefer `static` local variables** — static locals live in global BSS, not on the C stack. Stack access on the 6809 uses the S register with an offset, which is slightly slower than direct addressing.

**Inline assembly for inner loops** — if a loop runs every frame, a tight `asm {}` block is often 3–5× faster than the equivalent C.

**Use `register` variables** — CMOC tries to keep `register`-declared variables in 6809 registers (typically D, X, Y, U).

## Building manually (for reference)

The IDE handles this, but knowing the steps helps with debugging:

```bash
cmoc --dragon --org=0x3F00 -o program.bin main.c   # Dragon 32 target
lwasm --format=ihex -o program.hex main.asm         # If using separate asm
```

## Common errors

**"type not supported"** — CMOC doesn't support all C types. `float` and `double` are the most common unsupported types. Use integer fixed-point instead.

**"function not found in library"** — CMOC's standard library is a subset. Check the CMOC documentation for what's available. Many standard string/math functions are present; some aren't.

**Stack overflow** — CMOC uses a C software stack (separate from the 6809 hardware stack). Large local arrays or deep recursion can overflow it silently. Use `static` arrays and limit recursion depth.

**Inline assembly calling convention** — parameters in `asm {}` blocks are accessed by the C variable name, but the register they live in may vary. Read the CMOC documentation for how parameters and locals are passed.

## Official resources

- **[CMOC homepage](https://perso.b2b2c.ca/~sarrazip/dev/cmoc.html)** — documentation, downloads, and examples
- **[LWTOOLS / LWASM](http://lwtools.projects.l-com.net/)** — the assembler CMOC uses

## See also

- [6809 assembly](../assembly/6809.md) — the 6809 instruction set reference
- [Color BASIC](../basic/color-basic.md) — BASIC alternative for Dragon/CoCo
- [Dragon 32 / CoCo platform guide](../platforms/dragon-coco.md)
- [Vectrex platform guide](../platforms/vectrex.md)
- [IDE getting started](../ide/getting-started.md)

---
title: C with z88dk
description: Using the z88dk C compiler for Z80 platforms — ZX Spectrum, MSX, Amstrad CPC, and more.
---

# C with z88dk

**z88dk** is the C development kit for **Z80** systems — it's to Z80 machines what cc65 is to 6502 machines. It supports the ZX Spectrum, MSX, Amstrad CPC, and many other platforms, letting you write portable C code that compiles down to efficient Z80 machine code.

z88dk includes two C compilers:

| Compiler | Characteristics |
|----------|----------------|
| **sccz80** | z88dk's own compiler; conservative, predictable output |
| **zsdcc** | Port of SDCC; more optimisations, better standard compliance |

The IDE chooses the right compiler for the platform preset you select. Both produce code you can mix with hand-written Z80 assembly.

## Quick start in the IDE

1. Choose a **Z80 platform** (ZX Spectrum, MSX, etc.) and select **C / z88dk**.
2. Open the template — it shows the right `#include`s and the `main()` signature for that target.
3. **Build** and run in the emulator.

!!! tip "Check which compiler the preset uses"
    The build log will show either `sccz80` or `zsdcc`. Both are fine; `zsdcc` typically produces faster code, while `sccz80` is more predictable for beginners.

## Hello, ZX Spectrum

```c
#include <stdio.h>
#include <spectrum.h>

int main(void) {
    /* Set border colour to blue */
    zx_border(INK_BLUE);

    /* Print to screen */
    printf("Hello from z88dk!\n");

    return 0;
}
```

`spectrum.h` gives you helper functions like `zx_border()` and `zx_colour()` so you're not hand-calculating attribute bytes. Build, and it runs straight in the Spectrum emulator.

## Useful headers per platform

=== "ZX Spectrum"
    ```c
    #include <spectrum.h>   // zx_border, zx_colour, screen helpers
    #include <stdio.h>      // printf
    #include <stdlib.h>     // rand, abs
    #include <string.h>     // memcpy, memset, strlen
    #include <input.h>      // in_key_pressed, in_inkey
    #include <games.h>      // Joystick and game helpers
    ```

=== "MSX"
    ```c
    #include <msx.h>        // MSX BIOS calls
    #include <stdio.h>
    #include <stdlib.h>
    ```

=== "Amstrad CPC"
    ```c
    #include <cpc.h>        // CPC-specific helpers
    #include <stdio.h>
    ```

## Common patterns

### Screen output

```c
#include <stdio.h>

printf("Score: %d\n", score);   /* Standard output — works everywhere */
```

For the ZX Spectrum, `printf` goes through the ROM's print routine. It's not fast, but it works for text output and debugging.

### Colours and attributes (ZX Spectrum)

```c
#include <spectrum.h>

/* Set border colour */
zx_border(INK_RED);

/* Set ink/paper for next print operations */
printf("\x10\x01");   /* Ink 1 (Blue) — using Spectrum control codes */
printf("\x11\x06");   /* Paper 6 (Yellow) */

/* Set a specific character cell's attribute directly */
/* Attribute address = 0x5800 + row*32 + col */
volatile unsigned char *attr = (unsigned char*)0x5800 + (row * 32) + col;
*attr = INK_WHITE | PAPER_BLUE | BRIGHT;
```

Spectrum attribute constants from `spectrum.h`:

| Constant | Value |
|----------|-------|
| `INK_BLACK` … `INK_WHITE` | 0–7 |
| `PAPER_BLACK` … `PAPER_WHITE` | 0–7 (shifted to bits 3–5 in attribute byte) |
| `BRIGHT` | 0x40 |
| `FLASH` | 0x80 |

### Keyboard input (ZX Spectrum)

```c
#include <input.h>

/* Check if a specific key is held down */
if (in_key_pressed(IN_KEY_SCANCODE_z)) {
    /* Z key is held */
}

/* Read any key (like INKEY$) */
unsigned int key = in_inkey();
if (key) {
    /* key contains the key code */
}
```

### Memory operations

```c
#include <string.h>

/* Clear the Spectrum screen (pixel area) */
memset((void*)0x4000, 0x00, 6144);

/* Clear attributes to white-on-black */
memset((void*)0x5800, 0x38, 768);   /* 0x38 = white paper, black ink */

/* Copy a block of data */
memcpy(destination, source, length);
```

### Inline Z80 assembly

```c
/* Single-line inline assembly */
#asm
    nop
#endasm

/* Multi-line block */
#asm
    ld a, 2
    out (254), a    ; Set border to red (ZX Spectrum)
#endasm
```

With zsdcc (SDCC-based), the syntax uses `__asm__`:

```c
__asm__("nop");
__asm__(
    "ld a, #2\n"
    "out (#254), a\n"
);
```

Check which compiler your preset uses and use the appropriate syntax.

## Calling assembly from C

Write a `.asm` file:

```asm
; set_border.asm — callable from C
PUBLIC _set_border

._set_border
    ; Argument arrives in L register (z88dk calling convention)
    ld a, l
    out (254), a    ; Set ZX Spectrum border
    ret
```

Declare in C:

```c
extern void set_border(unsigned char colour);

set_border(2);   /* Red border */
```

The z88dk calling convention passes the first argument in HL (with the value in L for 8-bit args). Check the z88dk documentation for multi-argument functions.

## Types and sizes

| Type | Size | Notes |
|------|------|-------|
| `char` / `unsigned char` | 1 byte | Your most-used type |
| `int` / `unsigned int` | 2 bytes | Native 16-bit on Z80 |
| `long` | 4 bytes | Slow — avoid in hot paths |
| pointer | 2 bytes | 16-bit |

The Z80 is a 16-bit processor at heart (most registers are 16-bit), so `unsigned int` arithmetic is efficient. `unsigned char` is still fastest for small counters and array indices.

## Performance tips

**Use `unsigned char` for small counters** — the Z80's `DJNZ` instruction (decrement B and branch if not zero) is the fastest loop construct, and B is an 8-bit register.

**Use `memset` and `memcpy` for bulk operations** — z88dk implements these with `LDIR`, the Z80's block-copy instruction. It's much faster than a C loop.

**Avoid `long` arithmetic in inner loops** — 32-bit operations on the Z80 are slow multi-instruction sequences.

**Use `static` local variables for hot data** — keeps them in global memory rather than the software stack.

## Common mistakes

**Attribute vs pixel addressing on the Spectrum** — the pixel RAM ($4000–$57FF) and attribute RAM ($5800–$5AFF) are separate. Drawing to one doesn't affect the other; you usually need to update both.

**Non-linear Spectrum pixel layout** — pixel rows are stored in a non-linear order on the 48K Spectrum. If you're writing directly to pixel RAM rather than using library functions, you need to calculate addresses carefully:

```c
/* Address of pixel row y, column x (y: 0-191, x: 0-31) */
unsigned char *pixel_addr = (unsigned char*)0x4000
    + ((y & 7) << 8)
    + ((y & 0x38) << 2)
    + ((y >> 6) << 11)
    + x;
```

**Stack overflow** — z88dk uses a software stack separate from the Z80 hardware stack. Large local arrays or deep recursion can overflow it silently.

**ROM paging on 128K Spectrum** — if your target is the 128K Spectrum, be careful about paging in ROMs or RAM banks that overwrite your code.

## Official docs

- **[z88dk.org](https://z88dk.org)** — compiler documentation, target library reference, examples
- **[z88dk GitHub](https://github.com/z88dk/z88dk)** — source, wiki, and platform-specific guides

## See also

- [Z80 assembly](../assembly/z80.md) — Z80 assembly language reference
- [ZX Spectrum platform guide](../platforms/zx-spectrum.md)
- [ZX BASIC (Boriel)](../basic/zx-basic.md) — compiled BASIC alternative for the Spectrum
- [IDE getting started](../ide/getting-started.md)

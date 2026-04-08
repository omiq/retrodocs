# RGC BASIC — graphics (`basic-gfx` & Raylib)

**`basic-gfx`** is the graphical build of the interpreter, linked against **[Raylib](https://www.raylib.com/)**. It opens a window with a **40×25** (or **80×25** with `-columns 80`) PETSCII-style display, **virtual memory** for `POKE`/`PEEK`, **`INKEY$`**, **`TI`/`TI$`**, bitmap mode, PNG sprites, gamepads, and more — while sharing the same BASIC language as **`basic`**.

Build from source with **`make basic-gfx`** after Raylib is installed; releases ship **`basic-gfx`** next to **`basic`**.

## Typical commands

```bash
./basic-gfx examples/gfx_poke_demo.bas
./basic-gfx -petscii examples/gfx_inkey_demo.bas
./basic-gfx -petscii -charset lower examples/gfx_colaburger_viewer.bas
```

On Windows use `basic-gfx.exe`. Paths to assets are often **relative to the `.bas` file’s directory**.

## Text screen & virtual memory

- **C64-style layout** is default; **`#OPTION memory pet`** (or CLI `-memory pet`) can remap regions (screen, colour, charset, keyboard matrix, bitmap) — see upstream README **Meta directives** section.
- **`POKE` / `PEEK`** apply to this **virtual** address space (not your PC’s RAM).
- **`LOAD "file" INTO addr`** / **`LOAD @label INTO addr`** — load raw bytes into virtual memory (**gfx**; terminal build errors).
- **`MEMSET` / `MEMCPY`** — fill/copy bytes in virtual memory (**gfx**).

## Keyboard & time

- **`INKEY$`** — Non-blocking; returns one character or `""`. Case may vary; use **`UCASE$(INKEY$())`** for comparisons.
- **`INPUT`** — In gfx, reads from the **window** key queue (not the terminal).
- **`PEEK(56320 + code)`** — Poll a key map (**`GFX_KEY_BASE`**); codes documented in README (letters as uppercase ASCII, etc.).
- **`TI`** — 60 Hz jiffy counter (wraps per README); **`TI$`** — time string `HHMMSS`.
- **`SLEEP n`** — Pause in **ticks** (60 ≈ 1 second).

## Display modes

- **`SCREEN 1`** — 320×200 **1bpp** bitmap; **`SCREEN 0`** — back to text. **`PSET`/`PRESET`**, **`LINE`** for drawing.
- **`SCREENCODES ON|OFF`** — Treat stream bytes as PETSCII (e.g. `.seq` art viewers); **`OFF`** for normal ASCII `PRINT`.

## Sprites & scrolling

- **`LOADSPRITE slot, "file.png"`** — Optional tile size **`tw, th`** for tile sheets.
- **`DRAWSPRITE`**, **`DRAWSPRITETILE`**, **`SPRITEFRAME`**, **`UNLOADSPRITE`** — see README for full argument lists and **z-order**.
- **`SCROLL dx, dy`** — Pixel panning; **`SCROLLX()`** / **`SCROLLY()`** read offsets.
- **Gamepad:** **`JOY`/`JOYSTICK`**, **`JOYAXIS`** — port and button/axis indices differ slightly between **native Raylib** and **browser canvas** WASM; README tables are authoritative.

## Browser (IDE) vs native

The **WASM/canvas** build aims to mirror **`basic-gfx`** for teaching; a few host details (gamepad mapping, exact feature flags) may differ by release. Treat the **upstream README** and **CHANGELOG** as definitive for parity.

## See also

- [Terminal & PETSCII](terminal-petscii.md) — plain `basic` without a window
- [Web IDE](web-ide.md) — browser integration
- [Install & platforms](install.md) — obtaining binaries
- [github.com/omiq/rgc-basic — README](https://github.com/omiq/rgc-basic/blob/main/README.md) — full API detail

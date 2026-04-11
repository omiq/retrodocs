# RGC BASIC — graphics (`basic-gfx` & Raylib)

**`basic-gfx`** is the graphical build of the interpreter, linked against **[Raylib](https://www.raylib.com/)**. It opens a window with a **40×25** (or **80×25** with `-columns 80`) PETSCII-style display, **virtual memory** for `POKE`/`PEEK`, **`INKEY$`**, **`TI`/`TI$`**, bitmap mode, **PNG sprites with tile sheets, z-order, tint/scale, and collision**, viewport scrolling, gamepads, and more — while sharing the same BASIC language as **`basic`**.

Build from source with **`make basic-gfx`** after Raylib is installed; releases ship **`basic-gfx`** next to **`basic`**.

On Windows use `basic-gfx.exe`. Paths to assets are **relative to the `.bas` file’s directory** (or absolute).

## Quick start

Run locally from the repo **`examples/`** folder (or release archive):

```bash
./basic-gfx examples/gfx_poke_demo.bas
./basic-gfx -petscii examples/gfx_inkey_demo.bas
./basic-gfx -petscii -charset lower examples/gfx_colaburger_viewer.bas
./basic-gfx examples/gfx_sprite_hud_demo.bas
./basic-gfx examples/gfx_game_shell.bas
```

**Web IDE** — same **`.bas`** basenames as the IDE’s RGC BASIC preset ([`?file=…&platform=rgc-basic`](web-ide.md#opening-the-platform)):

| Example | Open in IDE |
|---------|-------------|
| `gfx_poke_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_poke_demo.bas&platform=rgc-basic) |
| `gfx_inkey_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_inkey_demo.bas&platform=rgc-basic) |
| `gfx_colaburger_viewer.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_colaburger_viewer.bas&platform=rgc-basic) |
| `gfx_sprite_hud_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_sprite_hud_demo.bas&platform=rgc-basic) |
| `gfx_game_shell.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_game_shell.bas&platform=rgc-basic) |

Tutorial-style demos (also listed under [Examples](#example-programs-in-the-repo)) include `tutorial_gfx_scroll.bas`, `tutorial_gfx_memory.bas`, `tutorial_gfx_tilemap.bas`, and `tutorial_gfx_gamepad.bas`.

## Text screen & virtual memory

- **C64-style layout** is default; **`#OPTION memory pet`** (or CLI `-memory pet`) can remap regions (screen, colour, charset, keyboard matrix, bitmap) — see the [upstream README — Meta directives](https://github.com/omiq/rgc-basic/blob/main/README.md#-features).
- **`POKE` / `PEEK`** apply to this **virtual** address space (not your PC’s RAM).
- **`LOAD "file" INTO addr`** / **`LOAD @label INTO addr`** — load raw bytes into virtual memory (**gfx**; terminal build errors).
- **`MEMSET` / `MEMCPY`** — fill/copy bytes in virtual memory (**gfx**).

## Keyboard & time

- **`INKEY$`** — Non-blocking; returns one character or `""`. Case may vary; use **`UCASE$(INKEY$())`** for comparisons.
- **`INPUT`** — In gfx, reads from the **window** key queue (not the terminal).
- **`PEEK(56320 + code)`** — Poll a key map (**`GFX_KEY_BASE`** = `0xDC00`); codes for letters use **uppercase ASCII** (e.g. W = 87). Supported keys include ASCII `A`–`Z`, `0`–`9`, Space (32), Enter (13), Esc (27), and C64 cursor codes Up (145), Down (17), Left (157), Right (29).
- **`TI`** — 60 Hz jiffy counter (wraps per README); **`TI$`** — time string `HHMMSS`.
- **`SLEEP n`** — Pause in **ticks** (60 ≈ 1 second).

## Bitmap mode (`SCREEN 1`)

- **`SCREEN 1`** — 320×200 **1 bpp** bitmap; **`SCREEN 0`** — back to 40×25 text.
- **`COLOR` / `BACKGROUND`** — Set pen and paper in bitmap mode (same C64-style indices as text).
- **`PSET x, y`** / **`PRESET x, y`** — Set/clear one pixel (clipped to the bitmap).
- **`LINE x1, y1 TO x2, y2`** — Bresenham line (same clipping).

Example: `./basic-gfx examples/gfx_bitmap_demo.bas` — [Web IDE](https://ide.retrogamecoders.com/?file=gfx_bitmap_demo.bas&platform=rgc-basic)

## `SCREENCODES` and text streams

- **`SCREENCODES ON|OFF`** — **`ON`**: treat stream bytes as **PETSCII** (e.g. `.seq` art viewers); **`OFF`**: normal ASCII `PRINT`.

## PNG sprites — full reference

Sprites use **numbered slots** (0 … 63 in the implementation). Only **`.png`** is loaded via this API; use **`LOAD "bin" INTO …`** for raw bytes.

### Loading and unloading

| Statement / function | Meaning |
|------------------------|---------|
| **`LOADSPRITE slot, "file.png"`** | Queue load from disk. Path relative to the **`.bas` file’s directory** or absolute. |
| **`LOADSPRITE slot, "tiles.png", tw, th`** | **Tile sheet**: image is a grid of **`tw`×`th`** pixel cells, row-major, left-to-right. |
| **`UNLOADSPRITE slot`** | Free texture and clear draw state; slot can be reused. No-op if empty. |

### Drawing and visibility

| Statement | Syntax | Notes |
|-----------|--------|--------|
| **`DRAWSPRITE`** | `DRAWSPRITE slot, x, y [, z [, sx, sy [, sw, sh ]]]` | Sets **persistent** pose: the same image is drawn **every frame** until another `DRAWSPRITE` for that slot or exit. |
| **`DRAWSPRITETILE`** | `DRAWSPRITETILE slot, x, y, tile_index [, z]` | **`tile_index`** is **1-based** (first tile = 1). Requires **`LOADSPRITE`** with two tile dimensions. |
| **`SPRITEVISIBLE`** | `SPRITEVISIBLE slot, 0 \| 1` | Hide/show without unloading. |

**Coordinates:** **`x`**, **`y`** are **pixel** coordinates on the **320×200** framebuffer (not character columns/rows). Text row *r* starts at **`y = r × 8`** (characters are 8 pixels tall).

**Depth (`z`):** Larger **`z`** draws **on top** (e.g. PETSCII/bitmap near **0**, HUD overlay **200**). Draw order is sorted by **`z`**.

**Source rectangle:** Omit **`sx`, `sy`** to use the top-left of the image. Omit **`sw`, `sh`** (or use ≤0) to use the full texture from **`(sx, sy)`**. **`DRAWSPRITE`** with explicit **`sx, sy, sw, sh`** supports arbitrary crops from a single PNG.

**Alpha:** PNG alpha is respected (transparency over text or bitmap).

### Tile sheets and animation

| Function / statement | Meaning |
|----------------------|---------|
| **`SPRITETILES(slot)`** | Number of tiles in a loaded tile sheet (after **`LOADSPRITE …, tw, th`**). |
| **`SPRITEW(slot)`** / **`SPRITEH(slot)`** | Pixel width/height: for tile sheets, **one cell’s** size; else full texture (**0** if not loaded). |
| **`SPRITEFRAME slot, frame`** | Set **1-based** tile index used when **`DRAWSPRITE`** omits **`sx, sy, sw, sh`** (same as choosing that tile with **`DRAWSPRITETILE`**). |
| **`SPRITEFRAME(slot)`** | Current **1-based** frame index. |

### Tint, opacity, and scale

| Statement | Syntax |
|-----------|--------|
| **`SPRITEMODULATE`** | `SPRITEMODULATE slot, alpha [, r, g, b [, scale_x [, scale_y]]]` |

- **`alpha`** and **`r`/`g`/`b`** are **0–255** (defaults **255**). **`alpha`** multiplies the PNG’s alpha.
- Optional **`scale_x`**, **`scale_y`** stretch the drawn sprite (default **1**). If you pass only **`scale_x`**, **`scale_y`** is set to the same value.
- Resets to **opaque white at 1×** on each **`LOADSPRITE`** / **`UNLOADSPRITE`**.

### Collision

| Function | Meaning |
|----------|---------|
| **`SPRITECOLLIDE(a, b)`** | **1** if axis-aligned bounding boxes of two **visible**, **drawn** sprites overlap; **0** otherwise. Empty or hidden slots never collide. |

## Viewport scrolling

- **`SCROLL dx, dy`** — Pixel offset for the **text/bitmap layer and sprites** (positive **`dx`** pans the world left; positive **`dy`** pans up). **`SCROLL 0, 0`** resets.
- **`SCROLLX()`** / **`SCROLLY()`** — Current offset (roughly **-32768..32767**).

Example: `examples/tutorial_gfx_scroll.bas` — [Web IDE](https://ide.retrogamecoders.com/?file=tutorial_gfx_scroll.bas&platform=rgc-basic)

## Gamepad

| Function | Meaning |
|----------|---------|
| **`JOY(port, button)`** / **`JOYSTICK`** | **1** if pressed, else **0**. Alias: **`JOYSTICK`**. |
| **`JOYAXIS(port, axis)`** | Stick/trigger **about -1000..1000** (axes **0–5**: left X/Y, right X/Y, left trigger, right trigger). |

Port **0** is the first controller. **Native `basic-gfx`** uses Raylib button codes **1–15** (**0** = unknown). **Canvas WASM** maps to the browser **Standard Gamepad** layout. The plain **`basic`** terminal build has no gamepad.

Example: `./basic-gfx examples/gfx_joy_demo.bas` — [Web IDE](https://ide.retrogamecoders.com/?file=gfx_joy_demo.bas&platform=rgc-basic)

## Window chrome (basic-gfx)

- **Title:** `#OPTION gfx_title "My Game"` or **`-gfx-title "My Game"`** (default `RGC-BASIC GFX`).
- **Border:** `#OPTION border 24` or **`-gfx-border 24`** — padding in pixels on each side; screen centered. Optional colour: `#OPTION border 10 cyan` or **`-gfx-border "10 cyan"`** (names or palette **0–15**).

## Browser (IDE) vs native

The **WASM/canvas** build aims to mirror **`basic-gfx`** for teaching; host details (gamepad mapping, async **`SLEEP`** / paint) can differ — see **[`web/README.md`](https://github.com/omiq/rgc-basic/blob/main/web/README.md)** and **`docs/gfx-canvas-parity.md`** in the repo. Tight loops without **`SLEEP`** can starve the browser tab; the upstream README discusses this.

## Example programs in the repo

| Focus | Examples | Web IDE |
|-------|----------|---------|
| Sprites + HUD | `gfx_sprite_hud_demo.bas`, `gfx_game_shell.bas`, `gfx_canvas_demo.bas` | [1](https://ide.retrogamecoders.com/?file=gfx_sprite_hud_demo.bas&platform=rgc-basic) · [2](https://ide.retrogamecoders.com/?file=gfx_game_shell.bas&platform=rgc-basic) · [3](https://ide.retrogamecoders.com/?file=gfx_canvas_demo.bas&platform=rgc-basic) |
| Scroll / memory / tiles / pad | `tutorial_gfx_scroll.bas`, `tutorial_gfx_memory.bas`, `tutorial_gfx_tilemap.bas`, `tutorial_gfx_gamepad.bas` | [1](https://ide.retrogamecoders.com/?file=tutorial_gfx_scroll.bas&platform=rgc-basic) · [2](https://ide.retrogamecoders.com/?file=tutorial_gfx_memory.bas&platform=rgc-basic) · [3](https://ide.retrogamecoders.com/?file=tutorial_gfx_tilemap.bas&platform=rgc-basic) · [4](https://ide.retrogamecoders.com/?file=tutorial_gfx_gamepad.bas&platform=rgc-basic) |
| PETSCII viewers | `gfx_colaburger_viewer.bas`, `gfx_inkey_demo.bas` | [1](https://ide.retrogamecoders.com/?file=gfx_colaburger_viewer.bas&platform=rgc-basic) · [2](https://ide.retrogamecoders.com/?file=gfx_inkey_demo.bas&platform=rgc-basic) |
| Bitmap | `gfx_bitmap_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_bitmap_demo.bas&platform=rgc-basic) |

Index listing: `examples/tutorial_gfx_index.bas` — [Web IDE](https://ide.retrogamecoders.com/?file=tutorial_gfx_index.bas&platform=rgc-basic). Static HTML overview: **`web/tutorial-gfx-features.html`** when you serve **`web/`** over HTTP.

## See also

- [Terminal & PETSCII](terminal-petscii.md) — plain `basic` without a window
- [Web IDE](web-ide.md) — browser integration
- [Install & platforms](install.md) — obtaining binaries
- [github.com/omiq/rgc-basic — README](https://github.com/omiq/rgc-basic/blob/main/README.md) — authoritative detail, CLI flags, and edge cases
- [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md) — per-release behaviour

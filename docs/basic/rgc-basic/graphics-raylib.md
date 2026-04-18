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
- **`KEYDOWN(code)`** — 1 while the key is currently held, else 0. Use for **diagonal movement** — `A+D` or `A+W` fire independently, unlike `INKEY$` which only surfaces one key at a time.
- **`KEYUP(code)`** — Inverse of `KEYDOWN`. 1 when the key is *not* held.
- **`KEYPRESS(code)`** — Rising-edge latch: returns 1 exactly once per press, then 0 until the key is released and pressed again. Good for pause toggles / single-shot actions.
- **`PEEK(56320 + code)`** — Lower-level key-map poll (`GFX_KEY_BASE` = `0xDC00`). The `KEYDOWN`/`KEYUP`/`KEYPRESS` functions are equivalent to `PEEK(GFX_KEY_BASE + code)` plus the edge-latch tracking, and survive `#OPTION memory` base changes.
- **Key codes:** uppercase ASCII for letters/digits (e.g. `W` = 87, `A` = 65); special keys Space (32), Enter (13), Esc (27), Tab (9), Backspace (8), and C64 cursor codes Up (145), Down (17), Left (157), Right (29).
- **`TI`** — 60 Hz jiffy counter (wraps per README); **`TI$`** — time string `HHMMSS`.
- **`SLEEP n`** — Pause in **ticks** (60 ≈ 1 second).
- **`VSYNC`** — Frame commit + ~16 ms wait. Atomically flips the `TILEMAP DRAW` / `SPRITE STAMP` build buffer to the show buffer so the renderer never displays a half-populated scene, then yields one display frame. Use `VSYNC` at the end of a per-frame loop instead of `SLEEP 1` for flicker-free output.

## Bitmap mode (`SCREEN 1`)

- **`SCREEN 1`** — 320×200 **1 bpp** bitmap; **`SCREEN 0`** — back to 40×25 text.
- **`COLOR` / `BACKGROUND`** — Set pen and paper in bitmap mode (same C64-style indices as text).
- **`PSET x, y`** / **`PRESET x, y`** — Set/clear one pixel (clipped to the bitmap).
- **`LINE x1, y1 TO x2, y2`** — Bresenham line (same clipping).
- **`RECT x1, y1 TO x2, y2`** — Rectangle outline in the current pen.
- **`FILLRECT x1, y1 TO x2, y2`** — Solid rectangle (either corner diagonal works).
- **`CIRCLE x, y, r`** — Midpoint-circle outline.
- **`FILLCIRCLE x, y, r`** — Solid disk.
- **`ELLIPSE x, y, rx, ry`** — Axis-aligned ellipse outline (midpoint algorithm).
- **`FILLELLIPSE x, y, rx, ry`** — Solid ellipse.
- **`TRIANGLE x1,y1, x2,y2, x3,y3`** — Triangle outline.
- **`FILLTRIANGLE x1,y1, x2,y2, x3,y3`** — Solid triangle (scanline fill).
- **`DRAWTEXT x, y, text$`** — Pixel-space text using the active 8×8 charset (OR blend, current pen). Unlike `PRINT` / `TEXTAT` this isn't tied to the 40×25 text grid, so HUDs can sit anywhere. Bytes of `text$` go through `petscii_to_screencode`.
- **`BITMAPCLEAR`** — Wipe the bitmap plane without touching text/colour RAM.

Examples: `./basic-gfx examples/gfx_bitmap_demo.bas` · `examples/gfx_hud_demo.bas` · `examples/gfx_ball_demo.bas`.

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
| **`SPRITETILES(slot)`** / **`TILE COUNT(slot)`** / **`SPRITE FRAMES(slot)`** | Number of tiles in a loaded tile sheet (after **`LOADSPRITE …, tw, th`** / `SPRITE LOAD …`). |
| **`SHEET COLS(slot)`** / **`SHEET ROWS(slot)`** | Grid shape of the loaded sheet. |
| **`SHEET WIDTH(slot)`** / **`SHEET HEIGHT(slot)`** | Cell dimensions in pixels. |
| **`SPRITEW(slot)`** / **`SPRITEH(slot)`** | Pixel width/height: for tile sheets, **one cell’s** size; else full texture (**0** if not loaded). |
| **`SPRITEFRAME slot, frame`** / **`SPRITE FRAME …`** | Set **1-based** tile index used when **`DRAWSPRITE`** omits **`sx, sy, sw, sh`** (same as choosing that tile with **`DRAWSPRITETILE`**). |
| **`SPRITEFRAME(slot)`** | Current **1-based** frame index. |
| **`ANIMFRAME(first, last, jiffies_per_frame)`** | Time-based frame cycler. Returns a 1-based index in `[first, last]`, advancing every `jiffies_per_frame` ticks (60 jiffies = 1 second). Feeds straight into `SPRITE FRAME`: e.g. `SPRITE FRAME 0, ANIMFRAME(1, 4, 6)` cycles four frames at 10 FPS without a counter variable. |

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

## Two-word command family

New graphics commands follow AMOS/STOS-style **verb/noun** spellings. Existing concat names (`LOADSPRITE`, `DRAWSPRITE`, `SPRITEFRAME`, `UNLOADSPRITE`, `DRAWSPRITETILE`, `DRAWTILEMAP`, `SPRITETILES`) stay as permanent aliases — both spellings tokenise to the same handler.

| Two-word (canonical) | Concat alias |
|---|---|
| `SPRITE LOAD slot, "file.png" [, tw, th]` | `LOADSPRITE` |
| `SPRITE DRAW slot, x, y [, z [, sx, sy [, sw, sh]]]` | `DRAWSPRITE` |
| `SPRITE FRAME slot, n` | `SPRITEFRAME` |
| `SPRITE FREE slot` | `FREESPRITE` / `UNLOADSPRITE` |
| `SPRITE FRAMES(slot)` | `SPRITETILES(slot)` |
| `SPRITE STAMP slot, x, y [, frame [, z]]` | *(new)* |
| `TILE DRAW slot, x, y, tile_idx [, z]` | `DRAWSPRITETILE` / `DRAWTILE` |
| `TILE COUNT(slot)` | `SPRITETILES(slot)` |
| `TILEMAP DRAW slot, x0, y0, cols, rows, map [, z]` | `DRAWTILEMAP` |
| `SHEET COLS(slot)` / `SHEET ROWS(slot)` / `SHEET WIDTH(slot)` / `SHEET HEIGHT(slot)` | *(new accessors)* |
| `IMAGE NEW slot, w, h` / `IMAGE FREE slot` / `IMAGE COPY …` / `IMAGE SAVE slot, "path.bmp"` | *(new blitter)* |

Pick whichever spelling reads cleaner in your program.

## Sprite stamping vs persistent draw

**`SPRITE DRAW`** tracks a single persistent position per slot — N calls with the same slot collapse to the last one. Use it for the player, a single enemy, a HUD panel, etc.

**`SPRITE STAMP slot, x, y [, frame [, z [, rot_deg]]]`** appends one cell to a per-frame list, so N stamps of one slot in one frame all render at distinct positions. Use it for **particles, bullets, enemy swarms, starfields** — any case where you'd previously have called `SPRITECOPY` into many slots. Optional `rot_deg` rotates around the sprite centre (raylib backend only — canvas/WASM accepts the arg but ignores it).

`frame` is a 1-based tile index; `0` or omitted falls back to the slot's current `SPRITE FRAME`. If the slot holds a single image with no tile grid the draw uses the full sprite rect.

Per-frame loop:

```basic
SCREEN 1
SPRITE LOAD 0, "particle.png"
SPRITE LOAD 1, "ship.png"
loop:
  IF KEYDOWN(ASC("Q")) THEN END
  CLS
  FOR I = 0 TO 49
    SPRITE STAMP 0, SX(I), SY(I), 0, 10
  NEXT I
  DRAWSPRITE 1, PLX, PLY, 100
  VSYNC
GOTO loop
```

Example: `examples/gfx_stamp_demo.bas`.

## Tilemaps (`TILEMAP DRAW`)

```basic
DIM MAP(COLS*ROWS-1)
REM … populate map with 1-based tile indices (0 = transparent) …
TILEMAP DRAW 0, 0, 0, COLS, ROWS, MAP()
```

One batched call stamps the whole grid — one interpreter dispatch regardless of tile count. Cells layer with `SPRITE STAMP` output; the renderer draws tiles before sprites so a player sprite at `z=100` composites on top of a background tilemap at `z=0`. Supports negative `x0`/`y0` for smooth scrolling under a fixed viewport.

Shape/metadata:

```basic
PRINT "sheet is "; SHEET COLS(0); "x"; SHEET ROWS(0)
PRINT "cell is ";  SHEET WIDTH(0); "x"; SHEET HEIGHT(0)
PRINT "total cells: "; TILE COUNT(0)
```

Examples: `examples/gfx_tilemap_demo.bas`, `examples/gfx_world_demo.bas` (40×40 world + push-scroll + WASD player).

## Blitter surfaces (`IMAGE NEW` / `COPY` / `SAVE`)

Off-screen 1bpp bitmap surfaces for scroll / parallax / work-buffer patterns from AMOS/STOS-style BASIC.

- **`IMAGE NEW slot, w, h`** — allocate an off-screen bitmap. `slot` is 1..31. Any dimensions; surface starts empty.
- **`IMAGE FREE slot`** — release it.
- **`IMAGE COPY src, sx, sy, sw, sh TO dst, dx, dy`** — rectangular 1bpp blit between any two slots. Slot `0` is the live visible bitmap (320×200), so visible↔offscreen copies work without conversion. Overlapping same-slot rects stage through a scratch row buffer.
- **`IMAGE SAVE slot, "path.bmp"`** — export as 24-bit BMP (pen=1 → white, pen=0 → black). Convert to PNG externally if needed.

**Smooth scroll recipe** (`examples/gfx_scroll_demo.bas`):

```basic
IMAGE NEW 1, 640, 200      : REM oversized world
REM … paint world into slot 1 …
REM each frame:
IMAGE COPY 1, XO, 0, 320, 200 TO 0, 0, 0
```

**Parallax** (`examples/gfx_parallax_demo.bas`): one surface per band, independent `XO` per band, one `IMAGE COPY` per band per frame.

**Screenshot**:

```basic
IMAGE COPY 0, 0, 0, 320, 200 TO 1, 0, 0
IMAGE SAVE 1, "shot.bmp"
```

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

# RGC BASIC — graphics (`basic-gfx` & Raylib)

**`basic-gfx`** is the graphical build of the interpreter, linked against **[Raylib](https://www.raylib.com/)**. It opens a window with a **40×25** (or **80×25** with `-columns 80`) PETSCII-style display, **virtual memory** for `POKE`/`PEEK`, **`INKEY$`**, **`TI`/`TI$`**, bitmap mode, **PNG sprites with tile sheets, z-order, tint/scale, and collision**, viewport scrolling, gamepads, and more — while sharing the same BASIC language as **`basic`**.

**Graphics 1.0** (current): a complete AMOS/STOS-class 2-D feature set — bitmap primitives (`PSET`/`LINE`/`RECT`/`FILLRECT`/`CIRCLE`/`FILLCIRCLE`/`ELLIPSE`/`FILLELLIPSE`/`TRIANGLE`/`FILLTRIANGLE`/`POLYGON`/`FILLPOLYGON`/`FLOODFILL`/`DRAWTEXT`), PNG sprites with rotation and multi-instance stamping, time-based animation, an array-driven tilemap renderer, a 1bpp blitter with file I/O (`IMAGE LOAD`/`SAVE`/`GRAB`/`COPY`), named keyboard polling (`KEYDOWN`/`KEYUP`/`KEYPRESS`), and an atomic double-buffered `VSYNC` frame commit.

Build from source with **`make basic-gfx`** after Raylib is installed; releases ship **`basic-gfx`** next to **`basic`**.

On Windows use `basic-gfx.exe`. Paths to assets are **relative to the `.bas` file’s directory** (or absolute).

## Quick start

Run locally from the repo **`examples/`** folder (or release archive):

```bash
./basic-gfx examples/gfx_showcase.bas        # Graphics 1.0 tour
./basic-gfx examples/gfx_world_demo.bas      # tilemap + scrolling + WASD
./basic-gfx examples/gfx_stamp_demo.bas      # SPRITE STAMP particles
./basic-gfx examples/gfx_rotate_demo.bas     # rotated sprites
./basic-gfx examples/gfx_anim_demo.bas       # ANIMFRAME boing ball
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

## Per-cell colour with `PAPER`

- **`BACKGROUND n`** sets the **global** background register (0–15) — used when `CLS` clears or when a `PRINT` writes into a cell with no explicit paper.
- **`PAPER n`** stamps only the **per-cell** `bgcolor[]` byte on subsequent `PRINT` output, without touching the global register. Use it to draw a highlighted menu row, a status-bar stripe, or a coloured card border without repainting the rest of the screen.

```basic
BACKGROUND 6                           ' global blue
PAPER 0 : COLOR 1 : PRINT "WHITE ON BLACK"
PAPER 2 : COLOR 7 : PRINT "YELLOW ON RED"
```

Example: `examples/gfx_menu_demo.bas` (selection bar + rainbow title via per-fragment `PAPER`/`COLOR`).

## Keyboard & time

- **`INKEY$`** — Non-blocking; returns one character or `""`. Case may vary; use **`UCASE$(INKEY$())`** for comparisons. (On CBM/PETSCII targets in upper/graphics mode keys already arrive uppercase, and `UCASE$` is a no-op there — compare against uppercase literals directly.)
- **`INPUT`** — In gfx, reads from the **window** key queue (not the terminal).
- **`KEYDOWN(code)`** — 1 while the key is currently held, else 0. Use for **diagonal movement** — `A+D` or `A+W` fire independently, unlike `INKEY$` which only surfaces one key at a time.
- **`KEYUP(code)`** — Inverse of `KEYDOWN`. 1 when the key is *not* held.
- **`KEYPRESS(code)`** — Rising-edge latch: returns 1 exactly once per press, then 0 until the key is released and pressed again. Good for pause toggles / single-shot actions.
- **`PEEK(56320 + code)`** — Lower-level key-map poll (`GFX_KEY_BASE` = `0xDC00`). The `KEYDOWN`/`KEYUP`/`KEYPRESS` functions are equivalent to `PEEK(GFX_KEY_BASE + code)` plus the edge-latch tracking, and survive `#OPTION memory` base changes.
- **Key codes:** uppercase ASCII for letters/digits (e.g. `W` = 87, `A` = 65); special keys Space (32), Enter (13), Esc (27), Tab (9), Backspace (8), and C64 cursor codes Up (145), Down (17), Left (157), Right (29).
- **`TI`** — 60 Hz jiffy counter (wraps per README); **`TI$`** — time string `HHMMSS`.
- **`SLEEP n`** — Pause in **ticks** (60 ≈ 1 second).
- **`VSYNC`** — Frame commit + ~16 ms wait. Atomically flips the `TILEMAP DRAW` / `SPRITE STAMP` build buffer to the show buffer so the renderer never displays a half-populated scene, then yields one display frame. Use `VSYNC` at the end of a per-frame loop instead of `SLEEP 1` for flicker-free output.

## Screen modes — `SCREEN 0..4`

Five distinct render modes share the same primitive vocabulary (`PSET`, `LINE`, `RECT`, `FILLRECT`, `CIRCLE`, `DRAWTEXT`, `CLS`, …). The difference is **what each pixel can carry** and **how big the plane is**.

| Mode | Size | Pixel | Memory / plane | Pen control |
|------|------|-------|----------------|-------------|
| `SCREEN 0` | 40×25 cells | PETSCII screencode + fg/bg index | 1 KB chars + 1 KB colour | `COLOR n`, `PAPER n`, `BACKGROUND n` |
| `SCREEN 1` | 320×200 | 1bpp + per-pixel palette index | 8 KB bitmap + 64 KB colour | `COLOR n` (0..15) |
| `SCREEN 2` | 320×200 | 32-bit RGBA | 256 KB | `COLOR n`, `COLORRGB r,g,b[,a]`, `BACKGROUNDRGB` |
| `SCREEN 3` | 320×200 | 8-bit palette index | 64 KB (reuses S1 colour plane) | `COLOR 0..255` |
| `SCREEN 4` | 640×400 | 32-bit RGBA | 1 MB | `COLOR n`, `COLORRGB r,g,b[,a]`, `BACKGROUNDRGB` |

### `SCREEN n`

- **Purpose**: switch render mode. Lazy-allocates RGBA / hi-RGBA planes on first entry.
- **Parameters**: `n` — `0` text, `1` bitmap, `2` 320×200 RGBA, `3` 256-colour indexed, `4` 640×400 RGBA.
- **Returns**: nothing. Errors with mode list on out-of-range.
- **Example**:
  ```basic
  SCREEN 2
  BACKGROUNDRGB 20, 20, 40 : CLS
  COLORRGB 255, 200, 0 : FILLCIRCLE 160, 100, 40
  ```

### Multi-buffer `SCREEN BUFFER` / `DRAW` / `SHOW` / `SWAP` / `COPY` / `FREE`

Slot 0 is the live `bitmap[]`, slot 1 is the `DOUBLEBUFFER` back-buffer, slots 2..7 are user-allocated. Lets you pre-render expensive scenes once and flip between them at zero per-frame cost (AMOS-style).

- **`SCREEN BUFFER n`** — allocate slot `n` (2..7). Statement; errors if already used or alloc fails.
- **`SCREEN DRAW n`** — retarget all bitmap writes (`PSET`, `LINE`, `CLS`, `DRAWTEXT`, …) to slot `n` (0..7). Returns nothing.
- **`SCREEN SHOW n`** — move the renderer's display plane to slot `n` (0..7).
- **`SCREEN SWAP a, b`** — atomically set `draw=a`, `show=b`. Useful for ping-pong page-flipping.
- **`SCREEN COPY src, dst`** — blit one allocated plane into another (any-to-any).
- **`SCREEN FREE n`** — release slot `n` (2..7). Refused if `n` is the active draw or show slot — switch off first.

**Example** — pre-render scenes A and B, flip on key:

```basic
SCREEN 1
SCREEN BUFFER 2 : SCREEN DRAW 2 : CLS : FILLRECT 40,40 TO 280,160
SCREEN BUFFER 3 : SCREEN DRAW 3 : CLS : FILLCIRCLE 160,100,60
SCREEN DRAW 0 : SCREEN SHOW 2
DO
  IF KEYPRESS(ASC(" ")) THEN SCREEN SHOW 5 - SHOWING : SHOWING = 5 - SHOWING
  VSYNC
LOOP
```

Demo: `examples/gfx_screen_buffer_demo.bas`.

### `LOADSCREEN path$ [, x [, y]]`

- **Purpose**: load any common image format (PNG / BMP / JPG / TGA / GIF) into the **current** screen plane. Behaviour dispatches on `SCREEN` mode (cell-quantise → dither → RGBA copy → palette match).
- **Parameters**:
  - `path$` — image file. **Use a literal quoted string in the IDE** so the asset pre-load regex picks it up before run.
  - `x`, `y` — optional offset (cells in `SCREEN 0`, pixels otherwise). Clipped.
- **Returns**: nothing. Errors on missing / unreadable / wrong format.
- **Example**:
  ```basic
  SCREEN 4 : LOADSCREEN "panorama.png"
  ```

Demo: `examples/gfx_loadscreen_demo.bas` (0/1/2/3/4 keys cycle modes on the same PNG).

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
- **`POLYGON n, vx(), vy()`** / **`FILLPOLYGON n, vx(), vy()`** — N-sided polygon (up to 256 vertices). `POLYGON` closes with `n` `LINE` segments; `FILLPOLYGON` fan-triangulates from vertex 0 (correct for convex shapes).
- **`FLOODFILL x, y`** — paint-bucket seed fill of the connected off region starting at `(x, y)`.
- **`DRAWTEXT x, y, text$`** — Pixel-space text using the active 8×8 charset (OR blend, current pen). Unlike `PRINT` / `TEXTAT` this isn't tied to the 40×25 text grid, so HUDs can sit anywhere. Bytes of `text$` go through `petscii_to_screencode`.
- **`BITMAPCLEAR`** — Wipe the bitmap plane without touching text/colour RAM.
- **`DOUBLEBUFFER ON` / `DOUBLEBUFFER OFF`** — toggle bitmap-plane double-buffering. Default **OFF** (legacy draw-as-you-go). With **ON**, BASIC still writes to `bitmap[]` but the renderer displays `bitmap_show[]`, and `VSYNC` atomically commits `build → show`. Combined with the always-double-buffered sprite cell list, a full per-frame `CLS : RECT … : FILLCIRCLE … : DRAWTEXT … : SPRITE STAMP … : VSYNC` sequence never shows a half-drawn frame. Toggling on eagerly promotes the current bitmap into the show plane so the first frame isn't blank. Canonical loop:

```basic
DOUBLEBUFFER ON
DO
  CLS
  FILLCIRCLE BX, BY, BR
  DRAWTEXT 12, 182, "BOUNCES " + STR$(BOUNCES)
  VSYNC
LOOP
```

Example: `examples/gfx_doublebuffer_demo.bas` (SPACE toggles the mode in-flight).

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
| `IMAGE NEW slot, w, h` / `IMAGE FREE slot` / `IMAGE COPY …` / `IMAGE GRAB slot, sx, sy, sw, sh` / `IMAGE LOAD slot, "path"` / `IMAGE SAVE slot, "path.png\|.bmp"` | *(blitter + screenshot)* |

Pick whichever spelling reads cleaner in your program.

## Sprite stamping vs persistent draw

**`SPRITE DRAW`** tracks a single persistent position per slot — N calls with the same slot collapse to the last one. Use it for the player, a single enemy, a HUD panel, etc.

### `SPRITE STAMP slot, x, y [, frame [, z [, rot_deg]]]`

- **Purpose**: append one sprite cell to the per-frame draw list. Unlike `SPRITE DRAW` (one persistent pose per slot — N calls collapse to the last), `STAMP` lets N draws of the **same** slot render at distinct positions in one frame. Used for particles, bullets, enemy swarms, starfields, anything where you would previously have called `SPRITECOPY` into many slots.
- **Parameters**:
  - `slot` — sprite slot 0..63 (must be `LOADSPRITE`'d).
  - `x`, `y` — pixel position on the framebuffer (320×200 in `SCREEN 1` / `SCREEN 2` / `SCREEN 3`; 640×400 in `SCREEN 4`).
  - `frame` — optional 1-based tile index; `0` or omitted falls back to the slot's current `SPRITE FRAME`. Single-image slots ignore.
  - `z` — optional integer depth; higher = on top. Default 0.
  - `rot_deg` — optional rotation in degrees around the sprite centre. **Raylib backend only** — canvas/WASM accepts the arg but ignores it.
- **Returns**: nothing.

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

## Blitter surfaces (`IMAGE NEW` / `COPY` / `GRAB` / `SAVE`)

Off-screen bitmap surfaces for scroll / parallax / work-buffer / screenshot patterns from AMOS/STOS-style BASIC.

- **`IMAGE NEW slot, w, h`** — allocate an off-screen **1bpp** bitmap. `slot` is 1..31. Any dimensions; surface starts empty.
- **`IMAGE FREE slot`** — release it (frees both the 1bpp buffer and any RGBA buffer a grab left behind).
- **`IMAGE COPY src, sx, sy, sw, sh TO dst, dx, dy`** — rectangular 1bpp blit between any two slots. Slot `0` is the live visible bitmap (320×200), so visible↔offscreen copies work without conversion. Overlapping same-slot rects stage through a scratch row buffer.
- **`IMAGE LOAD slot, "path"`** — read PNG / BMP / JPG / TGA / GIF into the slot as a 1bpp mask (luminance-threshold at 128; alpha=0 → off).
- **`IMAGE GRAB slot, sx, sy, sw, sh`** — snapshot a region of the **currently-displayed framebuffer** into `slot` as **32-bit RGBA** — bitmap + text + sprites + tilemap cells all composited, full palette and alpha. On desktop `basic-gfx` the grab blocks the interpreter for up to one display frame (~16 ms) while the render thread reads back the composited target. On canvas WASM the frame is composited inline (no threading). If an RGBA hook isn't available on the current build, falls back to a 1bpp copy of the bitmap plane.
- **`IMAGE SAVE slot, "path"`** — extension-dispatched export:
  - **`.png`** — 32-bit RGBA PNG. If the slot was populated by `IMAGE GRAB`, alpha and the full composite are preserved. Slots still holding a 1bpp mask write on-pixel = opaque white, off-pixel = `rgba(0,0,0,0)` (transparent — good for reusing a drawn panel as a sprite). Slot 0 without a grab resolves on/off through the current `COLOR` / `BACKGROUND`.
  - **anything else** — 24-bit BMP (no alpha channel; RGBA grabs are premultiplied against black on write, 1bpp slots stay pen=white/off=black).
- **`FILEEXISTS(path$)`** — returns **1** if the path is openable for reading, **0** otherwise. Works against MEMFS in browser WASM and the host filesystem natively. Pairs with `IMAGE SAVE` so programs can verify the file landed before telling the user or triggering a `DOWNLOAD`.
- **`DOWNLOAD path$`** — browser WASM: reads the file from MEMFS, wraps it in a Blob with a guessed MIME type, and fires a synthetic `<a download>` click so the user gets a real file on disk. Native builds: no-op with a one-shot stderr hint. Kept as a separate statement (not folded into `IMAGE SAVE`) so per-frame recorders don't spam 300 download prompts.

**Smooth scroll recipe** (`examples/gfx_scroll_demo.bas`):

```basic
IMAGE NEW 1, 640, 200      : REM oversized world
REM … paint world into slot 1 …
REM each frame:
IMAGE COPY 1, XO, 0, 320, 200 TO 0, 0, 0
```

**Parallax** (`examples/gfx_parallax_demo.bas`): one surface per band, independent `XO` per band, one `IMAGE COPY` per band per frame.

**Screenshot / animation frames → ffmpeg**:

```basic
VSYNC                                  : REM let the scene composite
IMAGE GRAB 1, 0, 0, 320, 200
IMAGE SAVE 1, "shot.png"               : REM full colour + alpha
IF FILEEXISTS("shot.png") THEN
  DOWNLOAD "shot.png"                  : REM browser gets a real file
END IF
```

Per-frame recorder — writes `frame_00001.png`, `frame_00002.png`, …:

```basic
N = 0
DO
  : REM … render …
  VSYNC
  IMAGE GRAB 1, 0, 0, 320, 200
  N = N + 1
  IMAGE SAVE 1, "frame_" + RIGHT$("00000" + STR$(N), 5) + ".png"
LOOP UNTIL N >= 300                    : REM 5s at 60 fps
```

Encode with ffmpeg:

```bash
ffmpeg -framerate 60 -i frame_%05d.png -c:v libx264 -pix_fmt yuv420p out.mp4
```

Example: `examples/gfx_screenshot_demo.bas` (S takes a numbered screenshot; commented-out per-frame recorder block at the bottom).

## RGBA blitter — `IMAGE CREATE`, `IMAGE BLEND`, `IMAGE DRAW`

The 1bpp blitter family above (`IMAGE NEW` / `COPY` / `LOAD` / `SAVE` / `GRAB`) handles silhouettes and screenshots. The **RGBA** family is used in `SCREEN 2` / `SCREEN 4` when you want full-colour alpha-composited work — sprite sheets with antialiased edges, parallax bands with soft fades, pre-baked HUD strips wider than the framebuffer.

### `IMAGE CREATE slot, w, h`

- **Purpose**: allocate an off-screen **RGBA** surface. Companion to `IMAGE NEW` (1bpp) — must be RGBA before `IMAGE LOAD` of a PNG with alpha if you want `IMAGE BLEND` to honour transparency.
- **Parameters**:
  - `slot` — 1..31 (slot 0 is the live framebuffer).
  - `w`, `h` — pixel dimensions, both > 0. `IMAGE LOAD` later may resize the slot to match the loaded PNG.
- **Returns**: nothing. Errors on bad slot / size / out of memory.
- **Example**:
  ```basic
  IMAGE CREATE 1, 64, 64
  IMAGE LOAD   1, "chick.png"
  ```

### `IMAGE BLEND src, sx, sy, sw, sh TO dst, dx, dy`

- **Purpose**: alpha-composited rectangular blit between two RGBA slots (Porter-Duff "source over"). Semi-transparent source pixels smooth-blend against the destination.
- **Parameters**:
  - `src` — RGBA source slot (1..31).
  - `sx, sy, sw, sh` — rectangle inside `src`.
  - `dst` — RGBA destination. Use **0** to route to the live `SCREEN 2` / `SCREEN 4` framebuffer; use 1..31 for an off-screen RGBA slot.
  - `dx, dy` — top-left in `dst`.
- **Returns**: nothing. Errors if either slot isn't RGBA, or `dst = 0` outside RGBA modes.
- **Example**:
  ```basic
  SCREEN 2
  LOADSCREEN "sky.png"
  IMAGE CREATE 1, 32, 32 : IMAGE LOAD 1, "chick.png"
  DO
    LOADSCREEN "sky.png"                       : REM reset background each frame
    IMAGE BLEND 1, 0, 0, 32, 32 TO 0, X, Y
    X = X + 1 : IF X > 320 THEN X = -32
    VSYNC
  LOOP
  ```

Demo: `examples/gfx_blend_demo.bas`.

### `IMAGE DRAW slot`

- **Purpose**: retarget every RGBA primitive (`LINE`, `FILLRECT`, `CIRCLE`, `DRAWTEXT`, `PSET`, `POLYGON`, …) to an off-screen `IMAGE CREATE` surface instead of the live framebuffer. Mirror of `SCREEN DRAW n` but routed into the IMAGE pool, so the canvas size is **arbitrary** (not 320×200 / 640×400). Pre-bake wide scroller strips, world maps, HUD layers, sprite atlases, then blit back with `IMAGE BLEND`.
- **Parameters**: `slot` — `0` (restore live screen) or `1..31` (RGBA-allocated surface).
- **Returns**: nothing. Errors on non-RGBA mode, or unallocated / 1bpp slot.
- **Example**:
  ```basic
  SCREEN 2
  IMAGE CREATE 1, 1280, 200                    : REM 4-screen-wide strip
  IMAGE DRAW 1
    FOR I = 0 TO 1279 STEP 16 : LINE I,0 TO I,199 : NEXT I
    DRAWTEXT 0, 0, "WIDE WORLD"
  IMAGE DRAW 0                                 : REM back to live
  IMAGE BLEND 1, SCROLL_X, 0, 320, 200 TO 0, 0, 0
  ```

## HUD overlay plane — `OVERLAY`

The raylib renderer composites in this order: bitmap plane → cell list (`TILEMAP DRAW` + `SPRITE STAMP`) → **overlay** (when active). `OVERLAY ON` redirects every bitmap-plane primitive (`PSET`, `LINE`, `FILLRECT`, `RECT`, `DRAWTEXT`, `CLS`) into a separate RGBA buffer drawn above world tiles. Result: HUD text and dialog boxes always sit above sprites and tilemap, never get painted over.

> **Screen-mode requirement:** redirect is honoured **only in `SCREEN 2` / `SCREEN 4`** (RGBA modes). In `SCREEN 0` / `SCREEN 1` / `SCREEN 3` the text / 1bpp / indexed primitives keep writing to their own planes; `OVERLAY ON` is accepted and the buffer auto-allocates, but stays empty so nothing visible composites on top. Use `SCREEN 2` (or `SCREEN 4`) when you want OVERLAY-based HUD; otherwise paint the HUD directly to the active plane after world tiles in your render order.

- **`OVERLAY ON`** — start redirecting. Lazy-allocates the buffer on first `ON`.
- **`OVERLAY OFF`** — back to the main bitmap (default).
- **`OVERLAY CLS`** — clear overlay to fully transparent (alpha 0). Don't confuse with bare `CLS` — `OVERLAY CLS` only clears the overlay plane regardless of redirection state.
- **Returns**: nothing.

**Canonical loop:**

```basic
DO
  CLS                                           ' clear world bitmap
  TILEMAP DRAW 0, 0, 0, COLS, ROWS, MAP()
  SPRITE STAMP 1, PX, PY, 0, 50

  OVERLAY ON
    OVERLAY CLS                                 ' clear HUD plane
    COLORRGB 0, 0, 0, 200 : FILLRECT 0, 0 TO 319, 23
    COLORRGB 255, 240, 80, 255 : DRAWTEXT 4, 4, "LIFE 3"
  OVERLAY OFF

  VSYNC
LOOP
```

Canvas WASM (frozen) flattens the overlay onto the bitmap plane — works for static HUDs but won't sit above tiles. Native `basic-gfx` and `basic-wasm-raylib` do the proper compositing.

## HUD authoring — panel PNG + attribute icons

Practical guide to drawing a Zelda / SNES-style HUD strip on top of a tile world. Covers asset layout, alpha, NPOT warning, z-ordering, IDE preload caveats. Companion demo: [`examples/hud_demo.bas`](https://github.com/omiq/rgc-basic/blob/main/examples/hud_demo.bas) ([open in IDE](https://ide.retrogamecoders.com/?file=hud_demo.bas&platform=rgc-basic)).

### Sheet layout

**Panel** — single PNG, RGBA. Suggested 320×24 (full-width strip) or 64×56 (corner card). Match the framebuffer native size: `SCREEN 2` = **320×200**, `SCREEN 4` = **640×400**. Don't draw at output scale — draw at native, the renderer upscales.

**Icons** — pack as a **tile sheet**. 16×16 cells in a row, e.g. 64×16 PNG = 4 icons. Load with cell dims so `SPRITE STAMP frame` selects each one:

```basic
SPRITE LOAD 5, "hud_icons.png", 16, 16
SPRITE STAMP 5, X, Y, ICON_INDEX, 260       ' z=260 above HUD panel
```

### Power-of-two warning (NPOT)

Some browsers / GPUs warn `GL: NPOT textures extension not found, limited NPOT support (no-mipmaps, no-repeat)` when a texture is non-power-of-two. **Informational** — for HUD strips at native res with no scaling or repeating, NPOT works fine. Pad to power-of-two dims (16, 32, 64, 128, 256, 512) only when you need mipmaps or texture repeat.

### Alpha

PNG alpha is honoured by `SPRITE LOAD` automatically. For `IMAGE LOAD` you **must** call `IMAGE CREATE slot, w, h` first to allocate an RGBA slot — without that, the legacy 1bpp path takes the PNG and alpha is lost:

```basic
IMAGE CREATE 1, 320, 24                       ' RGBA slot
IMAGE LOAD 1, "hud_panel.png"                 ' alpha preserved
IMAGE BLEND 1, 0, 0, 320, 24 TO 0, 0, 0       ' Porter-Duff over the live framebuffer
```

### Translucent panel — pen alpha

For a quick semi-transparent strip without a PNG, set the pen alpha and `FILLRECT`:

```basic
COLORRGB 0, 0, 0, 180                         ' 70% opaque black
FILLRECT 0, 0 TO 319, 23
```

Drawn into the overlay (or RGBA plane) so the world below partially shows through. Works in `SCREEN 2` / `SCREEN 4` only — `COLORRGB` alpha is ignored in `SCREEN 1` / `SCREEN 3` (palette-only).

### Filtering — `ANTIALIAS`

Default OFF (nearest-neighbour). For pixel-art HUD = **leave OFF**. Turn `ANTIALIAS ON` only if you scale the framebuffer up beyond 1× and want smooth edges (rare in retro look — usually OFF is correct).

### Z order — what stacks where

| Layer | Suggested z | How drawn |
|-------|-------------|-----------|
| World tiles | 0 | `TILEMAP DRAW` |
| World sprites | 50–100 | `SPRITE STAMP` |
| Player | 200 | `SPRITE STAMP` |
| HUD panel PNG | 250 | `SPRITE STAMP`, **or** `IMAGE BLEND` into overlay |
| HUD icons | 260 | `SPRITE STAMP` (higher z than panel) |
| HUD text | overlay-only | `DRAWTEXT` inside `OVERLAY ON … OFF` |

If you use OVERLAY (`SCREEN 2` / `SCREEN 4` only — see [OVERLAY](#hud-overlay-plane-overlay)), draw the panel + icons inside the overlay block too: `IMAGE BLEND` for the panel, `SPRITE STAMP` for icons, `DRAWTEXT` for counters. Otherwise stamp them with high `z` above world.

### `DRAWTEXT` vs PNG icons

`DRAWTEXT` paints with the active 8×8 chargen — fine for `LIFE 3`, score numbers. For heart / mana / coin glyphs use a PNG icon sheet. Mix freely:

```basic
SPRITE STAMP 5, 4, 4, ICON_HEART, 260         ' icon at left
DRAWTEXT 22, 8, "x" + STR$(LIVES)             ' "x3" text
SPRITE STAMP 5, 60, 4, ICON_KEY, 260
DRAWTEXT 78, 8, STR$(KEYS)
```

### IDE asset preload — literal path requirement

The IDE asset preloader regex scans the `.bas` source for **literal quoted strings** in `LOAD` calls and stages those files into MEMFS before run. Variable forms break the scan:

- ✓ `IMAGE LOAD 1, "hud_panel.png"` — staged into MEMFS
- ✗ `F$ = "hud_panel.png" : IMAGE LOAD 1, F$` — preloader misses it, runtime FILEIO fails

Workaround pattern (used by `map_editor.bas`): keep an `ASSET_HINT$` array of literals at the top of the program just to bait the preloader:

```basic
DIM ASSET_HINT$(1)
ASSET_HINT$(0) = "hud_panel.png"
ASSET_HINT$(1) = "hud_icons.png"
```

Also covers JSON tilesets — every `tileset.src` referenced inside any preloaded `.json` must itself be in `ASSET_HINT$`, since the preloader doesn't recurse into JSON.

### Native build paths

Asset paths are **relative to the `.bas` file's directory**. `examples/rpg/rpg.bas` finds `examples/rpg/hud_panel.png` via `IMAGE LOAD 1, "hud_panel.png"`. No `./` prefix needed; absolute paths also work.

### Build + deploy reminder

After dropping new PNG into `~/github/rgc-basic/examples/rpg/`:
1. Commit + push canonical
2. `cd ~/github/8bitworkshop && ./scripts/sync-rgc-basic.sh`
3. Update `presets/rgc-basic/presets.json` if filename is brand-new (sync script warns)
4. Deploy 8bitworkshop

---

## Palette file I/O

### `PALETTELOAD path$`

- **Purpose**: read a plain-text `.pal` palette file into the live 256-entry palette. Tolerates JASC-PAL headers, `#` comments, blank lines. Entries beyond the file's count are untouched.
- **Parameters**: `path$` — source file. Format: 256 lines of `R G B [A]`, decimal 0..255 each.
- **Returns**: nothing. Errors on missing / unreadable file.
- **Example**:
  ```basic
  PALETTELOAD "sunset.pal"
  PALETTEROTATE 16, 255                         ' cycle 240 entries
  ```

### `PALETTESAVE path$`

- **Purpose**: write the live palette to a plain-text `.pal` file. Round-trips through `PALETTELOAD`.
- **Parameters**: `path$` — destination file.
- **Returns**: nothing.
- **Example**:
  ```basic
  PALETTESAVE "my-tuned.pal"
  IF FILEEXISTS("my-tuned.pal") THEN DOWNLOAD "my-tuned.pal"
  ```

## Mouse (`basic-gfx` and canvas WASM)

| Function / statement | Meaning |
|----------------------|---------|
| **`GETMOUSEX()` / `GETMOUSEY()`** | Pointer in **framebuffer pixels** (same space as `DRAWSPRITE`). |
| **`ISMOUSEBUTTONPRESSED(n)`** | Rising-edge: **1** the frame the button goes down, else **0**. |
| **`ISMOUSEBUTTONDOWN(n)`** | **1** while the button is held. |
| **`ISMOUSEBUTTONRELEASED(n)`** | Falling-edge: **1** the frame the button goes up. |
| **`ISMOUSEBUTTONUP(n)`** | **1** while the button is not held. |
| **`MOUSESET x, y`** | Move the system pointer to `(x, y)` in framebuffer pixels. On WASM the host may clamp the move to the canvas; `MOUSESET` latches the logical position for a few frames so `GETMOUSEX/Y` report the requested value. |
| **`SETMOUSECURSOR code`** | Raylib `MouseCursor` codes — `0` default, `2` I-beam, `4` crosshair, `5` pointing hand, etc. Canvas/WASM maps the code to CSS `cursor`. |
| **`HIDECURSOR` / `SHOWCURSOR`** | Toggle pointer visibility. |

Button codes: **0** left, **1** right, **2** middle (Raylib `MouseButton` order).

Example: `examples/gfx_mouse_demo.bas` (paint with LEFT, clear with RIGHT, hide/show with MIDDLE, `MOUSESET` warp on LEFT+RIGHT, cursor shape changes by vertical zone).

## Anti-aliasing / texture filter

- **`ANTIALIAS ON`** — Bilinear filter on scaled sprites and the upscaled framebuffer. Smooth; useful if you're deliberately upsampling pixel art.
- **`ANTIALIAS OFF`** — Nearest-neighbour (the default). Hard pixels; classic retro look.

The mode applies globally to subsequently-loaded sprites and the render target. Toggle any time; the render thread re-applies the filter on the next tick.

Example: `examples/gfx_antialias_demo.bas` (SPACE flips modes; a 4× scaled ship shows the difference).

## Periodic timers

Cooperative callbacks fired between statements. Up to **12** timers (ids **1–12**), minimum interval **16 ms**, re-entrancy is skipped (not queued).

| Statement | Meaning |
|-----------|---------|
| **`TIMER id, interval_ms, FuncName`** | Register (or replace) timer `id` to call zero-arg `FUNCTION FuncName` every `interval_ms` ms. |
| **`TIMER STOP id`** | Disable without removing — re-enable later with `TIMER ON`. |
| **`TIMER ON id`** | Re-enable a stopped timer. |
| **`TIMER CLEAR id`** | Remove entirely. |

Timers reset at the start of each run. Works in terminal, `basic-gfx`, and WASM. Examples: `examples/timer_demo.bas`, `examples/timer_clock.bas`.

```basic
FUNCTION Tick()
  T = T + 1
  LOCATE 0, 0 : PRINT "TICK "; T; "    "
END FUNCTION

TIMER 1, 100, Tick                     ' every 100 ms
DO
  IF KEYDOWN(KEY_ESC) THEN EXIT
  VSYNC
LOOP
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
| Screenshot / ffmpeg frames | `gfx_screenshot_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_screenshot_demo.bas&platform=rgc-basic) |
| Mouse | `gfx_mouse_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_mouse_demo.bas&platform=rgc-basic) |
| Anti-alias toggle | `gfx_antialias_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_antialias_demo.bas&platform=rgc-basic) |
| Menu / PAPER | `gfx_menu_demo.bas` | [IDE](https://ide.retrogamecoders.com/?file=gfx_menu_demo.bas&platform=rgc-basic) |
| Timers | `timer_demo.bas`, `timer_clock.bas` | [1](https://ide.retrogamecoders.com/?file=timer_demo.bas&platform=rgc-basic) · [2](https://ide.retrogamecoders.com/?file=timer_clock.bas&platform=rgc-basic) |

Index listing: `examples/tutorial_gfx_index.bas` — [Web IDE](https://ide.retrogamecoders.com/?file=tutorial_gfx_index.bas&platform=rgc-basic). Static HTML overview: **`web/tutorial-gfx-features.html`** when you serve **`web/`** over HTTP.

## See also

- [Getting started](getting-started.md) — first program, frame loop, sprites in 30 lines
- [Language reference](language.md) — full statement / function table including detailed references for `OVERLAY`, `IMAGE CREATE/BLEND/DRAW`, `LOADSCREEN`, `MAPSAVE`, `BUFFER*`
- [Network & buffers](network-and-buffers.md) — pulling assets in over HTTP, slot-based file fetches
- [Terminal & PETSCII](terminal-petscii.md) — plain `basic` without a window
- [Web IDE](web-ide.md) — browser integration
- [Install & platforms](install.md) — obtaining binaries
- [github.com/omiq/rgc-basic — README](https://github.com/omiq/rgc-basic/blob/main/README.md) — authoritative detail, CLI flags, and edge cases
- [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md) — per-release behaviour

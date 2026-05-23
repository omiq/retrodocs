# RGC BASIC — getting started

This page gets a brand-new user from "what is this" to a running `.bas` program with sprites, sound, and input. It assumes no prior BASIC experience but assumes you can edit files and run a command in a terminal (or click around a web page).

If you've used BASIC before — Commodore, QBasic, Atari, AMOS — RGC BASIC will feel familiar. Skip ahead to the [Language reference](language.md).

---

## 1. Pick a way to run it

You have three options. Use whichever is easiest:

| Option | Setup | Best for |
|--------|-------|----------|
| **Web IDE** | None — open the link | Trying it out, sharing programs |
| **`basic-gfx` (native)** | Download a release | Local development, fast iteration, gamepads |
| **`basic` (terminal)** | Download a release | Scripting, pipes, no graphics |

### Web IDE (zero install)

Open <https://ide.retrogamecoders.com/?platform=rgc-basic>. Type a program in the editor, hit Run. That's it.

To open a bundled example: `https://ide.retrogamecoders.com/?file=trek.bas&platform=rgc-basic`.

### Native binaries

1. Grab the latest archive from <https://github.com/omiq/rgc-basic/releases/>.
2. Extract. You get `basic`, `basic-gfx`, and an `examples/` folder.
3. From a terminal:

   ```bash
   ./basic-gfx examples/boing.bas
   ```

macOS may quarantine the binary on first run — see [Install](install.md#macos-gatekeeper-unsigned-binaries).

---

## 2. Hello, world

Put this in `hello.bas`:

```basic
PRINT "HELLO, WORLD"
```

Run it: `./basic hello.bas` (terminal) or `./basic-gfx hello.bas` (window).

That's an entire valid program. No line numbers needed.

### A program with a loop

```basic
FOR I = 1 TO 10
  PRINT "COUNT: "; I
NEXT I
```

### A program with input

```basic
INPUT "WHAT IS YOUR NAME"; N$
PRINT "HELLO, "; N$
```

`PRINT` and `INPUT` are the two basics. `;` after `PRINT` suppresses the newline; `,` advances to the next comma-zone.

---

## 3. Core language — the cheat sheet

Every command below uses the **Purpose / Parameters / Returns / Example** format. Skim, run the examples, come back when you forget syntax. Full reference: [language.md](language.md).

### `PRINT expr [; or , …]`

- **Purpose**: write to stdout (terminal) or the active screen plane (gfx).
- **Parameters**: any expression. `;` between values suppresses spacing/newline; `,` advances to the next comma-zone column.
- **Returns**: nothing.
- **Example**:
  ```basic
  PRINT "X = "; 42, "READY"
  ```

### `INPUT [prompt$;] var [, var …]`

- **Purpose**: read line from stdin (terminal) or window key queue (gfx).
- **Parameters**: optional prompt string (with trailing `;`), then one or more variables to fill.
- **Returns**: nothing — variables are assigned in place.
- **Example**:
  ```basic
  INPUT "AGE"; A
  INPUT "HEIGHT, WEIGHT"; H, W
  ```

### `LET var = expr` *(LET optional)*

- **Purpose**: assign a value to a variable.
- **Parameters**: target variable, expression.
- **Returns**: nothing.
- **Example**:
  ```basic
  X = 5
  N$ = "HELLO"
  ```

### `IF cond THEN … [ELSE …] [END IF]`

- **Purpose**: branch on a condition. Inline single-line form, or block form with `END IF`.
- **Parameters**: numeric condition (zero = false, non-zero = true).
- **Returns**: nothing.
- **Example**:
  ```basic
  IF X > 10 THEN PRINT "BIG"
  IF X > 10 THEN
    PRINT "BIG"
  ELSE
    PRINT "SMALL"
  END IF
  ```

### `FOR i = a TO b [STEP s]` … `NEXT i`

- **Purpose**: counted loop.
- **Parameters**: counter `i`, start `a`, end `b`, optional step `s` (default 1, can be negative).
- **Returns**: nothing.
- **Example**:
  ```basic
  FOR I = 10 TO 1 STEP -1 : PRINT I : NEXT I
  ```

### `WHILE cond` … `WEND`  /  `DO` … `LOOP UNTIL cond`

- **Purpose**: condition-driven loop. `WHILE/WEND` tests at top; `DO/LOOP UNTIL` tests at bottom; bare `DO/LOOP` runs forever until `EXIT`.
- **Returns**: nothing.
- **Example**:
  ```basic
  X = 0 : WHILE X < 5 : X = X + 1 : PRINT X : WEND
  DO : INPUT "Q TO QUIT"; A$ : LOOP UNTIL A$ = "Q"
  ```

### `GOTO line_or_label`  /  `GOSUB line_or_label` … `RETURN`

- **Purpose**: unconditional jump (`GOTO`) or call/return (`GOSUB`/`RETURN`).
- **Parameters**: a numeric line number or a label (`mylabel:` defined elsewhere).
- **Returns**: nothing.
- **Example**:
  ```basic
  GOSUB greet : END
  greet:
    PRINT "HI" : RETURN
  ```

### `FUNCTION Name(p1, p2)` … `RETURN expr` … `END FUNCTION`

- **Purpose**: user-defined procedure with parameters, locals, recursion. Call **with parentheses**.
- **Parameters**: name + parameter list.
- **Returns**: value via `RETURN expr`, or `0` / `""` if no return.
- **Example**:
  ```basic
  FUNCTION Add(A, B)
    RETURN A + B
  END FUNCTION
  PRINT Add(3, 5)
  ```

### `DIM var(n)`  /  `DIM var(rows, cols)`  /  `DIM s$(n)`

- **Purpose**: declare an array. Indices are **0-based** — `DIM A(10)` allows 0..10.
- **Parameters**: name + one or more dimension sizes.
- **Returns**: nothing.
- **Example**:
  ```basic
  DIM SCORE(9)        ' 10 elements: SCORE(0)..SCORE(9)
  DIM GRID(7, 7)      ' 8x8 board
  ```

---

## 4. Your first graphical program

Save as `circle.bas`, run with `./basic-gfx circle.bas`:

```basic
SCREEN 1                     ' 320x200 bitmap mode
BACKGROUND 6 : CLS           ' blue
COLOR 7                      ' yellow pen
FILLCIRCLE 160, 100, 50      ' centre, radius
SLEEP 180                    ' 3 seconds @ 60 ticks/sec
```

**What's happening:**
- `SCREEN 1` switches into 320×200 1bpp graphics.
- `BACKGROUND` sets the clear colour (palette index 0..15).
- `COLOR` sets the pen.
- `FILLCIRCLE` is a primitive — same family as `RECT`, `LINE`, `PSET`, `DRAWTEXT`.
- `SLEEP` waits in 60 Hz ticks (so 60 ≈ one second).

Full primitive list and screen modes: [Graphics — bitmap mode](graphics-raylib.md#bitmap-mode-screen-1).

---

## 5. The frame loop pattern

Every game / animation in RGC BASIC follows the same shape:

```basic
SCREEN 1
DOUBLEBUFFER ON
DO
  CLS                                ' clear last frame
  IF KEYDOWN(ASC("Q")) THEN EXIT     ' poll input
  X = X + 1                          ' update state
  FILLCIRCLE X, 100, 8               ' draw
  VSYNC                              ' commit + wait one frame
LOOP
```

Pieces explained:

### `DOUBLEBUFFER ON`

- **Purpose**: enable two-plane bitmap buffering. Renderer shows a committed back-buffer; you draw to the front. `VSYNC` flips them atomically. Without this you can see half-drawn frames.
- **Parameters**: `ON` to enable, `OFF` to disable. Default OFF (legacy draw-as-you-go).
- **Returns**: nothing.

### `KEYDOWN(code)` / `KEYUP(code)` / `KEYPRESS(code)`

- **Purpose**: poll the keyboard. `KEYDOWN` is true while held (use for movement). `KEYPRESS` is true exactly once per press (use for pause toggles, fire-once actions). `KEYUP` is the inverse of `KEYDOWN`.
- **Parameters**: `code` — uppercase ASCII for letters/digits (`ASC("W")`), or special-key constant (`13` Enter, `27` Esc, `32` Space, `145` Up, `17` Down, `157` Left, `29` Right).
- **Returns**: 1 or 0.
- **Example**:
  ```basic
  IF KEYDOWN(ASC("A")) THEN X = X - 1
  IF KEYPRESS(ASC(" ")) THEN PAUSED = NOT PAUSED
  ```

### `VSYNC`

- **Purpose**: commit current frame and wait ≈ one display frame (16 ms at 60 Hz). Atomically flips the cell list (`SPRITE STAMP` + `TILEMAP DRAW`) and the bitmap plane (when `DOUBLEBUFFER ON`).
- **Parameters**: none.
- **Returns**: nothing.

---

## 6. Sprites in 30 lines

Drop a PNG named `ship.png` in the same folder as your `.bas`. Then:

```basic
SCREEN 1
SPRITE LOAD 0, "ship.png"            ' load PNG into slot 0
X = 160 : Y = 100
DOUBLEBUFFER ON
DO
  IF KEYDOWN(ASC("Q")) THEN EXIT
  IF KEYDOWN(ASC("A")) THEN X = X - 2
  IF KEYDOWN(ASC("D")) THEN X = X + 2
  IF KEYDOWN(ASC("W")) THEN Y = Y - 2
  IF KEYDOWN(ASC("S")) THEN Y = Y + 2
  CLS
  SPRITE DRAW 0, X, Y                ' persistent draw at (X, Y)
  VSYNC
LOOP
```

### `SPRITE LOAD slot, "file.png" [, tw, th]`

- **Purpose**: load a PNG into a numbered slot (0..63). Optional `tw, th` mark the image as a tile sheet (cells of `tw × th`).
- **Parameters**: `slot`, `path$`, optional tile width / height.
- **Returns**: nothing. Errors on missing file / bad PNG.

### `SPRITE DRAW slot, x, y [, z [, sx, sy [, sw, sh]]]`

- **Purpose**: persistent sprite pose — drawn every frame at this position until another `SPRITE DRAW` for that slot overrides. Use for the player, enemy, HUD panel.
- **Parameters**: slot, pixel `x`/`y`, optional `z` depth (higher = on top), optional source crop rect.
- **Returns**: nothing.

For **multi-instance** drawing (particles, bullet swarms), use `SPRITE STAMP` instead. See [Graphics — PNG sprites](graphics-raylib.md#png-sprites-full-reference).

---

## 7. Sound

Drop a `.wav` next to your `.bas`. Single-shot sample:

```basic
LOADSOUND 0, "boom.wav"
DO
  IF KEYPRESS(ASC(" ")) THEN PLAYSOUND 0
  IF KEYDOWN(ASC("Q")) THEN EXIT
  VSYNC
LOOP
```

### `LOADSOUND slot, "file.wav"`

- **Purpose**: load a WAV into a numbered slot (0..31).
- **Parameters**: slot, path. Path relative to the `.bas` directory or absolute.
- **Returns**: nothing.

### `PLAYSOUND slot`

- **Purpose**: play the loaded sample, non-blocking. Stops whatever was playing in the same voice.
- **Parameters**: slot.
- **Returns**: nothing.

### `SOUNDPLAYING()`

- **Purpose**: check if the current sample is still audible.
- **Parameters**: none.
- **Returns**: 1 while playing, 0 when idle.
- **Example**: `IF NOT SOUNDPLAYING() THEN PLAYSOUND 1`

For background music (MOD / XM / S3M / IT / OGG / MP3), use `LOADMUSIC` / `PLAYMUSIC`. See [language.md — sound](language.md#screen-timing-terminal-styling).

> **Browser autoplay rule:** the first call to `LOADSOUND` / `LOADMUSIC` must follow a user gesture (key press / mouse click). Gate it on `KEYPRESS(...)` or `ISMOUSEBUTTONPRESSED(0)`.

---

## 8. Pulling things in from the network

`HTTP$` fetches a string (small responses):

```basic
R$ = HTTP$("https://api.example.com/v1/ping")
PRINT "STATUS "; HTTPSTATUS(); ": "; R$
```

For larger responses or binaries (PNG / WAV / JSON > 4 KB), use `BUFFER*` or `HTTPFETCH`. See [Network & buffers](network-and-buffers.md).

---

## 9. Where to next

- **[Language reference](language.md)** — every statement, function, directive.
- **[Graphics (Raylib)](graphics-raylib.md)** — sprites, bitmap, screen modes, sound, input, mouse, gamepad.
- **[Web IDE](web-ide.md)** — running in the browser, `HTTP$`, focus model.
- **[Terminal & PETSCII](terminal-petscii.md)** — CLI flags, brace tokens, PETSCII colour codes.
- **[Network & buffers](network-and-buffers.md)** — HTTP, file-backed slots, binary I/O.
- **[Level authoring](level-authoring.md)** — `MAPLOAD` / `MAPSAVE` JSON tilemaps.

Read the bundled `examples/` folder. Every feature has at least one demo. Open them in the IDE: `https://ide.retrogamecoders.com/?file=NAME.bas&platform=rgc-basic`.

---

## 10. Common gotchas

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `INKEY$` always returns `""` in terminal | Plain `basic` has no key queue | Use `basic-gfx` or `KEYDOWN` in gfx |
| Browser audio silent | Autoplay policy | Trigger first `PLAYSOUND` from a `KEYPRESS` / mouse click |
| Sprite renders as black box | Loaded with `LOAD` instead of `SPRITE LOAD` | `SPRITE LOAD` for PNGs; `LOAD` is for raw bytes into virtual memory |
| Tight `DO/LOOP` makes browser tab unresponsive | No `SLEEP` / `VSYNC` to yield | Add `VSYNC` in the loop body |
| `RND(0)` returns the same number each run | Generator not seeded | Call `RND(-TI)` once at startup |
| Variable named `LINE` rejected | `LINE` is a reserved word | Pick a different name (e.g. `LN`) |
| File save in browser produced no file | Browser persists to MEMFS, not disk | After `IMAGE SAVE` / `MAPSAVE` etc., call `DOWNLOAD path$` to deliver as a real file |

If something else surprises you, check the [CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md) for recent semantic changes.

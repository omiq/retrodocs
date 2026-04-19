# RGC BASIC — language reference

This page documents **statements, functions, directives, and system variables** as implemented in the current interpreter. Behaviour can change between releases — confirm edge cases in the **[CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md)** and **[README](https://github.com/omiq/rgc-basic/blob/main/README.md)** on GitHub.

**Related:** [Terminal & PETSCII](terminal-petscii.md) (CLI, `CHR$`, colours) · [Graphics (`basic-gfx`)](graphics-raylib.md) (sprites, bitmap, `PEEK`, gamepad) · [Web IDE (WASM)](web-ide.md) (`HTTP$`, browser host)

---

## Program shape

| Topic | Behaviour |
|--------|-----------|
| **Line numbers** | Classic `10 PRINT …` / `20 …` programs. |
| **Numberless** | If the **first non-blank line** has no leading digits, the loader assigns internal line numbers; **labels** and structured blocks still work. |
| **Shebang** | `#!/usr/bin/env basic` on line 1 is ignored. |
| **Compact CBM syntax** | At load time, forms like `IFX<0THEN`, `FORI=1TO9`, `GOTO410` are normalized with spaces so the parser accepts them. |
| **Statement separator** | **`:`** runs multiple statements on one line: `A=1 : B=2 : PRINT A+B`. |

---

## Operators and expressions

| Kind | Operators |
|------|-----------|
| **Relational** | `<`, `>`, `=`, `<=`, `>=`, `<>` |
| **Arithmetic** | `+`, `-`, `*`, `/`, `^` (power), `MOD` (floored modulo) |
| **Bitwise** | `<<`, `>>`, `AND`, `OR`, `XOR` (integer parts of operands) |
| **Strings** | Concatenation with `+`; string/numeric comparisons where applicable |

**`RND(x)`** — Returns a value in **0..1** (uniform via `rand()`). If **`x < 0`**, the generator is **reseeded** (C64-style negative seed); the implementation uses `time` so runs differ, similar in spirit to **`RND(-TI)`** on a C64.

---

## Variables

| Kind | Rules |
|------|--------|
| **Numeric** | Names up to **31** significant characters; **`_`** allowed. |
| **String** | Name ends with **`$`**. |
| **Arrays** | **`DIM A(10)`**, **`DIM B(2,3)`** — indices are **0-based**: `DIM A(10)` allows **`0..10`**; `DIM C(2,3)` is a **3×4** matrix. |
| **Reserved words** | Identifiers that match keywords (**`IF`**, **`FOR`**, **`PRINT`**, …) **cannot** be variable names. **Labels** may still use names that look like keywords in some cases (e.g. **`CLR:`**). |

---

## Meta directives (`#` prefix)

Processed at **load time**. **`#OPTION`** values in the file **override** the same CLI flag.

| Directive | Purpose |
|-------------|---------|
| `#INCLUDE "path"` | Splice another file at this line. Avoid **duplicate line numbers** across includes; mixed numbered/numberless rules apply — errors are load-time. |
| `#OPTION petscii` | Same as **`-petscii`**. |
| `#OPTION petscii-plain` | Same as **`-petscii-plain`**. |
| `#OPTION charset upper` / `#OPTION charset lower` | PETSCII letter set. |
| `#OPTION palette ansi` / `#OPTION palette c64` | PETSCII colour mapping. |
| `#OPTION maxstr N` | String length limit (**1–4096**; default large). |
| `#OPTION columns N` | Print width (**1–255**; default **40**). |
| `#OPTION nowrap` | Do not wrap at column width. |
| `#OPTION memory c64` / `pet` / `default` | **basic-gfx / canvas WASM only** — virtual memory layout for **`POKE`/`PEEK`**. |
| `#OPTION screen $addr`, `#OPTION colorram …`, `#OPTION charmem …`, `#OPTION keymatrix …`, `#OPTION bitmap …` | Override individual regions (decimal or hex). |
| `#OPTION gfx_title "text"` | **basic-gfx** — window title (see also **`-gfx-title`**). |
| `#OPTION border N` or `#OPTION border N colour` | **basic-gfx** — padding around the drawable area (see [Graphics](graphics-raylib.md)). |

Design notes and history: **[meta-directives-plan.md](https://github.com/omiq/rgc-basic/blob/main/docs/meta-directives-plan.md)** in the repo.

---

## Statements (by category)

### Output and input

| Statement | Summary |
|-----------|---------|
| **`PRINT` / `?`** | Expressions; **`;`** suppresses newline; **`,`** advances to **comma zones** (width scales with **`-columns`**). |
| **`INPUT`** | Read into variables; optional **`"prompt";`** form. In **basic-gfx**, reads from the **window** queue. With stdin (terminal), supports **pipes**. |
| **`GET`** | **Non-blocking** single-character read into a string variable. If nothing waiting, result is **`""`**. Enter is **`CHR$(13)`** so **`ASC(K$)=13`** works. |

### Assignment and control

| Statement | Summary |
|-----------|---------|
| **`LET`** | Optional; **`A=1`** is fine without **`LET`**. |
| **Compound assign** | **`A++`** / **`A--`** increment / decrement by 1. **`A += expr`** / **`-=`** / **`*=`** / **`/=`** = `A = A op expr`. **`S$ += "x"`** concatenates; **`-= *= /=`** raise on strings. Statement-only (not expression). |
| **`IF … THEN`** | Inline (`IF X THEN 100`, `IF X THEN PRINT "Y"`) or block: **`IF` … `[ELSE]` … `END IF`**. Nested blocks supported. |
| **`WHILE` … `WEND`** | Pre-test loop. |
| **`DO` … `LOOP`** | Infinite until **`EXIT`**; or **`LOOP UNTIL expr`**. **`EXIT`** exits the **innermost** **`DO`**. |
| **`FOR` … `NEXT`** | Numeric **`FOR`** with optional **`STEP`** (positive or negative). |
| **`FOREACH var IN arr[()]` … `NEXT var`** | Iterate each element of a 1-D array (numeric or string). `NEXT var` advances; `EXIT` pops the innermost FOR/FOREACH. Empty arrays run zero iterations. |
| **`GOTO`** | Target is a line number or **label**. |
| **`GOSUB` / `RETURN`** | Subroutine stack; target line or label. |
| **`ON expr GOTO` / `ON expr GOSUB`** | Multi-way branch (e.g. **`ON N GOTO 100,200,300`**). |

### Data and comments

| Statement | Summary |
|-----------|---------|
| **`READ` / `DATA`** | Read literals into variables. |
| **`RESTORE`** | Reset **`DATA`** pointer; **`RESTORE line`** positions to first **`DATA`** at or after **`line`**. |
| **`REM`** / **`'`** | Comment to end of line. |
| **`END` / `STOP`** | Stop execution. |

### Arrays and structured data

| Statement | Summary |
|-----------|---------|
| **`DIM`** | Declare numeric or string arrays (**1-D or multi-D**). |
| **`SORT arr [, mode]`** | In-place **1-D** sort. **`mode`**: **`1`** or **`"asc"`** (default) ascending; **`-1`** or **`"desc"`** descending; numeric or string arrays. |
| **`SPLIT str$, delim$ INTO arr$`** | Split into a **pre-`DIM`med** 1-D string array. |
| **`JOIN arr$, delim$ INTO result$ [, count]`** | Join; if **`count`** omitted, uses count from last **`SPLIT`**. |

### Simple functions (`DEF FN`)

| Form | Example |
|------|---------|
| **`DEF FNname(params) = expr`** | One-line numeric function, e.g. **`DEF FNY(X)=SIN(X)`**. |

### User-defined procedures (`FUNCTION`)

| Form | Rules |
|------|--------|
| **`FUNCTION name [(p1, p2, …)]`** … **`RETURN [expr]`** … **`END FUNCTION`** | Call **with parentheses**: **`n = add(3,5)`**, **`sayhi()`**. Parameters are local; **recursion** supported. **`RETURN expr`** returns a value; bare **`RETURN`** / **`END FUNCTION`** without a prior return yields **0** / **`""`** in expression context. |

### File I/O (CBM-style)

| Statement / var | Summary |
|-----------------|--------|
| **`OPEN lfn, device, sec, "filename"`** | **Device 1** = host files; **secondary** **0** read, **1** write, **2** append. |
| **`PRINT# lfn, …`** | Write like **`PRINT`**, to file. |
| **`INPUT# lfn, var [, …]`** | Read tokens into variables. |
| **`GET# lfn, str$`** | One character into string variable. |
| **`CLOSE [lfn [, …]]`** | Close listed channels or **all** if omitted. |
| **`ST`** | After **`INPUT#`** / **`GET#`**: **0** = success, **64** = end of file, **1** = error / not open. |

### Memory and loading (**basic-gfx** / canvas)

| Statement | Summary |
|-----------|---------|
| **`POKE addr, byte`** | **Terminal:** no-op (compatibility). **Gfx:** writes **virtual** memory. |
| **`PEEK(addr)`** | **Terminal:** returns **0**. **Gfx:** reads virtual memory (**16-bit address**). |
| **`LOAD "path" INTO addr [, length]`** | Load **raw bytes** from file; optional max length. |
| **`LOAD @label INTO addr [, length]`** | Load from **`DATA`** bytes at **`label`**. |
| **`MEMSET addr, len, val`** | Fill virtual memory. |
| **`MEMCPY dest, src, len`** | Copy virtual memory. |

### Screen, timing, terminal styling

| Statement | Summary |
|-----------|---------|
| **`SLEEP n`** | Pause **`n`** ticks at **60 Hz** (≈ **`SLEEP 60`** ≈ one second in gfx; same tick unit used broadly). |
| **`LOCATE col, row`** | **0-based** cursor move (ANSI in terminal; gfx text cursor). |
| **`TEXTAT col, row, expr$`** | Move and print string at absolute position. |
| **`CURSOR ON` / `CURSOR OFF`** | Terminal: ANSI show/hide cursor. |
| **`DOWNLOAD path$`** | **Browser WASM:** reads the file from MEMFS, wraps it in a Blob with a guessed MIME type, triggers a real browser download. **Native:** no-op (file is already on disk); prints a one-shot hint on stderr. |
| **`COLOR n` / `COLOUR n`**, **`BACKGROUND n`**, **`PAPER n`** | C64-style indices **0–15** (foreground / background / per-cell paper). Named constants resolve everywhere a numeric colour is expected: **`BLACK WHITE RED CYAN PURPLE GREEN BLUE YELLOW ORANGE BROWN PINK DARKGRAY MEDGRAY LIGHTGREEN LIGHTBLUE LIGHTGRAY`** (plus `DARKGREY`/`MEDGREY`/`LIGHTGREY` spellings). |
| **`DOUBLEBUFFER ON` / `DOUBLEBUFFER OFF`** | **Gfx:** toggle bitmap-plane double-buffering (default OFF). With **ON**, renderer displays a committed back-buffer and only updates on `VSYNC` — matches the cell list so whole frames commit atomically. Shorthand for `SCREEN DRAW 0 : SCREEN SHOW 1` + auto-flip on `VSYNC`. |
| **`SCREEN BUFFER n`**, **`SCREEN DRAW n`**, **`SCREEN SHOW n`**, **`SCREEN FREE n`**, **`SCREEN SWAP a, b`**, **`SCREEN COPY src, dst`** | **Gfx:** multi-plane bitmap buffers (8 slots). Slot 0 = live `bitmap[]`, slot 1 = `DOUBLEBUFFER` back-buffer, slots 2..7 = user-allocated via `SCREEN BUFFER n`. `SCREEN DRAW n` retargets all bitmap writes (`PSET`, `LINE`, `CLS`, `DRAWTEXT`, ...); `SCREEN SHOW n` moves the renderer. `FREE` is refused if the slot is the active draw or show. `SWAP` sets draw=a, show=b atomically; `COPY` blits one plane into another. |
| **`CLS`**, **`CLS x, y TO x2, y2`** | Full-screen clear (terminal + gfx) or, in basic-gfx bitmap mode, clear only the given pixel rectangle on the current draw plane (same shape as `FILLRECT` with `COLOR 0`). Handy for redrawing only a HUD strip inside `DOUBLEBUFFER` / `SCREEN BUFFER` loops. |
| **`DRAWTEXT x, y, text$ [, scale]`** | **Gfx:** stamp string onto the bitmap at pixel `(x, y)` via active chargen, transparent OR blend, current pen. Optional integer `scale` (1..8, clamped) pixel-doubles each source pixel into a `scale × scale` block — 16×16 / 24×24 / ... text against the 8×8 chargen with no Font system. Per-call fg/bg and Font-slot arguments still wait on the Font work. |
| **`PAPER n`** | Per-cell background index (**0–15**); only subsequent `PRINT` output stamps `bgcolor[]`. Leaves the global `BACKGROUND` register untouched. |
| **`ANTIALIAS ON` / `ANTIALIAS OFF`** | **Gfx:** bilinear vs nearest-neighbour filter for sprites and the upscaled framebuffer (default **OFF**). |
| **`TIMER id, interval_ms, FuncName`** / **`TIMER STOP id`** / **`TIMER ON id`** / **`TIMER CLEAR id`** | Register, disable, re-enable, or remove a periodic timer. **12** timers max (ids **1–12**); minimum interval **16 ms**; `FuncName` is a zero-arg `FUNCTION`/`END FUNCTION` block. Re-entry is skipped, not queued. |
| **`SCREEN 0` / `SCREEN 1`**, **`PSET`**, **`PRESET`**, **`LINE`**, **`SCREENCODES`**, **`SCROLL`**, sprite statements | **Gfx / canvas** — see [Graphics](graphics-raylib.md). |
| **`LOADSOUND slot, "file.wav"`**, **`PLAYSOUND slot`**, **`STOPSOUND`**, **`UNLOADSOUND slot`**, **`SOUNDPLAYING()`** | **basic-gfx + basic-wasm-raylib (canvas WASM stays frozen):** single-voice WAV playback, 32 slots. `PLAYSOUND` is non-blocking and stops whatever was already playing. `SOUNDPLAYING()` returns **1** while audible, **0** when idle — self-clears at natural end-of-sample. Browsers require a user gesture (key / click) before `AudioContext` resumes, so gate the first cue on `KEYPRESS` or `ISMOUSEBUTTONPRESSED`. |

### Sprites and gamepad (gfx / canvas)

| Statements / functions | See |
|------------------------|-----|
| **`LOADSPRITE`** / **`SPRITE LOAD`**, **`DRAWSPRITE`** / **`SPRITE DRAW`**, **`DRAWSPRITETILE`** / **`TILE DRAW`**, **`UNLOADSPRITE`** / **`SPRITE FREE`**, **`SPRITEVISIBLE`**, **`SPRITEMODULATE`**, **`SPRITEFRAME`** / **`SPRITE FRAME`**, **`SPRITECOPY`**, **`SPRITE STAMP`** (multi-instance) | [Graphics — PNG sprites](graphics-raylib.md#png-sprites--full-reference) |
| **`TILEMAP DRAW`** (batched array → tile grid), **`DRAWTILEMAP`** (alias) | [Graphics — tilemaps](graphics-raylib.md#tilemaps-tilemap-draw) |
| **`IMAGE NEW`**, **`IMAGE FREE`**, **`IMAGE COPY … TO …`**, **`IMAGE LOAD`**, **`IMAGE GRAB`**, **`IMAGE SAVE`** | [Graphics — blitter surfaces](graphics-raylib.md#blitter-surfaces-image-new--copy--save) |
| **`RECT`** / **`FILLRECT`**, **`CIRCLE`** / **`FILLCIRCLE`**, **`ELLIPSE`** / **`FILLELLIPSE`**, **`TRIANGLE`** / **`FILLTRIANGLE`**, **`POLYGON`** / **`FILLPOLYGON`**, **`FLOODFILL`**, **`DRAWTEXT`** | [Graphics — bitmap mode](graphics-raylib.md#bitmap-mode-screen-1) |
| **`VSYNC`** (frame commit + wait one display frame) | [Graphics — keyboard & time](graphics-raylib.md#keyboard--time) |
| **`SPRITEW`**, **`SPRITEH`**, **`SPRITETILES`** / **`TILE COUNT`** / **`SPRITE FRAMES`**, **`SHEET COLS/ROWS/WIDTH/HEIGHT`**, **`SPRITEFRAME()`**, **`SPRITECOLLIDE`**, **`ISMOUSEOVERSPRITE(slot [, alpha_cutoff])`**, **`SPRITEAT(x, y)`**, **`SCROLLX`/`SCROLLY`**, **`JOY`**, **`JOYAXIS`**, **`KEYDOWN`/`KEYUP`/`KEYPRESS`**, **`ANIMFRAME`** | Same page |

### Other

| Statement | Summary |
|-----------|---------|
| **`CLR`** | Clear variables, **GOSUB**/**FOR** stacks, **`DATA`** pointer; **`DEF FN`** kept. |

---

## Intrinsic functions

Parentheses are required where shown. String functions use a trailing **`$`** in the usual BASIC style.

### Math

| Function | Notes |
|----------|--------|
| **`SIN`**, **`COS`**, **`TAN`** | Radians. |
| **`ABS`**, **`INT`**, **`SQR`**, **`SGN`**, **`EXP`**, **`LOG`** | Standard meanings. |
| **`RND(x)`** | See [Operators](#operators-and-expressions). |

### Strings

| Function | Signature / notes |
|----------|---------------------|
| **`LEN(s$)`** | Length. |
| **`STR$(n)`** | Number → string ( **`%g`** style). |
| **`VAL(s$)`** | Parse leading numeric. |
| **`CHR$(n)`** | Byte **`n & 0xFF`**; in **`-petscii`** terminal mode, maps control/colour to ANSI; in **gfx**, raw byte for screen semantics. |
| **`ASC(s$)`** | First character code, or **0** if empty. |
| **`INSTR(s$, find$ [, start])`** | **1-based** index, or **0**; optional **1-based** **`start`**. |
| **`REPLACE(s$, find$, repl$)`** | Replace all occurrences. |
| **`TRIM$(s$)`**, **`LTRIM$(s$)`**, **`RTRIM$(s$)`** | Whitespace trim. |
| **`FIELD$(s$, delim$, n)`** | **n**th field (**1-based**), awk-like. |
| **`UCASE$(s$)`**, **`LCASE$(s$)`** | ASCII case. |
| **`MID$(s$, start [, len])`** | **1-based** **`start`**. |
| **`LEFT$(s$, n)`**, **`RIGHT$(s$, n)`** | Substrings. |
| **`STRING$(n, c$)`** or **`STRING$(n, code)`** | Repeat character: count **`n`** and one-char string or numeric code. |

### Arrays

| Function | Notes |
|----------|--------|
| **`INDEXOF(arr, value)`**, **`LASTINDEXOF(arr, value)`** | **1-based** index in **1-D** array, or **0**; works for numeric or string arrays. |

### JSON

| Function | Notes |
|----------|--------|
| **`JSON$(json$, path$)`** | Extract by path (`"key"`, `"key[0]"`, `"a.b"`, …); returns string. Use **`VAL(JSON$(…))`** for numbers. |
| **`JSONLEN(json$, path$)`** | Count of entries at path (array / object), **0** for scalars or missing paths. Pairs with `FOR I = 0 TO JSONLEN(j$, "items") - 1`. |
| **`JSONKEY$(json$, path$, n)`** | 0-based Nth key when path resolves to an object; **`""`** for arrays or scalars. Enumerate fields without hard-coding names. |

### Environment and host

| Function | Notes |
|----------|--------|
| **`ENV$(name$)`** | Environment variable, or **`""`**. |
| **`FILEEXISTS(path$)`** | **1** if the path is openable for reading, **0** otherwise. Works against **MEMFS** in browser WASM and the host filesystem natively. Idiomatic post-save check: `IF FILEEXISTS(P$) THEN DOWNLOAD P$`. |
| **`CWD$()`**, **`CHDIR path$`** | Current working directory + change. Native `getcwd`/`chdir`; MEMFS on browser WASM via the same POSIX layer. `CHDIR` raises a runtime error on missing paths. |
| **`DIR$(path$ [, delim$])`** | Delimiter-joined (default newline) list of non-hidden names in `path$`. Returns **`""`** on failure. Capped by `#OPTION maxstr`. |
| **`DIR path$ INTO arr$ [, count]`** | Statement form: populate a 1-D string array (must be DIMmed) with filenames and optionally assign the count. Mirrors `SPLIT … INTO arr$ [, count]`. |
| **`TICKUS()`**, **`TICKMS()`** | Monotonic microsecond / millisecond counters. Origin is implementation-defined — differences are meaningful. Native: `clock_gettime(CLOCK_MONOTONIC)`. Browser WASM: `emscripten_get_now()`. |
| **`PLATFORM$()`** | Host string — see [Web IDE](web-ide.md#platform-and-capabilities) for **browser** vs native. |

### Evaluation and conversion

| Function | Notes |
|----------|--------|
| **`EVAL(expr$)`** | Evaluate **`expr$`** as a BASIC expression (numeric or string). Use **`CHR$(34)`** for embedded quotes. |
| **`DEC(s$)`** | Hex string → number; invalid → **0**. |
| **`HEX$(n)`** | Integer part → uppercase hex **without** **`$`**. |

### `PRINT` helpers

| Function | Notes |
|----------|--------|
| **`TAB(n)`**, **`SPC(n)`** | Column advance / spaces ( **`TAB`** wraps within **print width**). |

### Scripting and shell (native OS)

| Function | Notes |
|----------|--------|
| **`ARGC()`** | Count of arguments **after** the script path. |
| **`ARG$(n)`** | **`ARG$(0)`** = script path; **`ARG$(1)`**… = args. Out of range → **`""`**. |
| **`SYSTEM(cmd$)`** | Run shell command; returns **exit status**. **Browser WASM:** not available — returns **-1**. |
| **`EXEC$(cmd$)`** | **`stdout`** as string (up to interpreter max string size; trailing newline trimmed). **Browser WASM:** returns **`""`**. |

### HTTP (browser WASM only)

| Function | Notes |
|----------|--------|
| **`HTTP$(url$ [, method$ [, body$]])`** | **`fetch`**; response body as string. Alias: **`HTTP(url)`** without **`$`** calls the same intrinsic. |
| **`HTTPSTATUS()`** | Status from last **`HTTP$`**; **0** if failed / not WASM. |

Details: [Web IDE — `HTTP$`](web-ide.md#http-and-httpstatus).

### Graphics-only (see [Graphics](graphics-raylib.md))

**`INKEY$()`**, **`PEEK`**, **`KEYDOWN(code)`**, **`KEYUP(code)`**, **`KEYPRESS(code)`** (rising-edge latch), **`ANIMFRAME(first, last, jiffies)`** (time-cycled frame index), **`SPRITEW`**, **`SPRITEH`**, **`SPRITETILES`** / **`TILE COUNT`** / **`SPRITE FRAMES`**, **`SHEET COLS/ROWS/WIDTH/HEIGHT`**, **`SPRITEFRAME()`**, **`SPRITECOLLIDE`**, **`ISMOUSEOVERSPRITE(slot [, alpha_cutoff])`** (SCROLL-aware; one arg = bbox, two args = pixel-perfect alpha sampling), **`SPRITEAT(x, y)`** (topmost visible slot at point, Z tie-break; −1 if none), **`SCROLLX()`**, **`SCROLLY()`**, **`JOY`**, **`JOYSTICK`**, **`JOYAXIS`**.

---

## System variables

| Name | Behaviour |
|------|-----------|
| **`ST`** | Set by **`INPUT#`** / **`GET#`** (see [File I/O](#file-io-cbm-style)). |
| **`TI`** | **basic-gfx / canvas:** **60 Hz** jiffy counter (wraps per README). **Native terminal:** **not** jiffies — implementation uses **Unix time** (seconds) as a fallback so **`RND(-TI)`** still reseeds. **Canvas WASM (gfx):** derived from monotonic clock when per-frame ticks are not used. |
| **`TI$`** | **Gfx:** string **`HHMMSS`** from jiffy clock. **Terminal:** **wall-clock** **`HHMMSS`** from local time. |

Identifiers starting with **`TI`** are resolved with CBM-style rules ( **`TI`** vs **`TI$`** ).

---

## Where features work

| Feature | `basic` (terminal) | `basic-gfx` | Browser WASM |
|---------|---------------------|-------------|----------------|
| File I/O, **`ARG$`**, **`SYSTEM`**, **`EXEC$`** | Yes | Yes | **`SYSTEM`**/**`EXEC$`** stubbed; **`HTTP$`** for network |
| **`HTTP$` / `HTTPSTATUS`** | Returns **`""`** / **0** | Same | Yes (CORS) |
| **`POKE` / `PEEK`** | No-op / **0** | Virtual memory | Canvas host |
| Sprites, bitmap, **`SCROLL`**, gamepad | Error / stub | Yes | Canvas parity (see upstream) |
| **`INKEY$()`** | **`""`** (no key queue) | Yes | Yes (hosted input) |

---

## Reserved words (identifiers)

The interpreter keeps a fixed **`reserved_words[]`** table in **`basic.c`**: every keyword for statements and intrinsics (**`PRINT`**, **`FUNCTION`**, **`SPRITECOLLIDE`**, **`HTTPSTATUS`**, **`LOOP`**, **`EXIT`**, …) plus tokens such as **`INK`**, **`DOWN`**, **`JOIN`**, **`XOR`**, etc. Graphics 1.0 additions — **`RECT`**, **`FILLRECT`**, **`CIRCLE`**, **`FILLCIRCLE`**, **`ELLIPSE`**, **`FILLELLIPSE`**, **`TRIANGLE`**, **`FILLTRIANGLE`**, **`POLYGON`**, **`FILLPOLYGON`**, **`FLOODFILL`**, **`DRAWTEXT`**, **`VSYNC`** — are reserved too. **Do not use those spellings as variable names.** (Exact rules for **labels** vs identifiers are described in the upstream README.)

Authoritative list: **`reserved_words[]`** in **[basic.c](https://github.com/omiq/rgc-basic/blob/main/basic.c)**.

---

## Further reading

- [Terminal & PETSCII](terminal-petscii.md) — **`CHR$`** tables, CLI flags, PETSCII-plain
- [Graphics (Raylib)](graphics-raylib.md) — sprites, bitmap, examples
- [Web IDE](web-ide.md) — WASM, **`HTTP$`**, focus / keyboard
- [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic) — source, **`examples/`**, tests (many examples also open in the [Web IDE](web-ide.md) via `?file=<name>.bas&platform=rgc-basic` when bundled in the IDE preset)

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
| **Arithmetic** | `+`, `-`, `*`, `/`, **`\`** (integer divide, truncate-toward-zero, classic BASIC / QBasic-style), `^` (power), `MOD` (floored modulo). `\` pairs with `MOD`: `(a \ b) * b + (a MOD b) == a`. |
| **Bitwise** | `<<`, `>>`, `AND`, `OR`, `XOR` (integer parts of operands) |
| **Strings** | Concatenation with `+`; string/numeric comparisons where applicable. Backslash escapes inside double-quoted literals — **stable public API**, see "String escapes" below. |

**`RND(x)`** — Returns a value in **0..1** (uniform via `rand()`). If **`x < 0`**, the generator is **reseeded** (C64-style negative seed); the implementation uses `time` so runs differ, similar in spirit to **`RND(-TI)`** on a C64.

**`RNDINT(n)`** — Returns an **integer in 1..n** (inclusive), e.g. `RNDINT(6)` rolls a die. For **`n < 1`** returns **0**; **`RNDINT(negative)`** reseeds from the clock (like `RND(-1)`) and returns 0. Shares the same generator as `RND`, so either reseeds both. Unlike `RND` (which is fractional), `RNDINT` is **pure integer** — a program that uses only `RNDINT` for randomness transpiles to C with **no floating-point / fixed-point runtime**, so it stays small on RAM-tight 8-bit targets. Prefer it over `INT(RND(1)*n)+1` when you only need whole numbers.

### String escapes

Inside double-quoted string literals, the parser expands these backslash escapes at **load time** (before the program runs). Stable public API — relied on by external tools.

| Escape | Produces | Equivalent |
|--------|----------|------------|
| **`\n`** | line feed | `CHR$(10)` |
| **`\r`** | carriage return | `CHR$(13)` |
| **`\t`** | tab | `CHR$(9)` |
| **`\0`** | NUL byte | `CHR$(0)` |
| **`\\`** | literal backslash | `CHR$(92)` |
| **`\"`** | literal double-quote | `CHR$(34)` |
| **`\x`** *(unknown)* | passes through as literal `\x` | — |

Verified shape:

| Source | Length | Value |
|--------|-------:|-------|
| `"a\"b"` | 3 | `a"b` |
| `"x\ny"` | 3 | `x` + LF + `y` |
| `"\\"` | 1 | `\` |
| `"line1\nline2\t!"` | 13 | `line1` + LF + `line2` + TAB + `!` |

**SQL-style `""` doubling is NOT supported** — `"a""b"` parses as `"a"` adjacent to `"b"`, which is two string literals with no operator between them (a parse error in most positions, or empty-string in expression context). Use `\"` for an embedded double-quote.

Works in ASCII + PETSCII modes, terminal + gfx builds, SCREEN 0/1/2. Embedded NULs round-trip through concat / `MID$` / file I/O since the 2.1.1 big-strings refactor.

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
| `#OPTION columns N` | Print width (**1–255**; default **40**). Implicitly clears `nowrap` so the directive does what its name suggests. |
| `#OPTION nowrap` | Do not wrap at column width. Default for non-gfx variants (`basic`, `basic-wasm`); the host terminal / browser pane handles its own wrapping. |
| `#OPTION wrap` | Insert line breaks at column width (inverse of `#OPTION nowrap`). Default for gfx variants. Use to opt into wrap on a non-gfx build, or to override a host-applied `-nowrap`. |
| `#OPTION diagnostics` *(2.1.2)* | Same as **`-diagnostics`**. Default off. When set, fail-soft `HTTP$` / `HTTPFETCH` / `BUFFERFETCH` failures (status 0 or ≥ 400) emit a non-halting **`Warning`** with line context instead of failing silently, and populate **`LASTERROR$()`**. Use during development / tests to locate silent network failures. |
| `#OPTION http strict` / `#OPTION http loose` *(2.1.2)* | Mirror of `#OPTION json strict`. **Strict**: an HTTP failure (status 0 or ≥ 400) from `HTTP$` / `HTTPFETCH` / `BUFFERFETCH` halts with a runtime error instead of silently setting `HTTPSTATUS()`. **Loose** (default) continues — check `HTTPSTATUS()` yourself. Strict overrides the `#OPTION diagnostics` breadcrumb. |
| `#OPTION memory c64` / `pet` / `default` | **basic-gfx / canvas WASM only** — virtual memory layout for **`POKE`/`PEEK`**. |
| `#OPTION screen $addr`, `#OPTION colorram …`, `#OPTION charmem …`, `#OPTION keymatrix …`, `#OPTION bitmap …` | Override individual regions (decimal or hex). |
| `#OPTION gfx_title "text"` | **basic-gfx** — window title (see also **`-gfx-title`**). |
| `#OPTION border N` or `#OPTION border N colour` | **basic-gfx** — padding around the drawable area (see [Graphics](graphics-raylib.md)). |
| `#OPTION real` | **Transpiler (RGC-BASIC → C) only.** Keep floating-point / fixed-point maths. The C backend defaults to **integer** codegen for size on RAM-tight retro targets: fractional literals truncate, `/` is integer division, `^` is integer power, and `SQR` uses an integer square root. `#OPTION real` opts the file back into the fixed-point runtime so decimals, real `/`, and `SQR` behave like the interpreter. No effect on the interpreter (which is always real). For whole-number randomness without `#OPTION real`, use **`RNDINT(n)`** instead of `RND`. |

**Precedence for any setting that can be expressed both ways** (e.g. `columns`, `nowrap` / `wrap`, `palette`, `charset`, `maxstr`): per-script `#OPTION` directives beat CLI / launch flags, which beat the built-in default. So a script with `#OPTION COLUMNS 40` wraps at 40 even if the host passed `-nowrap`. This matches the mental model "`#OPTION` is per-script intent, `-flag` is environment default — intent wins".

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
| **`IF … THEN`** | Inline (`IF X THEN 100`, `IF X THEN PRINT "Y"`) or block: **`IF` … `[ELSE IF cond THEN]` … `[ELSE]` … `END IF`**. Nested blocks supported. |
| **`ELSE IF cond THEN` / `ELSEIF cond THEN`** | Multi-way block-form chain inside an existing `IF … END IF`. Both spellings (two-word `ELSE IF` and one-word `ELSEIF`) tokenise to the same handler; mix freely in one chain. **Block-form only** — no inline `IF a THEN x ELSE IF b THEN y` (use nested inline `IF … THEN … ELSE (IF … THEN …)` instead). Conditions are evaluated top-to-bottom; the first true branch fires and the rest skip to `END IF`. See [tests/else_if_test.bas](https://github.com/omiq/rgc-basic/blob/main/tests/else_if_test.bas) for the full behavior matrix. |
| **`SELECT CASE expr` … `CASE …` … `[CASE ELSE]` … `END SELECT`** *(2.1.2)* | Block multi-way dispatch; the modern replacement for `ON x GOTO` and long `IF/ELSEIF` ladders. The selector `expr` is evaluated **once**; it may be numeric or string. Each `CASE` accepts a **comma list** (`CASE 2, 3, 5`), a **relational test** (`CASE IS >= 10`, operators `= <> < <= > >=`), or a **range** (`CASE 1 TO 5`, `CASE "a" TO "m"`). `CASE ELSE` is the default branch. **Exactly one** matching body runs — there is no C-style fall-through. Nestable (depth 16); a `GOTO` out of a `CASE` body inside a `FUNCTION` unwinds cleanly. See [tests/select_case_test.bas](https://github.com/omiq/rgc-basic/blob/main/tests/select_case_test.bas). |
| **`WHILE` … `WEND`** | Pre-test loop. |
| **`DO` … `LOOP`** | Infinite until **`EXIT`**; or **`LOOP UNTIL expr`**. **`EXIT`** exits the **innermost** **`DO`**. |
| **`FOR` … `NEXT`** | Numeric **`FOR`** with optional **`STEP`** (positive or negative). |
| **`EXIT [DO\|FOR\|WHILE]`** *(2.1.2)* | Break out of the innermost loop of that kind. Bare **`EXIT`** and **`EXIT DO`** leave the innermost **`DO`** (unchanged); **`EXIT FOR`** leaves the innermost **`FOR`**/**`FOREACH`**; **`EXIT WHILE`** leaves the innermost **`WHILE`**. |
| **`CONTINUE FOR\|DO\|WHILE`** *(2.1.2)* | Skip the rest of this iteration and run the loop's test/increment (**`NEXT`** increments + tests; **`LOOP`** re-tests **`UNTIL`**/**`DO WHILE`**; **`WEND`** re-tests **`WHILE`**). The kind keyword is **required** (no bare `CONTINUE`). Safe from inside a block **`IF`** or **`SELECT CASE`** in the body — the block frames are unwound. See [tests/exit_continue_test.bas](https://github.com/omiq/rgc-basic/blob/main/tests/exit_continue_test.bas). |
| **`FOREACH var IN arr[()]` … `NEXT var`** | Iterate each element of a 1-D array (numeric or string). `NEXT var` advances; `EXIT` pops the innermost FOR/FOREACH. Empty arrays run zero iterations. |
| **`GOTO`** | Target is a line number or **label**. Jumping forward *within* a `FOR` body to a line that ends in `NEXT` is supported (the loop frame is preserved). `GOTO` does still reset `IF` / `WHILE` / `DO` nesting, so don't jump *into* the middle of those blocks. |
| **`GOSUB` / `RETURN`** | Subroutine stack; target line or label. |
| **`ON expr GOTO` / `ON expr GOSUB`** | Multi-way branch (e.g. **`ON N GOTO 100,200,300`**). |
| **`ASSERT cond [, msg$]`** *(2.1.2)* | Test a condition for regression / CI scripts. `cond` uses the same relational + `AND`/`OR` handling as **`IF`** (so bare **`=`** is equality). If false: halt with `Error … ASSERT failed: <msg>` and set exit code **2**. If true: continue. Pair with **`-json-status`** (see [terminal](terminal-petscii.md#command-line-options)) so `basic --json-status t.bas; echo $?` is a test gate. Used by the `conformance/` corpus. |

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
| **`ST`** | After **`INPUT#`** / **`GET#`** / **`GETBYTE`** / **`PUTBYTE`**: **0** = success, **64** = end of file, **1** = error / not open. |
| **`PUTBYTE #lfn, byte_expr`** | Single-byte raw write (binary file output). See [detailed reference](#binary-file-io-putbyte-and-getbyte). |
| **`GETBYTE #lfn, var`** | Single-byte raw read into numeric scalar; **-1** at EOF. See [detailed reference](#binary-file-io-putbyte-and-getbyte). |

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
| **`SCREEN 2`** | **Gfx:** 320×200 RGBA. Each pixel carries its own RGBA. 256 KB per plane, lazy-allocated on first entry. Use `COLORRGB r, g, b [, a]` / `BACKGROUNDRGB` for full-colour pens; palette `COLOR n` still works and syncs the RGBA pen via the palette table. |
| **`SCREEN 3`** | **Gfx:** 320×200 8bpp palette-indexed. 64 KB per plane (reuses the SCREEN 1 colour plane). `COLOR` / `BACKGROUND` accept 0..255 in this mode. 256-entry palette shared with SCREEN 1/2 — `PALETTESET` / `PALETTEROTATE` visibly retint every drawn pixel on the next frame without any redraw. Entries 0..15 = C64 defaults; 16..255 = HSV rainbow + greyscale by default. |
| **`SCREEN 4`** | **Gfx:** 640×400 RGBA "QB64-style" desktop canvas. Same primitives and pen system as `SCREEN 2` (`COLORRGB`, `BACKGROUNDRGB`, `LINE`, `RECT`, `FILLRECT`, `CIRCLE`, `DRAWTEXT`, `LOADSCREEN`, `IMAGE LOAD`/`BLEND`) — only the coordinate range and plane size differ (1 MB per plane vs 256 KB). Use for level editors, multi-pane HUDs, IDE-ish workspaces where 320×200 is too cramped. Demo: `examples/gfx_screen4_demo.bas`. |
| **`PALETTESET i, r, g, b [, a]`**, **`PALETTESETHEX i, "#RRGGBB[AA]"`**, **`PALETTERESET`**, **`PALETTEROTATE first, last [, step]`** | **Gfx:** retune the shared 256-entry palette. `PALETTEROTATE` shifts entries [first..last] in-place (one C-side memcpy swap, not 256 PALETTESETs) — classic palette cycling for water / fire / plasma retro effects. Read via **`PALETTE(i, chan)`** and **`PALETTEHEX$(i)`**. |
| **`PALETTELOAD path$`** / **`PALETTESAVE path$`** | **Gfx:** plain-text `.pal` file I/O (JASC-PAL compatible). Round-trips with the live palette. See [detailed reference](#palette-file-io). |
| **`LOADSCREEN path$ [, x [, y]]`** | **Gfx:** load a PNG / BMP / JPG / TGA / GIF into the current screen plane; behaviour depends on `SCREEN` mode. See [detailed reference](#loadscreen-path-x-y). |
| **`OVERLAY ON` / `OVERLAY OFF` / `OVERLAY CLS`** | **Gfx (raylib backend):** redirect bitmap-plane writes to an RGBA HUD plane that composites above tiles + sprites. See [detailed reference](#hud-overlay-raylib-basic-gfx-and-canvas-wasm). |
| **`IMAGE CREATE slot, w, h`**, **`IMAGE BLEND src, sx, sy, sw, sh TO dst, dx, dy`**, **`IMAGE DRAW slot`** | **Gfx (`SCREEN 2` / `SCREEN 4`):** RGBA off-screen surfaces + alpha-composited blits + draw-target retargeting. See [detailed reference](#rgba-blitter-image-create-image-blend-image-draw). |
| **`MAPSAVE path$ [, layer$]`** | **Gfx:** rewrite the named tile layer in the JSON last opened by `MAPLOAD`. See [detailed reference](#map-io-companion-to-mapload). |
| **`CLS`**, **`CLS x, y TO x2, y2`** | Full-screen clear (terminal + gfx) or, in basic-gfx bitmap mode, clear only the given pixel rectangle on the current draw plane (same shape as `FILLRECT` with `COLOR 0`). Handy for redrawing only a HUD strip inside `DOUBLEBUFFER` / `SCREEN BUFFER` loops. |
| **`DRAWTEXT x, y, text$ [, scale]`** / **`DRAWTEXT x, y, text$, fg, bg [, font [, scale]]`** | **Gfx:** stamp string onto the bitmap at pixel `(x, y)` via active chargen. `scale` 1..8 pixel-doubles each source pixel into a `scale × scale` block. Extended 5-arg form sets per-call foreground / background palette indices; `bg = -1` means transparent paper (non-glyph pixels untouched). `font` is parsed but currently ignored — reserved for the eventual `LOADFONT` work. **Inline PETSCII tokens (2.1):** 16 colour tokens (`{RED}`, `{WHITE}`, `{GREEN}`, …) swap the pen mid-string so one call paints multi-colour text. **`{REVERSE ON}` / `{REVERSE OFF}`** toggle reverse-video. With `bg >= 0` reverse fills the cell with fg and stamps glyph in bg (classic Commodore swap). With `bg < 0` reverse fills the cell with fg and leaves glyph pixels UNTOUCHED — whatever is painted underneath reads through the letter shape, giving a "gradient-coloured text" / knockout effect. Cursor-move tokens (`\n` / `\r` / `{HOME}` / `{CLEAR}` / `{DOWN}` / `{UP}` / `{LEFT}` / `{RIGHT}`) are consumed silently — DRAWTEXT is pixel-space, use multiple calls for multi-line layout. See `examples/gfx_drawtext_tokens_demo.bas`. |
| **`IMAGE DRAW slot`** *(2.1)* | **Gfx SCREEN 2 / 4 only:** retarget every RGBA primitive (`LINE`, `FILLRECT`, `CIRCLE`, `DRAWTEXT`, `PSET`, `POLYGON`, …) to an off-screen `IMAGE CREATE` surface instead of the live framebuffer. Mirror of `SCREEN DRAW n`, but routed into the IMAGE pool so the canvas size is arbitrary (not 320×200). `IMAGE DRAW 0` restores the live screen. Used to pre-bake wide scroller strips, world maps, HUD layers, reusable sprite atlases — then blit back with `IMAGE BLEND`. Non-RGBA modes raise a runtime error. See `examples/gfx_imagedraw_demo.bas`. |
| **`SCROLL ZONE id, y, h`**, **`SCROLL ZONE id, dx`**, **`SCROLL ZONE CLEAR id`**, **`SCROLL ZONE RESET id`** *(2.1)* | **Gfx RGBA:** declare up to 15 horizontal bands (ids 1..15) that scroll independently at composite time. `y, h` form declares the rect; two-arg form advances the zone's running dx (modular wrap on plane width, state persists across frames so one-per-frame = smooth scroll). Classic demo message-bar / foreground-only scroll / multi-band parallax. |
| **`SCROLL LINE y, dx`**, **`SCROLL LINE RESET`**, **`SCROLL RESET`** *(2.1)* | **Gfx RGBA:** per-scanline horizontal offset. Each row gets its own `dx`, applied at composite time. Stacks on top of `SCROLL ZONE` offsets. Raster-warp trick reproduced in software — water ripple, flag wave, heat haze, CRT jitter. `SCROLL LINE RESET` zeroes every row; `SCROLL RESET` nukes both zones and per-line state. See `examples/gfx_scrollzone_demo.bas`. |
| **`PAPER n`** | Per-cell background index (**0–15**); only subsequent `PRINT` output stamps `bgcolor[]`. Leaves the global `BACKGROUND` register untouched. |
| **`ANTIALIAS ON` / `ANTIALIAS OFF`** | **Gfx:** bilinear vs nearest-neighbour filter for sprites and the upscaled framebuffer (default **OFF**). |
| **`TIMER id, interval_ms, FuncName`** / **`TIMER STOP id`** / **`TIMER ON id`** / **`TIMER CLEAR id`** | Register, disable, re-enable, or remove a periodic timer. **12** timers max (ids **1–12**); minimum interval **16 ms**; `FuncName` is a zero-arg `FUNCTION`/`END FUNCTION` block. Re-entry is skipped, not queued. |
| **`SCREEN 0` / `SCREEN 1`**, **`PSET`**, **`PRESET`**, **`LINE`**, **`SCREENCODES`**, **`SCROLL`**, sprite statements | **Gfx / canvas** — see [Graphics](graphics-raylib.md). |
| **`LOADSOUND slot, "file.wav"`**, **`PLAYSOUND slot`**, **`STOPSOUND`**, **`UNLOADSOUND slot`**, **`SOUNDPLAYING()`** | **basic-gfx + basic-wasm-raylib (canvas WASM stays frozen):** single-voice WAV playback, 32 slots. `PLAYSOUND` is non-blocking and stops whatever was already playing. `SOUNDPLAYING()` returns **1** while audible, **0** when idle — self-clears at natural end-of-sample. Browsers require a user gesture (key / click) before `AudioContext` resumes, so gate the first cue on `KEYPRESS` or `ISMOUSEBUTTONPRESSED`. |
| **`LOADMUSIC slot, "song.mod"`**, **`PLAYMUSIC slot`**, **`STOPMUSIC slot`**, **`PAUSEMUSIC slot`** / **`RESUMEMUSIC slot`**, **`MUSICVOLUME slot, 0.0..1.0`**, **`MUSICLOOP slot, 0|1`**, **`UNLOADMUSIC slot`**, **`MUSICPLAYING(slot)`**, **`MUSICLENGTH(slot)`**, **`MUSICTIME(slot)`**, **`MUSICPEAK()`**, **`MUSICTITLE$(slot)`**, **`MUSICSAMPLENAME$(slot, idx)`**, **`MUSICCHANNELS(slot)`**, **`MUSICPATTERNS(slot)`**, **`MUSICORDERS(slot)`**, **`MUSICSAMPLECOUNT(slot)`** | **basic-gfx + basic-wasm-raylib (canvas WASM stays frozen):** streaming tracker-module / long-form playback via raylib `raudio` — **MOD / XM / S3M / IT / OGG / MP3**. Eight slots, separate pool from `LOADSOUND`. `MUSICLENGTH(slot)` returns total seconds (MOD length computed via pattern/tempo walk at load — jar_mod's built-in probe freezes Windows MinGW for tens of seconds, so we do it ourselves). `MUSICTIME(slot)` is elapsed seconds (wraps on loop). `MUSICPEAK()` is the 0..1 master-mix held-peak for VU meters. Same browser-autoplay rules as `LOADSOUND` — wait for a user gesture before the first `LOADMUSIC`. Example: `examples/gfx_music_demo.bas` with bundled Public-Domain tracks. |

### Sprites and gamepad (gfx / canvas)

| Statements / functions | See |
|------------------------|-----|
| **`LOADSPRITE`** / **`SPRITE LOAD`**, **`DRAWSPRITE`** / **`SPRITE DRAW`**, **`DRAWSPRITETILE`** / **`TILE DRAW`**, **`UNLOADSPRITE`** / **`SPRITE FREE`**, **`SPRITEVISIBLE`**, **`SPRITEMODULATE`**, **`SPRITEFRAME`** / **`SPRITE FRAME`**, **`SPRITECOPY`**, **`SPRITE STAMP`** (multi-instance) | [Graphics — PNG sprites](graphics-raylib.md#png-sprites-full-reference) |
| **`TILEMAP DRAW`** (batched array → tile grid), **`DRAWTILEMAP`** (alias) | [Graphics — tilemaps](graphics-raylib.md#tilemaps-tilemap-draw) |
| **`IMAGE NEW`**, **`IMAGE FREE`**, **`IMAGE COPY … TO …`**, **`IMAGE LOAD`**, **`IMAGE GRAB`**, **`IMAGE SAVE`** | [Graphics — blitter surfaces](graphics-raylib.md#blitter-surfaces-image-new-copy-grab-save) |
| **`RECT`** / **`FILLRECT`**, **`CIRCLE`** / **`FILLCIRCLE`**, **`ELLIPSE`** / **`FILLELLIPSE`**, **`TRIANGLE`** / **`FILLTRIANGLE`**, **`POLYGON`** / **`FILLPOLYGON`**, **`FLOODFILL`**, **`DRAWTEXT`** | [Graphics — bitmap mode](graphics-raylib.md#bitmap-mode-screen-1) |
| **`VSYNC`** (frame commit + wait one display frame) | [Graphics — keyboard & time](graphics-raylib.md#keyboard-time) |
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
| **`UCASE$(s$)`**, **`LCASE$(s$)`** | ASCII case (folds `A-Z`/`a-z`). On CBM/PETSCII transpiled targets these are no-ops on screen-letter codes (65-90), so they're safe to call but won't fold PETSCII case; in upper/graphics mode keys already arrive uppercase. |
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
| **`RGCVERSION$()`** *(2.1.2)* | Build's version + date + variant, e.g. `"v2.1.1-23-gabc1234 (2026-05-23) basic-wasm"`. Same format as the `-v` / `--version` flag's first line. Tools and tests can branch on minimum version (`IF RGCVERSION$() < "2.1.3-" THEN PRINT "needs 2.1.3+"`). Also exposed as a host-side ccall export `basic_get_version() → string` for JS hosts. |
| **`LASTERROR$()`** *(2.1.2)* | Formatted text of the last runtime diagnostic, e.g. `"Warning on line 20: OPEN: cannot open …"` or `"Error at lib.bas:110: …"`, or `""` if none yet. Pull-mode companion to `JSONSTATUS()` / `HTTPSTATUS()`. Captures hard errors and the soft `Warning` diagnostics; silent HTTP/JSON status failures are captured only under `#OPTION DIAGNOSTICS` (otherwise read `HTTPSTATUS()` / `JSONSTATUS()`). Host-side ccall export: `basic_get_lasterror() → string`. |

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

### HTTP and buffers (browser WASM + `basic-gfx`)

| Function / statement | Notes |
|----------------------|--------|
| **`HTTP$(url$ [, method$ [, body$]])`** | **`fetch`**; response body as string, capped at `#OPTION maxstr` (≤4 KB). Alias: **`HTTP(url)`** without **`$`** calls the same intrinsic. |
| **`HTTPSTATUS()`** | Status from last **`HTTP$`** / **`HTTPFETCH`** / **`BUFFERFETCH`**; **0** if failed / not WASM. |
| **`HTTPFETCH(url$, path$ [, method$ [, body$]])`** | One-shot HTTP-to-file. Bypasses the 4 KB string cap. See [detailed reference](#httpfetchurl-path-method-body). |
| **`BUFFERNEW slot`**, **`BUFFERFETCH slot, url$ [, method$ [, body$]]`**, **`BUFFERFREE slot`**, **`BUFFERLEN(slot)`**, **`BUFFERPATH$(slot)`** | Slot-based file-backed HTTP. Pulls arbitrary-size responses into a temp file you can `OPEN` / `GETBYTE` / `LOADSCREEN` / etc. See [Network & buffers](network-and-buffers.md) and [detailed reference](#buffer-slots-file-backed-http-fetches). |

Details: [Web IDE — `HTTP$`](web-ide.md#http-and-httpstatus); [Network & buffers](network-and-buffers.md).

### Graphics-only (see [Graphics](graphics-raylib.md))

**`INKEY$()`**, **`PEEK`**, **`KEYDOWN(code)`**, **`KEYUP(code)`**, **`KEYPRESS(code)`** (rising-edge latch), **`ANIMFRAME(first, last, jiffies)`** (time-cycled frame index), **`SPRITEW`**, **`SPRITEH`**, **`SPRITETILES`** / **`TILE COUNT`** / **`SPRITE FRAMES`**, **`SHEET COLS/ROWS/WIDTH/HEIGHT`**, **`SPRITEFRAME()`**, **`SPRITECOLLIDE`**, **`ISMOUSEOVERSPRITE(slot [, alpha_cutoff])`** (SCROLL-aware; one arg = bbox, two args = pixel-perfect alpha sampling), **`SPRITEAT(x, y)`** (topmost visible slot at point, Z tie-break; −1 if none), **`SCROLLX()`**, **`SCROLLY()`**, **`JOY`**, **`JOYSTICK`**, **`JOYAXIS`**.

---

## System variables

| Name | Behaviour |
|------|-----------|
| **`ST`** | Set by **`INPUT#`** / **`GET#`** (see [File I/O](#file-io-cbm-style)). |
| **`TI`** | **basic-gfx / canvas:** **60 Hz** jiffy counter (wraps per README). **Native terminal:** **not** jiffies — implementation uses **Unix time** (seconds) as a fallback so **`RND(-TI)`** still reseeds. **Canvas WASM (gfx):** derived from monotonic clock when per-frame ticks are not used. |
| **`TI$`** | **Gfx:** string **`HHMMSS`** from jiffy clock. **Terminal:** **wall-clock** **`HHMMSS`** from local time. |
| **`SCREEN_COLS`** | Text columns of the current machine / screen mode (no parens). Honours **`#OPTION columns N`**; **gfx** uses the active grid width, terminal uses the print width. |
| **`SCREEN_ROWS`** | Text rows the hardware offers **before a newline scrolls** (no parens). C64-class machine is **25** (so a C64 build is **40 × 25**). Use with **`SCREEN_COLS`** to lay out for narrow targets instead of hard-coding sizes. |

Identifiers starting with **`TI`** are resolved with CBM-style rules ( **`TI`** vs **`TI$`** ).

When transpiled to C (emit-c), **`SCREEN_COLS`** / **`SCREEN_ROWS`** map to the target adapter's `rgc_screen_w()` / `rgc_screen_h()`, so the same source adapts to each machine's real text grid (e.g. a 32-column target hides a wide legend that a 40-column target shows).

---

## Recently added — detailed reference

Every entry below follows the same shape: **Purpose**, **Parameters**, **Returns**, **Example**. Older entries already covered in the tables above are not repeated.

### Buffer slots — file-backed HTTP fetches

A `BUFFER` is a numbered slot (0..15) backed by a temp file the interpreter manages on disk (or in MEMFS on browser WASM). The point: `HTTP$()` returns a string capped by `#OPTION maxstr` (4 KB max), so you can't pull a 100 KB JSON or a 2 MB binary into memory in one shot. `BUFFER*` lets you stream the response into a file you can then `OPEN` like any other and walk byte-by-byte with `GETBYTE` or `INPUT#`.

Available in `basic-gfx` and browser WASM (`basic-wasm-raylib`); plain terminal `basic` returns 0 / `""` from `BUFFERLEN` / `BUFFERPATH$`.

#### `BUFFERNEW slot`

- **Purpose**: allocate a buffer slot and create its empty backing file. Replaces any prior occupant of the same slot.
- **Parameters**: `slot` — integer 0..15.
- **Returns**: nothing (statement). Errors hint "slot out of range" or "cannot create backing file".
- **Example**:
  ```basic
  BUFFERNEW 0
  ```

#### `BUFFERFETCH slot, url$ [, method$ [, body$]]`

- **Purpose**: HTTP fetch into the slot's backing file. Browser WASM only — native builds set `HTTPSTATUS()` to 0 and write nothing.
- **Parameters**:
  - `slot` — integer 0..15, must have been `BUFFERNEW`'d.
  - `url$` — full URL (must allow CORS from your page origin).
  - `method$` — optional, `"GET"` (default) / `"POST"` / `"PUT"` / `"DELETE"`.
  - `body$` — optional request body for POST/PUT.
- **Returns**: nothing (statement). Sets `HTTPSTATUS()` to the HTTP status code on completion.
- **Example**:
  ```basic
  BUFFERNEW 0
  BUFFERFETCH 0, "https://api.example.com/data"
  PRINT "got "; BUFFERLEN(0); " bytes, status "; HTTPSTATUS()
  ```

#### `BUFFERFREE slot`

- **Purpose**: unlink the backing file and release the slot. Idempotent — safe to call on an empty slot.
- **Parameters**: `slot` — integer 0..15.
- **Returns**: nothing (statement).
- **Example**:
  ```basic
  BUFFERFREE 0
  ```

#### `BUFFERLEN(slot)`

- **Purpose**: byte length of the slot's backing file (i.e., how much was downloaded).
- **Parameters**: `slot` — integer 0..15.
- **Returns**: numeric bytes; **0** if slot empty / unallocated / on the terminal build.
- **Example**:
  ```basic
  IF BUFFERLEN(0) = 0 THEN PRINT "empty response" : END
  ```

#### `BUFFERPATH$(slot)`

- **Purpose**: filesystem path of the slot's backing file. Pass to `OPEN`, `IMAGE LOAD`, `LOADSCREEN`, `MAPLOAD`, etc. so any path-taking command can consume HTTP-fetched bytes.
- **Parameters**: `slot` — integer 0..15.
- **Returns**: string path; **`""`** if slot empty / unallocated.
- **Example**:
  ```basic
  OPEN 1, 1, 0, BUFFERPATH$(0)
  GETBYTE #1, B
  CLOSE 1
  ```

See also: full walkthrough in [Network & buffers](network-and-buffers.md).

### `HTTPFETCH(url$, path$ [, method$ [, body$]])`

- **Purpose**: one-shot HTTP-to-file. Fetches `url$` and writes the body to `path$` directly (no slot bookkeeping). Use when you already have the destination path you want; use `BUFFER*` when you want the interpreter to pick a temp path for you.
- **Parameters**:
  - `url$` — full URL, CORS-aware on browser WASM.
  - `path$` — destination file path (MEMFS in browser, host FS native).
  - `method$` — optional, default GET.
  - `body$` — optional request body.
- **Returns**: numeric — non-zero on success, 0 on failure. Also sets `HTTPSTATUS()`.
- **Example**:
  ```basic
  IF HTTPFETCH("https://example.com/sky.png", "sky.png") THEN
    LOADSCREEN "sky.png"
  END IF
  ```

### Binary file I/O — `PUTBYTE` and `GETBYTE`

Pair with `OPEN lfn, device, sec, "filename"` (device 1 = host file, secondary 0/1/2 = read/write/append). `PRINT#`/`INPUT#` are line/token oriented; `PUTBYTE`/`GETBYTE` are raw single-byte for binary formats (PNG inspection, MOD parsing, custom save files).

#### `PUTBYTE #lfn, byte_expr`

- **Purpose**: write one byte (0..255) to an open file channel.
- **Parameters**:
  - `lfn` — logical file number from `OPEN` (1..255).
  - `byte_expr` — numeric, masked with `& 255`.
- **Returns**: nothing. Sets `ST = 0` on success, `ST = 1` if the channel is not open or the write failed.
- **Example**:
  ```basic
  OPEN 2, 1, 1, "save.bin"
  FOR I = 0 TO 255 : PUTBYTE #2, I : NEXT I
  CLOSE 2
  ```

#### `GETBYTE #lfn, var`

- **Purpose**: read one byte (0..255) from an open file channel into a numeric scalar.
- **Parameters**:
  - `lfn` — logical file number (1..255).
  - `var` — numeric scalar variable (not array, not string). Receives 0..255 on success or **-1** at EOF / on error.
- **Returns**: nothing. Sets `ST = 0` on success, `ST = 64` at EOF, `ST = 1` if the channel is not open.
- **Example**:
  ```basic
  OPEN 1, 1, 0, "data.bin"
  DO
    GETBYTE #1, B
    IF B = -1 THEN EXIT
    PRINT HEX$(B); " ";
  LOOP
  CLOSE 1
  ```

### Object overlays — `OBJLOAD` / `OBJSAVE`

Decouple object placement from terrain so a single base map can drive multiple gameplay variants (easy / hard, wave 1 / wave 2 / wave 3, base / mod, etc.). Pair with [`MAPLOAD`](#map-io-companion-to-mapload): load the base map first, then `OBJLOAD` an overlay file that replaces or extends the `MAP_OBJ_*` arrays.

Overlay schema (Shape A):

```json
{
  "format": 1,
  "kind": "objects-overlay",
  "appliesTo": "level1-overworld",
  "mode": "replace",
  "objects": [
    { "id": 100, "type": "enemy", "kind": "octorok",
      "shape": "rect", "x": 64, "y": 64, "w": 16, "h": 16 }
  ]
}
```

A Shape B overlay (full map JSON whose only populated layer is `obj`) is also accepted as a fallback so editors that only emit the wider schema still work. The runtime ignores `appliesTo` — it's documentation; check it from BASIC if you want a hard match.

#### `OBJLOAD path$ [, mode$]`

- **Purpose**: load an objects-overlay file into the existing `MAP_OBJ_*` arrays. Caller must `DIM` the arrays large enough for the total objects (base + overlay if appending).
- **Parameters**:
  - `path$` — overlay file. Browser WASM: must be bundled in the IDE preset.
  - `mode$` — optional. `"replace"` (default) clears `MAP_OBJ_COUNT` to 0 before loading. `"append"` stacks overlay objects on top of whatever's already in the arrays.
- **Returns**: nothing. Sets `MAP_OBJ_COUNT` to the new total. Errors on missing file, file > 4 MiB, unsupported format, missing objects array.
- **Example**:
  ```basic
  MAPLOAD "level1.json"
  IF DIFF$ = "hard" THEN
    OBJLOAD "level1.hard.objects.json"
  ELSE
    OBJLOAD "level1.easy.objects.json"
  END IF
  ```

#### `OBJSAVE path$`

- **Purpose**: write the current `MAP_OBJ_*` arrays as a Shape A objects-overlay file. Used by editors and by procedural-spawn programs that want to capture a generated wave.
- **Parameters**: `path$` — destination file.
- **Returns**: nothing. Errors if the path is unwritable.
- **Limitation**: `props` are **not** preserved in this build — overlay output is regenerated from the live arrays only. Hand-edit the JSON if you need props round-trip; a future revision will read `MAP_OBJ_PROPS$()`.
- **Shape detection**: when both `MAP_OBJ_W(i) = 0` and `MAP_OBJ_H(i) = 0`, the entry is emitted as `"shape": "point"` (no w/h fields). Otherwise `"shape": "rect"` with w/h.
- **Example**:
  ```basic
  OBJSAVE "level1.hard.objects.json"
  IF FILEEXISTS("level1.hard.objects.json") THEN DOWNLOAD "level1.hard.objects.json"
  ```

### Map I/O — companion to `MAPLOAD`

#### `MAPSAVE path$ [, layer$]`

- **Purpose**: rewrite the named tile layer's `data` array in the JSON last opened by `MAPLOAD` and write the patched JSON to `path$`. Use to round-trip live edits (a built-in level editor that mutates `MAP_BG()` then saves).
- **Parameters**:
  - `path$` — destination file. Browser WASM persists via the host's MEMFS — pair with `DOWNLOAD` to deliver as a real file.
  - `layer$` — optional, default `"bg"`. Use `"fg"` to save the foreground layer; the loader reads `MAP_FG()` for that case.
- **Returns**: nothing. Errors if no prior `MAPLOAD`, if the layer / `data` array is missing, or if `MAP_W * MAP_H` doesn't match the array DIM.
- **Example**:
  ```basic
  MAPLOAD "level1.json"
  MAP_BG(0) = 17                 : REM water at top-left
  MAPSAVE "level1.json"
  IF FILEEXISTS("level1.json") THEN DOWNLOAD "level1.json"
  ```

### HUD overlay (raylib `basic-gfx` and canvas WASM)

#### `OVERLAY ON | OVERLAY OFF | OVERLAY CLS`

- **Purpose**: redirect bitmap-plane primitives (`PSET`, `LINE`, `FILLRECT`, `RECT`, `DRAWTEXT`, `CLS`) to a second RGBA plane composited **above** the cell list (`TILEMAP DRAW` + `SPRITE STAMP`), so HUD text and dialog boxes always sit above world tiles. The raylib backend composites bitmap → cells → overlay; canvas WASM (frozen) currently flattens the overlay onto the bitmap plane (works for static HUDs but not for above-tile sorting).
- **Screen-mode requirement**: redirection is honoured **only in `SCREEN 2` and `SCREEN 4`** (the RGBA modes). The compositor renders the overlay on top in every mode, but in `SCREEN 0` (text), `SCREEN 1` (1bpp), and `SCREEN 3` (indexed) the primitives keep writing to their own planes (`text RAM`, `bitmap[]`, `bitmap_color[]`) — `OVERLAY ON` is accepted, the buffer auto-allocates, but stays empty so nothing visible composites on top. If you need a HUD over an indexed-mode world, paint it directly to the indexed plane last (after world tiles), or switch to `SCREEN 2` / `SCREEN 4`.
- **Parameters**:
  - `ON` — start redirecting bitmap-plane writes to the overlay (lazy-allocates the buffer).
  - `OFF` — back to the main bitmap (default).
  - `CLS` — clear the overlay to fully transparent (alpha 0).
- **Returns**: nothing.
- **Example**:
  ```basic
  DO
    CLS                                       : REM clear world bitmap
    TILEMAP DRAW 0, 0, 0, COLS, ROWS, MAP()
    SPRITE STAMP 1, PX, PY, 0, 50
    OVERLAY ON
      CLS                                     : REM clear overlay
      COLORRGB 0,0,0,255 : FILLRECT 0,0 TO 319,23
      COLORRGB 255,240,80,255 : DRAWTEXT 4,4,"LIFE 3"
    OVERLAY OFF
    VSYNC
  LOOP
  ```

### `LOADSCREEN path$ [, x [, y]]`

- **Purpose**: load a PNG / BMP / JPG / TGA / GIF into the **current** screen plane. Behaviour dispatches on the active `SCREEN` mode:
  - `SCREEN 0` (text) — cell-quantises to one fg + one bg hardware colour per cell + a PETSCII block glyph.
  - `SCREEN 1` (1bpp) — Floyd-Steinberg dithers to the 16 hardware colours; per-pixel index stored in `bitmap_color[]`.
  - `SCREEN 2` (RGBA 320×200) — full RGBA copy.
  - `SCREEN 3` (256-colour indexed) — nearest-RGB match into the 256-entry palette; alpha < 128 maps to current `BACKGROUND`.
  - `SCREEN 4` (RGBA 640×400) — same as `SCREEN 2` with 4× pixels.
- **Parameters**:
  - `path$` — image file. **Must be a literal quoted string** in browser WASM so the IDE's asset pre-load regex sees the filename and stages it into MEMFS before run.
  - `x`, `y` — optional offset. Character cells in `SCREEN 0`; pixels otherwise. Clipped to plane bounds.
- **Returns**: nothing. Errors if file unreadable / wrong format / out-of-mode.
- **Example**:
  ```basic
  SCREEN 2
  LOADSCREEN "sky.png"
  ```

### Palette file I/O

#### `PALETTELOAD path$`

- **Purpose**: read a plain-text `.pal` file into the live 256-entry palette. Tolerates JASC-PAL headers, `#` comments, blank lines. Missing entries beyond the file's count stay untouched. Pairs with `PALETTEROTATE` for retro palette-cycling on a hand-tuned palette.
- **Parameters**: `path$` — source file. Format: 256 lines of `R G B [A]` decimal 0..255.
- **Returns**: nothing. Errors if file missing / unreadable.
- **Example**:
  ```basic
  PALETTELOAD "sunset.pal"
  PALETTEROTATE 16, 255             : REM cycle bands 16..255
  ```

#### `PALETTESAVE path$`

- **Purpose**: write the live palette to a plain-text `.pal` file (256 entries, `R G B A` decimal). Round-trips through `PALETTELOAD`.
- **Parameters**: `path$` — destination file.
- **Returns**: nothing.
- **Example**:
  ```basic
  PALETTESAVE "my-tuned.pal"
  IF FILEEXISTS("my-tuned.pal") THEN DOWNLOAD "my-tuned.pal"
  ```

### RGBA blitter — `IMAGE CREATE` / `IMAGE BLEND` / `IMAGE DRAW`

The `IMAGE NEW` / `IMAGE COPY` / `IMAGE GRAB` / `IMAGE LOAD` / `IMAGE SAVE` family is documented under [Graphics — blitter surfaces](graphics-raylib.md#blitter-surfaces-image-new-copy-grab-save). The three commands below are the **RGBA** companions for full alpha-composited work in `SCREEN 2` / `SCREEN 4`.

#### `IMAGE CREATE slot, w, h`

- **Purpose**: allocate an **RGBA** off-screen surface (vs `IMAGE NEW` which is 1bpp). Must be RGBA before `IMAGE LOAD` if the source PNG has alpha that you want preserved through `IMAGE BLEND` — otherwise the legacy 1bpp path takes over and alpha is lost.
- **Parameters**:
  - `slot` — 1..31 (slot 0 is the live framebuffer).
  - `w`, `h` — pixel dimensions, both > 0. Any size; subsequent `IMAGE LOAD` resizes to match the PNG.
- **Returns**: nothing. Errors on bad slot / size / out of memory.
- **Example**:
  ```basic
  IMAGE CREATE 1, 64, 64
  IMAGE LOAD   1, "chick.png"
  ```

#### `IMAGE BLEND src, sx, sy, sw, sh TO dst, dx, dy`

- **Purpose**: alpha-composited blit (Porter-Duff "source over") between two RGBA slots. Semi-transparent source pixels smooth-blend against destination pixels.
- **Parameters**:
  - `src` — RGBA source slot (1..31).
  - `sx, sy, sw, sh` — rectangle inside `src`.
  - `dst` — RGBA destination slot. Use **0** to route to the live `SCREEN 2` / `SCREEN 4` framebuffer.
  - `dx, dy` — top-left in `dst`.
- **Returns**: nothing. Errors if either slot is non-RGBA, or `dst = 0` outside `SCREEN 2` / `SCREEN 4`.
- **Example**:
  ```basic
  SCREEN 2
  LOADSCREEN "sky.png"
  IMAGE CREATE 1, 32, 32 : IMAGE LOAD 1, "chick.png"
  IMAGE BLEND 1, 0, 0, 32, 32 TO 0, X, Y
  ```

#### `IMAGE DRAW slot`

- **Purpose**: retarget every RGBA primitive (`LINE`, `FILLRECT`, `CIRCLE`, `DRAWTEXT`, `PSET`, `POLYGON`, …) to an off-screen `IMAGE CREATE` surface instead of the live framebuffer. Mirrors `SCREEN DRAW n` but routed into the IMAGE pool, so canvas size is arbitrary (not tied to 320×200 / 640×400). Used to pre-bake wide scroller strips, world maps, HUD layers, reusable sprite atlases — then blit back with `IMAGE BLEND`.
- **Parameters**: `slot` — `0` to restore the live screen, or `1..31` for an `IMAGE CREATE`-allocated RGBA surface. Non-RGBA modes raise a runtime error.
- **Returns**: nothing.
- **Example**:
  ```basic
  SCREEN 2
  IMAGE CREATE 1, 1280, 200          : REM 4-screen-wide strip
  IMAGE DRAW 1                       : REM redirect drawing
  FOR I = 0 TO 1279 STEP 8 : LINE I,0 TO I,199 : NEXT I
  IMAGE DRAW 0                       : REM back to live
  IMAGE BLEND 1, SX, 0, 320, 200 TO 0, 0, 0
  ```

### Charset variants

`#OPTION charset` and the `-charset` CLI flag accept more than the original `upper` / `lower`:

| Token | Effect |
|-------|--------|
| `upper` | C64 default — uppercase + graphics |
| `lower` | C64 default — lower + uppercase mixed |
| `c64-upper`, `c64-lower` | Same as above, explicit family |
| `pet-upper`, `pet-lower` | PET-style alternate ROM (`pet_*.64c`). Aliases: `pet-graphics` (= upper), `pet-text` (= lower) |

- **Purpose**: pick which character ROM family + letter set is loaded into the chargen.
- **Returns**: load-time only; no runtime feedback. Unknown values print to stderr.
- **Example**:
  ```basic
  #OPTION charset pet-lower
  PRINT "PET-style lowercase"
  ```

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

- [Getting started](getting-started.md) — first-program tour for new users
- [Terminal & PETSCII](terminal-petscii.md) — **`CHR$`** tables, CLI flags, PETSCII-plain
- [Graphics (Raylib)](graphics-raylib.md) — sprites, bitmap, screen modes, sound, examples
- [Web IDE](web-ide.md) — WASM, **`HTTP$`**, focus / keyboard
- [Network & buffers](network-and-buffers.md) — `HTTP$` / `HTTPFETCH` / `BUFFER*`, binary I/O
- [Level authoring](level-authoring.md) — `MAPLOAD` / `MAPSAVE` JSON tilemaps
- [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic) — source, **`examples/`**, tests (many examples also open in the [Web IDE](web-ide.md) via `?file=<name>.bas&platform=rgc-basic` when bundled in the IDE preset)

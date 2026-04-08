# RGC BASIC — language reference (summary)

This page is a **structured summary** of the RGC BASIC language. For every edge case, keyword nuance, and latest addition, see the **[upstream README](https://github.com/omiq/rgc-basic/blob/main/README.md)** and **[CHANGELOG](https://github.com/omiq/rgc-basic/blob/main/CHANGELOG.md)**.

## Program shape

- **Line-numbered** programs (`10 PRINT …`, `20 …`) — classic CBM style.
- **Numberless** programs — if the first non-blank line has no leading digits, the interpreter assigns internal line numbers; you can still use **labels** and structured blocks.
- **Shebang** — `#!/usr/bin/env basic` on line 1 is ignored (useful for executable scripts on Unix).

Load-time **normalization** accepts compact CBM style without spaces (`IFX<0THEN`, `FORI=1TO9`, …).

## Meta directives (`#` prefix)

Processed at load time (see repo `docs/meta-directives-plan.md` for full detail):

| Directive | Purpose |
|-----------|---------|
| `#INCLUDE "path"` | Splice another file here (avoid duplicate line numbers in includes). |
| `#OPTION petscii` / `#OPTION charset lower` / `#OPTION palette c64` | Mirror CLI PETSCII/charset/palette options. |
| `#OPTION maxstr 255` / `#OPTION columns 80` / `#OPTION nowrap` | String length, print width, wrapping. |
| `#OPTION memory c64\|pet\|default` and region overrides | **basic-gfx / WASM canvas** — virtual memory layout for `POKE`/`PEEK` (see [Graphics](graphics-raylib.md)). |

## Core statements (selection)

| Area | Statements |
|------|------------|
| I/O | `PRINT` / `?`, `INPUT`, `GET` (non-blocking string), `LOCATE`, `TEXTAT` |
| Control | `IF … THEN` / `ELSE` / `END IF`, `WHILE`/`WEND`, `DO`/`LOOP`/`EXIT`, `FOR`/`NEXT`, `GOTO` (line or **label**), `GOSUB`/`RETURN`, `ON … GOTO`/`GOSUB` |
| Data | `READ`/`DATA`/`RESTORE`, `DIM`, `REM` / `'` |
| Functions | `DEF FN`, multi-line `FUNCTION` … `END FUNCTION` with `RETURN expr` |
| Files (CBM-style) | `OPEN`, `PRINT#`, `INPUT#`, `GET#`, `CLOSE`, system variable `ST` |
| Arrays & strings | `DIM`, `SORT`, `SPLIT`/`JOIN` |
| Misc | `END`, `STOP`, `CLR`, `POKE` (no-op in terminal for compatibility), `SLEEP` (ticks) |

**File I/O** uses logical file numbers and paths on **device 1** as in the README (`OPEN lfn, 1, sec, "filename"`).

## Intrinsic functions (selection)

| Category | Names |
|----------|--------|
| Math | `SIN`, `COS`, `TAN`, `ABS`, `INT`, `SQR`, `SGN`, `EXP`, `LOG`, `RND` |
| Strings | `LEN`, `VAL`, `STR$`, `CHR$`, `ASC`, `INSTR`, `REPLACE`, `TRIM$`, `LTRIM$`, `RTRIM$`, `FIELD$`, `UCASE$`, `LCASE$`, `MID$`, `LEFT$`, `RIGHT$` |
| Arrays | `INDEXOF`, `LASTINDEXOF` |
| JSON | `JSON$(json$, path$)` — extract by path string |
| Environment | `ENV$(name$)`, `PLATFORM$()` |
| Dynamic | `EVAL(expr$)` — evaluate expression string |
| Layout | `TAB`, `SPC` in `PRINT` |
| Hex | `DEC(s$)`, `HEX$(n)` |
| Scripting | `ARGC()`, `ARG$(n)`, `SYSTEM(cmd$)`, `EXEC$(cmd$)` |

## Variables

- **Numeric:** `A`, `my_var`, `score1` — names up to **31** significant characters; underscores allowed.
- **String:** names ending in `$` (e.g. `A$`, `name$`).
- **Arrays:** `DIM A(10)`, multi-dim `C(2,3)`; indices **0-based** internally (`DIM A(10)` → `0..10`).

Reserved words cannot be used as variable names; **labels** may coincide with keywords in some cases (see README).

## Terminal-only vs graphics-only

Some statements apply only to **`basic-gfx`** (virtual memory, `LOAD` into address, `MEMSET`, `MEMCPY`, sprites — see [Graphics](graphics-raylib.md)). The plain **`basic`** build reports errors for those if used.

## PETSCII tokens in strings

Inside **double-quoted strings**, `{TOKENS}` expand at load time to the equivalent of `CHR$(…)` sequences — colours (`{RED}`), `{HOME}`, `{CLR}`, numeric `{147}`, etc. See [Terminal & PETSCII](terminal-petscii.md) and repo **`docs/c64-color-codes.md`**.

## Further reading

- [Terminal & PETSCII](terminal-petscii.md) — `COLOR`, `CURSOR`, ANSI mapping
- [Graphics (Raylib)](graphics-raylib.md) — `SCREEN`, sprites, `TI`/`TI$`
- [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic) — full statement list and semantics

# RGC BASIC — terminal interpreter & PETSCII

The **`basic`** binary (Linux/macOS/WSL: `./basic`, Windows: `basic.exe`) runs programs from a file with **stdin/stdout** semantics: **`PRINT`** goes to standard output, **`INPUT`** reads lines from standard input. That suits **scripting**, **pipes**, and tools — plus optional **PETSCII→ANSI** so C64-style control codes render in a modern UTF-8 terminal.

---

## Invocation

```bash
./basic hello.bas
basic.exe hello.bas
```

With **no** filename, the interpreter prints **usage** to stderr.

**Usage line (terminal build):**

```text
basic [-petscii] [-petscii-plain] [-charset upper|lower] [-palette ansi|c64] [-maxstr N] [-columns N] [-nowrap] <program.bas>
```

---

## Command-line options

| Flag | Effect |
|------|--------|
| **`-petscii`** / **`--petscii`** | Map **`CHR$`** control and colour codes to **ANSI** escapes; map printable PETSCII to Unicode (block graphics, symbols, pound sign, etc.). |
| **`-petscii-plain`** / **`--petscii-plain`** | PETSCII **without** ANSI: control/colour bytes produce **no** visible output (alignment for **`.seq`** dumps); printable/graphics bytes still map to Unicode. **`CHR$(13)`** may still emit newline; see upstream for edge cases. |
| **`-charset upper`** / **`-charset lower`** | **Upper/graphics** vs **lower/upper** letter set when rendering PETSCII text. |
| **`-palette ansi`** / **`-palette c64`** | How PETSCII colours map: classic **16-colour ANSI** vs **256-colour** (`38;5;n`) C64-like indices. |
| **`-maxstr N`** | Maximum string length (**1–4096**); default is large. Use **`255`** for C64-like limits. |
| **`-columns N`** | **`PRINT`** width (**1–255**); default **40**. Comma zones scale (e.g. 10 columns per zone at 40-wide). |
| **`-nowrap`** | Do not insert line breaks at column width; let the terminal wrap. |

The same switches can be set in source with **`#OPTION`** (see [Language reference](language.md#meta-directives--prefix)).

---

## `CHR$` and PETSCII mode

In **`-petscii`** (non-plain) mode, selected **`CHR$`** values produce:

- **Cursor / screen**: e.g. **`147`** clear+home, **`19`** home, **`17`/`145`/`29`/`157`** cursor moves, **`20`** backspace-style delete, **`148`** insert behaviour (see upstream mapping).
- **Reverse video**: **`18`** on, **`146`** off.
- **Charset switch**: **`14`** lowercase mode, **`142`** uppercase/graphics.
- **Colours**: mapped to ANSI foreground SGR codes (and extended colours approximated).

In **`-petscii-plain`**, most control/colour codes produce **empty** output so columns stay aligned like a fixed C64 column layout; printable codes still map to Unicode (**`CHR$(13)`** still produces a newline in the upstream mapping).

### C64 palette indices (`COLOR` / `BACKGROUND`)

**`COLOR n`** / **`COLOUR n`** set foreground; **`BACKGROUND n`** sets background. Indices **0–15** map to ANSI (approximate C64 look):

| Index | `CHR$` (PETSCII) | `{TOKEN}` examples | Approx. colour |
|-------|------------------|--------------------|----------------|
| 0 | `144` | `BLACK` | black |
| 1 | `5` | `WHITE` | white |
| 2 | `28` | `RED` | red |
| 3 | `159` | `CYAN` | cyan |
| 4 | `156` | `PURPLE` | purple |
| 5 | `30` | `GREEN` | green |
| 6 | `31` | `BLUE` | blue |
| 7 | `158` | `YELLOW` | yellow |
| 8 | `129` | `ORANGE` | orange |
| 9 | `149` | `BROWN` | brown |
| 10 | `150` | `PINK`, light red | light red |
| 11 | `151` | `GRAY1`/`GREY1` | dark gray |
| 12 | `152` | `GRAY2`/`GREY2` | medium gray |
| 13 | `153` | `LIGHTGREEN` | light green |
| 14 | `154` | `LIGHTBLUE` | light blue |
| 15 | `155` | `GRAY3`/`GREY3` | light gray |

---

## Brace tokens in string literals

Inside **double-quoted strings**, **`{NAME}`** or **`{number}`** expands **at load time** into the same effect as inserting **`CHR$(…)`** sequences — so **`PRINT "{RED}HI"`** behaves like printing the PETSCII colour code and then **`HI`**.

- **Numeric forms**: **`{147}`**, **`{$93}`**, **`{0x93}`**, **`{%10010011}`** (decimal / hex / binary).
- **Named**: colours, **`{HOME}`**, **`{CLR}`**, **`{DOWN}`**, cursor keys, **`{RVS}`** / **`{RVS OFF}`**, **`{F1}`**…**`{F8}`**, **`{PI}`**, **`{RESET}`** / **`{DEFAULT}`** (ANSI reset in terminal), etc.

Full token tables: **[c64-color-codes.md](https://github.com/omiq/rgc-basic/blob/main/docs/c64-color-codes.md)** in the **rgc-basic** repo.

---

## Cursor and coordinates

| Statement | Behaviour |
|-----------|-----------|
| **`LOCATE col, row`** | Move cursor **without** printing. **0-based** **`col`**, **`row`**. Implemented as ANSI **`ESC[row+1;col+1H`**. |
| **`TEXTAT col, row, expr$`** | Move to **`(col,row)`** and print the string expression. |
| **`CURSOR ON`** / **`CURSOR OFF`** | Show/hide caret (**`ESC [ ?25 h/l`**). |

**Tip:** After the program exits, the shell may print a prompt and scroll. If your last line matters, **move the cursor** off the bottom row before **`END`** (e.g. **`LOCATE 0, 22`** and a “press key” line).

---

## Input: `GET`, `INPUT`, `INKEY$()`

| Mechanism | Terminal `basic` |
|-----------|------------------|
| **`INPUT`** | Line-oriented from **stdin** (works with **pipes** / redirects). |
| **`GET`** | **Non-blocking** one character into a string var; **`""`** if none. Enter = **`CHR$(13)`**. |
| **`INKEY$()`** | **Always returns `""`** in the normal terminal build — there is no non-blocking key queue. Use **`basic-gfx`** or **WASM** for **`INKEY$`**. |

---

## Shell scripting

| Topic | Behaviour |
|-------|-----------|
| **Pipes** | `echo 42 \| ./basic prog.bas` — **`INPUT`** reads the pipe. |
| **Redirect** | `./basic prog.bas > out.txt` — **`PRINT`** to file. |
| **Stderr** | Errors and usage go to **stderr**; **`PRINT`** stays on **stdout** when redirected. |
| **Arguments** | `./basic script.bas a b` → **`ARG$(0)`** = script path, **`ARG$(1)`**…**`ARG$(ARGC())`** = args. |
| **`SYSTEM` / `EXEC$`** | Full shell access on native OS (see [Language reference](language.md#scripting-and-shell-native-os)). |
| **Errors** | Runtime errors include **line number** and often a **`Hint:`** line. Load-time errors (bad **`#INCLUDE`**, duplicate lines, etc.) print before execution. |

Examples in the repo (also in the IDE preset): **`examples/scripting.bas`** — [Web IDE](https://ide.retrogamecoders.com/?file=scripting.bas&platform=rgc-basic); PETSCII / brace tokens — [petscii-data.bas](https://ide.retrogamecoders.com/?file=petscii-data.bas&platform=rgc-basic), [c64_control_codes_demo.bas](https://ide.retrogamecoders.com/?file=c64_control_codes_demo.bas&platform=rgc-basic).

---

## `POKE` / `PEEK` in the terminal build

- **`POKE`** is accepted but is a **no-op** (compatibility with old listings).
- **`PEEK(n)`** returns **0**.

Use **`basic-gfx`** for **virtual** screen RAM and real **`POKE`/`PEEK`** (see [Graphics](graphics-raylib.md)).

---

## See also

- [Language reference](language.md) — all statements and functions
- [Install & platforms](install.md) — binaries and builds
- [Graphics (Raylib)](graphics-raylib.md) — Raylib window, **`INKEY$`**, **`TI`**
- [Web IDE](web-ide.md) — WASM, **`HTTP$`**

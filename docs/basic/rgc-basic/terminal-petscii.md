# RGC BASIC — terminal interpreter & PETSCII

The **`basic`** binary (Linux/macOS/WSL: `./basic`, Windows: `basic.exe`) runs programs from a file with **stdin/stdout** semantics: `PRINT` goes to standard output, `INPUT` reads a line from standard input. That makes it ideal for **scripting**, pipes, and quick tools — plus optional **PETSCII→ANSI** translation so C64-style control codes look right in a modern terminal.

## Basic invocation

```bash
./basic hello.bas
basic.exe hello.bas
```

With no filename, the interpreter prints **usage** text to stderr.

## Command-line options (terminal)

| Flag | Effect |
|------|--------|
| `-petscii` / `--petscii` | Map `CHR$` control/colour codes to **ANSI**; printable PETSCII to Unicode (block graphics, symbols). |
| `-petscii-plain` / `--petscii-plain` | PETSCII without ANSI — controls invisible (alignment for `.seq`-style dumps). |
| `-charset upper\|lower` | Upper/graphics vs lower/upper character set for PETSCII output. |
| `-palette ansi\|c64` | How colours map (ANSI 16-colour vs 256-colour “C64-like” indices). |
| `-maxstr N` | Max string length (default large; use `255` for C64-like limits). |
| `-columns N` | Print width (default **40**; use **80** for wide listing). |
| `-nowrap` | Do not wrap at column width — let the terminal wrap. |

Same options can be set in source with **`#OPTION`** (see [Language reference](language.md)).

## PETSCII in the terminal

In **`-petscii`** mode, common **`CHR$`** values move the cursor, set colours, clear the screen, etc., mapped to ANSI escape sequences. Printable PETSCII codes map to Unicode so block graphics and icons display in UTF-8 terminals.

**`COLOR n` / `BACKGROUND n` / `COLOUR n`** — Use C64-style indices **0–15**; the interpreter maps them to ANSI foreground/background.

**`LOCATE col, row` / `TEXTAT col, row, text`** — **0-based** coordinates; implemented via ANSI cursor positioning.

**Cursor:** `CURSOR ON` / `CURSOR OFF` toggles visibility with ANSI codes.

### Keeping the last line visible

Terminals often scroll when the shell returns. If your UI ends on the **bottom row**, scroll or the prompt can push it away — **end by moving the cursor** (e.g. `LOCATE 0, 22` then `PRINT` a prompt) so the layout stays readable. (See upstream README “Keeping final text visible”.)

## Shell scripting

| Feature | Use |
|---------|-----|
| **Pipes** | `echo 42 \| ./basic prog.bas` — `INPUT` reads stdin. |
| **Redirect** | `./basic prog.bas > out.txt` |
| **Arguments** | `./basic script.bas a b` → `ARG$(0)` script path, `ARG$(1)`…`ARG$(ARGC())` args, `ARGC()` = count after script. |
| **Shell** | `SYSTEM("cmd")` — exit status; `EXEC$("cmd")` — capture stdout (length-capped). |
| **Errors** | Runtime errors on **stderr** with line number; many include a **`Hint:`** line. |

Example patterns live in **`examples/scripting.bas`** in the repo.

## `POKE` in terminal build

`POKE` is accepted as a **no-op** for compatibility with old listings; it does not modify real process memory. Use **`basic-gfx`** for virtual **screen RAM** and hardware-style addresses (see [Graphics](graphics-raylib.md)).

## See also

- [Install & platforms](install.md)
- [Language reference](language.md)
- [Graphics (Raylib)](graphics-raylib.md) — where `POKE`/`PEEK` matter
- [Web IDE](web-ide.md)

# TRSE (Turbo Rascal)

**TRSE** (Turbo Rascal Syntax Error) is a desktop IDE and compiler for 8-bit (and more) systems, created by Geir Straume. Programs are written in **Turbo Rascal** — a clean, Pascal-flavoured language that compiles directly to native machine code for your target platform.

!!! note "Desktop app"
    This section covers the **TRSE desktop IDE**. The browser-based web IDE at [ide.retrogamecoders.com](https://ide.retrogamecoders.com) is a separate tool — see [Getting started with the IDE](../ide/getting-started.md) for that.

## In this section

- **[The TRSE language](language.md)** — syntax, types, procedures, directives, and a minimal game loop. Start here if you're new to Turbo Rascal.
- **[Methods (reference)](reference/methods-index.md)** — complete listing of all built-in methods with parameters and platform compatibility, generated from the TRSE source.
- **[How the reference is generated](help-import.md)** — sources, regeneration script, and maintenance notes.

## Quick overview

TRSE programs are `.ras` files; reusable libraries are `.tru` unit files. A minimal program looks like:

```pascal
program HelloWorld;
@use "screen/screen"
var
    i : byte;
begin
    Screen::Clear(#Screen::screen0, key_space);
    Screen::PrintString(cstring("HELLO WORLD"), 10, 12, #Screen::screen0);
    while (true) do
        Screen::WaitForVerticalBlank();
end.
```

See **[The TRSE language](language.md)** for a full walkthrough.



The main TRSE project lives at **[github.com/leuat/TRSE](https://github.com/leuat/TRSE)** — tutorials, examples, and the full source are there.

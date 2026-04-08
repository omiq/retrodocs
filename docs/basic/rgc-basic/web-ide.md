# RGC BASIC — Web IDE (WASM)

The [Retro Game Coders IDE](https://ide.retrogamecoders.com/) embeds the RGC BASIC interpreter as **WebAssembly**. You get the same language in the browser: edit, build, and see output in the IDE without installing native binaries.

## Open the platform

1. In the IDE, choose the **RGC BASIC** platform from the platform selector, **or**
2. Use a direct link with query parameters:

**[ide.retrogamecoders.com/?platform=rgc-basic&file=petscii-data.bas](https://ide.retrogamecoders.com/?platform=rgc-basic&file=petscii-data.bas)**

- `platform=rgc-basic` selects the WASM toolchain.
- `file=` loads a starter example if that file exists in the project (change the name to try other samples).

## Behaviour notes

- **Output** — Runtime messages, errors, and `PRINT` output appear in the IDE’s output / console area (same family of diagnostics as the native interpreter: line numbers and `Hint:` lines where implemented).
- **Keyboard** — For programs that use `GET` / `INKEY$`, **click the emulator or canvas area first** so the browser sends key events to the interpreter. This matches the note in [Getting started with the IDE](../../ide/getting-started.md).
- **Gfx-oriented features** — The WASM build tracks the native **graphics** surface feature set where the canvas host implements them (virtual memory, sprites, scroll — see upstream README for the exact WASM/canvas parity list). When in doubt, compare with **`basic-gfx`** on your machine.

## When to use IDE vs native

| Situation | Prefer |
|-----------|--------|
| Teaching, sharing a link, no install | **Web IDE** |
| Pipes, `SYSTEM`, heavy file paths, automation | **Terminal `basic`** on your OS |
| Full Raylib window, local PNG paths, gamepad | **`basic-gfx`** locally |

## See also

- [Overview](../rgc-basic.md)
- [Install & platforms](install.md) — native binaries
- [Graphics (Raylib)](graphics-raylib.md) — what `basic-gfx` adds on desktop
- [IDE getting started](../../ide/getting-started.md)

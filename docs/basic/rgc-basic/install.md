# RGC BASIC — install & platforms

## Prebuilt binaries (recommended)

Official builds for **Windows, macOS, and Linux** are attached to GitHub **Releases**:

- **[Latest release](https://github.com/omiq/rgc-basic/releases/)** — versioned builds (e.g. **1.5.x**).
- **[Nightly](https://github.com/omiq/rgc-basic/releases/tag/nightly)** — built automatically from **`main`** each night.

Each archive typically includes:

| Binary | Role |
|--------|------|
| **`basic`** / **`basic.exe`** | **Terminal** interpreter — stdin/stdout, **`SYSTEM`**, PETSCII flags |
| **`basic-gfx`** / **`basic-gfx.exe`** | **Graphical** interpreter — Raylib window, **`POKE`/`PEEK`**, sprites, gamepad |
| **`examples/`** | Sample **`.bas`** files |

Extract the archive and run from a terminal or Explorer/Finder:

```bash
./basic examples/trek.bas
./basic-gfx -petscii examples/gfx_colaburger_viewer.bas
```

**Web IDE** (same **`.bas`** names as the IDE preset): [trek.bas](https://ide.retrogamecoders.com/?file=trek.bas&platform=rgc-basic) · [gfx_colaburger_viewer.bas](https://ide.retrogamecoders.com/?file=gfx_colaburger_viewer.bas&platform=rgc-basic)

On Windows use **`basic.exe`** / **`basic-gfx.exe`** and path separators as usual.

---

## Build from source

Clone **[github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic)** and use the **`Makefile`**. You need a **C99** toolchain.

```bash
git clone https://github.com/omiq/rgc-basic.git
cd rgc-basic
make              # terminal interpreter: basic (or basic.exe on Windows)
make basic-gfx    # requires Raylib (headers + lib) — see repo README
```

### Common `make` targets (upstream)

| Target | Output (typical) |
|--------|------------------|
| **`make`** | **`basic`** (terminal) |
| **`make basic-gfx`** | **`basic-gfx`** (Raylib) |
| **`make basic-wasm`** | **`web/basic.js`**, **`web/basic.wasm`** (Emscripten / emsdk) |
| **`make basic-wasm-canvas`** | Canvas PETSCII + gfx-oriented features (**`web/canvas.html`**, etc.) |
| **`make basic-wasm-modular`** | Modular WASM for embedded tutorial (**`tutorial-embedding.md`**) |
| **`make clean`** | Clean build artifacts |

**Raylib:** Install per OS (**`brew install raylib`** on macOS, distro packages or source build on Linux, bundled DLLs often ship with Windows release zips). Full dependency notes: **[README — Building](https://github.com/omiq/rgc-basic/blob/main/README.md#-building-from-source)**.

**Emscripten:** Use **emsdk** current SDK — avoid stale distro **`apt install emscripten`** for this project (upstream warns builds may not match CI). After toolchain changes: **`make clean`** and rebuild **`.js` + `.wasm` together**.

---

## macOS Gatekeeper (unsigned binaries)

Downloaded binaries may be blocked until allowed:

1. **Finder:** Control-click the binary → **Open** → confirm once.
2. **System Settings → Privacy & Security:** **Open Anyway** when listed.
3. **Terminal:** `xattr -d com.apple.quarantine /path/to/basic` (one-time).

---

## What runs where

| Platform | **`basic`** (terminal) | **`basic-gfx`** (Raylib) |
|----------|------------------------|---------------------------|
| Linux | Yes | Yes |
| macOS | Yes | Yes |
| Windows | Yes | Yes |
| Browser | [Web IDE](web-ide.md) WASM | Canvas host — see [Graphics](graphics-raylib.md) + upstream **`gfx-canvas-parity.md` |

Use **`PLATFORM$()`** in a program to see the host string (**`browser`** in WASM, **`linux-gfx`**, etc. — see [Web IDE](web-ide.md#platform-and-capabilities)).

---

## See also

- [Overview](../rgc-basic.md) — what RGC BASIC is
- [Language reference](language.md) — full API
- [Terminal & PETSCII](terminal-petscii.md) — CLI flags
- [Graphics (Raylib)](graphics-raylib.md) — **`basic-gfx`**
- [Web IDE](web-ide.md) — browser build

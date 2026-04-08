# RGC BASIC — install & platforms

## Prebuilt binaries (recommended)

Official builds for **Windows, macOS, and Linux** are attached to GitHub **Releases**:

- **[Latest release](https://github.com/omiq/rgc-basic/releases/)** — versioned builds (e.g. **1.5.0**).
- **[Nightly](https://github.com/omiq/rgc-basic/releases/tag/nightly)** — built automatically from `main` every night; use if you need the newest fixes.

Each archive typically includes:

| Binary | Role |
|--------|------|
| `basic` / `basic.exe` | **Terminal** interpreter — stdin/stdout, scripting, PETSCII flags |
| `basic-gfx` / `basic-gfx.exe` | **Graphical** interpreter — Raylib window, `POKE`/`PEEK`, sprites |
| `examples/` | Sample `.bas` files |

Extract the archive and run from a terminal or Explorer/Finder:

```bash
./basic examples/trek.bas
./basic-gfx -petscii examples/gfx_colaburger_viewer.bas
```

Paths shown are Unix-style; on Windows use `basic.exe` and backslashes as needed.

## Build from source

Clone [github.com/omiq/rgc-basic](https://github.com/omiq/rgc-basic) and use the project `Makefile`. You need a C toolchain; **graphics** requires **Raylib** installed so the `basic-gfx` target can link.

```bash
git clone https://github.com/omiq/rgc-basic.git
cd rgc-basic
make          # terminal interpreter
make basic-gfx   # after Raylib is available — see repo README for platform notes
```

Upstream `README.md` has the full matrix (dependencies per OS, Visual Studio, etc.).

## macOS Gatekeeper (unsigned binaries)

Downloaded binaries may be blocked until you allow them. Typical approaches:

1. **Finder:** Control-click the binary → **Open** → confirm once.
2. **Settings → Privacy & Security:** use **Open Anyway** when macOS lists the blocked app.
3. **Terminal (one-time):** `xattr -d com.apple.quarantine /path/to/basic`

This is normal for unsigned open-source tools.

## What runs where

| Platform | `basic` (terminal) | `basic-gfx` (Raylib) |
|----------|--------------------|----------------------|
| Linux | Yes | Yes |
| macOS | Yes | Yes |
| Windows | Yes | Yes |
| Browser (IDE) | N/A — use [Web IDE](web-ide.md) WASM build | Canvas host implements gfx-oriented features |

Use `PLATFORM$()` in a program to see how the interpreter classifies the host (e.g. `linux-terminal`, `windows-gfx`).

## See also

- [Overview](../rgc-basic.md) — what RGC BASIC is
- [Terminal & PETSCII](terminal-petscii.md) — CLI flags and PETSCII mode
- [Graphics (Raylib)](graphics-raylib.md) — `basic-gfx` features

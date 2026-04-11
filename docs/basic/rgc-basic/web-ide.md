# RGC BASIC — Web IDE (WASM)

The [Retro Game Coders IDE](https://ide.retrogamecoders.com/) embeds the RGC BASIC interpreter as **WebAssembly**. You get the same language in the browser: edit, run, and share without installing native binaries.

---

## Opening the platform

1. In the IDE, choose **RGC BASIC** from the platform selector, **or**
2. Use a direct link with query parameters, for example:

**[ide.retrogamecoders.com/?file=petscii-data.bas&platform=rgc-basic](https://ide.retrogamecoders.com/?file=petscii-data.bas&platform=rgc-basic)**

- **`platform=rgc-basic`** selects the WASM toolchain.
- **`file=`** is the **basename** of a program bundled with the **RGC BASIC** preset in the IDE (same filenames as in the **rgc-basic** repo’s `examples/` tree, e.g. `gfx_poke_demo.bas`, `trek.bas`). Pattern: `https://ide.retrogamecoders.com/?file=<name>.bas&platform=rgc-basic`

Documentation links **Web IDE** next to an example only when that **`*.bas`** ships in the IDE preset (the **8bitworkshop** `presets/rgc-basic/` package).

---

## Output and diagnostics

- **`PRINT`** output, runtime errors, and load-time errors appear in the IDE output / console area.
- Messages follow the same style as native builds where implemented: **BASIC line numbers** and **`Hint:`** suggestions.

---

## Keyboard and focus

For programs using **`GET`**, **`INKEY$`**, or **`INPUT`** in a canvas / embedded view, **click the emulator or canvas first** so the browser routes key events to the interpreter. This matches [Getting started with the IDE](../../ide/getting-started.md).

---

## Platform and capabilities

**`PLATFORM$()`** in Emscripten builds returns **`"browser"`** (not the `linux-terminal`-style strings used on native OS). Native builds return **`linux-terminal`**, **`mac-terminal`**, **`windows-terminal`**, or **`windows-gfx`** / **`linux-gfx`** / **`mac-gfx`** when linked with gfx.

### What works in the browser

| Feature | WASM (typical) |
|---------|------------------|
| Core BASIC, files in virtual FS (where exposed) | Yes |
| **`HTTP$` / `HTTPSTATUS()`** | Yes — **`fetch`** (see below) |
| **`SYSTEM` / `EXEC$`** | **Stubbed** — **`SYSTEM`** returns **-1**, **`EXEC$`** returns **`""`** |
| **`INKEY$()`**, **`GET`** | Yes when the host wires keyboard (IDE / canvas) |
| Gfx / canvas (PETSCII, bitmap, sprites) | When the page uses the **canvas** host — parity with **`basic-gfx`** is documented upstream (**`docs/gfx-canvas-parity.md`**). |

---

## `HTTP$` and `HTTPSTATUS`

**Browser-only** (Emscripten). On native **`basic`**, **`HTTP$`** returns **`""`** and **`HTTPSTATUS()`** returns **0** — use **`EXEC$("curl …")`** instead.

### Syntax

```text
HTTP$(url$ [, method$ [, body$]])
```

- **`url$`** — HTTPS URL (must allow **CORS** from your page’s origin).
- **`method$`** — Optional; e.g. **`"GET"`**, **`"POST"`**. Omit for default GET-like behaviour (see upstream).
- **`body$`** — Optional request body for POST/PUT.

**`HTTP(url)`** without **`$`** is treated as a call to the same intrinsic as **`HTTP$`** (so **`HTTP`** is not mistaken for a user function named **`HTTP`**).

**`HTTPSTATUS()`** — No arguments. Returns the **HTTP status code** of the **last** **`HTTP$`** call, or **0** on failure / non-WASM.

### CORS

The remote API must send **Cross-Origin Resource Sharing** headers that allow your IDE origin. If the request fails, status may be **0** and the body empty — test in browser devtools Network tab.

### Example

**`examples/http_time_london.bas`** in the repo fetches a public time API ([open in Web IDE](https://ide.retrogamecoders.com/?file=http_time_london.bas&platform=rgc-basic)):

```basic
U$ = "https://timeapi.io/api/TimeZone/zone?timeZone=Europe/London"
R$ = HTTP$(U$)
IF HTTPSTATUS() <> 200 THEN PRINT "HTTP error "; HTTPSTATUS(): END
```

---

## Async / responsiveness

The upstream README notes that **WASM** uses **`emscripten_sleep`** so the tab can paint; **tight loops** without **`SLEEP`** or output can still make the browser report “Page Unresponsive” where **`basic-gfx`** feels fine. Prefer periodic **`SLEEP`**, or split work — see **`docs/gfx-canvas-parity.md`** and **`examples/wasm_canvas_hang_probe.bas`** ([Web IDE](https://ide.retrogamecoders.com/?file=wasm_canvas_hang_probe.bas&platform=rgc-basic)).

---

## Builds in the repo (for contributors)

From **rgc-basic** (see upstream **README**):

- **`make basic-wasm`** — Terminal WASM (`web/basic.js`, `web/basic.wasm`).
- **`make basic-wasm-canvas`** — Canvas + PETSCII / bitmap / sprites (`web/canvas.html`, etc.).
- **`make basic-wasm-modular`** — For embedded tutorial pages.

Serve **`web/`** over HTTP and open **`canvas.html`** or **`tutorial.html`** as documented in **`web/README.md`**.

---

## When to use IDE vs native

| Situation | Prefer |
|-----------|--------|
| Teaching, sharing a link, no install | **Web IDE** |
| Pipes, **`SYSTEM`**, local paths, automation | **Terminal `basic`** |
| Full Raylib window, local PNGs, gamepad | **`basic-gfx`** |

---

## See also

- [Overview](../rgc-basic.md)
- [Install & platforms](install.md) — native binaries
- [Language reference](language.md) — **`HTTP$`**, **`PLATFORM$`**
- [Graphics (Raylib)](graphics-raylib.md) — desktop gfx; canvas parity notes
- [IDE getting started](../../ide/getting-started.md)

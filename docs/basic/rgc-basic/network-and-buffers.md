# RGC BASIC — network and buffers

Three layers of HTTP support, picked by what you want to do with the response:

| Use case | API | Why |
|----------|-----|-----|
| Small JSON / text response (≤ 4 KB) | `HTTP$()` | One-call simplicity, returns a string |
| Save response as a file by path | `HTTPFETCH()` | One call, no slot bookkeeping, lets `LOADSCREEN` / `OPEN` consume the file |
| Stream a large / binary response, walk byte-by-byte | `BUFFER*` | The interpreter manages a temp file slot you can `OPEN` / `GETBYTE` |

All three honour CORS — the remote endpoint must allow your IDE origin. Set `HTTPSTATUS()` after every call. Native `basic` (no gfx) returns `""` / `0` / writes nothing — this whole subsystem requires `basic-gfx`, `basic-wasm-raylib`, or browser WASM.

---

## 1. `HTTP$` — string response (small)

### `HTTP$(url$ [, method$ [, body$]])`

- **Purpose**: HTTP fetch; returns response body as a string. Capped at `#OPTION maxstr` (default large, but ≤ **4096 bytes**) — anything longer is truncated.
- **Parameters**:
  - `url$` — full URL.
  - `method$` — optional, default `"GET"`. `"POST"`, `"PUT"`, `"DELETE"`, etc.
  - `body$` — optional request body for POST/PUT.
- **Returns**: string. `""` on failure.
- **Example**:
  ```basic
  R$ = HTTP$("https://timeapi.io/api/TimeZone/zone?timeZone=Europe/London")
  IF HTTPSTATUS() <> 200 THEN PRINT "ERR "; HTTPSTATUS() : END
  PRINT R$
  ```

### `HTTPSTATUS()`

- **Purpose**: HTTP status of the most recent `HTTP$` / `HTTPFETCH` / `BUFFERFETCH` call.
- **Parameters**: none.
- **Returns**: numeric status code (200, 404, 500, …); **0** on network failure / non-WASM.
- **Example**:
  ```basic
  R$ = HTTP$(U$)
  IF HTTPSTATUS() = 0 THEN PRINT "NETWORK DOWN" : END
  IF HTTPSTATUS() >= 400 THEN PRINT "HTTP "; HTTPSTATUS() : END
  ```

### Aliasing — `HTTP(url)` without `$`

Calling `HTTP(url)` (no `$`) tokenises to the same intrinsic. Lets BASIC users who don't yet know about the `$` convention type `R$ = HTTP(U$)` and have it work — the parser disambiguates so `HTTP` alone never resolves to a user-defined function called `HTTP`.

---

## 2. `HTTPFETCH` — one-shot HTTP-to-file

When you already know the destination path:

### `HTTPFETCH(url$, path$ [, method$ [, body$]])`

- **Purpose**: fetch `url$` and write the body to `path$` directly (no slot allocation). Bypasses the `HTTP$` 4 KB string cap.
- **Parameters**:
  - `url$` — full URL.
  - `path$` — destination file path. **Browser WASM** writes to MEMFS — pair with `DOWNLOAD path$` if you want a real file. **Native** writes to disk.
  - `method$`, `body$` — optional, same as `HTTP$`.
- **Returns**: numeric — non-zero on success, 0 on failure. Also sets `HTTPSTATUS()`.
- **Example**:
  ```basic
  IF HTTPFETCH("https://example.com/sky.png", "sky.png") THEN
    LOADSCREEN "sky.png"
  ELSE
    PRINT "FETCH FAILED, STATUS "; HTTPSTATUS()
  END IF
  ```

Useful when the next thing the program does is open the path with another statement that takes a path argument: `LOADSCREEN`, `IMAGE LOAD`, `LOADSPRITE`, `LOADSOUND`, `LOADMUSIC`, `MAPLOAD`, `OPEN`.

---

## 3. `BUFFER*` — slot-based file-backed HTTP

When you don't want to choose the path, or you're going to do significant streaming work over the response. The interpreter manages 16 slots (0..15) each backed by a temp file it cleans up on exit.

### `BUFFERNEW slot`

- **Purpose**: allocate the slot — creates an empty backing file. Idempotent: re-calling on a used slot wipes the prior occupant.
- **Parameters**: `slot` — 0..15.
- **Returns**: nothing.
- **Example**: `BUFFERNEW 0`

### `BUFFERFETCH slot, url$ [, method$ [, body$]]`

- **Purpose**: HTTP fetch into the slot's backing file. The body lands in the file, regardless of size — no 4 KB cap.
- **Parameters**:
  - `slot` — must have been `BUFFERNEW`'d.
  - `url$` — full URL.
  - `method$`, `body$` — optional.
- **Returns**: nothing. Sets `HTTPSTATUS()`.
- **Example**: `BUFFERFETCH 0, "https://api.example.com/big.json"`

### `BUFFERFREE slot`

- **Purpose**: unlink the backing file and release the slot. Safe to call on an empty slot.
- **Parameters**: `slot` — 0..15.
- **Returns**: nothing.

### `BUFFERLEN(slot)`

- **Purpose**: byte length of the slot's backing file (i.e., how much was downloaded).
- **Parameters**: `slot`.
- **Returns**: numeric. **0** if slot empty / unallocated.
- **Example**: `IF BUFFERLEN(0) = 0 THEN PRINT "EMPTY RESPONSE" : END`

### `BUFFERPATH$(slot)`

- **Purpose**: filesystem path of the slot's backing file. Pass to **any** path-taking statement: `OPEN`, `IMAGE LOAD`, `LOADSCREEN`, `LOADSPRITE`, `LOADSOUND`, `MAPLOAD`, etc.
- **Parameters**: `slot`.
- **Returns**: string path. `""` if slot empty.
- **Example**: `OPEN 1, 1, 0, BUFFERPATH$(0)`

---

## 4. Worked example — find a string in a 100 KB response

`HTTP$` truncates the response at 4 KB. To search a large endpoint, fetch into a buffer slot and walk byte-by-byte:

```basic
BUFFERNEW 0
BUFFERFETCH 0, "https://api.example.com/data"
PRINT "STATUS "; HTTPSTATUS(); ", "; BUFFERLEN(0); " BYTES"

TARGET$ = "CollectionDay"
TLEN = LEN(TARGET$)
WINDOW$ = STRING$(TLEN, 32)            ' pre-fill with spaces
FOUND = 0 : BYTES = 0

OPEN 1, 1, 0, BUFFERPATH$(0)
DO
  GETBYTE #1, B
  IF B = -1 THEN EXIT                  ' EOF
  BYTES = BYTES + 1
  WINDOW$ = RIGHT$(WINDOW$, TLEN - 1) + CHR$(B)
  IF WINDOW$ = TARGET$ THEN FOUND = 1 : EXIT
LOOP
CLOSE 1

IF FOUND THEN PRINT "FOUND AT "; BYTES ELSE PRINT "NOT FOUND"
BUFFERFREE 0
```

Demo: `examples/buffer_http_demo.bas`.

---

## 5. Worked example — stream a binary asset

Pull a PNG out of an API and use it directly:

```basic
BUFFERNEW 0
BUFFERFETCH 0, "https://example.com/api/sprite/42.png"
IF HTTPSTATUS() = 200 THEN
  SCREEN 1
  SPRITE LOAD 0, BUFFERPATH$(0)
  DO
    SPRITE DRAW 0, 160, 100
    VSYNC
    IF KEYDOWN(ASC("Q")) THEN EXIT
  LOOP
END IF
BUFFERFREE 0
```

The same pattern works with `LOADSCREEN` (PNG → screen plane), `LOADSOUND` (WAV), `LOADMUSIC` (MOD/XM/S3M/IT/OGG/MP3), `MAPLOAD` (JSON tilemap), `IMAGE LOAD` (PNG to off-screen blitter).

---

## 6. Binary file I/O — `PUTBYTE` / `GETBYTE`

Once a file exists (downloaded into a buffer, written by `IMAGE SAVE`, or any other route), you can read or write it byte-by-byte.

### `OPEN lfn, device, secondary, "filename"`

CBM-style — covered in [language.md — File I/O](language.md#file-io-cbm-style). Recap:

- **`device`** = `1` for host files.
- **`secondary`** = `0` read, `1` write, `2` append.
- **`lfn`** = logical file number (1..255), used in subsequent calls.

### `PUTBYTE #lfn, byte_expr`

- **Purpose**: write one byte (0..255) to an open channel.
- **Parameters**: `lfn`, byte expression (masked with `& 255`).
- **Returns**: nothing. Sets `ST = 0` on success, `ST = 1` if the channel isn't open or the write failed.
- **Example**:
  ```basic
  OPEN 2, 1, 1, "out.bin"
  FOR I = 0 TO 255 : PUTBYTE #2, I : NEXT I
  CLOSE 2
  ```

### `GETBYTE #lfn, var`

- **Purpose**: read one byte from an open channel into a numeric scalar.
- **Parameters**: `lfn`, target numeric variable (not array, not string).
- **Returns**: nothing. Sets `var` to 0..255 on success, **-1** at EOF or on error. Sets `ST = 0` / `64` / `1` (success / EOF / not-open).
- **Example**:
  ```basic
  OPEN 1, 1, 0, "in.bin"
  DO
    GETBYTE #1, B
    IF B = -1 THEN EXIT
    PRINT HEX$(B); " ";
  LOOP
  CLOSE 1
  ```

### `EOF(lfn)` (alternate end-of-file probe)

- **Purpose**: check whether the next read would hit end-of-file on the channel.
- **Parameters**: `lfn`.
- **Returns**: 1 at EOF, 0 otherwise.
- **Example**: `DO WHILE NOT EOF(1) : GETBYTE #1, B : … : LOOP`

---

## 7. CORS, errors, browser specifics

| Issue | Symptom | Fix |
|-------|---------|-----|
| CORS not allowed | `HTTPSTATUS() = 0`, body empty | Test in browser DevTools Network tab. Endpoint must send `Access-Control-Allow-Origin` covering your IDE origin. |
| Asset auto-preload missed it | 404 in browser even though the file is bundled | The IDE scans `LOADSCREEN "lit.png"` literals; a variable form (`F$ = "x.png" : LOADSCREEN F$`) won't be staged into MEMFS. Use a literal — or use `BUFFERFETCH` / `HTTPFETCH` to download at runtime. |
| Native build silent | All HTTP calls return `""` / `0` | Plain `basic` has no HTTP. Use `basic-gfx`, `basic-wasm-raylib`, or run the program in the Web IDE. |
| First audio fetch hangs in the browser | Browser autoplay policy | `LOADSOUND` / `LOADMUSIC` first call must follow a user gesture (`KEYPRESS` / `ISMOUSEBUTTONPRESSED`). |
| `BUFFERFETCH` returns instantly with status 0 | Pre-WASM run | The fetch is async — `BUFFERFETCH` blocks via `emscripten_sleep` so by the time it returns `HTTPSTATUS()` is set. If you see 0, the request never reached the network — check the URL and CORS. |

---

## 8. See also

- [Web IDE — `HTTP$`](web-ide.md#http-and-httpstatus) — IDE-specific notes.
- [Language reference — File I/O](language.md#file-io-cbm-style) — `OPEN` / `PRINT#` / `INPUT#` / `GET#`.
- [`examples/buffer_http_demo.bas`](https://github.com/omiq/rgc-basic/blob/main/examples/buffer_http_demo.bas) — sliding-window string search.
- [`examples/http_time_london.bas`](https://github.com/omiq/rgc-basic/blob/main/examples/http_time_london.bas) — minimal `HTTP$` demo.

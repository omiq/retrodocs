# RGC BASIC — authoring levels (`MAPLOAD` vs BASIC builder)

RGC BASIC ships two ways to load a tile-based level into the
maplib `MAP_*` globals:

1. **JSON map files** loaded at runtime by `MAPLOAD path$`
   (canonical, v1.1+).
2. **BASIC builder functions** that fill `MAP_BG()`, `MAP_OBJ_*()`
   etc. by hand (the v0 approach the Zelda-lite MVP shipped with).

Both end up in the same place — the `MAP_*` globals — so the
runtime engine, collision, camera, and rendering code is identical.
The difference is **where the level data lives**: an external,
diffable JSON file, or a `FUNCTION` of `FOR`/`MAP_BG(…)=…`
assignments inline with your game code.

This page shows both, and explains when each wins.

## Quick comparison

|                          | BASIC builder         | JSON + `MAPLOAD`            |
|--------------------------|-----------------------|-----------------------------|
| Edit in any text tool    | yes                   | yes                         |
| Diff cleanly in git      | yes (mostly)          | yes                         |
| External tools (Tiled)   | no                    | one-way import planned      |
| Procedural / RNG levels  | natural               | needs an export pass        |
| Hot-reload at runtime    | re-run program        | `MAPLOAD` again             |
| Map size limit           | 4 KB BASIC string × N | bounded by free heap        |
| Where rendering code is  | unchanged             | unchanged                   |

For *static, hand-authored* levels the JSON path is the canonical
choice from v1.1 onward. For *generated* levels (procedural caves,
seeded overworld) the BASIC builder still wins — you can run a
generator on every level entry without touching disk.

## Side by side: same overworld, two ways

Both snippets produce the same 32×32 grass-with-tree-border
overworld with a water pond, a dirt L-shaped path, sand around a
door, three rocks, and three objects (player spawn, door to cave,
NPC).

### BASIC builder (`level1_overworld.bas`)

```basic
GRASS_TILE = 1
TREE_TILE  = 563
DIRT_TILE  = 1402
SAND_TILE  = 733
WATER_TILE = 17
ROCK_TILE  = 208
DOOR_TILE  = 346

FUNCTION LoadOverworld()
  MAP_W      = 32
  MAP_H      = 32
  MAP_TILE_W = 16
  MAP_TILE_H = 16

  ' Floor every cell with grass.
  FOR I = 0 TO MAP_W * MAP_H - 1
    MAP_BG(I) = GRASS_TILE
    MAP_FG(I) = 0
  NEXT I

  ' Tree border + water pond + dirt path + sand patch + rocks
  ' (~50 more lines of FOR / MAP_BG(R*MAP_W+C) = TILE assignments) ...

  ' Solid tile id list.
  MAP_COLL_COUNT = 3
  MAP_COLL(0) = WATER_TILE
  MAP_COLL(1) = TREE_TILE
  MAP_COLL(2) = ROCK_TILE

  ' Object list.
  MAP_OBJ_COUNT = 3
  MAP_OBJ_TYPE$(0) = "spawn"
  MAP_OBJ_KIND$(0) = "player"
  MAP_OBJ_X(0) = 4 * 16
  MAP_OBJ_Y(0) = 28 * 16
  '... etc ...
END FUNCTION
```

Caller does `#INCLUDE "level1_overworld.bas"` then
`LoadOverworld()` to populate the globals.

### JSON + `MAPLOAD` (`level1_overworld.json`)

```json
{
  "format": 1,
  "id": "level1-overworld",
  "size":     { "cols": 32, "rows": 32 },
  "tileSize": { "w": 16, "h": 16 },
  "tilesets": [
    {
      "id": "overworld",
      "src": "Overworld.png",
      "cellW": 16, "cellH": 16,
      "tiles": {
        "17":  { "solid": true, "kind": "water" },
        "563": { "solid": true, "kind": "tree"  },
        "208": { "solid": true, "kind": "rock"  }
      }
    }
  ],
  "layers": [
    { "name": "bg", "type": "tiles", "tilesetId": "overworld",
      "data": [ /* 32 * 32 = 1024 ints, row-major */ ] },
    { "name": "fg", "type": "tiles", "tilesetId": "overworld",
      "data": [ /* same shape */ ] },
    { "name": "obj", "type": "objects", "objects": [
      { "id": 1, "type": "spawn", "kind": "player",
        "shape": "point", "x": 64, "y": 448 },
      { "id": 2, "type": "door",  "kind": "cave",
        "shape": "rect", "x": 256, "y": 128, "w": 16, "h": 16,
        "props": { "leadsTo": "level1-cave", "spawnAt": 1 } },
      { "id": 3, "type": "npc",   "kind": "old_man",
        "shape": "rect", "x": 128, "y": 384, "w": 16, "h": 32,
        "props": { "dialogue": "OLD MAN: TAKE THIS GUIDE TO THE CAVE." } }
    ]}
  ],
  "camera": { "start": { "x": 0, "y": 0 },
              "scrollDir": "free", "speedPxPerSec": 0,
              "mode": "follow" }
}
```

Caller does:

```basic
DIM MAP_BG(1023)
DIM MAP_FG(1023)
DIM MAP_COLL(15)
DIM MAP_OBJ_TYPE$(15) : DIM MAP_OBJ_KIND$(15)
DIM MAP_OBJ_X(15) : DIM MAP_OBJ_Y(15)
DIM MAP_OBJ_W(15) : DIM MAP_OBJ_H(15)
DIM MAP_OBJ_ID(15)
DIM MAP_TILESET_ID$(7) : DIM MAP_TILESET_SRC$(7)

MAPLOAD "level1_overworld.json"
```

The arrays are pre-DIMmed by the *caller*, not by the loader, so
the engine knows its own caps. `MAPLOAD` writes count globals
(`MAP_OBJ_COUNT`, `MAP_COLL_COUNT`, `MAP_TILESET_COUNT`) so loops
don't need a hard-coded length.

## What `MAPLOAD` populates

After a successful `MAPLOAD` call, these globals reflect the loaded
map:

| Global                          | Source field                                                                |
|---------------------------------|-----------------------------------------------------------------------------|
| `MAP_W`, `MAP_H`                | `size.cols`, `size.rows`                                                    |
| `MAP_TILE_W`, `MAP_TILE_H`      | `tileSize.w`, `tileSize.h`                                                  |
| `MAP_BG(N)`                     | layer where `name == "bg"`, `data[]` row-major                              |
| `MAP_FG(N)`                     | layer where `name == "fg"` (optional)                                       |
| `MAP_COLL_COUNT`, `MAP_COLL(N)` | every tile id whose `tilesets[*].tiles[id].solid == true`                   |
| `MAP_OBJ_COUNT`                 | total objects across object layers                                          |
| `MAP_OBJ_TYPE$/KIND$/X/Y/W/H/ID(N)` | parallel arrays per object                                              |
| `MAP_TILESET_COUNT`             | number of tilesets                                                          |
| `MAP_TILESET_ID$(N)`            | `tilesets[N].id`                                                            |
| `MAP_TILESET_SRC$(N)`           | `tilesets[N].src` — pass to `SPRITE LOAD slot, MAP_TILESET_SRC$(N), w, h`   |
| `MAP_CAM_START_X/Y`             | `camera.start.x`/`.y`                                                       |
| `MAP_CAM_SCROLL_DIR$`           | `camera.scrollDir`                                                          |
| `MAP_CAM_SPEED_PX_PER_FRAME`    | `camera.speedPxPerSec / 60` (rounded)                                       |

Schema details, including objects (`type` / `kind` / `shape` /
`props`), camera modes (`auto` / `follow` / `room`), and v1.1+
deferrals (RLE, animations, parallax, polygon shapes) are in the
[map format spec](https://github.com/omiq/rgc-basic/blob/main/docs/map-format.md).

## Migrating from a builder to JSON

The `examples/rpg/` MVP-2 game ships both. The migration was
mechanical:

1. **Generate the JSON** from the existing builder. Run a one-shot
   Python or BASIC script that imitates each `MAP_BG(R*MAP_W+C) = …`
   line, builds the same flat int array, and emits a JSON object
   alongside the source. (See `examples/rpg/level1_overworld.json`
   for the canonical output.)
2. **Drop the `#INCLUDE`** of the builder.
3. **Add the tileset DIM lines** (`MAP_TILESET_ID$`, `MAP_TILESET_SRC$`).
4. **Replace `LoadOverworld()`** with `MAPLOAD "level1_overworld.json"`.
5. **(Optional)** remove the builder `.bas` file from the runtime
   path; keep it in the repo as authoring reference, or delete it
   entirely once you trust the JSON.

Engine code (`HandleInput`, `HandleInteract`, `CheckDoor`,
`UpdateCamera`, render functions) needs **zero** changes — it
reads the same `MAP_*` globals either way.

## When the BASIC builder still wins

- **Procedural levels.** A roguelike that re-rolls the dungeon
  every run wants `RND()` and `FOR` loops, not a JSON file. Build
  the map in BASIC each time you enter a level; reach for `MAPLOAD`
  only for hand-authored set pieces.
- **Tiny maps.** A two-screen tutorial that fits in 30 lines of
  BASIC isn't worth a separate file — keep it inline.
- **Live-edit instrumentation.** If you're tuning collision flags or
  enemy placements while running, mutating BASIC variables (or
  re-running the program) can be tighter than re-saving JSON.

For everything else — overworld + dungeon room sets, shooter scroll
data, anything you'd hand to an external editor someday —
`MAPLOAD` is the canonical path.

## See also

- [`map-format.md`](https://github.com/omiq/rgc-basic/blob/main/docs/map-format.md) —
  the v1 schema spec, decision log, and v1.1+ deferral list.
- [`overlay-plane.md`](https://github.com/omiq/rgc-basic/blob/main/docs/overlay-plane.md) —
  HUD layer composited above tiles (used by the Zelda-lite MVP for
  its dialog box).
- `examples/rpg/rpg.bas` — the production user; loads two JSON
  levels, swaps tilesets, walks the same `MAP_*` arrays the v0
  shooter MVP did.

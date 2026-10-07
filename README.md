# UI/UX Pro Max

A slipwai extension: optional dev tooling a generated or adopted project can elect at `./init`.

Installs the ui-ux-pro-max skill into skills/: an offline, searchable design-system generator (styles, palettes, type pairings, chart types and UX rules by product type) a slice consults before deciding what its screen looks like. Needs a browser app.

## Installing

```sh
slipwai extension install uipro
```

Then, in a project:

```sh
./init --extension uipro
```

`./init` offers it in the extension menu too, where it was installed when the project was generated.

## What is in here

| File | What it is |
| --- | --- |
| `extension.json` | The manifest: what the catalogue shows, which keel schema it speaks, and the points it hooks |
| `init.py` | The entry point `./init --extension uipro` runs |

## The six obligations

An extension's entry point meets all six, and `slipwai extension check` says so:

1. **Idempotent** — running it twice does what running it once did.
2. **Non-fatal** — a tool it cannot install is said, not fatal.
3. **Projects** — its `AGENTS.md` block is marker-fenced and replaced whole.
4. **Gated** — state that can go stale ships a `check-uipro.py`.
5. **Recovers** — every failure path names the command that fixes it.
6. **Merges** — a hand-edited file is merged, never overwritten.

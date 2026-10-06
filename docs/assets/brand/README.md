# OpenLFCP mark

The OpenLFCP mark is an echo tick: the same check appearing a second time,
a change showing up in another place. Use these files as they are.

| File | Use |
| --- | --- |
| `openlfcp-mark.svg` | light backgrounds |
| `openlfcp-mark-dark.svg` | dark backgrounds |
| `favicon.svg` | browser tabs and other small sizes; switches to the dark tile under `prefers-color-scheme: dark` |
| `mark-256.png` | raster fallback where SVG is not accepted |

## Colours

- **#14432F**, deep taiga: the primary colour, the tile on light
  backgrounds.
- **#3A8A62**: the tile on dark backgrounds.
- White ticks: the front tick solid, the echo behind it at 45 % opacity
  (50 % on the dark tile, 55 % in the favicon, so it survives at small
  sizes).

## Rules

- Don't recolour, stretch, rotate or redraw the mark.
- Don't show it smaller than 16 px; below 32 px use `favicon.svg`.
- Spell the name "OpenLFCP".

In a README, pick the variant by colour scheme with `<picture>`:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/openlfcp/.github/main/docs/assets/brand/openlfcp-mark-dark.svg">
  <img src="https://raw.githubusercontent.com/openlfcp/.github/main/docs/assets/brand/openlfcp-mark.svg" width="64" height="64" alt="OpenLFCP">
</picture>
```

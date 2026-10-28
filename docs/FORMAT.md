# Data formats

**Cells** (`data/*-cells.txt`): one line, `x,y;x,y;...`. A cell (x, y) is the unit square [x, x+1] × [y, y+1], x to the
right, y up. Same convention as Silverstein's `data/cells.txt`.

**Outline** (`data/*-outline.svg`): the cells in light grey and the single boundary cycle as one black polygon. One grid
square is 5 mm at the nominal size, so the file prints at scale. SVG y points down.

**Folding data** (`data/*-folds.json`), read by `viewer/index.html` (the same format as Silverstein's viewer):
- `cells`: as above; `root`: the cell nearest the middle of the net.
- `boxes[]`: one entry per box, with
  - `box`: dimensions;
  - `face[i]`: face (0–5) that cell i lands on;
  - `panel[i]`: flat panel of cell i (cells on one face that touch);
  - `rootPanel`, `panels`: the panel containing `root`, number of panels;
  - `hinges[]`: `[child panel, parent panel, cell in parent, cell in child]`, a tree from `rootPanel` outward; every
    hinge turns by 90°;
  - `faceup`: the side the hinges turn to.

  The fold was replayed with exact integer rotations: every cell ends on a different unit square of the box surface.

**Series table** (`data/family.csv`): `area, p, q, c, H, m, W, boxes, note`; one row per member shown in the README.

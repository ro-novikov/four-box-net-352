# Construction of the four-box nets

The construction is the one of Reed Silverstein and Conner Silverstein
([four-box-net-532, docs/how-we-found-the-four-box-net.md](https://github.com/Sprite143/four-box-net-532/blob/main/docs/how-we-found-the-four-box-net.md)),
generalised from strip direction (2, 1) to any direction (p, q). Section 1 restates their idea; sections 2–4 are the
generalisation; section 5 gives the rule for m and the limit of two reflections per edge.

## 1. Strip, two reflection gluings per edge, four pillowcases

Start with a W × H rectangle ("precursor strip") and join its left and right edges, so positions along the strip are
taken modulo W. Glue the bottom edge to itself by the reflection x ↔ a − x (mod W) and the top edge by x ↔ b − x
(mod W). The surface obtained is flat with four corner points of total angle 180° each: a doubled rectangle, or
*pillowcase*. Its shape depends only on the shift b − a.

Allow two values on each edge, a ∈ {0, α} and b ∈ {b₁, b₂}. The four combinations give four shifts
{b₁, b₂, b₁ − α, b₂ − α}, and so four different pillowcases from one strip.

A pillowcase with sides A × B becomes a box 2 × (A − 2) × (B − 2) once each of its four corners is replaced by a small
notch (squares removed); wherever a notch of one folding lies on a fold line of another folding, the matching piece across that fold line must be a tab (squares added), so that all four foldings stay exact. Surface area: 2AB − 8.

## 2. Direction (p, q) and the lattice condition

The pillowcase is a rectangle only if its translation lattice ⟨(W, 0), (b − a, 2H)⟩ contains two perpendicular vectors
of the right size. With the strip direction (p, q), p and q coprime, p + q odd, N = p² + q², the vectors are
U = μ·(p, q) and V = ν·(−q, p) with μ = 2Hk/q, ν = 2Hl/p, and they span the lattice exactly when

    W = 2·H·N·m / (p·q),   m = k·l,   gcd(k, l) = 1.

After rotating by (p, q) and scaling by 1/√N the pillowcase sides are A = H·k/q and B = H·l/p. With H = c·p·q:

    A = c·p·k,   B = c·q·l,   box 2 × (A − 2) × (B − 2),   area 2AB − 8 = 2c²·p·q·m − 8.

A number m with exactly two distinct prime factors has four ordered factorisations m = k·l with gcd(k, l) = 1; they give the four boxes. For each factorisation the shift s = b − a is any solution of
k·s ≡ μ·p and l·s ≡ −ν·q (mod W); a, b are then chosen so that the four shifts are one per factorisation.

**Example, area 352.** (p, q) = (4, 3), N = 25, c = 1, H = 12, m = 15, W = 750. Gluings: bottom a ∈ {0, 300}, top
b ∈ {32, 282}.

The four pillowcases and boxes are listed in the README (section Construction).

**Silverstein's 532** is (p, q) = (2, 1), c = 3, H = 6, m = 15, W = 450 = 75H, the values in their write-up.

## 3. Resampling onto the grid

The precursor is rotated by (p, q) and scaled by 1/√N. A final unit square (i, j) is kept when the centre of the
square maps into the precursor:

    x = p·(i + ½) − q·(j + ½),   y = q·(i + ½) + p·(j + ½),   (x, y) inside the strip.

For 352 this gives a staircase strip of W·H/N = 360 squares = 2AB, it folds onto the four flat pillowcases, before any corner change.

## 4. Corners: nets A and B

The resampled strip folds onto the four pillowcases, not yet onto boxes. The corners are changed on the final grid:

Both nets remove 20 squares and add 12, never the same square. Net B has only domino notches and tabs (10 and 6); in
each of the four foldings the corners of the pillowcase are simply cut off, one corner square on each layer at each
corner. Net A has notches and tabs of one or two squares (16 and 10); in each folding two of the corners are formed
differently: two squares that a plain cut would remove are kept, and two squares next to them are left out.

- **Net A** (`data/net-352-a-cells.txt`): at corner points of the bottom and top gluings, small sets of squares
  are removed (notches); each removal is propagated along the fold lines of the other foldings as the rotated copy added
  on the other side (tab), then removed again, and so on, which keeps every gluing exact. Candidate shapes are tried
  near each corner point and each result is tested by a fold checker. 20 squares removed, 12 added.
- **Net B** (`data/net-352-b-cells.txt`): the same strip, with the corners found by an exact integer program. For every
  folding F of the resampled strip and every square z of its pillowcase, with x = removed and y = added squares,

      x[q_F(z)] − Σ_{y : F(y) = z} y = [z lies in one of the four corner squares of side h/2 on either sheet]

  (h = 2 here); solved with CP-SAT, then checked by the fold checkers.

**Two identical halves.** Each net is made of two identical halves: its pattern repeats after half the length of the
strip. Each reflection gluing x ↔ a − x (mod W) has two fixed points, a/2 and a/2 + W/2, so the strip, the gluings and
the corners all repeat after W/2. The 532 net of Silverstein and Silverstein has the same structure. Up to the
symmetries of the strip, nets A and B differ in 20 squares.

## 5. Notches and tabs: the rule for m, and two reflections per edge

On one long edge of the strip (a cycle of length W), take two reflections x ↦ c₁ − x and x ↦ c₂ − x with c₁, c₂ even,
so that each has two corner points, at c/2 and c/2 + W/2. Following a notch from one corner point, it alternates
notch, tab, notch, … along the chain of partners until it reaches the next corner point, which must again be a notch,
so the chain has even length. This works exactly when 2^v divides c₁ − c₂, where 2^v is the largest power of 2 that
divides W: then every chain from a corner point ends at a corner point after an even number of steps and every
closed chain has even length, so the labelling exists. In the family, the parameter sets that pass are exactly those
with m odd (checked for all 860 parameter sets in the search range).

Three reflections on one edge: the three pairwise conditions can all hold (for example W = 6, c = 0, 2, 4), but no
labelling of notches and tabs fits all three at once (proved in [multi-box-nets](https://github.com/ro-novikov/multi-box-nets),
`docs/proofs.md`, Corollary 5). The limit of two reflection gluings per edge, and with it of four boxes for one strip,
was stated by Silverstein and Silverstein in [five-box-net-2128](https://github.com/Sprite143/five-box-net-2128); for
notches and tabs it follows. For exact corner shapes (section 4) neither the rule nor the limit is proved here, and the
rule for m is then not a condition in general (`docs/proofs.md`, remark after Lemma 2). A fifth box needs a folding
that does not act on a whole edge.

#!/usr/bin/env python3
"""Check which rectangular boxes a polyomino net folds onto (grid-line folds only). Python 3 standard library only.

A net is a set of unit cells (x, y), the cell [x, x+1] x [y, y+1]. Cells that share an edge stay joined; every other
edge is cut. The net folds onto the box a x b x c iff its cells can be placed on the box surface so that every surface
square is covered exactly once and every pair of joined cells lands on two surface squares that meet along the same
box edge, consistently oriented (the paper may be turned over).

Method: put cell 0 on every surface square in each of the 8 orientations (4 rotations x 2 sides of the paper) and
propagate along the net's adjacencies by rolling a tangent frame over the box (exact integer arithmetic, coordinates
doubled). A placement succeeds when all cells land on distinct squares and every adjacency is consistent.

usage:
  python3 verify_folds.py cells.txt                 # every box with the net's surface area
  python3 verify_folds.py cells.txt 1x2x58 2x2x43   # only the listed boxes
  python3 verify_folds.py cells.txt --facemap out.json   # also write, per folding, the box face of every cell
cells.txt: "x,y;x,y;..." (whitespace and newlines are ignored)
Exit code 0 iff every listed box folds (or, without a list, the run completed).
"""
import sys, json
from collections import deque

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))   # right, up, left, down in the plane


def read_cells(path):
    txt = open(path).read().replace('\n', ';').replace(' ', '')
    cells = [tuple(int(v) for v in t.split(',')) for t in txt.split(';') if t]
    if len(set(cells)) != len(cells): raise SystemExit('duplicate cells')
    return cells


def topology(cells):
    """connected, Euler characteristic V - E + F (1 for a disk), and diagonal pinch points"""
    S = set(cells); n = len(S)
    seen = {cells[0]}; st = [cells[0]]
    while st:
        x, y = st.pop()
        for dx, dy in DIRS:
            c = (x + dx, y + dy)
            if c in S and c not in seen: seen.add(c); st.append(c)
    V = {(x + i, y + j) for x, y in S for i in (0, 1) for j in (0, 1)}
    E = {(x, y, 0) for x, y in S} | {(x, y + 1, 0) for x, y in S} | {(x, y, 1) for x, y in S} | {(x + 1, y, 1) for x, y in S}
    pinch = 0
    for vx, vy in V:   # a vertex whose four cells are occupied only diagonally
        a, b, c, d = ((vx - 1, vy - 1) in S, (vx, vy - 1) in S, (vx, vy) in S, (vx - 1, vy) in S)
        if (a and c and not b and not d) or (b and d and not a and not c): pinch += 1
    return {'cells': n, 'connected': len(seen) == n, 'euler': len(V) - len(E) + n, 'pinch_points': pinch}


def boxes_of_area(S):
    out = []
    for a in range(1, S):
        for b in range(a, S):
            if 2 * a * b >= S: break
            num = S // 2 - a * b
            if S % 2 == 0 and num > 0 and num % (a + b) == 0 and num // (a + b) >= b: out.append((a, b, num // (a + b)))
    return out


def surface(a, b, c):
    """all surface squares as (centre, normal) in doubled coordinates; box [0,2a] x [0,2b] x [0,2c]"""
    D = (2 * a, 2 * b, 2 * c); sq = []
    for ax in range(3):
        u, v = [k for k in range(3) if k != ax]
        for side in (0, 1):
            n = [0, 0, 0]; n[ax] = 1 if side else -1
            for i in range(D[u] // 2):
                for j in range(D[v] // 2):
                    p = [0, 0, 0]; p[ax] = D[ax] * side; p[u] = 2 * i + 1; p[v] = 2 * j + 1
                    sq.append((tuple(p), tuple(n)))
    return D, sq


def add(p, q, k=1): return (p[0] + k * q[0], p[1] + k * q[1], p[2] + k * q[2])
def neg(p): return (-p[0], -p[1], -p[2])


def step(D, p, fr, d):
    """move from the square at centre p with frame fr = (u, v, n) one cell in plane direction d (0..3)"""
    u, v, n = fr
    t = (u, v, neg(u), neg(v))[d]                     # travel direction on the surface
    q = add(p, t, 2)
    ax = next(k for k in range(3) if t[k])
    if 0 < q[ax] < D[ax]:                             # same face
        return q, fr
    q = add(add(p, t), neg(n))                        # roll over the edge: new normal = t, new travel = -n
    if d == 0: fr2 = (neg(n), v, t)
    elif d == 1: fr2 = (u, neg(n), t)
    elif d == 2: fr2 = (n, v, t)
    else: fr2 = (u, n, t)
    return q, fr2


def frames(n):
    """the 8 tangent frames (u, v) at a square with normal n"""
    ax = next(k for k in range(3) if n[k]); t1, t2 = [k for k in range(3) if k != ax]
    e = lambda k, s: tuple(s if i == k else 0 for i in range(3))
    basis = [e(t1, 1), e(t2, 1), e(t1, -1), e(t2, -1)]
    out = []
    for r in range(4):
        u = basis[r]
        for v in (basis[(r + 1) % 4], basis[(r + 3) % 4]):
            out.append((u, v, n))
    return out


def fold(cells, box, want_map=False):
    """returns (folds?, number of placements of cell 0 that work, face map of the first one)"""
    a, b, c = box
    D, sq = surface(a, b, c)
    if len(sq) != len(cells): return False, 0, None
    idx = {cl: i for i, cl in enumerate(cells)}
    nb = [[idx.get((x + dx, y + dy)) for dx, dy in DIRS] for (x, y) in cells]
    found, first = 0, None
    for p0, n0 in sq:
        for fr0 in frames(n0):
            pos = [None] * len(cells); fr = [None] * len(cells); used = {p0}
            pos[0], fr[0] = p0, fr0; dq = deque([0]); ok = True
            while dq and ok:
                i = dq.popleft()
                for d in range(4):
                    j = nb[i][d]
                    if j is None: continue
                    q, f2 = step(D, pos[i], fr[i], d)
                    if pos[j] is None:
                        if q in used: ok = False; break
                        pos[j], fr[j] = q, f2; used.add(q); dq.append(j)
                    elif pos[j] != q or fr[j] != f2:
                        ok = False; break
            if ok and len(used) == len(cells):
                found += 1
                if first is None:
                    first = [face_name(D, fr[i][2]) for i in range(len(cells))]
                if not want_map: return True, found, first
    return found > 0, found, first


def face_name(D, n):
    names = {(1, 0, 0): '+x', (-1, 0, 0): '-x', (0, 1, 0): '+y', (0, -1, 0): '-y', (0, 0, 1): '+z', (0, 0, -1): '-z'}
    return names[n]


def main():
    args = sys.argv[1:]
    if not args: print(__doc__); sys.exit(2)
    fmap = None
    if '--facemap' in args:
        k = args.index('--facemap'); fmap = args[k + 1]; args = args[:k] + args[k + 2:]
    cells = read_cells(args[0]); t = topology(cells)
    print(f"net: {t['cells']} cells, connected {t['connected']}, Euler characteristic {t['euler']}, pinch points {t['pinch_points']}")
    if not (t['connected'] and t['euler'] == 1 and t['pinch_points'] == 0): print('NOT A SIMPLE POLYOMINO'); sys.exit(1)
    listed = [tuple(sorted(int(v) for v in s.split('x'))) for s in args[1:]]
    boxes = listed or boxes_of_area(len(cells))
    allok, maps = True, {}
    for bx in boxes:
        ok, k, m = fold(cells, bx)
        print(f"{'x'.join(map(str, bx)):>12}  {'FOLDS' if ok else 'does not fold'}")
        if ok and m: maps['x'.join(map(str, bx))] = m
        allok &= ok
    if fmap: json.dump({'cells': cells, 'faces': maps}, open(fmap, 'w'))
    if listed: print('ALL LISTED BOXES FOLD' if allok else 'SOME LISTED BOX DOES NOT FOLD'); sys.exit(0 if allok else 1)


if __name__ == '__main__':
    main()

# Verification

## Standalone script (Python 3, standard library only)

```
python3 verify/verify_folds.py data/net-352-a-cells.txt            # every box of area 352
python3 verify/verify_folds.py data/net-352-a-cells.txt 2x7x18     # only the listed boxes
```

It checks that the net is one simple polyomino (connected, Euler characteristic 1, no corner-only contacts) and, for
each box, places the first square on every surface square in all 8 orientations and rolls the net over the box; a box
folds when every square lands on a different surface square and every pair of joined squares lands on squares that
meet along the same box edge. Expected output: `expected-output-a.txt`, `expected-output-b.txt`.

## The hidny checker

`ValidNetSolutionChecker` from [hidny/CuboidSimplePhaseNetSearch](https://github.com/hidny/CuboidSimplePhaseNetSearch),
called for each box through `CheckNet.java` (from Silverstein's repository, MIT). For both nets it reports the same four
boxes among the ten boxes of area 352. Tested with Java 21; run from the repository root:

```
git clone https://github.com/hidny/CuboidSimplePhaseNetSearch
git -C CuboidSimplePhaseNetSearch checkout 3142fef   # the version tested here
javac -d classes -sourcepath CuboidSimplePhaseNetSearch/src verify/CheckNet.java
java -Xss512m -cp classes CheckNet data/net-352-a-cells.txt 1,2,58 2,2,43 2,3,34 2,4,28 2,7,18 2,8,16 2,10,13 4,4,20 4,8,12 7,8,8
```

The checker prints a long diagnostic log; the result lines have the form `2x7x18 : FOLDS` or `2x3x34 : does not fold`
(filter with `| grep " : "`).

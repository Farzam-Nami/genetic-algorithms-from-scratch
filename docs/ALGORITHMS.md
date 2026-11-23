# Genetic-algorithm implementations

Each script follows the same conceptual sequence: initialize a random population; evaluate fitness; select parents; apply crossover and mutation; preserve the best individuals as defined by the script; repeat until a stopping condition is met.

## 1. Maximum of x²

**Representation.** A candidate is an integer `x` in `[0,255]`. For crossover and mutation, its eight-bit binary representation is used. Its fitness is `f(x)=x²`, so larger values are always better. The known mathematical optimum is `x=255`, `f(255)=65,025`.

**Operators.** Fitness-proportionate (roulette-wheel) parent selection, one-point crossover on the eight-bit strings, single-bit mutation, and elitism. An individual with fitness zero has zero selection weight unless all candidates have zero fitness, in which case selection is uniform.

**Stopping.** The search ends after 20 generations without a different best score or after 50 generations. Results depend on the sampled initial population and mutations.

## 2. TSP over 51 cities

**Input.** `TSP51.txt` has 51 lines, each with a one-based city ID and integer x/y coordinates. The Python chromosome stores zero-based indices (0–50). The input is read into `citiesX` and `citiesY` arrays in file order.

**Representation.** A chromosome is a permutation of all 51 city indices. The Euclidean distance between city indices `a` and `b` is:

`d(a,b) = sqrt((x[a]-x[b])² + (y[a]-y[b])²)`

The full tour length includes the last-to-first edge:

`L(p) = Σ d(p[i], p[(i+1) mod 51])`

The script uses `fitness(p)=1/L(p)`, so shorter tours receive larger fitness values.

**Operators.** Roulette-wheel parent selection based on inverse tour length; permutation-preserving crossover that copies a parent prefix and fills the remaining positions in the other parent's order; and swap mutation. Preserving an entire permutation is essential: duplicated or missing cities would not represent a valid tour.

**Stopping.** The iteration ends after 3000 generations with an unchanged recorded shortest path or at 20000 generations. The resulting tour is a heuristic candidate, not a proven shortest path.

## 3. Eight Queens

**Representation.** A chromosome is an eight-element permutation. The index is a board column, and its value specifies the queen's row in that column. This enforces one queen in each row and each column automatically.

**Fitness.** For every unordered pair of queens `(i,j)`, the script adds one if the queens do not share a diagonal (`|i-j| != |p[i]-p[j]|`). There are `8 choose 2 = 28` pairs. Fitness 28 therefore identifies a valid eight-queens arrangement.

**Operators.** Roulette-wheel selection; the same permutation-preserving prefix-and-fill crossover used for TSP; swap mutation; and one preserved best chromosome per generation.

**Stopping.** The script exits when fitness reaches 28, when the maximum number of unchanged generations is met, or when the overall generation limit is reached. It prints the chromosome and an ASCII board representation.

## Fitness, selection and randomness

The roulette-wheel functions turn nonnegative fitness values into probabilities:

`p_i = fitness_i / Σ fitness_j`.

If the total fitness is zero, uniform probabilities are used. Selection is probabilistic and normally samples chromosomes with replacement, except where the X² script removes already selected individuals in its selection loop.

Neither TSP nor Eight Queens uses a binary chromosome. Their permutation operators maintain each element exactly once; ordinary bitwise crossover would not preserve this constraint. The source scripts expose the probability and generation parameters near the beginning of each file.

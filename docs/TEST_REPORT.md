# Verification and tests

## Automated suite

Install `requirements.txt`, then run:

```bash
python -m unittest discover -s tests -v
```

**10 automated tests pass**. They verify:

- Eight-bit encoding/decoding and the square-function fitness values.
- Fitness selection of elite individuals even when the best candidate is at the last list position.
- Valid probability distributions when every candidate has zero fitness.
- Mutation access to the final bit in an eight-bit chromosome.
- The 51 distinct, consecutively numbered city records in `TSP51.txt`.
- Euclidean tour length, including the edge returning to the start city, and reciprocal tour fitness.
- Permutation validity after TSP crossover/mutation and after Eight Queens crossover/mutation, including repeated operations.
- A known Eight Queens arrangement with fitness 28 and an all-diagonal arrangement with fitness 0.

All three source scripts pass Python syntax compilation.

## Full-script runs

With `random.seed(73)` set before executing each script, the following complete runs succeeded:

- `X2.py` finished with a recorded best objective value of **65,025** (`x = 255` is the analytical maximizer).
- `eightQueen.py` reached a fitness value of **28** after 16 generations and printed a legal eight-queen board.

The TSP operator and route-distance tests pass against the supplied coordinate format. The TSP program is an iterative heuristic with a large generation cap; no optimality certificate is claimed for any tour it prints.

## Interpretation

Stochastic population initialization, roulette selection, crossover and mutation make the result dependent on the random sequence. To compare two runs, record their random seeds, populations, generation limits and final fitness or route length. An objective value of 28 in Eight Queens proves a non-attacking arrangement; a short TSP route alone does not prove global optimality.

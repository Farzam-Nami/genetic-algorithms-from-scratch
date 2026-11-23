# Genetic Algorithms from Scratch

Three genetic-algorithm exercises from a Computational Intelligence programming course. The solutions use explicit Python/NumPy loops for population initialization, fitness calculation, selection, crossover, mutation, and generation updates.

## Exercises

| Task | Folder | Problem | Chromosome | Objective |
| --- | --- | --- | --- | --- |
| 1 | `exercises/1_X2/` | Maximize `f(x) = x²`, with integer `0 ≤ x ≤ 255` | Eight-bit binary string (population stored as decimal integers) | Maximize `x²`; mathematical maximum is `65,025` at `x=255` |
| 2 | `exercises/2_TSP51/` | Travelling Salesperson Problem over 51 cities | Permutation of city indices 0–50 | Minimize closed-tour Euclidean length |
| 3 | `exercises/3_eightQueen/` | Eight Queens | Permutation of rows for columns 0–7 | Maximize non-attacking queen pairs (28 is a solution) |

Every exercise uses its own script and parameters. The implementations are stochastic and do not claim a guaranteed optimal TSP tour.

## Requirements

- Python 3.10 or later
- NumPy

```bash
python -m pip install -r requirements.txt
```

## Run the programs

At the repository root:

```bash
python exercises/1_X2/X2.py
python exercises/2_TSP51/TSP.py
python exercises/3_eightQueen/eightQueen.py
```

The scripts print their current fitness or tour length as generations evolve. The TSP script reads `exercises/2_TSP51/TSP51.txt` using a path relative to the script itself; it does not depend on the terminal's working directory. Its input file lists **51 city IDs and their x/y coordinates**.

The first task searches an eight-bit integer space. The TSP task represents each candidate route as a permutation and includes the return leg to the first city in the distance. Eight Queens represents one queen per row and column automatically through a permutation; its fitness counts pairs without diagonal conflicts.

## Parameters and stopping conditions

| Task | Population | Crossover | Mutation | Elitism | Stop conditions |
| --- | ---: | ---: | ---: | ---: | --- |
| `X2.py` | 31 | 0.80 | 0.02 | 0.02 rate | 20 unchanged generations or 50 generations |
| `TSP.py` | 50 | 0.95 | 0.05 | 0.02 rate | 3000 unchanged generations or 20000 generations |
| `eightQueen.py` | 20 | 0.90 | 0.01 | At least one elite | 28 non-attacking pairs, 1000 unchanged generations or 10000 generations |

Mutation and crossover are probabilistic; not every generation necessarily improves the best fitness. The scripts are intentionally procedural, allowing the individual GA steps to be followed directly.

## Structure

```text
genetic-algorithms-from-scratch/
├── exercises/
│   ├── 1_X2/X2.py
│   ├── 2_TSP51/
│   │   ├── TSP.py
│   │   └── TSP51.txt
│   └── 3_eightQueen/eightQueen.py
├── tests/
├── docs/
│   ├── ALGORITHMS.md
│   ├── API_REFERENCE.md
│   └── TEST_REPORT.md
├── requirements.txt
└── README.md
```

## Documentation

- [Genetic operators and objective functions](docs/ALGORITHMS.md)
- [Functions and module reference](docs/API_REFERENCE.md)
- [Verification and tests](docs/TEST_REPORT.md)

Run automated tests with:

```bash
python -m unittest discover -s tests -v
```

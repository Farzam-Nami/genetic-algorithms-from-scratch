# Python functions and data reference

Each exercise is a standalone procedural script. It initializes its population and enters the generation loop when executed. Operators use module-level values such as `populationSize`, `bits`, `cityCount` and `queenCount` as described below.

## `exercises/1_X2/X2.py`

| Function | Arguments | Return value / role |
| --- | --- | --- |
| `findMax(population)` | Sequence of numeric fitness values | Maximum value in that sequence. |
| `fitnessCalculator(population)` | Decimal chromosomes | NumPy vector with the square of each individual. |
| `findElite(fitnessList,elitesCount)` | Fitness vector, desired elite count | Indices of highest-fitness individuals; marks selected entries in the supplied vector to avoid duplicates. |
| `binaryEncode(decimalList)` | Sequence of integers 0–255 | List of eight-character binary strings. |
| `decimal(binaryList)` | Sequence of binary strings | List of corresponding decimal integers. |
| `rouletteWheel(list)` | Decimal chromosomes | NumPy selection-probability vector calculated from squared fitness. |
| `parentSelection(noElitePopulation,parentsCount)` | Non-elite chromosomes and even number of parents | List of pairs of selected chromosome indices. |
| `crossover(encodedPopulation,indexes,bits)` | Encoded population, parent-index pairs, bit count | Encoded chromosomes after one-point crossover. |
| `mutate(population,rate,bits)` | Encoded population, mutation fraction, bit count | Encoded chromosomes after selected bits are flipped. |

Population parameters: `bits=8`, `populationSize=31`, `elitismRate=0.02`, `crossoverRate=0.8`, and `mutationRate=0.02`. The main loop converts binary chromosomes to decimal integers after mutation.

## `exercises/2_TSP51/TSP.py`

| Function | Arguments | Return value / role |
| --- | --- | --- |
| `findMin(list)` | Numeric sequence | Index of the smallest value. |
| `findMax(list)` | Numeric sequence | Index of the largest value. |
| `calculateDistance(city1,city2)` | Zero-based city indices | Euclidean distance using `citiesX` and `citiesY`. |
| `shortestPath(chromosome)` | Permutation of city indices | Total length of the closed route, including its return to the first city. |
| `chromosomeFitness(chromosome)` | City permutation | Reciprocal of its closed-tour length. |
| `fitnessCalculator(population)` | Population of routes | NumPy vector of inverse-route-length fitness values. |
| `findElite(fitnessList,elitesCount)` | Fitness vector, number of elites | Indices of the best candidates. |
| `rouletteWheel(list)` | Fitness vector | Normalized roulette-wheel probabilities. |
| `parentSelection(PopulationFitness,parentsCount)` | Fitness vector, number of parents | Paired indices drawn according to roulette probabilities. |
| `crossover(Population,indexes,cityCount,rate)` | Population, index pairs, number of cities, crossover probability | Permutations after prefix-based crossover. |
| `mutate(population,rate,cityCount)` | Population, mutation probability, number of cities | Chromosomes with selected positions swapped. |

The coordinate file has 51 records. A chromosome is a list/array of the integers 0–50 in some order. The main loop compares route lengths but selects parents using reciprocal route lengths.

## `exercises/3_eightQueen/eightQueen.py`

| Function | Arguments | Return value / role |
| --- | --- | --- |
| `findMax(list)` | Numeric values | Index of the largest value. |
| `findMin(list)` | Numeric values | Index of the smallest value. |
| `chromosomeFitness(chromosome)` | Eight-value row permutation | Number of non-attacking queen pairs; 28 is a valid complete solution. |
| `printChessBoard(chromosome)` | Eight-value row permutation | Prints an 8 × 8 text board with `x` for a queen and `-` for an empty square. |
| `findElite(fitnessList,elitesCount)` | Fitness vector and elite count | Indices of the best candidate chromosomes. |
| `crossover(Population,indexes,queenCount,rate)` | Population, index pairs, number of queens, crossover probability | A population of valid permutations. |
| `rouletteWheel(list)` | Fitness vector | Fitness-proportionate selection probabilities. |
| `parentSelection(PopulationFitness,parentsCount)` | Fitness vector, number of parents | Parent pairs represented by indices. |
| `mutate(population,rate,queenCount)` | Population, mutation probability, number of queens | Population with random position swaps. |
| `fitnessCalculator(population)` | Population of queen permutations | Vector of non-attacking-pair counts. |

The eight-queens fitness does not need to test row or column conflicts because the chromosome is a permutation. Only diagonal conflicts are possible.

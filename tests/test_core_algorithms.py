"""Tests of the optimization operators without running the interactive experiments."""

import ast
import random
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "exercises"


def load_functions(script, names, **values):
    """Load only selected function definitions from a standalone exercise script."""
    tree = ast.parse(script.read_text(encoding="utf-8"))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    module = ast.Module(body=functions, type_ignores=[])
    namespace = {"random": random, "np": np, **values}
    exec(compile(module, str(script), "exec"), namespace)
    return namespace


class GeneticAlgorithmTests(unittest.TestCase):
    def test_binary_encoding_round_trip(self):
        f = load_functions(ROOT / "1_X2" / "X2.py", {"binaryEncode", "decimal", "fitnessCalculator"})
        values = [0, 1, 7, 127, 255]
        self.assertEqual(f["decimal"](f["binaryEncode"](values)), values)
        self.assertEqual(list(f["fitnessCalculator"](values)), [0, 1, 49, 16129, 65025])

    def test_tsp_crossover_keeps_city_permutations(self):
        f = load_functions(ROOT / "2_TSP51" / "TSP.py", {"crossover", "mutate"})
        size = 51
        pop = np.array([list(range(size)), list(range(size - 1, -1, -1))])
        random.seed(17)
        children = f["crossover"](pop, [[0, 1]], size, 1.0)
        for child in children:
            self.assertEqual(sorted(child.tolist()), list(range(size)))
        mutated = f["mutate"](children, 1.0, size)
        for child in mutated:
            self.assertEqual(sorted(child.tolist()), list(range(size)))

    def test_queens_nonattacking_pairs(self):
        f = load_functions(ROOT / "3_eightQueen" / "eightQueen.py", {"chromosomeFitness", "crossover"})
        self.assertEqual(f["chromosomeFitness"]([0, 4, 7, 5, 2, 6, 1, 3]), 28)
        self.assertEqual(f["chromosomeFitness"](list(range(8))), 0)
        pop = np.array([list(range(8)), list(range(7, -1, -1))])
        random.seed(23)
        for child in f["crossover"](pop, [[0, 1]], 8, 1.0):
            self.assertEqual(sorted(child.tolist()), list(range(8)))


if __name__ == "__main__":
    unittest.main()

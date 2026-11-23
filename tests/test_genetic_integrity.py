"""Tests chromosome validity, selection, and the given optimization objectives."""

import ast
import math
import random
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "exercises"


def functions_from_file(script, names, **variables):
    tree = ast.parse(script.read_text(encoding="utf-8"))
    code = ast.Module(
        body=[node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names],
        type_ignores=[]
    )
    scope = {"random": random, "np": np, "math": math, **variables}
    exec(compile(code, str(script), "exec"), scope)
    return scope


class GeneticIntegrityTests(unittest.TestCase):
    def test_best_individual_can_be_at_final_index(self):
        for file in ("1_X2/X2.py", "2_TSP51/TSP.py", "3_eightQueen/eightQueen.py"):
            with self.subTest(problem=file):
                scope = functions_from_file(ROOT / file, {"findElite"}, populationSize=4)
                winners = scope["findElite"](np.array([2., 1., 3., 10.]), 2)
                self.assertEqual(list(map(int, winners)), [3, 2])

    def test_roulette_probability_fallback_for_zero_fitness(self):
        x2 = functions_from_file(ROOT / "1_X2/X2.py", {"fitnessCalculator", "rouletteWheel"})
        self.assertTrue(np.allclose(x2["rouletteWheel"]([0, 0, 0, 0]), [.25] * 4))
        for file in ("2_TSP51/TSP.py", "3_eightQueen/eightQueen.py"):
            scope = functions_from_file(ROOT / file, {"rouletteWheel"})
            self.assertTrue(np.allclose(scope["rouletteWheel"]([0, 0, 0]), [1 / 3] * 3))

    def test_binary_mutation_can_reach_last_bit(self):
        class FixedRandom:
            def random(self):
                return 0.99
        scope = functions_from_file(ROOT / "1_X2/X2.py", {"mutate"})
        original_random = scope["random"]
        scope["random"] = FixedRandom()
        try:
            result = scope["mutate"](["00000000"], 1, 8)
            self.assertEqual(result[0], "00000001")
        finally:
            scope["random"] = original_random

    def test_tsp_distance_closes_the_cycle(self):
        scope = functions_from_file(
            ROOT / "2_TSP51/TSP.py", {"calculateDistance", "shortestPath", "chromosomeFitness"},
            citiesX=[0, 3, 0], citiesY=[0, 0, 4]
        )
        self.assertAlmostEqual(scope["shortestPath"]([0, 1, 2]), 12.0)
        self.assertAlmostEqual(scope["chromosomeFitness"]([0, 1, 2]), 1 / 12)

    def test_city_dataset_has_exactly_51_unique_identifiers(self):
        rows = (ROOT / "2_TSP51" / "TSP51.txt").read_text().splitlines()
        cities = [line.split() for line in rows if line.strip()]
        self.assertEqual(len(cities), 51)
        self.assertEqual(sorted(int(row[0]) for row in cities), list(range(1, 52)))
        self.assertTrue(all(len(row) == 3 for row in cities))

    def test_permutation_operators_preserve_all_values(self):
        for file, size in (("2_TSP51/TSP.py", 51), ("3_eightQueen/eightQueen.py", 8)):
            with self.subTest(problem=file):
                scope = functions_from_file(ROOT / file, {"crossover", "mutate"})
                random.seed(2207)
                pop = np.array([list(range(size)), list(range(size - 1, -1, -1))])
                for _ in range(50):
                    pop = scope["crossover"](pop, [[0, 1]], size, 1)
                    pop = scope["mutate"](pop, 1, size)
                    self.assertTrue(all(sorted(row) == list(range(size)) for row in pop))

    def test_eight_queens_solution_fitness(self):
        scope = functions_from_file(ROOT / "3_eightQueen/eightQueen.py", {"chromosomeFitness"})
        self.assertEqual(scope["chromosomeFitness"]([0, 4, 7, 5, 2, 6, 1, 3]), 28)
        self.assertEqual(scope["chromosomeFitness"](list(range(8))), 0)


if __name__ == "__main__":
    unittest.main()

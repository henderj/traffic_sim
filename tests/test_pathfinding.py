import unittest
from typing import List
import src.traffic_sim.pathfinding as pf
from src.traffic_sim.pathfinding import PointGraph, Point


class Test_PathFinding(unittest.TestCase):
    def test_pointGraph(self):
        edges = {Point(0, 0): [Point(1, 0), Point(0, 1)]}
        graph = PointGraph(edges)

        keyTypes = set(map(type, graph.edges))
        self.assertEqual(keyTypes, {Point})

        valueTypes = set(map(type, graph.edges[(0, 0)]))
        self.assertEqual(valueTypes, {Point})

    def test_pointGraph_1(self):
        edges = {(0, 0): [(1, 0), (0, 1)]}
        graph = PointGraph(edges)

        keyTypes = set(map(type, graph.edges))
        self.assertEqual(keyTypes, {Point})

        valueTypes = set(map(type, graph.edges[(0, 0)]))
        self.assertEqual(valueTypes, {Point})

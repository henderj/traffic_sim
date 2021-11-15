import src.traffic_sim.mapgenerator as mapgen
import unittest

from src.traffic_sim.mapgenerator import (
    grass,
    northCheck,
    eastCheck,
    southCheck,
    westCheck,
    getBitmaskValue,
    ud,
    lr,
    udlr,
    d,
    u,
    l,
    r,
    dr,
    dl,
    ur,
    ul,
)
from src.traffic_sim.pathfinding import PointGraph, Point

n = grass


class Test_TestMapGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.graphNodes = {
            (0, 1): [(1, 1)],
            (0, 4): [(3, 4)],
            (1, 0): [(1, 1), (4, 0)],
            (1, 1): [(0, 1), (1, 0), (1, 3), (3, 1)],
            (1, 3): [(1, 1), (3, 3)],
            (3, 1): [(1, 1), (3, 3)],
            (3, 3): [(1, 3), (3, 1), (3, 4), (4, 3)],
            (3, 4): [(3, 3), (0, 4)],
            (4, 0): [(1, 0), (4, 3)],
            (4, 3): [(3, 3), (4, 0)],
        }
        self.graph = PointGraph(self.graphNodes)
        self.mapsize = (5, 5)

    def test_generate_1(self):
        ids = [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ]
        expectedSpriteIds = [
            [n, dr, lr, lr, lr, dl],
            [r, udlr, lr, dl, ud],
            [n, ud, n, ud, ud],
            [n, ur, lr, udlr, ul],
            [n, n, n, u, n],
        ]

        actualSpriteIds = mapgen.generate(ids).spriteIds
        # self.assertListEqual(expectedSpriteIds, actualSpriteIds)

    def test_northCheck(self):
        point1 = Point(1, 1)
        point2 = Point(1, 3)
        point3 = Point(0, 1)
        self.assertTrue(northCheck(point1, self.graph))
        self.assertTrue(northCheck(point2, self.graph))
        self.assertFalse(northCheck(point3, self.graph))

    def test_northCheck_2(self):
        point1 = Point(2, 1)
        point2 = Point(1, 2)
        self.assertFalse(northCheck(point1, self.graph))
        self.assertTrue(northCheck(point2, self.graph))

    def test_northCheck_3(self):
        point1 = Point(1, 4)
        point2 = Point(2, 2)
        self.assertFalse(northCheck(point1, self.graph))
        self.assertFalse(northCheck(point2, self.graph))

    def test_eastCheck(self):
        point1 = Point(1, 0)
        point2 = Point(0, 1)
        point3 = Point(3, 1)
        self.assertTrue(eastCheck(point1, self.graph))
        self.assertTrue(eastCheck(point2, self.graph))
        self.assertFalse(eastCheck(point3, self.graph))

    def test_eastCheck_2(self):
        point1 = Point(2, 1)
        point2 = Point(1, 2)
        point3 = Point(1, 4)
        self.assertTrue(eastCheck(point1, self.graph))
        self.assertFalse(eastCheck(point2, self.graph))
        self.assertTrue(eastCheck(point3, self.graph))

    def test_eastCheck_3(self):
        point1 = Point(0, 0)
        point2 = Point(2, 2)
        self.assertFalse(eastCheck(point1, self.graph))
        self.assertFalse(eastCheck(point2, self.graph))

    def test_southCheck(self):
        point1 = Point(1, 0)
        point2 = Point(1, 1)
        point3 = Point(3, 4)
        self.assertTrue(southCheck(point1, self.graph))
        self.assertTrue(southCheck(point2, self.graph))
        self.assertFalse(southCheck(point3, self.graph))

    def test_southCheck_2(self):
        point1 = Point(2, 1)
        point2 = Point(1, 2)
        self.assertFalse(southCheck(point1, self.graph))
        self.assertTrue(southCheck(point2, self.graph))

    def test_southCheck_3(self):
        point1 = Point(0, 0)
        point2 = Point(2, 2)
        self.assertFalse(southCheck(point1, self.graph))
        self.assertFalse(southCheck(point2, self.graph))

    def test_westCheck(self):
        point1 = Point(1, 1)
        point2 = Point(3, 1)
        point3 = Point(3, 4)
        self.assertTrue(westCheck(point1, self.graph))
        self.assertTrue(westCheck(point2, self.graph))
        self.assertFalse(westCheck(point3, self.graph))

    def test_westCheck_2(self):
        point1 = Point(2, 1)
        point2 = Point(1, 2)
        self.assertTrue(westCheck(point1, self.graph))
        self.assertFalse(westCheck(point2, self.graph))

    def test_westCheck_3(self):
        point1 = Point(0, 0)
        point2 = Point(2, 2)
        self.assertFalse(westCheck(point1, self.graph))
        self.assertFalse(westCheck(point2, self.graph))

    def test_getBitmaskValue_1(self):
        point1 = Point(1, 1)
        expected1 = 15
        point2 = Point(3, 1)
        expected2 = 10
        point3 = Point(3, 4)
        expected3 = 1
        self.assertEqual(getBitmaskValue(point1, self.graph), expected1)
        self.assertEqual(getBitmaskValue(point2, self.graph), expected2)
        self.assertEqual(getBitmaskValue(point3, self.graph), expected3)

    def test_getBitmaskValue_2(self):
        point1 = Point(2, 1)
        expected1 = 6
        point2 = Point(1, 2)
        expected2 = 9
        self.assertEqual(getBitmaskValue(point1, self.graph), expected1)
        self.assertEqual(getBitmaskValue(point2, self.graph), expected2)

    def test_getBitmaskValue_3(self):
        point1 = Point(0, 0)
        expected1 = 0
        point2 = Point(2, 2)
        expected2 = 0
        self.assertEqual(getBitmaskValue(point1, self.graph), expected1)
        self.assertEqual(getBitmaskValue(point2, self.graph), expected2)

    # def test_generate_2(self):
    #     ids = [
    #         [0, 0, 1, 1, 0, 0, 0],
    #         [0, 0, 0, 1, 0, 0, 0],
    #         [0, 1, 0, 1, 0, 0, 0],
    #         [0, 1, 1, 1, 1, 1, 1],
    #         [0, 0, 0, 1, 0, 0, 0],
    #         [0, 0, 0, 1, 0, 0, 0],
    #         [0, 0, 0, 1, 0, 0, 0],
    #     ]
    #     expectedSpriteIds = [
    #         [grass, grass, lend, ulturn, grass, grass, grass],
    #         [grass, grass, grass, down, grass, grass, grass],
    #         [grass, uend, grass, down, grass, grass, grass],
    #         [grass, drturn, right, cross, right, right, rend],
    #         [grass, grass, grass, down, grass, grass, grass],
    #         [grass, grass, grass, down, grass, grass, grass],
    #         [grass, grass, grass, dend, grass, grass, grass],
    #     ]

    #     actualSpriteIds = mapgen.generate(ids).spriteIds
    #     self.assertListEqual(expectedSpriteIds, actualSpriteIds)


if __name__ == "__main__":
    unittest.main()

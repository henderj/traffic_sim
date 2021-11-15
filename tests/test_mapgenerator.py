import src.traffic_sim.mapgenerator as mapgen
import unittest

from src.traffic_sim.mapgenerator import (
    grass,
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

n = grass


class Test_TestMapGenerator(unittest.TestCase):
    def test_generate_1(self):
        mapSize = (5, 5)
        graphNodes = {
            (0, 1): [(1, 1)],
            (1, 0): [(1, 1), (2, 0)],
            (1, 1): [(0, 1), (1, 0), (1, 3), (3, 1)],
            (1, 3): [(1, 1), (3, 3)],
            (3, 1): [(1, 1), (3, 3)],
            (3, 3): [(1, 3), (3, 1), (3, 4), (4, 3)],
            (3, 4): [(3, 3)],
            (4, 0): [(1, 0), (4, 3)],
            (4, 3): [(3, 3), (4, 0)],
        }
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
        self.assertListEqual(expectedSpriteIds, actualSpriteIds)

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

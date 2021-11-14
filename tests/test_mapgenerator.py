import src.traffic_sim.mapgenerator as mapgen
import unittest

from src.traffic_sim.mapgenerator import (
    grass,
    down,
    right,
    cross,
    uend,
    dend,
    rend,
    lend,
    urturn,
    ulturn,
    drturn,
    dlturn,
)


class Test_TestMapGenerator(unittest.TestCase):
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
            [grass, grass, grass, uend, grass, grass, grass],
            [grass, grass, grass, down, grass, grass, grass],
            [grass, grass, grass, down, grass, grass, grass],
            [lend, right, right, cross, right, right, rend],
            [grass, grass, grass, down, grass, grass, grass],
            [grass, grass, grass, down, grass, grass, grass],
            [grass, grass, grass, dend, grass, grass, grass],
        ]

        actualSpriteIds = mapgen.generate(ids).spriteIds
        self.assertListEqual(expectedSpriteIds, actualSpriteIds)

    def test_generate_2(self):
        ids = [
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ]
        expectedSpriteIds = [
            [grass, grass, lend, ulturn, grass, grass, grass],
            [grass, grass, grass, down, grass, grass, grass],
            [grass, uend, grass, down, grass, grass, grass],
            [grass, drturn, right, cross, right, right, rend],
            [grass, grass, grass, down, grass, grass, grass],
            [grass, grass, grass, down, grass, grass, grass],
            [grass, grass, grass, dend, grass, grass, grass],
        ]

        actualSpriteIds = mapgen.generate(ids).spriteIds
        self.assertListEqual(expectedSpriteIds, actualSpriteIds)


if __name__ == "__main__":
    unittest.main()

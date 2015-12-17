######################################################################
##   Lab L2: Caves and Back Tracking
##   Jacob Stoebel (stoebelj)
## CSC 326, Data Structures
## test.py
## Purpose: runs through a test suite.


import sys
sys.path.insert(0, '..')
import unittest
import main

CAVE_1_LOC = r'../caves/cave1.txt'  #using a large map
CAVE_3_LOC = r'../caves/cave3.txt'


class TestHelpers(unittest.TestCase):

    def test_build_map(self):
        """tests the build map helper function"""

        in_map =[ ['W', 'W', 'W'],
        ['W', 'M', 'W'],
        ['W', 'W', 'W'] ]

        expected_complete = [ ['W', 'W', 'W'],
        ['W', '.', 'W'],
        ['W', 'W', 'W'] ]

        expected_hunter = [ ['?', '?', '?'],
        ['?', 'M', '?'],
        ['?', '?', '?'] ]

        complete_map, hunter_map = main.build_maps(in_map)

        self.assertEqual(complete_map, expected_complete)       #test complete map
        self.assertEqual(hunter_map, expected_hunter)       #test hunter map

    def test_parse_map(self):
        """tests the parse map helper function."""

        expected_parse = [
            ['W', 'W', 'W', 'W', 'W'],
            ['W', '.', '.', '.', 'W'],
            ['W', '.', 'T', '.', 'W'],
            ['W', 'M', '.', '.', 'W'],
            ['W', 'W', 'W', 'W', 'W']
        ]

        map = main.parse_map(CAVE_3_LOC)

        self.assertEqual(map, expected_parse)       #test complete map

class TestCave(unittest.TestCase):
    """
    tests for Cave class
    """

    def test_loc(self):
        """tests initial location of hunter
        pre: none
        post: new locaiton is correct"""
        cave = main.Cave(CAVE_1_LOC)
        self.assertEqual(cave.location, (4, 7))
        cave.root.destroy()

    def test_get_terrain(self):
        """tests the get terrain method
        pre: none
        post: locations at given coordinates are given"""
        cave = main.Cave(CAVE_1_LOC)
        self.assertEqual(cave.get_terrain((0, 0)), 'W')
        self.assertEqual(cave.get_terrain((4, 1)), '.')
        cave.root.destroy()

    def test_get_terrain_assertion_error(self):
        """tests the get terrain method with a coordinate < 0
        pre: none
        post: an AssertionError is raised."""
        cave = main.Cave(CAVE_1_LOC)
        with self.assertRaises(AssertionError):
            cave.get_terrain((-1, 0))
        cave.root.destroy()

    def test_get_terrain_fail(self):
        """tests the get terrain if a coordinate is too large
        pre: none
        post: an IndexError is raised."""

        cave = main.Cave(CAVE_1_LOC)
        cave_rows = len(cave.complete_map)
        with self.assertRaises(IndexError):
            self.assertEqual(cave.get_terrain((cave_rows, 0)), None)
        cave.root.destroy()

    def test_inspect(self):
        """tests the inspect method on valid data
        pre: none
        post: the correct terrain type is given"""

        cave = main.Cave(CAVE_1_LOC)
        north_of_me = cave.inspect('n')
        self.assertEqual(north_of_me, '.')
        cave.root.destroy()

    def test_inspect_fail(self):
        """tests the inspect method on invalid data
        pre: none
        post: a KeyError is raised."""

        cave = main.Cave(CAVE_1_LOC)
        with self.assertRaises(KeyError):
            cave.inspect('beans')
        cave.root.destroy()

    def test_forward(self):
        """tests the forward method. Here the hunter should move one space north.
        pre: none
        post: the new location is correct"""

        cave = main.Cave(CAVE_1_LOC)
        cave.forward()
        self.assertEqual(cave.location, (4, 6))     #expected new location
        cave.root.destroy()

    def test_back_track(self):
        """
        pre: none
        post: hunter goes back to the first location in the history stack
        """

        cave = main.Cave(CAVE_3_LOC)
        cave.history.push((2, 1))     #let's pretend that  the hunter began at (2, 1)
        cave.back_track()
        self.assertEqual(cave.location, (2, 1))     #expected new location
        self.assertEqual(len(cave.history), 0)          #expected new length of history
        cave.root.destroy()

    def test_move(self):
        """
        pre: none
        post: hunter moves to (2, 1)
        """
        cave = main.Cave(CAVE_3_LOC)
        cave.move((2,1))        #move to 2,1
        self.assertEqual(cave.location, (2,1) )
        cave.root.destroy()

    def test_report_path(self):
        cave = main.Cave(CAVE_3_LOC)
        for i in range(3):
            coord = (i, i)      #a fake coordinate
            cave.history.push(coord)

        cave.report_path()      #should print out (2,2), (1,1), (0,0)
        cave.root.destroy()

    def test_update(self):

        cave = main.Cave(CAVE_3_LOC)
        expected_map = '''?  ?  ?  ?  ?\n?  ?  ?  ?  ?\n?  ?  ?  ?  ?\n?  M  ?  ?  ?\n?  ?  ?  ?  ?\n'''
        self.assertEqual(expected_map, cave.map.cget('text'))
        cave.root.destroy()

    def test_wrap_up(self):
        cave = main.Cave(CAVE_3_LOC)
        cave.wrap_up()
        self.assertEqual('Quit', cave.step_btn.cget('text'))
        cave.root.destroy()

if __name__ == '__main__':
    unittest.main()
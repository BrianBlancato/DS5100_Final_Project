import unittest
import pandas as pd
from collections import Counter
from typing import List
from montecarlosimulator import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def setUp(self):
        faces = [1, 2, 3, 4, 5, 6]
        self.die = Die(faces)

    def test_change_weight(self):
        self.die.change_weight(3, 3)
        weight_for_face3 = self.die.show().loc[self.die.show()['face'] == 3, 'weight'].values[0]
        self.assertEqual(weight_for_face3, 3.0)
        with self.assertRaises(ValueError):
            self.die.change_weight('A', 4)
        with self.assertRaises(ValueError):
            self.die.change_weight(2, 'elephant')

    def test_roll(self):
        rolled_faces = self.die.roll(10)
        valid_faces = self.die.show()['face'].values
        for roll in rolled_faces:
            self.assertIn(roll, valid_faces)

    def test_show(self):
        self.assertIsInstance(self.die.show(), pd.DataFrame)


class TestGame(unittest.TestCase):
    def setUp(self):
        faces1 = [1, 2, 3, 4, 5, 6]
        self.test_die = Die(faces1)
        self.game = Game([self.test_die, self.test_die, self.test_die])
    
    def test_play(self):
        self.game.play(25)
        results = self.game.show('wide')
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(results.shape, (25, 3))
        self.assertEqual(list(results.index), list(range(1,26)))
        self.assertEqual(list(results.columns), [1, 2, 3])
        for i in range(1, 26):
            for j in [1, 2, 3]:
                self.assertIn(results.loc[i,j], [1, 2, 3, 4, 5, 6])

    
    def test_show(self):
        self.game.play(10)
        with self.assertRaises(ValueError):
            self.game.show(form="invalid")
        self.assertIsInstance(self.game.show(), pd.DataFrame)
        wide_results = self.game.show('wide')
        self.assertEqual(len(wide_results.columns), 3)
        expected_wide_index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertListEqual(wide_results.index.tolist(), expected_wide_index)
        narrow_results = self.game.show('narrow')
        self.assertIsInstance(narrow_results.index, pd.MultiIndex)
        self.assertEqual(len(narrow_results.columns), 1)

    
class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces = [1, 2, 3, 4, 5, 6]
        self.die = Die(faces)
        self.game = Game([self.die, self.die])
        self.game.play(10)
        self.analyzer = Analyzer(self.game)
 
    def test_jackpot(self):
        self.assertIsInstance(self.analyzer.jackpot(), int)
        if self.analyzer.jackpot() != 0:
            self.assertIsInstance(self.analyzer.jackpot_data, pd.DataFrame)
            self.assertTrue((self.analyzer.jackpot_data.nunique(axis=1) == 1).all())
            for idx in self.analyzer.jackpot_data.index:
                self.assertTrue(self.game.show().loc[idx].equals(self.analyzer.jackpot_data.loc[idx]))

    def test_combo(self):
        self.analyzer.combo()
        self.assertIsInstance(self.analyzer.combos, pd.DataFrame)
        self.assertIsInstance(self.analyzer.combos.index, pd.MultiIndex)
        self.assertEqual(self.analyzer.combos['count'].sum(), 10)
        
    def test_face_counts_per_roll(self):
        self.analyzer.face_counts_per_roll()
        self.assertIsInstance(self.analyzer.face_counts, pd.DataFrame)
        self.assertEqual(len(self.analyzer.face_counts), 10)
        self.assertTrue((self.analyzer.face_counts.sum(axis=1) == 2).all())


if __name__ == '__main__':
    unittest.main(verbosity=3)
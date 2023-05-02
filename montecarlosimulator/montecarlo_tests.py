import unittest
import pandas as pd
from montecarlosimulator import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def setUp(self):
        faces = [1, 2, 3, 4, 5, 6]
        self.die = Die(faces)

    def test_change_weight(self):
        self.die.change_weight(3, 3)
        weight_for_face3 = self.die.show().loc[self.die.show()['face'] == 3, 'weight'].values[0]
        #Tests if the weight for 3 was changed to 3
        self.assertEqual(weight_for_face3, 3.0)
        #Tests for an invalid face
        with self.assertRaises(ValueError):
            self.die.change_weight('A', 4)
        #Tests for an invalid weight
        with self.assertRaises(ValueError):
            self.die.change_weight(2, 'elephant')

    def test_roll(self):
        rolled_faces = self.die.roll(10)
        valid_faces = self.die.show()['face'].values
        #Tests if roll results are face values
        for roll in rolled_faces:
            self.assertIn(roll, valid_faces)

    def test_show(self):
        #Tests if show returns a dataframe
        self.assertIsInstance(self.die.show(), pd.DataFrame)


class TestGame(unittest.TestCase):
    def setUp(self):
        faces1 = [1, 2, 3, 4, 5, 6]
        self.test_die = Die(faces1)
        self.game = Game([self.test_die, self.test_die, self.test_die])
    
    def test_play(self):
        self.game.play(25)
        results = self.game.show('wide')
        #Tests if play populated game reults private dataframe dataframe
        self.assertIsInstance(results, pd.DataFrame)
        #Tests if game results dataframe was 25 rows (rolls) and 3 columns (dice)
        self.assertEqual(results.shape, (25, 3))
        #Tests if game results has the roll number as index
        self.assertEqual(list(results.index), list(range(1,26)))
        #Tests if game results has colums for dice
        self.assertEqual(list(results.columns), [1, 2, 3])
        #Tests if game results was populated with valid faces
        for i in range(1, 26):
            for j in [1, 2, 3]:
                self.assertIn(results.loc[i,j], [1, 2, 3, 4, 5, 6])

    def test_show(self):
        self.game.play(10)
        #Tests the exception by passing an invalid argument
        with self.assertRaises(ValueError):
            self.game.show(form="invalid")
        #Tests if show returns a dataframe without an argument
        self.assertIsInstance(self.game.show(), pd.DataFrame)
        wide_results = self.game.show('wide')
        #Tests wide format has correct amount of rows
        self.assertEqual(len(wide_results.columns), 3)
        expected_wide_index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #Tests if wide index is equal to roll numbers
        self.assertListEqual(wide_results.index.tolist(), expected_wide_index)
        narrow_results = self.game.show('narrow')
        #Tests narrow dataframe is multi-indexed
        self.assertIsInstance(narrow_results.index, pd.MultiIndex)
        #Tests narrow format has 1 column
        self.assertEqual(len(narrow_results.columns), 1)

    
class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces = [1, 2, 3, 4, 5, 6]
        self.die = Die(faces)
        self.game = Game([self.die, self.die])
        self.game.play(10)
        self.analyzer = Analyzer(self.game)
 
    def test_jackpot(self):
        #Tests jackpot returns an int
        self.assertIsInstance(self.analyzer.jackpot(), int)
        if self.analyzer.jackpot() != 0:
            #Tests if a jackpot_data is a dataframe
            self.assertIsInstance(self.analyzer.jackpot_data, pd.DataFrame)
            #Tests that every row of jackpot_data are the same face value
            self.assertTrue((self.analyzer.jackpot_data.nunique(axis=1) == 1).all())
            #Tests that jackpot_data index is the correct roll number
            for idx in self.analyzer.jackpot_data.index:
                self.assertTrue(self.game.show().loc[idx].equals(self.analyzer.jackpot_data.loc[idx]))

    def test_combo(self):
        self.analyzer.combo()
        #Tests that combo created a combos dataframe
        self.assertIsInstance(self.analyzer.combos, pd.DataFrame)
        #Tests that combos has a multi column index
        self.assertIsInstance(self.analyzer.combos.index, pd.MultiIndex)
        #Tests if the count of combinations is equal to the amount of rolls
        self.assertEqual(self.analyzer.combos['count'].sum(), 10)
        
    def test_face_counts_per_roll(self):
        self.analyzer.face_counts_per_roll()
        #Tests that face_count_per_roll created a face_counts dataframe
        self.assertIsInstance(self.analyzer.face_counts, pd.DataFrame)
        #Tests that face_counts has a row for each roll
        self.assertEqual(len(self.analyzer.face_counts), 10)
        #Tests that each row has values for each dice face result (2 dice rolled so each row sum should be 2)
        self.assertTrue((self.analyzer.face_counts.sum(axis=1) == 2).all())


if __name__ == '__main__':
    unittest.main(verbosity=3)
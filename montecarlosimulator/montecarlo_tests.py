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
        self.die.change_weight(1, 6.0)
        self.assertEqual(self.die.show().loc[1, 'weight'], 2.0)

    def test_roll(self):
        self.assertIn(self.die.roll()[0], self.die.show().index)

def tesst_show(self):
    self.assertIsInstance(self.die.sholw(), pd.DataFrame)

class TestGame(unittest.TestCase):
    def setUp(self):
        faces1 = [1, 2, 3, 4, 5, 6]
        faces2 = ['A', 'B', 'C', 'D', 'E']
        self.die1 = Die(faces1)
        self.die2 = Die(faces2)
        self.game = Game([self.die1, self.die2])
        self.game.play(3)
    
    def test_show_wide(self):
        self.assertIsInstance(self.game.show("wide"), pd.DataFrame)
    
    def test_show_narrow(self):
        self.assertIsInstance(self.game.show("narrow"), pd.DataFrame)
    
class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces1 = [1, 2, 3, 4, 5, 6]
        faces2 = ['A', 'B', 'C', 'D', 'E']
        self.die1 = Die(faces1)
        self.die2 = Die(faces2)
        self.game = Game([self.die1, self.die2])
        self.game.play(3)
        self.analyzer = Analyzer(self.game)
 
    def test_jackpot(self):
        self.assertIsInstance(self.analyzer.jackpot(), int)

    def test_combo(self):
        self.assertIsInstance(self.analyzer.combo(), pd.DataFrame)
        
    def test_face_counts_per_roll(self):
        result = self.analyzer.face_counts_per_roll()
        print(result)
        self.assertIsInstance(result, pd.DataFrame)

if __name__ == '__main__':
    unittest.main(verbosity=3)
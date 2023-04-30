import pandas as pd
import numpy as np
import random
from typing import List
from collections import Counter
from itertools import combinations

class Die:
    def __init__(self, faces):
        self._df = pd.DataFrame({'face': faces, 'weight': [1.0] * len(faces)})
        #self._df.set_index('face', inplace=True)
    
    def change_weight(self, face, new_weight):
        if face not in self._df['face'].values:
            raise ValueError('Invalid Face')
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise ValueError('Invalid Weight')
        self._df.loc[self._df['face'] == face, 'weight'] = new_weight

    def roll(self, roll_count=1):
        outcomes = []
        for i in range(roll_count):
            face = random.choices(self._df['face'], weights=self._df['weight'])[0]
            outcomes.append(face)
        return outcomes
        
    def show(self):
        return self._df
    
class Game:
    def __init__(self, dice:List[Die]):
        self.dice = dice
        self.results = None

    def play(self, rolls):
        self.results = pd.DataFrame(index=range(1, rolls+1), columns=range(1, len(self.dice)+1))
        for i, die in enumerate(self.dice):
            self.results.iloc[:, i] = die.roll(rolls)
        
    def show(self, form: str = "wide"):
        if form =="wide":
            return self.results
        elif form == "narrow":
            return self.results.unstack().to_frame()
        else:
            raise ValueError("Invalid option for 'form'. Please choose either 'wide' or 'narrow'.")      

class Analyzer:
    def __init__(self, game):
        self.game = game
        self.data = self.game.results
        self.face_dtype = game.dice[0]._df.index.dtype
        self.jackpot_data = None
        self.face_counts = None
    
    def jackpot(self):
        self.jackpot_data = self.data[self.data.apply(lambda row: row.nunique() == 1, axis = 1)]
        self.jackpot_data.index = self.data[self.data.apply(lambda row: row.nunique() == 1, axis = 1)].index
        return sum(self.data.apply(lambda row: row.nunique() == 1, axis =1))
        
    def combo(self):
        combos = self.data.groupby(list(self.data.columns)).size().rename('count')
        combos = combos.reset_index().set_index(list(self.data.columns))
        return combos
    
    
    def face_counts_per_roll(self):
        self.face_counts = self.data.apply(lambda row: row.value_counts(), axis=1, result_type='expand').fillna(0)
        self.face_counts = self.face_counts.astype(int)
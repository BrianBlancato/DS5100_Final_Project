import pandas as pd
import random
from typing import List
from collections import Counter
from itertools import combinations

class Die:
    def __init__(self, faces):
        self._df = pd.DataFrame({'face': faces, 'weight': [1.0] * len(faces)})
        self._df.set_index('face', inplace=True)
    
    def change_weight(self, face, new_weight):
        if face not in self._df.index:
            raise ValueError('Invalid Face')
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise ValueError('Invalid Weight')
        self._df.loc[face, 'weight'] = new_weight

    def roll(self, roll_count=1):
        outcomes = []
        for i in range(roll_count):
            face = random.choices(self._df.index, weights=self._df['weight'])[0]
            outcomes.append(face)
        return outcomes
        
    def show(self):
        return self._df
    
class Game:
    def __init__(self, dice:List[Die]):
        self.dice = dice
        self.results = None

    def play(self, rolls):
        self.results = pd.DataFrame(columns=["Roll Number", "Die Number", "Result"])
        for i in range(rolls):
            for j, die in enumerate(self.dice):
                roll_result = die.roll()
                self.results.loc[len(self.results)] = [i+1, j+1, roll_result]
        
    def show(self, form: str = "wide"):
        if form =="wide":
            wide_result = self.results.pivot(index="Roll Number", columns ="Die Number", values = "Result")
            return wide_result
        elif form == "narrow":
            narrow_result = self.results.set_index(["Roll Number", "Die Number"])["Result"]
            return narrow_result
        else:
            raise ValueError("Invalid option for 'form'. Please choose either 'wide' or 'narrow'.")

class Analyzer:
    def __init__(self, game):
        self.game = game
        self.data = self.game.results
        self.face_dtype = game.dice[0]._df.index.dtype
        self.jackpot_data = None
    
    def jackpot(self):
        jackpot_count = 0
        for roll_num, roll_data in self.data.iterrows():
            if roll_data['Result'].duplicated().all():
                jackpot_count += 1
            self.jackpot_data = pd.DataFrame({'jackpot_count': [jackpot_count]}, index=[0])
            self.jackpot_data.index.name = 'roll number'
            return jackpot_count
        
    def combo(self):
        combo_counts = Counter()
        for roll_num, roll_data in self.data.iterrows():
            combo_counts.update([tuple(roll_data.tolist())])
        combo_data = pd.DataFrame(combo_counts.values(), index=combo_counts.keys(), columns=['combo_count'])
        combo_data.index.names = ['face_combo']
        combo_data = combo_data.sort_values(by='combo_count', ascending=False)
        return combo_data
    
    def face_counts_per_roll(self):
        face_counts = pd.DataFrame(columns=self.game.dice[0]._df.index)
        for roll in self.game.results.index:
            roll_tuple = tuple(roll)
            counts = self.game.results.loc[roll].value_counts().sort_index()
            face_counts.loc[roll_tuple] = counts
        self.faces_counts = face_counts.fillna(0).astype(int)

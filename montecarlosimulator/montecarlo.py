import pandas as pd
import random
from typing import List

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
                self.result.loc[len(self.result)] = [i+1, j+1, roll_result]
        
    def show(self, form: str = "wide"):
        if form =="wide":
            wide_result = self.result.pivot(index="Roll Number", columns ="Die Number", values = "Result")
            return wide_result
        elif form == "narrow":
            narrow_result = self.result.set_index(index["Roll Number", "Die Number"])["Result"]
            return narrow_result
        else:
            raise ValueError("Invalid option for 'form'. Please choose either 'wide' or 'narrow'.")



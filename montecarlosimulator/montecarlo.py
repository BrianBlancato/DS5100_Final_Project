import pandas as pd
import numpy as np
import random
from typing import List


class Die:
    def __init__(self, faces):
        self.__die_df = pd.DataFrame({'face': faces, 'weight': [1.0] * len(faces)})
        self.face_type = self.__die_df['face'].dtype
    
    def change_weight(self, face, new_weight):
        if not (self.__die_df['face'] == face).any():
            raise ValueError('Invalid Face')
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise ValueError('Invalid Weight')
        self.__die_df.loc[self.__die_df['face'] == face, 'weight'] = new_weight

    def roll(self, roll_count=1):
        roll_results = []
        for i in range(roll_count):
            face = random.choices(self.__die_df['face'], weights=self.__die_df['weight'])[0]
            roll_results.append(face)
        return roll_results
        
    def show(self):
        return self.__die_df
    
class Game:
    def __init__(self, dice:List[Die]):
        self.dice = dice
        self.__results = None

    def play(self, rolls):
        self.__results = pd.DataFrame(index=range(1, rolls+1), columns=range(1, len(self.dice)+1))
        for i, die in enumerate(self.dice):
            self.__results.iloc[:, i] = die.roll(rolls)
        
    def show(self, form: str = "wide"):
        if form =="wide":
            return self.__results
        elif form == "narrow":
            return self.__results.unstack().to_frame()
        else:
            raise ValueError("Invalid option for 'form'. Please choose either 'wide' or 'narrow'.")      

class Analyzer:
    def __init__(self, game):
        self.__data = game.show('wide')
        self.face_dtype = game.dice[0].face_type
        self.jackpot_data = None
        self.face_counts = None
        self.combos = None
    
    def jackpot(self):
        self.jackpot_data = self.__data[self.__data.apply(lambda row: row.nunique() == 1, axis = 1)]
        self.jackpot_data.index = self.__data[self.__data.apply(lambda row: row.nunique() == 1, axis = 1)].index
        return sum(self.__data.apply(lambda row: row.nunique() == 1, axis =1))
        
    def combo(self):
        self.combos = self.__data.groupby(list(self.__data.columns)).size().rename('count')
        self.combos = self.combos.reset_index().set_index(list(self.__data.columns))
        return self.combos
    
    
    def face_counts_per_roll(self):
        self.face_counts = self.__data.apply(lambda row: row.value_counts(), axis=1, result_type='expand').fillna(0)
        self.face_counts = self.face_counts.astype(int)
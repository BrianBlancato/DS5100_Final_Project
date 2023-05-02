import pandas as pd
import numpy as np
import random
from typing import List


class Die:
    """
    This class creates a 'die', which is any discrete random variable
    associated with a stochastic process, sush as using a deck of cards 
    or flipping a coin or speaking a language.  A die has N sides, or "faces"
    and W weights and can be rolled to select a face.

    ATTRIBUTES
    __die_df    a private dataframe with columns for face and weight of the die
    face_type   dtype of the faces in the die

    METHODS
    __init__    Initializes a Die object with the given array of faces
    change_weight   Changes the weight of the specified face to a new weight
    roll    Simulates rolling the die for a given amount of times
    show    Returns the dataframe created in the initializer
    """
    def __init__(self, faces):
        """
        DESCRIPTION
            The initializer takes an array of faces as an argument and 
            internally initializes the weights to 1.0 for each face. The faces and 
            weights are stored in a private dataframe that is shared by the 
            other methods in the Die class.
        
        INPUTS
        faces   an array of strings or numbers

        RETURNS
        None
        """
        self.__die_df = pd.DataFrame({'face': faces, 'weight': [1.0] * len(faces)})
        self.face_type = self.__die_df['face'].dtype
    
    def change_weight(self, face, new_weight):
        """
        DESCRIPTION
            A method to change the weight of a specified face. Takes two arguments, 
            the face and the new weight. Also checks if the face and weight passed
            are valid.
        
        INPUTS
        face    a string or number that is a valid face for the Die. 
        new_weight  a number that can be converted to a floating point

        RETURNS
        None
        """
        #Checks if the given face is in the Die. Raises an error if not
        if not (self.__die_df['face'] == face).any():
            raise ValueError('Invalid Face')
        #Converts the given weight to float, raises error if it can't
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise ValueError('Invalid Weight')
        self.__die_df.loc[self.__die_df['face'] == face, 'weight'] = new_weight

    def roll(self, roll_count=1):
        """
        DESCRIPTION
            A method to roll the die one or more times. Takes a parameter of how many
            times the die is to be rolled; defaults to 1. The roll is a random sample
            from the vector of faces according to the weights. Returns a list of outcomes
            that are not stored internally
        
        INPUTS
        roll_count  int for the amount of rolls. Defaults to 1.

        RETURNS
        roll_results    a list of faces randomly selected according to weight
        """
        #Temporary list for results
        roll_results = []
        #Randomly selects a face according to weight for amount of rolls, adds face to list that is returned
        for i in range(roll_count):
            selected_face = random.choices(self.__die_df['face'], weights=self.__die_df['weight'])[0]
            roll_results.append(selected_face)
        return roll_results
        
    def show(self):
        """
        DESCRIPTION
            A method to show the user the die's current set of faces and weights
        
        INPUT
        None

        RETURNS
        __die_df    private dataframe with columns face and weight
        """
        return self.__die_df
    
class Game:
    """
    Creates a Game which consists of rolling one or more dice of similarly defined
    dice (Die Objects). A Game is initiated by passing a list of dice.
    A Game that is played will roll all dice and the results will be saved for 
    the most recent play.

    ATTRIBUTES
    dice    list of similarly defined Die objects
    __results   private dataframe of roll results for the most recent play

    METHODS
    __init__    Initializes a Game object from a list of Die objects passed
    play    Rolls the dice in the Game for a specified amount of times
    show    returns a wide or narrow view of the Game results
    """
    def __init__(self, dice:List[Die]):
        """
        DESCRIPTION
            Initializes the Game object. Takes a list of already initiated similar
            Die objects. Similar Die objects have the same number of sides and associated faces.
            The Die Objects may have its own weights.
        
        INPUTS
        dice    a list of initiated similar Die objects

        RETURNS
        None
        """
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
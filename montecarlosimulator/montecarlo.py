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
    Creates a Game object which consists of rolling one or more dice of similarly defined
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
        """
        DESCRIPTION
            A method to roll the dice in the Game object a specified amount of times.
            All dice will be rolled and the results will be saved in a private dataframe 
            of shape N rolls by M dice.
        
        INPUTS
        rolls   ints to specify how many times the dice should be rolled

        RETURNS
        None
        """
        #Creates private dataframe of shape N rolls by M dice
        self.__results = pd.DataFrame(index=range(1, rolls+1), columns=range(1, len(self.dice)+1))
        #Rolls each dice in the Game and saves result in private dataframe
        for i, die in enumerate(self.dice):
            self.__results.iloc[:, i] = die.roll(rolls)
        
    def show(self, form: str = "wide"):
        """
        DESCRIPTION
            A method to show the user the results of the most recent play.  There are two
            options, wide and narrow, which is used as the single parameter.  The wide form
            returns a dataframe with a single column index with the roll number and each die
            as a column.  The narrow form returns a dataframe with a two-column index with
            the roll number & the die number and a column for the face rolled.
            The string argument is defualted to wide. An invalid argument will raise an exception.
        
        INPUTS
        form    a string of "wide" or "narrow"

        RETURNS
        A dataframe of results with a shape depending on the argument.
        """
        if form =="wide":
            return self.__results
        elif form == "narrow":
            return self.__results.unstack().to_frame()
        #Raises exception if form is not "wide" or "narrow"
        else:
            raise ValueError("Invalid option for 'form'. Please choose either 'wide' or 'narrow'.")      

class Analyzer:
    """
    Creates an Analyzer object from a Game object. An analyzer takes the results of a single
    game and computes various descriptive statisticall properties about it.  These properties
    results are available as attributes of an Analyzer object.

    ATTRIBUTES
    face_dtype  Data type for the faces of the Die object in the Game object.
    jackpot_count    int representing the count of jackpot rolls during the game.
    jackpot_data    dataframe of jackpot rolls, index is roll number, columns for each Dice.
    face_counts    dataframe with the number of times a face appeared each roll.
    combos  dataframe of distinct combinations of faces rolled with their counts.

    METHODS
    __init__    Initializes an Analyzer object from a Game object argument.
    jackpot     Computes how many times the game resulted in all faces being identical.
    combo   Computes the distinct combinations of faces rolled, along with their counts.
    face_counts_per_roll    Computes how many times a given face is rolled in each event
    """
    def __init__(self, game):
        """
        DESCRIPTION
            Initializes an Analyzer object from a single Game object analyzer.
            The Game object should be initiated.
        
        INPUTS
        game    Initiated Game object

        RETURNS
        None
        """
        self.__data = game.show('wide')
        self.face_dtype = game.dice[0].face_type
        self.jackpot_count = int
        self.jackpot_data = None
        self.combos = None
        self.face_counts = None
    
    def jackpot(self):
        """
        DESCRIPTION
            A method to compute how many times the game resulted in all faces being
            identical. Returns an integer for the number the number of times a jackpot
            occured. Saves a public dataframe of jackpot results with the roll number
            as a named index.
        
        INPUTS
        None

        RETURNS
        jackpot_count   int, number of times a jackpot occured in the Game
        """
        #Only saves jackpot rolls from the Game results in a new dataframe, jackpot_data
        self.jackpot_data = self.__data[self.__data.apply(lambda row: row.nunique() == 1, axis = 1)]
        #Sets jackpot_data index to the roll number of the jackpot
        self.jackpot_data.index = self.__data[self.__data.apply(lambda row: row.nunique() == 1, axis = 1)].index
        #Computes jackpot_count by checking how many rows are in jackpot_data
        self.jackpot_count = self.jackpot_data.shape[0]
        return self.jackpot_count
        
    def combo(self):
        """
        DESCRIPTION
            A method to compute the distinct combinations of faces rolled, along with
            their counts.  The combinations are stored in a sorted public dataframe that
            is multi-columned indexed and a column for their count.  This method has no
            inputs or returns.  The combo dataframe is a public attribute of the analyzer
            object that is named "combos"
        
        INPUTS
        None

        RETURNS
        None
        """
        #creates new df by grouping the rows of Game Results by list of dice and calculates their count
        self.combos = self.__data.groupby(list(self.__data.columns)).size().rename('count')
        #sets the index of combos to a multi-index based on the list of dice
        self.combos = self.combos.reset_index().set_index(list(self.__data.columns))
    
    def face_counts_per_roll(self):
        """
        DESCRIPTION
            A method to compute how many times a given face is rolled in each event.
            The results are saved in a public attribute dataframe called face_counts.
            The dataframe has an index of the roll number and face values as columns.
            The columns will have the amount of times that face appeared for the 
            corresponding roll number. The method does not have inputs or retun anything

        INPUTS
        None

        RETURNS
        None
        """
        self.face_counts = self.__data.apply(lambda row: row.value_counts(), axis=1, result_type='expand').fillna(0)
        self.face_counts = self.face_counts.astype(int)
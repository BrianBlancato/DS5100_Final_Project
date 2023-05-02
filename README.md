# DS5100_Final_Project

<font size="6"> **Metadata** </font>  
This is a Monte Carlo Simulator by Brian Blancato, a gradudate datascience student.  
In this python package you will be able to create an object that is a discrete random variable associated with a stochastic processs.  This object will have customizable faces and weights to run through monte carlo simulations.  The package also contains self analyzing tools to compute various descriptive statistical properties about the simulation results.  
  
<font size="6"> **Synopsis** </font>  
Read below for instructions on how to install, import, create dice, play games and analyze games.  
  
<font size="2"> **Installing** </font>   
 To install the python package on your local machine follow this step.  
   
  - Go to your command line and enter this command  

      pip install "git+https://github.com/BrianBlancato/DS5100_Final_Project.git"  
  
The package is now installed in your python enviroment.  
  
<font size="2"> **Importing** </font>  
To import the python module run this python code.  
    
    import montepythonsimulator  
  
You are now ready to use the montepythonsimulator.  
  
<font size="2"> **Creating dice** </font>  
To create dice, follow the python code below.  
  
    #Die needs an array of faces as a parameter  
    fair_die = montecarlosimulator.Die([1, 2, 3, 4, 5, 6])  

    #Change the weight of face 3 to 6.0  
    fair_die.change_weight(3, 6.0)  

<font size="2"> **Playing Games** </font>  

    #First, create a game with two fair die  
    game = montecarlosimulator.Game([fair_die, fair_die])  

    #Now it's time to play 5 dice rolls  
    game.play(5)  

    #See results  
    game.show("wide")

<font size="2"> **Analyzing Games** </font>  

    #First, create an analyzer  
    analyzer = montecarlosimulator.Analyzer(game) 

    #See how many jackpots occurred  
    analyzer.jackpot()  

    #See which rolls the jackpots occurred  
    analyzer.jackpot_data  

    #To see the distinct combinations of faces rolled, along with their counts  
    analyzer.combo()  
    analyzer.combos  

    #To see how many times a given face is rolled in each event  
    analyzer.face_counts_per_roll()  
    analyzer.face_counts  
  
<font size="6"> **API Description** </font>  
<font size="2"> **Die Class** </font>  
    This class creates a 'die', which is any discrete random variable
    associated with a stochastic process, such as using a deck of cards 
    or flipping a coin or speaking a language.  A die has N sides, or "faces"
    and W weights and can be rolled to select a face.

    ATTRIBUTES
    face_type   dtype of the faces in the die.

    METHODS
    change_weight   Changes the weight of the specified face to a new weight.
    roll            Simulates rolling the die for a given number of times.
    show            Returns the dataframe created in the initializer.  
      
<font size="2"> **change_weight** </font>  

            DESCRIPTION
            A method to change the weight of a specified face. Takes two arguments, 
            the face and the new weight. Also checks if the face and weight passed
            are valid.
        
            INPUTS
            face        a string or number that is a valid face for the Die.
            new_weight  a number that can be converted to a floating point.

            RETURNS
            None  
              
<font size="2"> **roll** </font>  

            DESCRIPTION
            A method to roll the die one or more times. Takes a parameter of how many
            times the die is to be rolled; defaults to 1. The roll is a random sample
            from the vector of faces according to the weights. Returns a list of outcomes
            that are not stored internally.
        
            INPUTS
            roll_count  int for the amount of rolls. Defaults to 1.

            RETURNS
            roll_results    a list of faces randomly selected according to weight.  
              
            <font size="2"> **show** </font>  
            DESCRIPTION
            A method to show the user the die's current set of faces and weights
        
            INPUT
            None

            RETURNS
            __die_df    private dataframe with columns face and weight  
              

<font size="2"> **Game Class** </font>    
    Creates a Game object which consists of rolling one or more dice of similarly defined
    dice (Die Objects). A Game is initiated by passing a list of dice.
    A Game that is played will roll all dice and the results will be saved for 
    the most recent play.

    ATTRIBUTES
    dice        list of similarly defined Die objects

    METHODS
    play        Rolls the dice in the Game for a specified amount of times
    show        returns a wide or narrow view of the Game results  
      
<font size="2"> **play** </font>  

            DESCRIPTION
            A method to roll the dice in the Game object a specified number of times.
            All dice will be rolled and the results will be saved in a private dataframe 
            of shape N rolls by M dice.
        
            INPUTS
            rolls   ints to specify how many times the dice should be rolled

            RETURNS
            None  
              
<font size="2"> **show** </font>

            DESCRIPTION
            A method to show the user the results of the most recent play.  There are two
            options, wide and narrow, which is used as the single parameter.  The wide form
            returns a dataframe with a single column index with the roll number and each die
            as a column.  The narrow form returns a dataframe with a two-column index with
            the roll number & the die number and a column for the face rolled.
            The string argument is defaulted to wide. An invalid argument will raise an exception.
        
            INPUTS
            form    a string of "wide" or "narrow"

            RETURNS
            A dataframe of results with a shape depending on the argument.  
              
                
 <font size="2"> **Analyzer Class** </font>  
    Creates an Analyzer object from a Game object. An analyzer takes the results of a single
    game and computes various descriptive statistical properties about it.  These properties
    results are available as attributes of an Analyzer object.

    ATTRIBUTES
    face_dtype  Data type for the faces of the Die object in the Game object.
    jackpot_count    int representing the count of jackpot rolls during the game.
    jackpot_data    dataframe of jackpot rolls, index is roll number, columns for each Dice.
    face_counts    dataframe with the number of times a face appeared each roll.
    combos  dataframe of distinct combinations of faces rolled with their counts.

    METHODS
    jackpot     Computes how many times the game resulted in all faces being identical.
    combo   Computes the distinct combinations of faces rolled, along with their counts.
    face_counts_per_roll    Computes how many times a given face is rolled in each event  
      
<font size="2"> **jackpot** </font>

            DESCRIPTION
            A method to compute how many times the game resulted in all faces being
            identical. Returns an integer for the number the number of times a jackpot
            occurred. Saves a public dataframe of jackpot results with the roll number
             as a named index.
        
            INPUTS
            None

            RETURNS
            jackpot_count   int, number of times a jackpot occurred in the Game  
              
<font size="2"> **combo** </font>

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
              
<font size="2"> **face_count_per_roll** </font>

            DESCRIPTION
            A method to compute how many times a given face is rolled in each event.
            The results are saved in a public attribute dataframe called face_counts.
            The dataframe has an index of the roll number and face values as columns.
            The columns will have the amount of times that face appeared for the 
            corresponding roll number. The method does not have inputs or return anything

            INPUTS
            None

            RETURNS
            None  
              
                
<font size="4"> **Manifest** </font>  
-> DS5100_Final_Project
|        .gitignore  
|        LICENSE  
|        montecarlo_demo.ipynb  
|        setup.py  
|        README.md  
|        ->montecarlosimulator  
|                __init__.py  
|                montecarlo.py  
|                montecarlo_tests.py  
|                test_results.txt
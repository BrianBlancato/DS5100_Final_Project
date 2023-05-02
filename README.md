# DS5100_Final_Project

<font size="4"> **Metadata** </font>  
This is a Monte Carlo Simulator by Brian Blancato, a gradudate datascience student.  
In this python package you will be able to create an object that is a discrete random variable associated with a stochastic processs.  This object will have customizable faces and weights to run through monte carlo simulations.  The package also contains self analyzing tools to compute various descriptive statistical properties about the simulation results.  
  
<font size="4"> **Synopsis** </font>  
Read below for instructions on how to install, import, create dice, play games and analyze games  
  
 <font size="2"> **Installing** </font>   
 To install the python package on your local machine follow this step.  
   
  - Go to your command line and enter this command  
      pip install "git+https://github.com/BrianBlancato/DS5100_Final_Project.git"  
  
The package is now installed in your python enviroment.  
  
<font size="2"> **Importing** </font>  
To import the python module run this python code  
    
    import montepythonsimulator  
  
You are now ready to use the montepythonsimulator  
  
<font size="2"> **Creating dice** </font>  
To create dice, follow the python code below.  
  
    #Die needs an array of faces as a parameter  
    fair_die = montecarlosimulator.Die([1, 2, 3, 4, 5, 6])  
    #Change the weight of face 3 to 6  
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
  
<font size="4"> **API Description** </font>  
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

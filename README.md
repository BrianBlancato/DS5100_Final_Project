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

<font size="2"> **Playing Games** </font>
#First, create a game  
    game = montecarlosimulator.Game([fair_die])  
#

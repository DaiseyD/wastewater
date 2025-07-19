# Wastewater simulation automation documentation

## Ruby


### CONSTS
contains constants needed to run the program
- DBFILEPATH: contains the path of the .icmm database you wish to use for the simulations
-ALLTYPES: when set to true, will support changing all data types, when set to false, will only support numerical datatypes

### wasteautomation.rb
This is the main script used to run the program, it does the following steps:
1. Set up the Logger
2. initialize the ICMUtil class
3. Get the network info from the ICMUtil class and write it to a file for the UI to read
4. Launch the ui and wait for it to finish executing
5. read the parameters from the UI and initialize the Simulator class with those parameters
6. The simulator class sets up the scenarios for which to run the simulations
7. Simulator class runs and exports the simulations


### UICommunicator
This is a class that does the writing and reading of the files that are used for communicating with the UI. 

### ICMUtil
This class helps with the communication with Infoworks ICM objects. Objects that are used for manipulating/viewing the Infoworks ICM network are stored here. Methods for adjusting the network and getting the network information are found in this class. It requires the STRATEGIES constant that is in ScenarioManager.rb to notify the UI of which strategies are implemented in the ScenarioManager

### Simulator
This class contains the code to setup and run the simulations. First it calls the ScenarioManager to create the correct scenarios given the parameters and strategies. It then runs a simulation for every scenario with every rainfall event that is in the parameters acquired from the UI. The results from this simulation are then exported with a copy of the network state and a file explaining the changes made to the network for every scenario.

### ScenarioManager
This class is called to handle the adjusting of the scenarios to fit with the parameters specified. It will run through every parameter to be changed and apply the strategy specified with the values provided. The constant STRATEGIES is used to communicate to the UI which strategies are implemented.

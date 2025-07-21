# DG.Infoworks
## Requirements
- python (pip)
- Ruby
- Infoworks ICM
- ICMExchange


## What this program does exactly
This program is an extension to Infoworks ICM which facilitate the creation of large amount of datasets. 

### How to use
Make sure you have ICMExchange installed, this comes with the installation of Infoworks ICM.

1. Setup an Infoworks ICM network
2. Set the DBFILEPATH in rubyscripts/CONSTS.RB to the filepath of the .icmm database
3. Open a terminal in the root folder of this project (the one that contains the folders: pythonui and rubyscripts)
4. Install the python requirements using: pip install -r pythonui/requirements.txt
5. Run the following command: [FULL PATH OF ICMEXCHANGE.EXE] ./rubyscripts/DGInfoworks.rb
6. Modify the parameters as necessary in the ui and click the submit button in the main window when done
7. Wait for the simulations to finish and export
8. Results can be found in the results folder


## CONSTS
contains constants needed to run the program
- DBFILEPATH: contains the path of the .icmm database you wish to use for the simulations
- ALLTYPES: when set to true, will support changing all data types, when set to false, will only support numerical datatypes

## Modifying strategies
It is possible to create a custom strategy, to do this, create a new function in the ScenarioManager. If the strategy should create new scenarios, follow the example of the ChangeAllStrategy method. Otherwise, follow the example of the randomRange method. 
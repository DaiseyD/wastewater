# Requirements
- python (pip)
- Ruby
- Infoworks ICM
- ICMExchange


# What this program does exactly




# How to run 
1. Put the filepath of your .icmm file into ```rubyscripts/CONSTS.rb``` variable name: DBFILEPATH
2. Install the python requirements using: pip install -r pythonui/requirements.txt
4. Run ICMExchange with wasteautomation.rb as the first argument, example:
```[ICMEXCHANGE.EXE FULL PATH] rubyscripts/wasteautomation.rb```
5. Wait for the UI to open and customize the simulations you will run
6. Click the submit button in the UI, the UI will close and the simulations will be run and exported to results automatically




# Known improvement points
- no rainfall event info, you will have to gamble on the duration and timestep in the ui
- no adjusting non-numerical values
- selection objects not implemented


# requirements
Ruby
Python pyside6
Iexchange
Infoworks ICM
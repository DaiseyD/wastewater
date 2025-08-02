# Ruby components



## ICMUtil
tasks:
- contain variables for communicating with Infoworks

things I dont like:
- doing the getNetworkInfo and the complicated changeValues through strategies feels a bit weird, this could be done in the ScenarioManager class maybe




## DGInfoworks
tasks:
- initialize classes and call the necessary functions

## UICommunicator
tasks:
- write json file for ui
- read json file from ui
things to improve:
- potentially include more info in the parameterfile (like name of the network and stuff)

## Simulator
tasks:
- setup sccenariomanager
- setup initial scenarioname
- run the simulations
- export the simulations
things I dont like:
- theres a couple massive functions in there which shouldd be split into more function calls maybe: (setup(), run(), export(), cleanup())

## ScenarioManager
tasks: 
- apply changes as specified in scenariomanager
things I dont like:
- feels complicated (maybe improve the names of the functions)


## Error handling
- Custom error classes
- Proper logging when encountering
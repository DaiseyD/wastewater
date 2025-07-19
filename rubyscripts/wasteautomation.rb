require_relative './ICMUtil.rb'
require_relative './Simulator.rb'
require_relative './CONSTS.rb'
require_relative './UICommunicator.rb'
require_relative './ScenarioManager.rb'
require 'logger'


logfile = File.open("logs/logfile.log", "a")
$logger = Logger.new(logfile)



icm = ICMUtil.new(DBFILEPATH)
puts "setting up json file for ui"
networkInfo = icm.getNetworkInfo()
networkInfo['strategies'] = STRATEGIES
UICommunicator.writeNetworkInfo("communication/ICMInfo.json", networkInfo)
puts "finished setting up json file"
puts "launching ui"
system("py pythonui/pyqt.py")
puts "Ui finished"
puts "reading ui results"
modificationObj =  UICommunicator.readParameterFile("communication/uiresults.json")
puts "finished processing ui results"
puts "setting up simulations"
simulator = Simulator.new(icm, modificationObj)
simulator.setupAndRunSimulations()
puts "Simulation has finished and is exported"
puts "exiting"

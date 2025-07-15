require 'json'
require_relative './ICMAPI.rb'
require_relative './StrategyPicker.rb'
require_relative './Simulator.rb'
require_relative './CONSTS.rb'
require 'logger'

$logger = Logger.new("logs/logfile.log")



icm = ICMUtil.new(DBFILEPATH)
$logger.info "setting up json file for ui"
icm.setupjsonfile(icm.openNetwork, icm.db, "communication/ICMInfo.json")
$logger.info "finished setting up json file"

$logger.info "launching ui"
test=system("py pythonui/pyqt.py")
puts test
$logger.info "Ui finished"
$logger.info "reading ui results"

modificationObj =  icm.readuiresults("communication/uiresults.json")
$logger.info "finished processing ui results"
$logger.info "starting mass simulation"
simulator = Simulator.new(icm, modificationObj)
simulator.setupAndRunSimulations()
$logger.info "Simulation has finished and is exported"
$logger.info "exiting"

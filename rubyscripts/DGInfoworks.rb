require_relative './ICMUtil.rb'
require_relative './Simulator.rb'
require_relative './CONSTS.rb'
require_relative './UICommunicator.rb'
require_relative './ScenarioManager.rb'
require 'logger'


logfile = File.open("logs/logfile.log", "a")
$logger = Logger.new(logfile)

class DGInfoworks
    def initialize(dbfilepath)
        @icm = ICMUtil.new(dbfilepath)
        @networkInfo = @icm.getNetworkInfo()
    end

    # launches the ui, raises exception if ui return an exit code != 0
    def launchui()
        UICommunicator.writeNetworkInfo("communication/ICMInfo.json", @networkInfo)
        pythonStatus = system("py pythonui/pyqt.py")
        if(pythonStatus == false)
            raise Exception.new "UI was closed instead of submitted, exiting"
        end
    end

    # runs the simulations as specified in the file created by the ui
    def runSimulations()
        modificationObj =  UICommunicator.readParameterFile("communication/uiresults.json")
        puts "finished processing ui results, setting up simulations"
        simulator = Simulator.new(@icm, modificationObj)
        simulator.setupAndRunSimulations()
        puts "Simulation has finished and is exported"
    end
end


dgi = DGInfoworks.new(DBFILEPATH)
dgi.launchui()
dgi.runSimulations()
puts "exiting"

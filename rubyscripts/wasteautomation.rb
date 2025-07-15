require 'json'
require_relative './ICMAPI.rb'
require_relative './StrategyPicker.rb'
require_relative './Simulator.rb'
require 'logger'

$logger = Logger.new("logfile.log")

def jsonobjecthelper(object)
    name = object.table_info.name
    fieldarr = []
    object.table_info.fields.each do |field|
        unsupported = ["Flag", "Date", "String", "Array:Long", "Array:Double", "GUID", "WSStructure"]
        supported = ["Boolean", "Single", "Double", "Short", "Long"]
        if unsupported.include?(field.data_type)

        elsif supported.include?(field.data_type)
            aux = { "name" => field.name, "type" => field.data_type, "value" => object[field.name]}
            fieldarr << aux
        else 
            puts field.data_type
        end
    end
    jsonobject = {"name"=> name, "fields"=> fieldarr}
    return jsonobject
end


def setupjsonfile(on, db, filepath) # on means open network
    networkobjects = []
    on.table_names.each do | tableName| 
        if on.row_objects(tableName).length > 0
            object = on.row_objects(tableName)[0]
            networkobjects << jsonobjecthelper(object)
        end
    end
    rainfallevents = []
    i=1
    while true
        begin
            rainfallevent = db.model_object_from_type_and_id 'Rainfall Event', i
            rainfallevents << { 'id' => i, 'name' => rainfallevent.name}
        rescue Exception => e
            if !e.message.include?("Error 50 : Attempting to access a recycled object")
                break
            end
            $logger.info(e.message)
        end
        i = i + 1
    end
    i=1
    wastewater = []
    while true
        begin
            wastewaterobj = db.model_object_from_type_and_id 'Waste Water', i
            wastewater << { 'id' => i, 'name' => wastewaterobj.name}
        rescue Exception => e
            if !e.message.include?("Error 50 : Attempting to access a recycled object")
                $logger.info(e.message)
                break
            end
            $logger.info(e.message)
        end
        i = i + 1
    end
    i=1
    selectionArray= []
    while true
        begin
            selectionList = db.model_object_from_type_and_id 'Selection List',i
            selectionArray << selectionList.name
        rescue Exception => e
            if !e.message.include?("Error 50 : Attempting to access a recycled object")
                $logger.info(e.message)
                break
            end
            $logger.info(e.message)
        end
        i = i + 1
    end     
    jsonobject = {"networkobjects" => networkobjects, "rainfallevents" => rainfallevents, "selectionobjects" => selectionArray, "strategies" => STRATEGIES, "wasteOutput" => wastewater}
    File.open(filepath, "w"){|f| f.write(jsonobject.to_json())}
end


def launchui(filepath)
    if File.exists?(filepath)
        system("py pythonui/pyqt.py #{filepath}")
    else
        $logger.error("file for ui to load does not exist")
        raise Exception.new("file for ui to read does not exist")
    end
end


def readuiresults(filepath)
    file = File.open(filepath)
    uiresultsjson = JSON.load(file)
    file.close()
    return uiresultsjson
end

icm = ICMUtil.new('C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm')
$logger.info "setting up json file for ui"
setupjsonfile(icm.openNetwork, icm.db, "test.json")
$logger.info "finished setting up json file"

$logger.info "launching ui"
launchui("test.json")
$logger.info "Ui finished"
$logger.info "reading ui results"

modificationObj =  readuiresults("uiresults.json")
$logger.info "finished processing ui results"
$logger.info "starting mass simulation"
simulator = Simulator.new(icm, modificationObj)
simulator.setupAndRunSimulations()
$logger.info "Simulation has finished and is exported"
$logger.info "exiting"
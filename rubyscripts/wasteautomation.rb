require 'json'
require_relative './ICMAPI.rb'

def jsonobjecthelper(object)
    name = object.table_info.name
    fieldarr = []
    object.table_info.fields.each do |field|
        aux = { "name" => field.name, "type" => field.data_type, "value" => object[field.name]}
        fieldarr << aux
    end
    jsonobject = {"name"=> name, "fields"=> fieldarr}
    return jsonobject
end

def setupjsonfile(on, db) # on means open network
    networkobjects = []
    on.table_names.each do | tableName| 
        if on.row_objects(tableName).length > 0
            object = on.row_objects(tableName)[0]
            networkobjects << jsonobjecthelper(object)
        end
    end
    rainfallevents = []
    begin
        i = 1
        while true 
            rainfallevent = modificationObj['rainfallevents']
            rainfallevents << { 'id' => i, 'name' => rainfallevent.name}
            i = i +1
        end
    rescue Exception => e
    end
    i=1
    selectionArray= []
    while true
        begin
            selectionList = db.model_object_from_type_and_id 'Selection List',i
            selectionArray << selectionList.name
        rescue Exception => e
            if e.message.include?("File Not Found")
                    break
            end
            puts "recycled object index found: skipping"
        end
        i = i + 1
    end
        
    jsonobject = {"networkobjects" => networkobjects, "rainfallevents" => rainfallevents, "selectionobjects" => selectionArray}
    File.open("test.json", "w"){|f| f.write(jsonobject.to_json())}
end


def launchui(filepath)
    if File.exists?(filepath)
        system("py pythonui/pyqt.py #{filepath}")
    else
        puts "File #{filepath} does not exist."
    end
end


def readuiresults(filepath)
    file = File.open(filepath)
    uiresultsjson = JSON.load(file)
    file.close()
    puts uiresultsjson
    uiresultsjson.keys.each { | key | 
        puts key
        puts uiresultsjson[key]
    }
    return uiresultsjson
end

def changeAllValues(openNetwork, type, field, value)
    objects = openNetwork.row_objects(type) # objects are all objects of a type, example: hw_conduit
    objects.each do | object | 

            
        object[field] = value
        object.write
    end
end


def changeAllstrategy(scenarios, values, fieldName, typeName, icm)
    newscenarios = []
    scenarios.each do |s|
        icm.openNetwork.current_scenario = s
        values.each_with_index do | value, index | 
            scenarioName = "#{s}.#{index}"
            newscenarios << scenarioName
            icm.openNetwork.add_scenario(scenarioName, "#{s}", "testscenario")
            icm.openNetwork.current_scenario = scenarioName
            icm.openNetwork.transaction_begin
            icm.changeAllValues(typeName, fieldName, value)
            icm.openNetwork.transaction_commit
        end
    icm.openNetwork.delete_scenario(s)
    end
    return newscenarios

end

def massSimulation(icm, modificationObj)
    base = icm.db.root_model_objects[2] #dont remember why this is 2
    basename = "testStratSimulation"
    baseint = 0
    scenarios = []
    
    while true
        begin
            baseint = baseint + 1
            scenarioname = "#{basename}#{baseint}"
            scenariotest = icm.openNetwork.add_scenario(scenarioname, "Base", "testscenario")
            puts "Scenario #{scenarioname} created"
            break
        rescue Exception => e
            if !e.message.include?("already exists")
                puts e
                break
            end
        end
    end
    scenarios << scenarioname
    modificationObj['parameters'].keys.each { |key|  
        typeObject = modificationObj['parameters'][key]
        typeObject.keys.each do  |fieldName|
            scenarios = changeAllstrategy(scenarios, typeObject[fieldName], fieldName, key, icm)
        end
    }
    
    validations = icm.openNetwork.validate(scenarios)
    icm.net.commit("committing scenarios")
    puts("scenarios committed")
    baseint =0 
    while true 
        begin
            runname = "testfull#{baseint}"
            baseint = baseint + 1
            extraParameters = modificationObj['simparameters']
            rainfallevents = modificationObj['rainfallevents']
            run = base.new_run(runname, icm.net, nil, rainfallevents, scenarios, extraParameters) #run=mo.new_run(name,network,commit_id,rainfalls_and_flow_surveys,scenarios,parameters)
            break
        rescue Exception => e
            if e.message != "new_run : name already in use"
                puts "error: unknown problem encountered"
                puts e
                exit
            else 
                puts "name: #{runname} already in use, trying new name"
            end
        end
    end
    puts "run created"
    mocsims = run.children # sims as a modelobjectcollection object
    sims = []
    mocsims.each { |x| sims << x }
    WSApplication.connect_local_agent(1)
    jobids = WSApplication.launch_sims(sims, '.', false, 1, 0)
    WSApplication.wait_for_jobs(jobids, true, 100000000)
    currpath = Dir.pwd
    basepath = "#{currpath}\\results\\#{runname}"
    begin
        Dir.mkdir basepath
    rescue Exception => e
    end
    puts "exporting to #{basepath}"
    sims.each do | sim | 
        path = "#{currpath}\\#{runname}\\#{sim.name}"
        begin
            Dir.mkdir "#{currpath}\\#{runname}\\#{sim.name}"
        rescue Exception => e
        end
        test=sim.results_csv_export(nil,  path)
    end    
end




icm = ICMUtil.new('C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm')
setupjsonfile(icm.openNetwork, icm.db)

puts "launching ui"
launchui("test.json")
puts "Ui finished"
puts "reading ui results"
modificationObj =  readuiresults("uiresultscopy.json")
puts "finished processing ui results"
puts "starting mass simulation"
massSimulation(icm, modificationObj)
puts "mass simulation finished"


# puts "Running simulation"
# runSimulation(db, net)
# puts "Simulation finished"

# objecttest = on.row_objects("hw_node").pop
# puts objecttest.table_info.tableinfo_json

puts "exiting"
require 'json'

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
        rainfallevent = db.model_object_from_type_and_id 'Rainfall Event', i
        rainfallevents << { 'id' => i, 'name' => rainfallevent.name}
        i = i +1
    end
    rescue Exception => e
        puts e
        puts "last index = #{i-1}" #remove this at some point lol
    end
    jsonobject = {"networkobjects" => networkobjects, "rainfallevents" => rainfallevents}
    File.open("test.json", "w"){|f| f.write(jsonobject.to_json())}
end


def launchui(filepath)
    if File.exists?(filepath)
        system("py pythonui/pyqt.py #{filepath}")
    else
        puts "File #{filepath} does not exist."
    end
end

def runSimulation(db, network) #simobject seems to be the first child of a run WSModelObject
    #arr=WSApplication.launch_sims(sims, server, results_on_server, max_threads, after)
    # puts db.root_model_objects.class

    base = db.root_model_objects[2] #dont remember why this is 2
    rainfallevent = db.model_object_from_type_and_id 'Rainfall Event', 1
    runname = "meeting0"
    run = base.new_run(runname, network, nil, rainfallevent, nil, {"Duration" => 2, "TimeStep" => 1}) #run=mo.new_run(name,network,commit_id,rainfalls_and_flow_surveys,scenarios,parameters)
    sim = run.children[0]
    WSApplication.connect_local_agent(1)
    WSApplication.launch_sims([sim], '.', false, 1, 0)
    while sim.status == "None" 
        puts "running"
        sleep(1)
    end
    puts "exporting hopefully"
    path = "C:\\Users\\dijks\\Documents\\wastewatersimulation\\wastewater\\results\\#{runname}"
    Dir.mkdir path
    test=sim.results_csv_export(nil,  path)
    puts test.class
    puts "exported"
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

def massSimulation(db, net, openNetwork, toModifyObj)

    base = db.root_model_objects[2] #dont remember why this is 2
    rainfallevent = db.model_object_from_type_and_id 'Rainfall Event', 1
    basename = "we1231arawe"
    baseint = 0
    scenarios = []

    toModifyObj.keys.each { |key|  
        scenarioname = "#{basename}#{baseint}"
        scenariotest = openNetwork.add_scenario(scenarioname, "Base", "testscenario")
        openNetwork.current_scenario = scenarioname
        scenarios << scenarioname
        openNetwork.transaction_begin  
        changeAllValues(openNetwork, key, "top_roughness_CW", 1.4)
        openNetwork.transaction_commit
        baseint = baseint+1
    }
    
    openNetwork.transaction_begin
    validation = openNetwork.validate(scenarios)
    openNetwork.transaction_commit
    openNetwork.transaction_end

    runname = "12312"
    run = base.new_run(runname, net, nil, rainfallevent, scenarios, {"Duration" => 2, "TimeStep" => 1}) #run=mo.new_run(name,network,commit_id,rainfalls_and_flow_surveys,scenarios,parameters)
    sim = run.children[0]
    WSApplication.connect_local_agent(1)
    WSApplication.launch_sims([sim], '.', false, 1, 0)
    while sim.status == "None" 
        puts "running"
        sleep(1)
    end
    puts "exporting hopefully"
    path = "C:\\Users\\dijks\\Documents\\wastewatersimulation\\wastewater\\results\\#{runname}"
    Dir.mkdir path
    test=sim.results_csv_export(nil,  path)


end

db = WSApplication.open 'C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm'
net=db.model_object_from_type_and_id 'Model Network',2
openNetwork = net.open
setupjsonfile(openNetwork, db)
# puts "launching ui"
# launchui("test.json")
# puts "Ui finished"
puts "reading ui results"
toModifyObj =  readuiresults("uiresults.json")
puts "finished processing ui results"
puts "starting mass simulation"
massSimulation(db, net, openNetwork, toModifyObj)
puts "mass simulation finished"


# puts "Running simulation"
# runSimulation(db, net)
# puts "Simulation finished"

# objecttest = on.row_objects("hw_node").pop
# puts objecttest.table_info.tableinfo_json

puts "exiting"
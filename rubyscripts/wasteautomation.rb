require 'json'
require_relative './ICMAPI.rb'
require_relative './StrategyPicker.rb'

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
    i=1
    while true
        begin
            rainfallevent = db.model_object_from_type_and_id 'Rainfall Event', i
            rainfallevents << { 'id' => i, 'name' => rainfallevent.name}
        rescue Exception => e
            if !e.message.include?("Error 50 : Attempting to access a recycled object")
                break
            end
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
                break
            end
        end
        i = i + 1
    end
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
        
    jsonobject = {"networkobjects" => networkobjects, "rainfallevents" => rainfallevents, "selectionobjects" => selectionArray, "strategies" => STRATEGIES, "wasteOutput" => wastewater}
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
    return uiresultsjson
end

def chooseScenarioName(icm, basename)
    allScenarios = []
    icm.openNetwork.scenarios do |s|
        allScenarios << s
    end
    workname = basename
    baseint = 0
    lambda_inScenario = lambda {|name, scenarios|
        scenarios.each do | s |
            if(s.include?(name))
                return true
            end
        end
        return false
        }
    while lambda_inScenario.call(workname, allScenarios)
        workname = "#{basename}#{baseint}"
        baseint = baseint+1
    end
    return workname
end

def massSimulation(icm, modificationObj)
    # base = icm.db.root_model_objects[2] #dont remember why this is 2
    base = icm.db.model_object_from_type_and_id( icm.net.parent_type(), icm.net.parent_id())
    
    basename = modificationObj['SceneName']
    baseint = 0
    
    scenarioname = chooseScenarioName(icm, basename)
    scenariotest = icm.openNetwork.add_scenario(scenarioname, "Base", "testscenario")  
    puts "Scenario #{scenarioname} created"
    
    scenarios = []
    scenarios << scenarioname

    stratPicker = StrategyPicker.new(icm, scenarios, modificationObj)
    stratPicker.runLoop
    scenarios = stratPicker.scenarios
    
    validations = icm.openNetwork.validate(scenarios)
    if validations.error_count > 0
        raise Exception.new("could not validate, please check in infoworks icm what is wrong with the scenario")
    end
    icm.net.commit("committing scenarios")
    puts("scenarios committed")
    baseint =0 
    baserunname = modificationObj['RunName']
    runname = baserunname
    while true 
        begin  
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
                runname = "#{baserunname}#{baseint}"
                baseint = baseint+1
            end
        end
    end
    puts "run #{runname} created"
    mocsims = run.children # sims as a modelobjectcollection object
    sims = []
    mocsims.each { |x| sims << x }
    WSApplication.connect_local_agent(1)
    jobids = WSApplication.launch_sims(sims, '.', false, 1, 0)
    WSApplication.wait_for_jobs(jobids, true, 100000000)
    currpath = Dir.pwd
    basepath = "#{currpath}\/results\/#{runname}"
    begin
        Dir.mkdir basepath
    rescue Exception => e
    end
    sims.each_with_index do | sim, index | 
        path = "#{basepath}\/#{sim.name}"
        begin
            Dir.mkdir path
        rescue Exception => e
            puts "something went wrong creating directory for results"
            puts e.message
            exit
        end
        scenarioFoundFlag = false
        scenarios.each do |scene| 
            if sim.name.include?("#{scene} ")
                icm.openNetwork.current_scenario = scene
                scenarioFoundFlag = true
                break
            end
        end
        if !scenarioFoundFlag
            raise Exception.new("scenario not found")
        end

        icm.openNetwork.csv_export("results/#{runname}/#{sim.name}/network_#{icm.openNetwork.current_scenario}", {'Multiple Files' => true}) # this argument takes relative file position
        puts "exporting to: #{path}"
        test=sim.results_csv_export(nil,  path)
    end 

end




icm = ICMUtil.new('C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm')
puts "setting up json file for ui"
setupjsonfile(icm.openNetwork, icm.db)
puts "finished setting up json file"
# puts "launching ui"
# launchui("test.json")
# puts "Ui finished"
puts "reading ui results"
modificationObj =  readuiresults("uiresults.json")
puts "finished processing ui results"
puts "starting mass simulation"
massSimulation(icm, modificationObj)
puts "mass simulation finished"
puts "exiting"
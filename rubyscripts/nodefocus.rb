def printCWRoughness(hw_conduits)
    hw_conduits.each do | hw_conduit | 
        puts hw_conduit["bottom_roughness_CW"]
    end
end

def setCWRoughness(hw_conduits)
    hw_conduits.each do | hw_conduit | 
        hw_conduit["bottom_roughness_CW"] = 1.0
        hw_conduit.write
    end
end

def changeConduit(hw_conduit)
    # if hw_conduit.class != WShw_conduit
    #     raise "hw_conduit is not a WShw_conduit"
    # end

    puts hw_conduit.table_info.fields.class
    hw_conduit.table_info.fields.each do | field | 
        # puts field.name
        # puts field.description
        # puts field.data_type
        # puts "\n"
        if field.data_type == "Double" || field.data_type == "Single" || field.data_type == "Long" || field.data_type == "Short"
            puts field.name
            puts hw_conduit[field.name]
        end
    end
    #puts hw_conduit.field.class
end

def runSimulation(db, network) #simobject seems to be the first child of a run WSModelObject
    #arr=WSApplication.launch_sims(sims, server, results_on_server, max_threads, after)
    # puts db.root_model_objects.class

    # puts db.root_model_objects.length
    base = db.root_model_objects[2]
    puts base.name
    # puts base.methods - Object.methods
    run = base.new_run("testrunrubymeeting", network, nil, nil, nil, {}) #run=mo.new_run(name,network,commit_id,rainfalls_and_flow_surveys,scenarios,parameters)
    sim = run.children[0]
    WSApplication.connect_local_agent(1)
    WSApplication.launch_sims([sim], '.', false, 1, 0)
    while sim.status == "None" 
        puts "running"
        sleep(1)
    end
end

db = WSApplication.open 'C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm'



net=db.model_object_from_type_and_id 'Model Network',2
on = net.open
# runSimulation(db, net)
puts "about to run separatescript.rb"
system("glimmer ./rubyscripts/separatescript.rb") 
puts "separatescript.rb has run"
puts File.exists?("test.txt")


hw_conduits = on.row_objects("hw_conduit") #hw_hw_conduits is an array of
puts hw_conduits.length()
hw_conduit = hw_conduits.pop

# changeConduit(hw_conduit)
printCWRoughness(hw_conduits)
on.transaction_begin
setCWRoughness(hw_conduits)
on.transaction_commit
printCWRoughness(hw_conduits)



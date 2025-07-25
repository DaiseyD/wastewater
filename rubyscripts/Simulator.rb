require_relative "./ScenarioManager.rb"
class Simulator
    attr_accessor :icm, :inputParams, :scenarioInfo

    def initialize(icm, inputParams)
        @icm = icm
        @inputParams = inputParams
        @scenarioInfo = {}
    end

    # read the params from the file created by the UI and sets up the simulation object, then runs and exports the simulations
    def setupAndRunSimulations()
        params = self.massSimulation()
        self.runSimulations(params['sims'], params['runname'], params['scenarios'])
    end
    
    # delete
    def cleanupScenarios(scenarios)
        @icm.openNetwork.current_scenario = "Base"
        scenarios.each do |scene| 
            @icm.openNetwork.delete_scenario(scene)
            $logger.info("deleted scenario: #{scene}")
        end
    end
    
    def massSimulation()
        base = @icm.db.model_object_from_type_and_id( @icm.net.parent_type(), @icm.net.parent_id())
        basename = @inputParams['RunName']
        baseint = 0
        scenarioname = self.chooseScenarioName(basename) #helps with picking a unique base scenario name
        scenariotest = @icm.openNetwork.add_scenario(scenarioname, "Base", "testscenario")  
        $logger.info("Scenario #{scenarioname} created")
        scenarioManager = ScenarioManager.new(@icm, scenarioname, @inputParams)
        scenarioManager.runLoop()
        scenarioObject = scenarioManager.scenarios
        scenarios = scenarioObject.keys
        validations = @icm.openNetwork.validate(scenarios)
        if validations.error_count > 0
            raise Exception.new("could not validate, please check in infoworks icm what is wrong with the scenario")
        end
        @icm.net.commit("committing #{scenarioname} changes")
        baseint =0 
        baserunname = @inputParams['RunName']
        runname = baserunname
        while true 
            begin  
                extraParameters = @inputParams['simparameters']
                rainfallevents = @inputParams['rainfallevents']
                run = base.new_run(runname, @icm.net, nil, rainfallevents, scenarios, extraParameters) #run=mo.new_run(name,network,commit_id,rainfalls_and_flow_surveys,scenarios,parameters)
                break
            rescue Exception => e
                if e.message != "new_run : name already in use"
                    $logger.fatal(e.message)
                    raise(e)
                else 
                    $logger.info( "name: #{runname} already in use, trying new name")
                    runname = "#{baserunname}#{baseint}"
                    baseint = baseint+1
                end
            end
        end
        $logger.info("run #{runname} created")
        mocsims = run.children # sims as a modelobjectcollection object
        sims = []
        mocsims.each { |x| sims << x }
        params = {"sims" => sims, "runname" =>runname, "scenarios" => scenarioObject}
        return params
    end


    def runSimulations(sims, runname, scenariosObject)
        WSApplication.connect_local_agent(1)
        jobids = WSApplication.launch_sims(sims, '.', false, 1, 0)
        WSApplication.wait_for_jobs(jobids, true, 100000000)
        currpath = Dir.pwd
        basepath = "#{currpath}\/results\/#{runname}"
        begin
            Dir.mkdir basepath
        rescue Exception => e
        end
        puts "Exporting to #{basepath}"
        File.open("#{basepath}/inputParams.json", "w"){|f| f.write(@inputParams.to_json())}
        sims.each_with_index do | sim, index | 
            path = "#{basepath}/#{sim.name}"
            resultpath = "#{path}/sim_results"
            begin
                Dir.mkdir path
                Dir.mkdir "#{path}/current_network"
                Dir.mkdir resultpath
            rescue Exception => e
                $logger.error(e.message)
                raise(e)
            end
            scenarioFoundFlag = false
            scenarioName = ""
            scenariosObject.keys.each do |scene| 
                if sim.name.include?("#{scene} ")
                    @icm.openNetwork.current_scenario = scene
                    scenarioFoundFlag = true
                    break
                end
            end
            if !scenarioFoundFlag
                raise Exception.new("scenario not found")
            end
            relativepath = "results/#{runname}/#{sim.name}"
            @icm.openNetwork.csv_export("#{relativepath}/current_network/#{icm.openNetwork.current_scenario}", {'Multiple Files' => true}) # this argument takes relative file position
            $logger.info( "exporting to: #{path}")
            File.open("#{relativepath}/changes.json", "w"){|f| f.write(scenariosObject[@icm.openNetwork.current_scenario].to_json())}
            sim.results_csv_export(nil,  resultpath)
        end 
        cleanupScenarios(scenariosObject.keys)
        @icm.net.commit("deleted scenarios from #{runname}")
    end

    #function for picking a unique base name for the scenario to avoid duplicate scenario bugs
    def chooseScenarioName(basename)
        allScenarios = []
        @icm.openNetwork.scenarios do |s|
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
    
end
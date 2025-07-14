class Simulator
    attr_accessor :icm, :modObj

    def initialize(icm, modObj)
        @icm = icm
        @modObj = modObj
    end

    def setupAndRunSimulations()
        params = self.massSimulation(@icm, @modObj)
        self.runSimulations(@icm, params['sims'], params['runname'], params['scenarios'])
    end
    

    def massSimulation(icm, modificationObj)
        base = icm.db.model_object_from_type_and_id( icm.net.parent_type(), icm.net.parent_id())
        basename = modificationObj['SceneName']
        baseint = 0
        scenarioname = chooseScenarioName(icm, basename)
        scenariotest = icm.openNetwork.add_scenario(scenarioname, "Base", "testscenario")  
        $logger.info("Scenario #{scenarioname} created")
        scenarios = [scenarioname]
        stratPicker = StrategyPicker.new(icm, scenarios, modificationObj)
        stratPicker.runLoop
        scenarios = stratPicker.scenarios
        
        validations = icm.openNetwork.validate(scenarios)
        if validations.error_count > 0
            raise Exception.new("could not validate, please check in infoworks icm what is wrong with the scenario")
        end
        icm.net.commit("committing scenarios")
        $logger.info("scenarios committed")
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
                    $logger.fatal(e.message)
                    exit
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
        params = {"sims" => sims, "runname" =>runname, "scenarios" => scenarios}
        return params
    end


    def runSimulations(icm, sims, runname, scenarios)
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
                $logger.error("something went wrong creating directory for results")
                $logger.error(e.message)
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
            $logger.info( "exporting to: #{path}")
            test=sim.results_csv_export(nil,  path)
        end 
    end


end
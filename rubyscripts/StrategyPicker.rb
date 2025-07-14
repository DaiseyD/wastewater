STRATEGIES = ['changeAll', "randomRange"]
class StrategyPicker
    attr_accessor :icm, :scenarios, :modObj        

    strategies = ['changeAll', "randomRange", "randomSelect"]

    def initialize(icm, scenarios, modObj)
        @icm = icm
        @scenarios = scenarios
        @modObj = modObj
    end

    def strategies
        return @@strategies
    end

    def runLoop()
        @modObj['parameters'].keys.each do |key|  
            typeObject = @modObj['parameters'][key]
            typeObject.keys.each do  |fieldName|
                self.callCorrectStrategy(key, fieldName, typeObject[fieldName])
            end
        end    
    end

    def callCorrectStrategy(typeName, fieldName, fieldObject)
        stratName = fieldObject['strategy']
        values = fieldObject['values']
        case stratName
        when "changeAll"
            self.changeAllStrategy(values, fieldName, typeName)
        when "randomRange"
            self.randomRange(values, fieldName, typeName)
        else 
            raise Exception.new("Could not find strategy listed")
        end
    end


    def changeAllStrategy(values, fieldName, typeName)
        newscenarios = []
        @scenarios.each do |s|
            @icm.openNetwork.current_scenario = s
            values.each_with_index do | value, index | 
                scenarioName = "#{s}.#{index}"
                newscenarios << scenarioName
                @icm.openNetwork.add_scenario(scenarioName, "#{s}", "#{s}.#{"#{typeName}-#{fieldName}-#{index}"}")
                @icm.openNetwork.current_scenario = scenarioName
                @icm.openNetwork.transaction_begin
                @icm.changeAllValues(typeName, fieldName, value)
                @icm.openNetwork.transaction_commit
            end
            @icm.openNetwork.delete_scenario(s)
        end
        @scenarios = newscenarios
    end

    def randomRange(values, fieldName, typeName)
        random = Random.new
        @scenarios.each do |s| 
            @icm.openNetwork.current_scenario = s
            max = values.max()
            min = values.min()
            @icm.openNetwork.transaction_begin
            @icm.changeRandomRangeValues(typeName, fieldName, min, max, random)
            @icm.openNetwork.transaction_commit
        end
    end

    def randomSelect(values, fieldName, typeName)
        random = Random.new
        @scenarios.each do |s|
            @icm.openNetwork.current_scenario = s
            @icm.openNetwork.transaction_begin
            @icm.changeRandomSelectValues(typeName, fieldName, values, random)
            @icm.openNetwork.transaction_commit
        end
    end
end
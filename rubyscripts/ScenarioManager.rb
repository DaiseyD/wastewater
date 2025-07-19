STRATEGIES = ['changeAll', "randomRange", "randomSelect"]

def merge_recursively(a, b)
  a.merge(b) {|key, a_item, b_item| merge_recursively(a_item, b_item) }
end

class ScenarioManager
    attr_accessor :icm, :scenarios, :inputParams        

    def initialize(icm, scenarios, inputParams)
        @icm = icm
        @scenarios = scenarios
        @inputParams = inputParams
    end


    def runLoop()
        @inputParams['parameters'].keys.each do |key|  
            typeObject = @inputParams['parameters'][key]
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
        when "randomSelect"
            self.randomSelect(values, fieldName, typeName)
        else 
            raise Exception.new("Could not find strategy listed")
        end
    end


    def changeAllStrategy(values, fieldName, typeName)
        newscenarios = {}
        @scenarios.keys.each do |s|
            @icm.openNetwork.current_scenario = s
            values.each_with_index do | value, index | 
                scenarioName = "#{s}.#{index}"
                newscenarios[scenarioName] = merge_recursively(@scenarios[s], {typeName => {fieldName => value} })
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
        @scenarios.keys.each do |s| 
            @icm.openNetwork.current_scenario = s
            max = values.max()
            min = values.min()
            @icm.openNetwork.transaction_begin
            @icm.changeRandomRangeValues(typeName, fieldName, min, max, random)
            @icm.openNetwork.transaction_commit
            merge_recursively(@scenarios[s], {typeName => {fieldName=> "random range #{min}-#{max}"}})
        end
    end

    def randomSelect(values, fieldName, typeName)
        random = Random.new
        @scenarios.keys.each do |s|
            @icm.openNetwork.current_scenario = s
            @icm.openNetwork.transaction_begin
            @icm.changeRandomSelectValues(typeName, fieldName, values, random)
            @icm.openNetwork.transaction_commit
            merge_recursively(@scenarios[s], {typeName => {fieldName=> "randomly selected"}})
        end
    end
end
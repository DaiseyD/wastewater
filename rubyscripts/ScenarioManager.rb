STRATEGIES = ['changeAll', "randomRange", "randomSelect"]

# does a deep merge for 2 dictionary objects
def merge_recursively(a, b)
  return a.merge(b) {|key, a_item, b_item| merge_recursively(a_item, b_item) }
end

class ScenarioManager
    attr_accessor :icm, :scenarios, :inputParams        

    def initialize(icm, inputParams)
        @icm = icm
        @scenarios = {icm.openNetwork.current_scenario => {}}
        @inputParams = inputParams
    end

    # goes through every parameter in the input params and calls the correct strategy
    def runLoop()
        @inputParams['parameters'].keys.each do |key|  
            typeObject = @inputParams['parameters'][key]
            typeObject.keys.each do  |fieldName|
                self.callCorrectStrategy(key, fieldName, typeObject[fieldName])
            end
        end    
    end

    #calls the strategy that the inputParameter specifies on the type and field a specified
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

    # A strategy that changes all elements of typeName to each value, for i scenarios and k values: k*i scenarios will be created
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
                objects = @icm.getObjectsOfType(typeName)
                @icm.changeObjectsValues(objects, fieldName, value)
                @icm.openNetwork.transaction_commit
            end
            @icm.openNetwork.delete_scenario(s)
        end
        @scenarios = newscenarios
    end

    # A strategy that sets each [fieldName] of all objects of [typeName] to a random value between the min and max of the values specified in the inputparameters
    def randomRange(values, fieldName, typeName)
        random = Random.new
        @scenarios.keys.each do |s| 
            @icm.openNetwork.current_scenario = s
            max = values.max()
            min = values.min()
            @icm.openNetwork.transaction_begin
            objects = @icm.getObjectsOfType(typeName)
            objects.each do |object|
                @icm.changeValue(object, fieldName, random.rand(min..max))
            end
            @icm.openNetwork.transaction_commit
            @scenarios[s] =  merge_recursively(@scenarios[s], {typeName => {fieldName=> "random range #{min}-#{max}"}})
        end
    end

    # A strategy that sets each [fieldName] of all objects of [typeName] to a randomly selected value specified in inputparams
    def randomSelect(values, fieldName, typeName)
        random = Random.new
        @scenarios.keys.each do |s|
            @icm.openNetwork.current_scenario = s
            @icm.openNetwork.transaction_begin
            @icm.changeRandomSelectValues(typeName, fieldName, values, random)
            objects = @icm.getObjectsOfType(typeName)
            objects.each do |object|
                newvalue = values[random.rand(0...values.length())]
                @icm.changeValue(object, fieldName, newvalue)
            end
            @icm.openNetwork.transaction_commit
            @scenarios[s] = merge_recursively(@scenarios[s], {typeName => {fieldName=> "randomly selected"}})
        end
    end
end
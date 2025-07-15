class ICMUtil
    attr_accessor :db, :net, :openNetwork
    
    def initialize(dbfilepath)
        @db = WSApplication.open dbfilepath
        @net = choosenetwork()
        @openNetwork = @net.open()
    end

    def choosenetwork
        begin
            i = 1
            while true
                netex = db.model_object_from_type_and_id 'Model Network', i
                puts "#{i}: #{netex.name}"
                i = i + 1
            end        
        rescue Exception=> e
        end
        puts "what network do u want to choose (I recommend 2)"
        choice = STDIN.gets
        return db.model_object_from_type_and_id 'Model Network', choice.to_i
    end

    def deleteAllScenarios()
        @openNetwork.scenarios do |s|
            if s.downcase!= "base" and s.downcase!= "aux"
                @openNetwork.delete_scenario(s)
            end
        end
        @net.commit("deleted all scenarios")
    end

    def changeValue(object, field, newvalue)
        object[field] = newvalue
        object.write
    end

    def changeAllValues(type, field, value)
        objects = @openNetwork.row_objects(type)
        objects.each do | object | 
            changeValue(object,field, value)
        end
    end

    def changeRandomRangeValues(type, field, min, max, randomizer)
        objects = @openNetwork.row_objects(type)
        objects.each do | object |
            value = randomizer.rand(min..max)
            changeValue(object,field, value)
        end
    end

    def changeRandomSelectValues(type, field, values, randomizer)
        objects = @openNetwork.row_objects(type)
        objects.each do |object| 
            index = randomizer.rand(0...values.length()) # triple dot not single dot (exclude max value)
            value = values[index]
            changeValue(object,field, value)
        end
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

    def readuiresults(filepath)
        file = File.open(filepath)
        uiresultsjson = JSON.load(file)
        file.close()
        return uiresultsjson
    end

end

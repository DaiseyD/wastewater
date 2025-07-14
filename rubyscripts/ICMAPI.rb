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

    def changeAllValues(type, field, value)
        objects = @openNetwork.row_objects(type)
        objects.each do | object | 
            object[field] = value
            object.write
        end
    end

    def changeRandomRangeValues(type, field, min, max, randomizer)
        objects = @openNetwork.row_objects(type)
        objects.each do | object |

            val = randomizer.rand(min..max)
            object[field] = val
            object.write
        end
    end

end

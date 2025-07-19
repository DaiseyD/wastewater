require 'json'
class UICommunicator

    # writes an [object] to a [filepath] in json format
    def self.writeNetworkInfo(filepath, object)
        File.open(filepath, "w"){ |f| 
        f.write(object.to_json())
        }
    end

    # reads a jsonfile and returns the object created from that file
    def self.readParameterFile(filepath)
        file = File.open(filepath)
        uiresultsjson = JSON.load(file)
        file.close()
        return uiresultsjson
    end
end
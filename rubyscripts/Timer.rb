require 'singleton'
require 'json'
class Timer
    include Singleton
    attr_accessor :start_time, :end_time, :summary

    def initialize()
        @start_time = Time.now
        @summary = []
    end

    def addBreakpoint(name)
        @summary << {"name" => "#{name}", "time" => Time.now}
    end
    def finish()
        @end_time = Time.now
    end

    def export()
        result = {}
        prevtime = @start_time
        @summary.each{ |breakinfo|
            name = breakinfo['name']
            finishtime = breakinfo['time']
            elapsedtime = finishtime - prevtime
            result[name] = elapsedtime
            prevtime = finishtime
        }
        result['totaltime'] = @end_time - @start_time
        return result
    end
end



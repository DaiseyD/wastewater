require_relative './ICMUtil.rb'
require 'logger'

logfile = File.open("logs/logfile.log", "a")
$logger = Logger.new(logfile)

icm = ICMUtil.new('C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm')
icm.getNetworkInfo()

icm.openNetwork.transaction_begin
icm.changeValue(icm.openNetwork.row_objects("hw_subcatchment")[0], "area_measurement_type", "Percent" )
puts  icm.openNetwork.row_objects("hw_subcatchment")[0].id
icm.openNetwork.transaction_commit
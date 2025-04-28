puts WSApplication.methods - Object.methods
puts "breakpoint"
db = WSApplication.open 'C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm'
puts db.methods - Object.methods

db.root_model_objects.each do |o|
puts o.path

net=db.model_object_from_type_and_id 'Model Network',2


puts "Breakpoint\n\n\n"
puts net.methods - Object.methods

on = net.open

puts "\n\n\n\n"

puts on.methods - Object.methods
puts "\n\n"
puts on.table_names
puts "\n\n"
# puts on.row_objects("hw_conduit").methods - Object.methods
objecttest = on.row_objects("hw_conduit").pop
puts objecttest.methods - Object.methods
puts "\n test \n"
puts objecttest.table_info.tableinfo_json
end
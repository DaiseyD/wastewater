db = WSApplication.open 'C:\Users\dijks\Documents\wastewatersimulation\wastewater\test0\test.icmm'
begin
    i = 1
    while true 
        rainfallevent = db.model_object_from_type_and_id 'Rainfall Event', i
        puts rainfallevent.name
        i = i +1
    end

rescue Exception => e
    puts "last index = #{i-1}"
end
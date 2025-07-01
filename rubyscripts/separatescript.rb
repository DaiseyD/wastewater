require 'json'
require 'glimmer-dsl-swt'

include Glimmer


file = File.open("test.json", "r")
jsondata = JSON.load(file) 
file.close

glimmerdata = []
jsondata.each do |item| 
  puts "Table: #{item['tableName']}"
  glimmerdata << [item['tableName']]
end

def createNewWindow(index, item)
  shell{ 
    minimum_size 400, 300
    text item['tableName']
    scrolled_composite{  
      layout_data :fill, :fill, true, true
      composite{
        grid_layout {
          num_columns 3
          make_columns_equal_width false
          margin_width 20
          margin_height 10
        }
        label{
          text "fieldname"
        }
        label{

          text "type"
        }

        label{

          text "value"
        }
        item["fields"].each do |field|
          label{
            text field[1]["name"]
          }
          label{
            text field[1]["type"]
          }
          label{
            text "to do"
          }
        end
    }
  }
  }.open
end


shell { |shell_proxy|
  minimum_size 800, 600
  row_layout :vertical
  
  text 'Wastewater Simulation'

  grid_layout {
    make_columns_equal_width false
    margin_width 0
    margin_height 0
    horizontal_spacing 0
  }

  jsondata.each {|item, index|
    button(){
      text item['tableName']
      on_widget_selected do
        createNewWindow(index, item)
      end
    }
  }

}.open
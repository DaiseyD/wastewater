require 'glimmer-dsl-libui'

include Glimmer

window('hello world', 300, 200) {
  button('Button') {
    on_clicked do
      msg_box('Information', 'You clicked the button')
    end
  }
}.show
puts "Hello World"
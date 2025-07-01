require 'glimmer-dsl-swt'

include Glimmer

shell { |shell_proxy|
  row_layout :vertical
  
  text 'Hello, Dialog!'
  
  7.times { |n|
    dialog_number = n + 1
    
    button {
      layout_data {
        width 200
        height 50
      }
      text "Dialog #{dialog_number}"
      
      on_widget_selected do
        # pass the shell proxy as a parent to make the dialog support hitting the escape button for closing alone without closing app
        dialog(shell_proxy) { |dialog_proxy|
          row_layout(:vertical) {
            center true
          }
          
          text "Dialog #{dialog_number}"
          
          label {
            text "Given `dialog` is modal, you cannot interact with the main window till the dialog is closed."
          }
          composite {
            row_layout {
              margin_height 0
              margin_top 0
              margin_bottom 0
            }

            label {
              text "Unlike `message_box`, `dialog` can contain arbitrary widgets:"
            }
            radio {
              text 'Radio'
            }
            checkbox {
              text 'Checkbox'
            }
          }
          button {
            text 'Close'
            
            on_widget_selected do
              dialog_proxy.close
            end
          }
        }.open
      end
    }
  }
}.open
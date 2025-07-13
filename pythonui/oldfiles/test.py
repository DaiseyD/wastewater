import tkinter as tk
from tkinter import ttk

# Set up a TKinter window
root = tk.Tk()
root.geometry('600x400')
root.title('Name Picker')
# Split window left/right
l_frm =ttk.Frame(root, width=300)
l_frm.pack(expand=True, fill='both', side='left')
l_frm.pack_propagate(0)

r_frm = ttk.Frame(root, width=300)
r_frm.pack(expand=True, fill='both', side='right')
r_frm.pack_propagate(0)

# Right side border
##in_frm = ttk.Frame(r_frm, borderwidth=3, relief='sunken')
##in_frm.pack(expand=True, fill='both')
# Output text
tk.Label(l_frm, text='This label is showing some text...'
        ).pack(expand=True, fill='both', side='left')

out_lbl = tk.Label(r_frm, bg='green', text='')
out_lbl.pack(expand=True, fill='both')

root.mainloop()
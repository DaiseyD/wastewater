import json
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def getjsondata():
    try:
        with(open("testcopy.json", "r")) as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        exit(1)
        
def expandTableInNewWindow(data, value):
    new_window = Toplevel(root, height=100, width=100)
    new_window.title(value['name'])
    new_window.columnconfigure(0, weight=2)
    new_window.rowconfigure(0, weight=2)
    columns = ["Name", "Type", "Value"]
    tree = ttk.Treeview(new_window, columns=columns, show='headings')
    tree.rowconfigure(0, weight=1)
    tree.columnconfigure(0, weight=1)
    i =0
    for field in value["fields"]:
        tree.insert('', END, values=(field["name"], field["type"], field["value"]))
        i = i + 1
    tree.grid(row=0, column=0, sticky=(N, W, E, S))
    new_window.geometry("1000x1000")

def setupLeftFrame(networkobject, parent):
    leftFrame = Frame(parent)
    leftFrame.grid(row=0, column=0, sticky=W)
    leftCanvas =Canvas(leftFrame, bg="cyan")
    leftCanvas.pack(side='left', fill=BOTH, expand=True)

    sb = Scrollbar(leftFrame, orient=VERTICAL, command=leftCanvas.yview)
    sb.pack(side='right', fill=Y)
    leftCanvas.configure(yscrollcommand=sb.set)

    labelowner = Canvas(leftCanvas)
    labelowner.bind("<Configure>",lambda e: leftCanvas.configure(scrollregion=leftCanvas.bbox("all")))
    leftCanvas.create_window(0,0, window=labelowner)
    for (index, item) in enumerate(networkobjectsdata):
        baseFrame = Frame(labelowner, borderwidth=3, relief="groove")
        baseFrame.pack(side='top')

        l= Label(baseFrame, text=item["name"])
        l.grid(column=0, row=index, sticky=E)
        i = index
        Button(baseFrame
                , text="Expand and edit"
                , command = lambda item = item :  expandTableInNewWindow(networkobjectsdata, item)).grid(column=1, row=networkobjectsdata.index(item), sticky=W)
        
def setupRightFrame(rainfalldata, root):
    rightframe = Frame(root, width=400, bg="red")
    rightframe.grid(row=0, column=1, sticky=E)
    for (index, item) in enumerate(rainfalldata):
        Label(rightframe, text=item['name']).grid(column=0, row=index, sticky=E)
        Checkbutton(rightframe).grid(column=1, row=index)

rawdata = getjsondata()
networkobjectsdata = rawdata["networkobjects"]

root = Tk()
root.geometry("800x600")
root.title("Waste simulation parameters")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

setupLeftFrame(networkobjectsdata, root)
setupRightFrame(rawdata['rainfallevents'], root)


root.mainloop()
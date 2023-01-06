#!/usr/bin/python
try:
	import pip
except:
    print("need to import pip");
    subprocess.call(python_exe +' Inputs/pip/get-pip.py --proxy="http://proxy-chain.intel.com:911"')
    import pip
from arrayFunctions import *
from guiBuild import *
import platform
	  
from tkinter import *
from tkinter import ttk
### For matplot lib not to crash in the exe file:
import ctypes
import sys

### Main Root
root = Tk()
root.title('Array Summary Tool')

mainframe = ttk.Frame(root, padding="150 150 150 150")
mainframe.grid(column=0, row=0, sticky=('news'))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

background_label = Label(mainframe)
background_label.place(relx=0.5, rely=0.5, anchor=CENTER)

#### Main buttons
# button_dicc = Button(mainframe, text="DICC data analysis", height = 1, width = 20, command = dicc, borderwidth = 4, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
# button_dicc.grid(row = 0, column = 2, rowspan = 1 )

button_vcc = Button(mainframe, text="Vmin plots", height = 1, width = 20, command = vminGUI, borderwidth = 4, bg = 'blue', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_vcc.grid(row = 1, column = 2, rowspan = 1 )

button_repair = Button(mainframe, text="Repair", height = 1, width = 20, command = repairGUI, borderwidth = 4, bg = 'purple', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_repair.grid(row = 2, column = 2, rowspan = 1 )

button_binning = Button(mainframe, text="Binning", height = 1, width = 20, command = arrayGUI, borderwidth = 4, bg = 'blue', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_binning.grid(row = 3, column = 2, rowspan = 1 )

button_tt = Button(mainframe, text="Test Time Kappa", height = 1, width = 20, command = ttGUI, borderwidth = 4, bg = 'purple', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_tt.grid(row = 4, column = 2, rowspan = 1 )

button_b98 = Button(mainframe, text="Bin98/99 Summary", height = 1, width = 20, command = bin9899GUI, borderwidth = 4, bg = 'blue', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_b98.grid(row = 5, column = 2, rowspan = 1 )
### Main loop
root.mainloop()
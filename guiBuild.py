from tkinter import *
from tkinter import ttk
from arrayFunctions import *
import os

def productCode(position,root1):
	textP = Label(root1,text='Please enter your product code, e.g. 8PQKCVN:',width=50, height=1)
	textP.grid(row=position,column=2,rowspan = 1)
	position += 1
	devStep = Entry(root1)
	devStep.grid(row=position,column=2,rowspan = 1)
	devStep.insert(0,'8PQKCVN')
	position += 1

	return position,devStep

def tpPath(position,root1):
	textP = Label(root1,text='Please enter the full path to your TP:',width=50, height=1)
	textP.grid(row=position,column=2,rowspan = 1)
	position += 1
	tpPath = StringVar(root1,value='I:\\program\\1274\\eng\\hdmtprogs\\adn_sds\\TestProgram\\ADNECJX61D2425UTDG')
	tpPathEntry = Entry(root1,textvariable=tpPath,width=100)
	tpPathEntry.grid(row=position,column=2,rowspan=1)
	position += 1

	return position,tpPath

def lotNumber(position, root1):
	textl = Label(root1,text='Please enter your lot number:',width=30, height=1)
	textl.grid(row=position,column=2,rowspan = 1)
	position += 1
	numLot = Entry(root1)
	numLot.insert(0,'3425C0T00')
	numLot.grid(row=position,column=2,rowspan = 1)
	position += 1
	
	return position,numLot

def getFlow(position,root1,flowOptions):
	textM = Label(root1,text='Please choose flow:', width=50, height=1)
	textM.grid(row=position,column=2,rowspan = 1)
		
	flow = StringVar(root1)
	position += 1
	dropF = OptionMenu(root1, flow, *flowOptions)
	dropF.grid(row=position,column=2,rowspan = 1)
	position += 1

	return position,flow

def getModule(position,root1):
	textM = Label(root1,text='Please specify your submodule:\nNote: memory can only handle one module at a time!\ne.g. "ARR_GRT"', width=50, height=3)
	textM.grid(row=position,column=2,rowspan = 1)
	
	position += 1
	module = Entry(root1)
	module.grid(row=position,column=2,rowspan = 1)
	module.insert(0,'ARR_GRT')
	position += 1

	return position,module

def getEmail(position,root1):
	textM = Label(root1,text='Please enter your email:', width=50, height=1)
	textM.grid(row=position,column=2,rowspan = 1)
	
	position += 1
	email = Entry(root1,width=30)
	email.grid(row=position,column=2,rowspan = 1)
	email.insert(0,'aoife.barnes@intel.com')
	position += 1

	return position,email

def getOperation(position,root1):
	textM = Label(root1,text='Please enter your operation, e.g. 119325:', width=50, height=1)
	textM.grid(row=position,column=2,rowspan = 1)
	
	position += 1
	oper = Entry(root1)
	oper.grid(row=position,column=2,rowspan = 1)
	oper.insert(0,'119325')
	position += 1

	return position,oper

def arrayGUI():
	master = Tk()
	master.title("Array Binning Summary")
	
	position=1
	position,devStep = productCode(position,master)
	position,email = getEmail(position,master)

	button = Button(master, text = "LET'S GO!", command = lambda: arraySummary(devStep.get(),email.get()))
	button.grid(row = 3, column = 2,rowspan = 1)

	master.mainloop()
	
def repairGUI():
	###Root sicc
	root1 = Tk()
	root1.title('Repair Rate Summary')
	tabControl = ttk.Notebook(root1)

	tab1 = ttk.Frame(tabControl)
	tab2 = ttk.Frame(tabControl)

	tabControl.add(tab1, text='MV Repair Summary')
	tabControl.add(tab2, text='Prod Repair Summary')
	tabControl.pack(expand=1, fill="both")
	
	### MV Repair comparison ###
	#########################################################################################################################
	i=1 # marker for the layout of GUI
	i,devStep = productCode(i,tab1)
	i,numLot = lotNumber(i,tab1)
	i,mail = getEmail(i,tab1)
	
	button = Button(tab1, text = "LET'S GO!", command = lambda: repairSummary(type="eng",devrevstep=devStep.get(),lotNum=numLot.get(),email=mail.get()))
	button.grid(row = i, column = 2,rowspan = 1)
	i += 1

	### Average 7-day Prod TT Summary per module ###
	#########################################################################################################################
	i,devStepProd = productCode(i,tab2)
	i,operProd = getOperation(i,tab2)
	i,mailProd = getEmail(i,tab2)
	buttonProd = Button(tab2, text = "LET'S GO!", command = lambda: repairSummary(type="prod",devrevstep=devStepProd.get(),operation=str(operProd.get()),email=mailProd.get()))
	buttonProd.grid(row = i, column = 2,rowspan = 1)

	root1.mainloop()

def prodRepairGUI(position,master,devStep):
	# Operation
	textT = Label(master,text= 'Please choose operation:',width=30, height=1)
	textT.grid(row=position,column=2,rowspan = 1)
	position += 1
	
	operations = ["132330","132331","132332","132322","132323","132324","132325","132326","119325"]
	global oper
	oper = StringVar(master)
	oper.set("119325")
	
	drop1 = OptionMenu(master, oper, *operations)
	drop1.grid(row=position,column=2,rowspan = 1)
	position += 1

	position,email = getEmail(position,master)

	button = Button(master, text = "LET'S GO!", command = lambda: repairSummary(type="prod",devrevstep=devStep.get(),operation=oper.get(),email=email.get()))
	button.grid(row = position, column = 2,rowspan = 1)

def engRepairGUI(position,master,devStep):
	# Lot Number
	global lotNum
	position,lotNum = lotNumber(position,master)
	position,email = getEmail(position,master)
	button = Button(master, text = "LET'S GO!", command = lambda: repairSummary(type="eng",devrevstep=devStep.get(),lotNum=lotNum.get(),email=email.get()))
	button.grid(row = position, column = 2,rowspan = 1)

def vminGUI():
	###Root sicc
	root1 = Tk()
	root1.title('Vmin Data Analysis')	

	i=1 # marker for position on GUI
	i,tpName = tpPath(i,root1)
	buttonTP = Button(root1, text = "Find my modules!", command = lambda: vminTP(i,root1,tpName.get()))
	buttonTP.grid(row = i, column = 2,rowspan = 1)

	root1.mainloop()

def vminTP(i,root1,path):
	flowOptions = ["PREHVQK","POSTHVQK","END"]
	moduleOptionsAll = os.listdir(path+"\\Modules")
	moduleOptions = [m for m in moduleOptionsAll if 'ARR_' in m]
	print("Found modules: ",moduleOptions)
	i += 1
	i,devStep = productCode(i,root1)
	i,numLot = lotNumber(i,root1)
	i,module,flow = moduleAndFlow(i,root1,moduleOptions,flowOptions)
		
	button = Button(root1, text = "LET'S GO!", command = lambda: vminPull(devStep.get(), numLot.get(),module.get(),flow.get()))
	button.grid(row = i, column = 2,rowspan = 1)
	
def ttGUI():
	###Root sicc
	root1 = Tk()
	root1.title('Test Time Analysis')
	tabControl = ttk.Notebook(root1)

	tab1 = ttk.Frame(tabControl)
	tab2 = ttk.Frame(tabControl)

	tabControl.add(tab1, text='MV Summary')
	tabControl.add(tab2, text='Average Prod TT Summary')
	tabControl.pack(expand=1, fill="both")
	
	### MV vs Prod TT comparison ###
	#########################################################################################################################
	flowOptions = ["BEGIN","PREHVQK","STRESS","POSTHVQK","END","SDTSTRESS","SDTEND"]

	i=1 # marker for the layout of GUI
	i,devStep = productCode(i,tab1)
	i,numLot = lotNumber(i,tab1)
	i,module = getModule(i,tab1)
	i,flow = getFlow(i,tab1,flowOptions)
	i,email = getEmail(i,tab1)
	
	button = Button(tab1, text = "LET'S GO!", command = lambda: ttPull(devStep.get(), numLot.get(),module.get(),flow.get(),email.get()))
	button.grid(row = i, column = 2,rowspan = 1)
	i += 1

	### Average 7-day Prod TT Summary per module ###
	#########################################################################################################################
	i,devStepProd = productCode(i,tab2)
	i,operationProd = getOperation(i,tab2)
	i,moduleProd = getModule(i,tab2)
	i,mailProd = getEmail(i,tab2)
	buttonProd = Button(tab2, text = "LET'S GO!", command = lambda: avgProdTTPull(devStepProd.get(),moduleProd.get(),operationProd.get(),mailProd.get()))
	buttonProd.grid(row = i, column = 2,rowspan = 1)

	root1.mainloop()

def chngGUI():
	root1 = Tk()
	root1.title('TP Changes Analysis')
	
	moduleOptions = ["ARR_CCF", "ARR_GRT", "ARR_MBIST"]
	flowOptions = ["BEGIN","PREHVQK","STRESS","POSTHVQK","END","SDTSTRESS","SDTEND"]

	i=1 # marker for the layout of GUI
	i,devStep = productCode(i,root1)
	i, numLot = lotNumber(i,root1)
	i,module,flow = moduleAndFlow(i,root1,moduleOptions,FlowOptions)	
	
	button = Button(root1, text = "LET'S GO!", command = lambda: chngPull(devStep.get(), numLot.get(),module.get(),flow.get()))
	button.grid(row = i, column = 2,rowspan = 1)

	root1.mainloop()

def bin9899GUI():
	root = Tk()
	root.title('Bin 98/99 Analysis')
	i=1

	i,devStep = productCode(i,root)
	i,oper = getOperation(i,root)
	i,module = getModule(i,root)
	i,mail = getEmail(i,root)

	button = Button(root, text = "LET'S GO!", command = lambda: bin9899Pull(devStep.get(),module.get(),oper.get(),mail.get()))
	button.grid(row = i, column = 2,rowspan = 1)

	root.mainloop()

def runAllGUI():
	root = Tk()
	root.title('Config set for multiple')
	tabControl = ttk.Notebook(root)

	tab1 = ttk.Frame(tabControl)
	tab2 = ttk.Frame(tabControl)

	tabControl.add(tab1, text='Engineering Analysis')
	tabControl.add(tab2, text='Production Analysis')
	tabControl.pack(expand=1, fill="both")

	flowOptions = ["BEGIN","PREHVQK","STRESS","POSTHVQK","END","SDTSTRESS","SDTEND"]

	###############################################
	##### TAB 1 : ENGINEERING ANALYSIS ON MVS #####
	###############################################
	engOptions = ['Test Time Analysis', 'Vmin Plots', 'Binning Summary', 'Repair Summary']
	selectedEngOptions =[]
	for x in range(len(engOptions)):
	    l = Checkbutton(tab1, text=engOptions[x], variable=engOptions[x],command=lambda x=engOptions[x]:selectedEngOptions.append(x))
	    l.grid(row=x,column=2,rowspan = 1)
	i = x+1

	i,engProductCode = productCode(i,tab1)
	i,engLotNum = lotNumber(i,tab1)
	i,engModule = getModule(i,tab1)
	i,engFlow = getFlow(i,tab1,flowOptions)
	i,engMail = getEmail(i,tab1)
	i,engOperation = getOperation(i,tab1)

	Button(tab1,text="Ok",command=lambda: selectAllPull('prod',selectedEngOptions,engProductCode.get(),engOperation.get(),engLotNum,engModule.get(),engFlow.get(),engMail.get())).grid(row=i,column=2,rowspan = 1)
	
	###############################################
	######### TAB 2 : PRODUCTION ANALYSIS #########
	###############################################
	prodOptions = ['Test Time Analysis','Repair Summary', 'Bin98/99 Summary']
	selectedprodOptions =[]
	for x in range(len(prodOptions)):
	    l = Checkbutton(tab2, text=prodOptions[x], variable=prodOptions[x],command=lambda x=prodOptions[x]:selectedprodOptions.append(x))
	    l.grid(row=x,column=2,rowspan = 1)
	i=x+1

	i,prodProductCode = productCode(i,tab2)
	i,prodModule = getModule(i,tab2)
	i,prodMail = getEmail(i,tab2)
	i,prodOperation = getOperation(i,tab2)

	Button(tab2,text="Ok",command=lambda: selectAllPull('prod',selectedprodOptions,prodProductCode.get(),prodOperation.get(),None,prodModule.get(),None,prodMail.get())).grid(row=i,column=2,rowspan = 1)
	
	root.mainloop()

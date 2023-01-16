import os
import os.path
import subprocess
try:
    import PyUber
except:
    print("need to import PyUber using pip");
    subprocess.call(python_exe + ' -m pip install pywin32 --proxy="http://proxy-chain.intel.com:911"')
    subprocess.call(python_exe + ' -m pip install https://github.intel.com/fabnet/PyUber/zipball/master --proxy="http://proxy-chain.intel.com:911"');
    import PyUber
import pandas as pd
import numpy as np
import win32com.client as win32 
import matplotlib.pyplot as plt
from sqlFunctions import *
from jmpPull import *
from datetime import date
from datetime import datetime
import time
#from empiricaldist import Cdf

########################################
########## CLEAN UP FUNCTIONS ##########
########################################
def splitTT(row):
	new = row['TESTTIME'].split('_')
	sizeNew = len(new[3])
	new = new[3]
	return float(new[:sizeNew-2])

########################################
######## SQL COLLECTION FUNCTION #######
########################################
def getSQL(devStep=None, site=None, typeOfPull=None, numLot=None, operation=None, wafer=None, selectModule=None,selectFlow=None):
	"""getSQL: takes multiple user inputs, creates SQL text files to pull data, outputs data into CSV and returns the CSV string as a dataframe
	Inputs:	devStep:		user specified product code, e.g. 8PQKCVN,
			site:			site to pull data from, is it prod or eng data?
			typeOfPull:		used to create SQL text files and CSV depending on what kind of data user has selected
			numLot:			user specified lot number
			operation:		user selected operation code
			selectModule:	only pull data from specific module
			selectFlow:		only pull data from specific flow
	"""
	# Initiate SQL data input and output paths
	source_path = os.path.dirname(os.path.realpath(__file__));
	sqlPullPath = source_path+"\\sqlTextFiles\\"+typeOfPull+"Pull.txt"
	sqlPullPathReplace = source_path+"\\sqlTextFiles\\"+typeOfPull+"PullReplace.txt"
	sqlOutputPath = source_path+"\\sqlOutputCSV\\"+typeOfPull+"SqlOutput.csv"
	
	# Rebuild SQL file based on user inputs
	rebuildSQLFile(devStep, numLot,selectModule, selectFlow, operation, wafer, sqlPullPath, sqlPullPathReplace)
	
	# Then we need to pull the data
	sqlBuildAndRun(site,sqlPullPathReplace, sqlOutputPath)
	rawData = pd.read_csv(sqlOutputPath)
	
	#Check if CSV file is empty - if so, exit out of program
	if(rawData.empty):
		print("This MV does not contain this module...\nPlease try again.")
	return rawData

########################################
############ MAILING SECTION ###########
########################################
def Emailer(dataArrayFrameBody,dataRepairFrameBody, subject, recipient):
	print("Sending email to "+recipient)
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = recipient
	mail.Subject = subject
	#mail.Body = '''Please find data attached and below.\n\n{}\n{}'''.format(dataArrayFrameBody.to_string(),dataRepairFrameBody)
	mail.HTMLBody = '''<h3>Please find data attached and below.</h3>{}<br>{}'''.format(dataRepairFrameBody.to_html(),dataArrayFrameBody.to_html())
	mail.send
	print('Email sent!')

def singleEmailer(dataFrameBody, subject, recipient):
	print("Sending email to "+recipient)
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = recipient
	mail.Subject = subject
	#mail.Body = '''Please find data attached and below.\n\n{}\n{}'''.format(dataArrayFrameBody.to_string(),dataRepairFrameBody)
	mail.HTMLBody = '''<h3>Please find data attached and below.</h3>{}'''.format(dataFrameBody.to_html())
	mail.send
	print('Email sent!')

def sendToExcel(df,tableType):
	source_path = os.path.dirname(os.path.realpath(__file__));
	today = date.today()
	now = datetime.now()
	d1 = today.strftime("%Y_%m_%d")
	dt_string = now.strftime("%H:%M:%S")
	sheetName = tableType + "("+dt_string+")"
	outputExcel = source_path+"\\generatedOutputs\\output_"+d1+".xlsx"

	with pd.ExcelWriter(outputExcel,mode='a') as writer:
		df.to_excel(writer,sheet_name=sheetName)
	print("Output saved to "+outputExcel)

#########################################
####### BINNING SUMMARY FUNCTIONS #######
#########################################
def arraySummary(devRevStep,email="aoife.barnes@intel.com"):
	"""arraySummary is a function called by the GUI with user inputs to create a binning summary from the last 3 weeks of engineering runs, and send to the user via email.
		Inputs:	devStep:		user input to specify product code.
	"""
	arrayCsvContent = getSQL(devStep = devRevStep, site='D1D', typeOfPull='array')
	finalArrayDF = createBinSummaryDF(arrayCsvContent)
	
	singleEmailer(finalArrayDF, 'Daily Array MV Summary', email)

def createBinSummaryDF(origDF):
	print("Creating array binning summary...")
	arrayBins = [1,2,3,21,52,61,62]
	arrayBinsOnly = origDF[origDF['INTERFACE_BIN'].isin(arrayBins)]
	# Create binning summary per MV
	new = arrayBinsOnly.groupby(['LOT','INTERFACE_BIN']).size()
	new_df = new.to_frame(name = 'BIN_COUNT').reset_index()
	newPivot = new_df.pivot(index='LOT',columns='INTERFACE_BIN').fillna(0).astype(int)
	## TODO: need to count all the die, not just the array bins for sum!! ##
	newPivot['Total Die'] = newPivot.apply(np.sum, axis=1)
	return newPivot

########################################	
####### REPAIR SUMMARY FUNCTIONS #######
########################################
def repairSummary(type="eng",devrevstep=None,operation=None,lotNum=None,email="aoife.barnes@intel.com"):
	"""repairSummary is a function called by the GUI with user inputs to create a repair rate summary from prod or from an MV, and send to the user via email. 
		The repair rate is calculated by the number of die that pass the post HRY instance in BEGIN over the number of die that fail the pre HRY instance (die sent for repair).
		Inputs:	type:			would the user like to pull data from production or from engineering
				devStep:		user input to specify product code,
				operation:		specify production operation code
	"""
	if type=="prod":
		print("Prod,",str(operation))
		repairCsvContent = getSQL(devStep=devrevstep,typeOfPull='prodRepair',site='F28',operation=str(operation))
		# Only select array bins of choice
		finalRepairDF = createRepairSummary(repairCsvContent)
		emailHeader = 'Daily Array MV Summary in Production for '+str(devrevstep)

	if type=="eng":
		repairCsvContent = getSQL(devStep=devrevstep,typeOfPull='repair',site='D1D',numLot=lotNum)
		# Only select array bins of choice
		finalRepairDF = createRepairSummary(repairCsvContent)
		emailHeader = 'Daily Array MV Summary for '+str(lotNum)
	
	singleEmailer(finalRepairDF, emailHeader, email)
	## TODO: automate email send to the current user ##

def createRepairSummary(origDF):
	"""createRepairSummary is a function to compute the repair rate per test instances in production for a given product. The function takes in a raw dataframe, computes the number of die sent for repair (pre HRY failures) and the number of die successfully repaired (post HRY pass rate).
		Inputs:	origDF:	a raw dataframe of data retrieved for all array repair instances in production for a given product
		Outputs:	outputDF:	dataframe containing repair rate summary to be sent to user
	"""
	print("Creating repair rate summary...")
	# Convert repair rate to string (mainly to handle errors)
	origDF['STRING_ALTERNATIVE'] = origDF['STRING_ALTERNATIVE'].apply(str)
	# Create a new column to tell whether a die has passed or failed
	origDF['Pass_Fail'] = origDF.apply(lambda row: categorise(row), axis =1)
	countRepairPerInstance = origDF.groupby(['TEST_NAME','Pass_Fail']).size() # create new DF grouped by result and test instance
	countRepairPerInstanceColumns = countRepairPerInstance.to_frame(name = 'REPAIR_COUNT').reset_index()
	# Keep only those die that have passed post HRY (successful repair) or failed pre HRY (sent for repair)
	countRepairPerInstanceColumns = countRepairPerInstanceColumns[((countRepairPerInstanceColumns.Pass_Fail=='P')&(countRepairPerInstanceColumns.TEST_NAME.str.contains("_POST_")))|((countRepairPerInstanceColumns.Pass_Fail=='F')&(countRepairPerInstanceColumns.TEST_NAME.str.contains("_PRE_")))]
	# Split the test name to remove the pre/post specification
	countRepairPerInstanceColumns['TEST_NAME'] = countRepairPerInstanceColumns.apply(lambda row: splitTestName(row), axis = 1)
	finalCountRepairPerInstance = countRepairPerInstanceColumns.pivot_table(index='TEST_NAME',columns='Pass_Fail',fill_value=0, aggfunc=np.sum) # pivot this table to get summary of repair results
	finalCountRepairPerInstance['Total Die'] = finalCountRepairPerInstance['REPAIR_COUNT']['F'] # add total number of die column
	finalCountRepairPerInstance['Repair Rate'] = 100*(finalCountRepairPerInstance['REPAIR_COUNT']['P'])/finalCountRepairPerInstance['Total Die'] # calculate repair rate
	outputDF = pd.DataFrame().assign(TestName=finalCountRepairPerInstance.reset_index()['TEST_NAME'], NumUnitRepaired = finalCountRepairPerInstance.reset_index()['REPAIR_COUNT']['P'], UnitsSentToRepair = finalCountRepairPerInstance.reset_index()['Total Die'], RepairPercent = finalCountRepairPerInstance.reset_index()['Repair Rate'])
	return outputDF

def categorise(row):
	if all(item=="0" for item in row['STRING_ALTERNATIVE']):
		return "P"
	else:
		return "F"

def splitTestName(row):
	new = row['TEST_NAME'].split('_')
	return '_'.join(new[0:11])
	
########################################	
######## VMIN SUMMARY FUNCTIONS ########
########################################
def vminPull(devStep, numLot, selectModule,selectFlow):
	"""vminPull is a function called by the GUI with user inputs and build a CSV file containing vmin info from an MV to be used later for plots.
		Inputs:	devStep:		user input to specify product code,
				numLot:			MV lot number, specified by user,
				selectModule:	module selected by user to review,
				selectFlow:		Flow selected by user to review.
	"""
	source_path = os.path.dirname(os.path.realpath(__file__));
	vminCSVPath = source_path+"\\sqlOutputCSV\\"+"vminCSV.csv"
	# Pull SQL data
	vminRawData = getSQL(devStep=devStep, site="D1D", typeOfPull="vmin",numLot=numLot, selectModule=selectModule,selectFlow=selectFlow)
	# Collect data and build CSV that has been filtered correctly
	vminTestNames = vminCollectCSV(vminCSVPath, vminRawData)
	jmpPlot(testNames,vminCSVPath) # plot vmin in JMP

def vminCollectCSV(vminCSVPath, vminRawData):
	# Create path to write CSV

	# Create new dataframe
	vminData = pd.DataFrame()
	# Check if data is string format, e.g. 0.5|0.6..., or integer. 
	if isinstance(vminRawData,str): # if string, split string and convert to integer
		vminData['VMIN']=vminRawData['VMIN'].str.split('|').str[0]
		vminData['TEST_NAME'] = vminRawData['TEST_NAME']
	else:
		vminData = vminRawData[['TEST_NAME','VMIN']]
	# Remove SD and ADTL data
	vminData = vminData[vminData['TEST_NAME'].str.contains("::ADTL")==False]
	vminData = vminData[vminData['TEST_NAME'].str.contains("::SD")==False]
	vminData = vminData[vminData['VMIN']>0] # Removing all negative values, e.g. -999s, etc.
	vminData.to_csv(vminCSVPath)
	print("Vmin data written to CSV file.")
	# Get test names from data frame
	return vminData['TEST_NAME'].values.tolist()	

########################################
###### TESTTIME SUMMARY FUNCTIONS ######
########################################
def avgProdTTPull(devStep,module,oper,mail="aoife.barnes@intel.com"):
	"""avgProdTTPull is a function called by the GUI with user inputs and build a testtime summary of over the last 5 days in production to get an average GDTT and BDTT per module
		Inputs:	devStep:user input to specify product code,
				module:	module selected by user to review.
	"""
	start_time = time.time()

	# Get a list of lots and take a random sample of 3 lots
	lotList = getSQL(devStep=devStep, site="F28", operation=oper, typeOfPull="lot")
	smallLotList = lotList.sample(n=3)	
	lotListString = "','".join(smallLotList['LOT'].to_list())

	waferList = getSQL(devStep=devStep, site="F28", operation=oper, numLot=lotListString, typeOfPull="wafer")
	waferList = waferList.applymap(str)
	smallWaferListTop = waferList.groupby('LOT').head(2).reset_index(drop=True)
	smallWaferListBottom = waferList.groupby('LOT').tail(2).reset_index(drop=True)
	waferListString = "','".join(smallWaferListTop['WAFER_ID'].to_list())
	waferListString = waferListString+"','".join(smallWaferListTop['WAFER_ID'].to_list())

	print("Parsing production TT data... this could take a few moments. Please be patient with me :)\n",lotListString)
	avgttRawData = getSQL(devStep=devStep, selectModule=module, numLot=lotListString, operation=oper, wafer=waferListString, site="F28", typeOfPull="avgProdTT")
	avgttRawData['TESTTIME'] = avgttRawData.apply(lambda row: splitTT(row), axis = 1)
	print("Testtime per module now available")
	# Find the sum of the TT per die
	ttRawDataPerDie = avgttRawData.groupby(['LOT','WAFER_ID','X','Y','IB'],as_index=False)['TESTTIME'].sum()
	print(ttRawDataPerDie)
	# Separate sum in GD vs BD
	gdTTDataPerDie = ttRawDataPerDie.loc[ttRawDataPerDie['IB'] < 8]
	bdTTDataPerDie = ttRawDataPerDie.loc[ttRawDataPerDie['IB'] >= 8]

	# Get the GDTT / BDTT avg, median & std dev
	avgGDTT = gdTTDataPerDie['TESTTIME'].mean()
	avgBDTT = bdTTDataPerDie['TESTTIME'].mean()
	medGDTT = gdTTDataPerDie['TESTTIME'].median()
	medBDTT = bdTTDataPerDie['TESTTIME'].median()
	stdGDTT = gdTTDataPerDie['TESTTIME'].std()
	stdBDTT = bdTTDataPerDie['TESTTIME'].std()

	# Tabulate neatly
	outputTable = {'Avg Testtime':[avgGDTT,avgBDTT],'Median Testtime':[medGDTT,medBDTT],'STD Testtime':[stdGDTT,stdBDTT]}
	outputDF = pd.DataFrame(outputTable,index=["GDTT","BDTT"])

	emailHeader = 'Average 7-day TT for '+str(module)
	singleEmailer(outputDF, emailHeader, mail)

	print("My program took ", (time.time()-start_time)/60, " minutes to run")
	#sendToExcel(outputDF,"Avg TT Summary Prod")

def ttPull(devStep, numLot, selectModule, selectFlow,userEmail):
	"""ttPull is a function called by the GUI with user inputs and build a testtime summary of an MV vs the latest TP in prod, and send to the user via email
		Inputs:	devStep:		user input to specify product code,
				numLot:			MV lot to compare to latest prod TP, specified by user,
				selectModule:	module selected by user to review,
				selectFlow:		Flow selected by user to review.
	"""
	ttRawData = getSQL(devStep=devStep, site="D1D", typeOfPull="tt",numLot=numLot, selectModule=selectModule,selectFlow=selectFlow)
	ttRawProdData = getSQL(devStep=devStep, site="F28", typeOfPull="ttProd",numLot='%', selectModule=selectModule,selectFlow=selectFlow)
	
	tpName, ttOut = ttComparison(ttRawData, ttRawProdData)
	emailHeader = 'TT Comparison of '+str(numLot)+' against prod data for '+tpName
	
	singleEmailer(ttOut, emailHeader, userEmail)
	
def ttComparison(mvDF, prodDF):
	"""ttComparison is a function to collect testtime data from an MV and compare against the latest TP in production. It returns a clean merged table of both eng/prod outputs along with a comparison of the TT mean.
	Inputs:	mvDF:	dataframe containing data from the eng MV,
			prodDF:	dataframe containing data from production.

	Outputs:	tpName:		output the latest TP name in production from which TT data has been used for analysis
				mergedDF:	output of the merged data table with eng, prod and comparison data to be sent to user
	"""
	print("Creating a testtime comparison...")
	prodDF['TESTTIME_PROD'] = prodDF.apply(lambda row: splitTT(row), axis = 1)
	tpName = prodDF['PROGRAM_NAME'][0]
	print(tpName)
	mvDF['TESTTIME_MV'] = mvDF.apply(lambda row: splitTT(row), axis = 1)
	avgProd = prodDF.groupby('TEST_NAME').agg({'TESTTIME_PROD': ['mean','min','max']})
	avgMV = mvDF.groupby('TEST_NAME').agg({'TESTTIME_MV': ['mean','min','max']})
	mergedDF = pd.merge(left=avgMV, right=avgProd, how='outer', on='TEST_NAME')
	#mergedDF = avgMV.compare(avgProd, result_names=("MV","Prod"))
	mergedDF['Diff_mean'] = mergedDF['TESTTIME_MV']['mean']-mergedDF['TESTTIME_PROD']['mean']
	return tpName,mergedDF


########################################
##### TP CHANGE SUMMARY FUNCTIONS ######
########################################
def chngPull(devStep, numLot, selectModule, selectFlow):
	"""chngPull is a function called by the GUI with user inputs to build a TP change summary of an MV vs the latest TP in prod, and send to the user via email
		Inputs:	devStep:		user input to specify product code,
				numLot:			MV lot to compare to latest prod TP, specified by user,
				selectModule:	module selected by user to review,
				selectFlow:		Flow selected by user to review.
	"""
	ttRawData = getSQL(devStep=devStep, site="D1D", typeOfPull="tt",numLot=numLot, selectModule=selectModule,selectFlow=selectFlow)
	ttRawProdData = getSQL(devStep=devStep, site="F28", typeOfPull="ttProd",numLot='%', selectModule=selectModule,selectFlow=selectFlow)
	
	tpName, ttOut = ttComparison(ttRawData, ttRawProdData)
	emailHeader = 'TT Comparison of '+str(numLot)+' against prod data for '+tpName
	
	singleEmailer(ttOut, emailHeader, 'aoife.barnes@intel.com')


########################################
######### Bin 98/99 FUNCTIONS ##########
########################################
def bin9899Pull(devStep, selectModule, operation, mail='aoife.barnes@intel.com'):
	"""chngPull is a function called by the GUI with user inputs to build a TP change summary of an MV vs the latest TP in prod, and send to the user via email
		Inputs:	devStep:		user input to specify product code,
				numLot:			MV lot to compare to latest prod TP, specified by user,
				selectModule:	module selected by user to review,
				selectFlow:		Flow selected by user to review.
	"""
	bin9899RawData = getSQL(devStep=devStep, site="F28", typeOfPull="bin9899",numLot='%', selectModule=selectModule,operation=operation)
	
	
	emailHeader = 'Bin 98/99 Analysis for '+str(devStep)
	
	singleEmailer(bin9899RawData, emailHeader,mail)


########################################
######### Config Set FUNCTIONS #########
########################################
def selectAllPull(engOrProd,pullTypeList,devStep,operation,lotNum,selectModule,selectFlow,userEmail='aoife.barnes@intel.com'):
	if engOrProd=='eng':
		for pullType in pullTypeList:
			if pullType=='Test Time Analysis':
				ttPull(devStep, lotNum, selectModule, selectFlow,userEmail)
			elif pullType=='Vmin Plots':
				vminPull(devStep, lotNum, selectModule,selectFlow)
			elif pullType=='Binning Summary':
				arraySummary(devStep,userEmail)
			elif pullType=='Repair Summary':
				repairSummary(engOrProd,devStep,operation,lotNum,userEmail)
			else:
				print("Invalid choice")
	elif engOrProd=="prod":
		for pullType in pullTypeList:
			if pullType=='Test Time Analysis':
				avgProdTTPull(devStep,selectModule,operation,userEmail)
			elif pullType=='Repair Summary':
				repairSummary(engOrProd,devStep,operation,lotNum,userEmail)
			elif pullType=='Bin98/99 Summary':
				bin9899Pull(devStep, selectModule, operation, userEmail)
			else:
				print("Invalid choice")
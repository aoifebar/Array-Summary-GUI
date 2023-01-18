try:
    import PyUber
except:
    print("need to import PyUber using pip");
    subprocess.call(python_exe + ' -m pip install pywin32 --proxy="http://proxy-chain.intel.com:911"')
    subprocess.call(python_exe + ' -m pip install https://github.intel.com/fabnet/PyUber/zipball/master --proxy="http://proxy-chain.intel.com:911"');
    import PyUber

def sqlBuildAndRun(sourceSite, sqlPullPath, sqlOutputPath):
	"""sqlBuildAndRun uses an SQL text file to pull data from a specificed ARIES/XEUS site and feeds the output into a CSV file
		Inputs:	sourceSite:		specify whether you are pulling data from prod site or eng site, e.g. D1D, F28
				sqlPullPath:	path to text file with SQL pull code
				sqlOutputPath:	path to send the output data to
	"""
	print("Reading sql " + str(sqlPullPath.resolve()))
	with open(sqlPullPath, 'r') as file : # Read in the default sql script
		uberScript = file.read()
	
	print("SQL Ready to Run, letsago");
	conn = PyUber.connect(datasource=("%s_PROD_ARIES" % sourceSite));

	curr = conn.cursor();
	curr.execute(uberScript);
	curr.to_csv(sqlOutputPath);
	print("SQL complete! Written to "+str(sqlOutputPath.resolve()));

def rebuildSQLFile(devstep = None, lotNum=None, module=None, flow=None, operation=None, wafer=None, sqlPullPathBlank=None, sqlPullPath=None):
	""" rebuildSQLFile creates a new SQL text file from user inputs to enable correct SQL pull
		Inputs:	devstep:			default=None, specifies product code, e.g. 8PQKCVN
				lotNum				default=None, specifies MV lot number
				module:				default=None, if a specific module needs to be searched
				flow:				default=None, if a specific flow needs to be searched
				sqlPullPathBlank:	default=None, initial SQL file befores changes, this file contains "####<input>####" that need to be replaced
				sqlPullPath:		default=None, rebuilt SQL file that will be used for SQL pull, this file has all the "####<input>####" replaced by user inputs
	"""
	print("Rebuilding SQL file for user inputs.")
	with open(sqlPullPathBlank, 'r') as file : # Read in the default sql script
		initialScript = file.read()
	
	# Rewrite SQL text file	
	with open(sqlPullPath, 'w') as writeFile:
		fileToWrite = initialScript
		if devstep is not None:
			fileToWrite = fileToWrite.replace("####DEVREVSTEP####",devstep)
		if lotNum is not None:
			fileToWrite = fileToWrite.replace("####LOT####",lotNum)
		if module is not None:
			fileToWrite = fileToWrite.replace("####MODULE####",module)
		if operation is not None:
			fileToWrite = fileToWrite.replace("####OPERATION####",operation)
		if wafer is not None:
			fileToWrite = fileToWrite.replace("####WAFER####",wafer)
		if flow is not None:
			fileToWrite = fileToWrite.replace("####FLOW####", flow)
		if(module=='ARR_MBIST' or flow=='END'):
			fileToWrite = fileToWrite.replace("--####MBIST/END####", '')
		else:
			fileToWrite = fileToWrite.replace("--####PBIST####", '')
		writeFile.write(fileToWrite)
	
import sys
import xml.etree.ElementTree
import os
import csv
import subprocess
from os.path import expanduser
import itertools
import operator
import numpy as np
import os
from pathlib import Path

def __init__():
    letsgo=1;

def jmpPlot(listOfTests, csvVminPath,selectModule,selectFlow):
	print("Setting up jmp files")
	home = os.path.expanduser("~");
	sourcePath = os.path.dirname(os.path.realpath(__file__));
	
	jmpScriptToEdit = sourcePath+"\\jmpFiles\\vminPlotRead.jsl"
	jmpScriptToWrite = sourcePath+"\\jmpFiles\\vminPlotWrite.jsl"
	jmpScriptToRun = Path(r".\jmpFiles\vminPlotWrite.jsl")
	jmpSaveDir = sourcePath+"\\jmpFiles\\vminPlots"
	
	if (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\11\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\11\\jmp.exe";
	elif (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\12\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\12\\jmp.exe";
	elif (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\13\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\13\\jmp.exe";
	elif (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\14\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\14\\jmp.exe";
	    print("I have not fully validated JMP 14, so if it breaks... I blame them and them alone.");
	else:
	    print("You don't have JMP 11-13, you're pretty screwed :( ");
	
	## need to point to and take in the correct jsl for the analysis
	    ### This function takes the list of supplies and uses them to plug lists into the jmp script, which should enable greatness
	print("Editing Jmp File");
	supplyList = [];
	
	with open(jmpScriptToEdit, 'r') as file : # Read in the default sql script
	    jmpScript = file.read()
	    
	jmpScript = jmpScript.replace('###RAWDATA###', csvVminPath);
	jmpScript = jmpScript.replace('###SAVEDIR###', jmpSaveDir);
	jmpScript = jmpScript.replace('###TEST_NAMES###', '",\n"'.join(listOfTests));
	jmpScript = jmpScript.replace('###MODULE###', selectModule);
	jmpScript = jmpScript.replace('###FLOW###', selectFlow);
	
	with open(jmpScriptToWrite, 'w') as file: # Write the file out again
	    file.write(jmpScript);
	
	print("Done editing Jmp File");
	
	print("Kicking off JMP. Fingers crossed");
	checkSource = os.path.splitdrive(home);
	if(checkSource[0] == r"C:"):
	    print("Running jmp from local computer");
	    #os.system(str(jmpScriptToRun));
	    subprocess.call("JMPbackgroundcaller.exe "+str(jmpScriptToRun),shell=False);
	else:
	    print("I am so confused, what madness is this running from not the C drive. Plz review/fix/hack around me");
	
	print("JMP Run complete!");

def jmpRepeatabilityPlot(listOfTests, csvVminPath,selectModule):
	print("Setting up jmp files")
	home = os.path.expanduser("~");
	sourcePath = os.path.dirname(os.path.realpath(__file__));
	
	jmpScriptToEdit = sourcePath+"\\jmpFiles\\vminRepeatabilityPlotRead.jsl"
	jmpScriptToWrite = sourcePath+"\\jmpFiles\\vminRepeatabilityPlotWrite.jsl"
	jmpScriptToRun = Path(r".\jmpFiles\vminRepeatabilityPlotWrite.jsl")
	jmpSaveDir = sourcePath+"\\jmpFiles\\vminPlots"
	
	if (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\11\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\11\\jmp.exe";
	elif (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\12\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\12\\jmp.exe";
	elif (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\13\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\13\\jmp.exe";
	elif (os.path.exists("C:\\Program Files\\SAS\\JMPPRO\\14\\jmp.exe")):
	    jmpdir = "C:\\Program Files\\SAS\\JMPPRO\\14\\jmp.exe";
	    print("I have not fully validated JMP 14, so if it breaks... I blame them and them alone.");
	else:
	    print("You don't have JMP 11-13, you're pretty screwed :( ");
	
	## need to point to and take in the correct jsl for the analysis
	    ### This function takes the list of supplies and uses them to plug lists into the jmp script, which should enable greatness
	print("Editing Jmp File");
	supplyList = [];
	
	with open(jmpScriptToEdit, 'r') as file : # Read in the default sql script
	    jmpScript = file.read()
	    
	jmpScript = jmpScript.replace('###RAWDATA###', csvVminPath);
	jmpScript = jmpScript.replace('###SAVEDIR###', jmpSaveDir);
	jmpScript = jmpScript.replace('###TEST_NAMES###', '",\n"'.join(listOfTests));
	jmpScript = jmpScript.replace('###MODULE###', selectModule);
	
	with open(jmpScriptToWrite, 'w') as file: # Write the file out again
	    file.write(jmpScript);
	
	print("Done editing Jmp File");
	
	print("Kicking off JMP. Fingers crossed");
	checkSource = os.path.splitdrive(home);
	if(checkSource[0] == r"C:"):
	    print("Running jmp from local computer");
	    #os.system(str(jmpScriptToRun));
	    subprocess.call("JMPbackgroundcaller.exe "+str(jmpScriptToRun),shell=False);
	else:
	    print("I am so confused, what madness is this running from not the C drive. Plz review/fix/hack around me");
	
	print("JMP Run complete!");
	print("Plots are available in "+jmpSaveDir+"_distros_"+selectModule+"_Repeatability.jrn");
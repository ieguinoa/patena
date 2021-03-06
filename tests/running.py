import operator
import os
import errno
from math import *
import sys
from os.path import isfile
from itertools import *
import numpy as np
import string
sys.path.insert(0, 'graphics')   #GRAPHICS FUNCTIONS


def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


#####CREATE RESULTS DIRS
try:
    os.makedirs(getScriptPath()+"/Results")
except OSError as exc: 
    if exc.errno == errno.EEXIST and os.path.isdir(getScriptPath()+"/Results"):
        pass
      
      
      

#***********************************************************************

def printHelp():
  print endl + "The usage mode is: "


#***********************************************************************


def getRunCommand(outPath,beta,length=None,seq=None):
  if seq==None and length!=None:   #RANDOM SEQUENCE 
    return 'python ../bleach.py --nopasta --testoutput ' + outPath + ' --length ' + str(length) + ' --beta ' + str(beta)  
  elif seq!=None and length==None:   #DEFINED SEQUENCE
    return 'python ../bleach.py --nopasta --testoutput ' + outPath + ' --seq '+  seq + ' --beta ' + str(beta)  
  else:
    print 'ERROR: Attempting a wrong execution format' 
    exit()
    
#***********************************************************************
#************************** Global Variables ***************************
#***********************************************************************

endl = "\n"
tab = "\t"
defaultBeta=2.0 # DEFAULT BETA VALUE
length=50   #DEFAULT LENGTH VALUE

timeTest=False
betaTest=False
divergenceTest=False
#scoreTest=False
#mutAttemptTest=False



#  EXECUTION Id . Identify runs
exeId=os.getpid() 


#************************
#Folders and files names:
#************************
#PATHS
basePath=getScriptPath() + '/'
baseOutputPath= basePath + 'Results/'




# NATURAL SEQUENCES FOR TESTS
naturalSeq=[]
#HAEMOGLOBIN
naturalSeq.append("MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG")  

#INSULIN
naturalSeq.append("MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN")

#HISTONE H1
naturalSeq.append("MTENSTSAPAAKPKRAKASKKSTDHPKYSDMIVAAIQAEKNRAGSSRQSIQKYIKSHYKVGENADSQIKLSIKRLVTTGVLKQTKGVGASGSFRLAKSDE")


naturalLinker='NEVSSPEIIRQHLANHPAATHTKAVALGTEETQTTIQRPRSEPDTGNPCHTTKLLHRDSVDSAPILTAFNSSHKGRINCNSN'


#*********************
#***DEFAULT VALUES***
#*******************



#********************************
#***** CHECK INPUT PARAMETERS **
#******************************

for i in range(1,len(sys.argv)):
  arg = sys.argv[i]
  if (arg=='--beta' or arg== '-b'):
    #TEST BETA vs ITERATIONS-TIME
    betaTest=True

  elif (arg=='--time' or arg== '-t'):
    #TEST total time vs sequence length
    timeTest=True  
  
  elif (arg=='--length' or arg== '-l'):
    #DEFINE SEQUENCE LENGTH (USED IN SOME OF THE TESTS)
    length= sys.argv[i+1] 

  elif (arg=='--divergence' or arg== '-d'):
   divergenceTest=True


      
#***********************************************************************
#************************** TESTING BETA VALUES ************************
#***********************************************************************

if betaTest:
	outputPath=baseOutputPath + 'test-beta-'+ str(exeId) 
	os.mkdir(outputPath)
	for betaValue in np.arange(2.0,2.5,0.1):  #NUMBER OF BETA VARIATIONS
		#betaValue= 1.0 + (0.5*value)  
		
		#FIRST MAKE 3 TESTs WITH RANDOM SEQs
		for x in range(3):
		  runCommand=getRunCommand(outputPath,betaValue,length)
		  #runCommand ='python bleach.py --beta ' + str(betaValue) +  " --length " + str(length) + ' --nopasta --testoutput ' + outputPath
		  print runCommand
		  os.system(runCommand)
		  
		#THEN 3 MORE TESTs WITH NATURAL SEQs	
		for x in range(3):
		  runCommand=getRunCommand(outputPath,betaValue,seq=naturalSeq[x][:length])
		  print runCommand
		  os.system(runCommand)
			
			
			
			
      
      
      
#***********************************************************************
#************************** TESTING TIMES    ***************************
#***********************************************************************

if timeTest:
  beta=defaultBeta
  outputPath=baseOutputPath + 'test-time-'+ str(beta) + '-'+ str(exeId)
  os.mkdir(outputPath)
  #for length in([5] + range(10,60,10)):
  for length in range(10,60,10):
    for x in range(3):  # 3 execution with random seqs
      runCommand=getRunCommand(outputPath, beta, length)
      print runCommand
      os.system(runCommand)
    for x in range(3):  #3 executions with 
      runCommand=getRunCommand(outputPath, beta, seq=naturalSeq[x][:length])
      print runCommand
      os.system(runCommand)


    
if divergenceTest:
   beta=defaultBeta
   length=30
   seq=naturalSeq[1][:length]
   outputPath=baseOutputPath + 'test-divergence-beta-' + str(beta) + '-' +str(exeId)
   os.mkdir(outputPath)
   for iteration in range(0,60):
	runCommand='python ../bleach.py --minoutput ' + outputPath + ' --seq '+  seq + ' --beta ' + str(beta)
        #print runCommand
 	os.system(runCommand)			

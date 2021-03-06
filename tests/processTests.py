import operator
import os
import errno
from math import *
import urllib2
import StringIO
import sys
import sys
from os.path import isfile
from itertools import *
import numpy as np
import string
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde
#import statistics
sys.path.insert(0, 'graphics')   #GRAPHICS FUNCTIONS
import glob
from graphs import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  	FROM BETA TEST, PLOT:
#		-SCATTER EACH TOTAL TIME IN TIME vs BETA PLOT (DIFFERENT COLOR FOR RAND/SEQ)
#		-SCATTER SCORE vs STEP# FOR A FEW DIFFERENT BETA VALUES(SHOULD I PUT A LIMIT IN STEP# AXIS?)
#		-SCATTER MUTAttempts vs 
#def processBetaTestResults2(basePath):
  #xSeqValues,ySeqValues=[],[]
  #xRandValues,yRandValues=[],[]
  #iterations,mutAttempts,stepScores, colorValues=[],[],[],[]
  #for files in os.listdir(basePath):
    #randomSeq=False
    #if not(files.endswith('.png')):
  ##CHANGE THIS LOOP FOR  
  ##for filename in glob.glob(os.path.join(basePath, '*.out')):
  ##AND CHANGE THE TESTOUTPUT IN BLEACH
      #with open(basePath+'/'+files,'r') as rawdata:
	#betaValue=0.0
	#time=0.0 #default value(in case the execution has not finished)
	#for lines in rawdata.readlines():
	  #cols=lines.split('\t')
	  ##print cols
	  #if cols[0]=='RAND' or cols[0]=='SEQ':
	    #if cols[0]=='RAND':
	      #randomSeq=True
	    #else:
	      #randomSeq=False
	    #betaValue=float(cols[1])
	  #if cols[0]=='END':
	    #time=float(cols[1])
	  #if cols[0]=='LOOP1' or cols[0]=='LOOP2':
	    #if betaValue==0.5:
	      #mutAttempts.append(int(cols[2]))
	      #stepScores.append(float(cols[3]))
	      #iterations.append(int(cols[1]))
	      ##colorValues.append(int(betaValue*35))
	      #colorValues.append('red')
	      ##the iteration time is stored in cols[4] 
	    ##if betaValue==1.0:
	      ##mutAttempts.append(int(cols[2]))
	      ##stepScores.append(float(cols[3]))
	      ##iterations.append(int(cols[1]))
	      ###colorValues.append(int(betaValue*35))
	      ##colorValues.append('blue')
	    #if betaValue==1.5:
	      #mutAttempts.append(int(cols[2]))
	      #stepScores.append(float(cols[3]))
	      #iterations.append(int(cols[1]))
	      ##colorValues.append(int(betaValue*35))
	      #colorValues.append('green')
	    #if cols[0]=='LOOP2':
		#print 'AT LEAST 1 REACHED SECOND LOOP'
	#if time>7000:
	  #time=7000
	##if betaValue==0.4 and time>3000:
	  ##print files
	#if randomSeq:
	  #xRandValues.append(betaValue)	  
	  #yRandValues.append(time) 
	#else:
	  #xSeqValues.append(betaValue)
	  #ySeqValues.append(time)
	##if betaValue==0.0:
	  ##print files
    #params = {
	  #'xlabel': u"Beta values",
	  #'ylabel': u"Total time [s]",
	  #'xRandValues': xRandValues,
	  #'xSeqValues': xSeqValues,
	  #'yRandValues':yRandValues,
	  #'ySeqValues':ySeqValues,
	  #'filename': basePath+'/beta-vs-time-length50.png',
	  #'title': 'Sequence length=50'
      #}	
    #scatterGraphBinaryColour(**params)
   



#  	FROM TIME TEST, PLOT:
#		-SCATTER EACH TOTAL TIME IN TIME vs LENGTH PLOT (DIFFERENT COLOR FOR RAND/SEQ)
#		-
#		-
def processTimeTestResults(basePath):
  xSeqValues,ySeqValues=[],[]   
  xRandValues,yRandValues=[],[]
  iterations,colorValues,mutAttempts,stepScores=[],[],[],[]
  for files in os.listdir(basePath):
    randomSeq=False
    if not(files.endswith('.png')):
      with open(basePath+'/'+files,'r') as rawdata:
	time=0.0 #default value(in case the execution has not finished)
	length=0
	for lines in rawdata.readlines():
	  cols=lines.split('\t')
	  #print cols
	  if cols[0]=='RAND' or cols[0]=='SEQ':
	    if cols[0]=='RAND':
	      randomSeq=True
	    else:
	      randomSeq=False
	    betaValue=float(cols[1])  
	    length=float(cols[2])
            print length
	  if cols[0]=='END':
	    time=float(cols[1])/60.0
	    print time
	  if cols[0]=='LOOP1' or cols[0]=='LOOP2':
	    colorValues.append(int(betaValue*35))
	    iterations.append(int(cols[1]))
	    mutAttempts.append(int(cols[2]))
	    stepScores.append(float(cols[3]))
	    #the iteration time is stored in cols[4] 
	    if cols[0]=='LOOP2':
	      print 'AT LEAST 1 REACHED SECOND LOOP'
	if randomSeq:
	  xRandValues.append(length)	  
	  yRandValues.append(time) 
	else:
	  xSeqValues.append(length)
	  ySeqValues.append(time)
    params = {
	  'xlabel': u"Sequence length",
	  'ylabel': u"Total time [min]",
	  'xRandValues': xRandValues,
	  'xSeqValues': xSeqValues,
	  'yRandValues':yRandValues,
	  'ySeqValues':ySeqValues,
	  'filename': basePath+'/seqLength-vs-time-beta1.png',
	  'title': 'Beta value = 1.0'
      }	
    scatterGraphBinaryColour(**params)



###################################################
####    PROCESS BETA TESTS RESULTS AND PLOT: ######
####    BETA(x)   vs  NUMBER OF ITERATIONS + NUMBER OF MUT. ATTEMPTS  ##########
####    MEAN TIMES, INCLUDES ERROR      ###########
###################################################

def makeBetaVsIteration(basePath):
  betaSeqDictTime,betaRandDictTime={},{}  #save pairs (beta-[list of times])
  betaIterations,betaMutAttempts,betaMutAttemptsPerIteration={},{},{}  #save pairs (beta-[list of iterations/mutAttempts])
  #iterations,mutAttempts,stepScores, colorValues=[],[],[],[]
  excludeList=[0.6,0.7,0.8,0.9,1.1,1.2,1.3,1.4,1.6,1.7,1.8,1.9,2.1,2.2,2.4]
  for files in os.listdir(basePath):
    randomSeq=False
    if not(files.endswith('.png')):
      with open(basePath+'/'+files,'r') as rawdata:
        betaValue=0.0
	iterations=0
	mutAttempts=0
        time=200.0 #default value(in case the execution has not finished)

        #PROCESS FILE: SAVE BETA VALUE, RAND/NATURAL AND ELAPSED TIME
        for lines in rawdata.readlines():
          cols=lines.split('\t')
          #print cols
          if cols[0]=='RAND' or cols[0]=='SEQ':
            betaValue=float(cols[1])
            if cols[0]=='RAND':
              randomSeq=True
            else:
              randomSeq=False
          if cols[0]=='END':
            time=float(cols[1])/60.0
            #if time>5000:
              #time=5000
	  if cols[0]=='LOOP1' or cols[0]=='LOOP2':	
      		iterations+=1
		mutAttempts+=float(cols[2])
 	
	#if iterations>5000:
	#	iterations=5000
	#print str(mutAttempts) + str(files)
	if mutAttempts > 15000:
		mutAttempts=15000
	#SAVE EXECUTION DATA IN DICTIONARIES
        if betaValue not in excludeList:
	  #print betaValue
	  #print mutAttempts
	  if betaValue in betaIterations:
		betaIterations[betaValue].append(iterations)
		betaMutAttempts[betaValue].append(mutAttempts)
		betaMutAttemptsPerIteration[betaValue].append(mutAttempts/iterations)
	  else:
		betaIterations[betaValue]=[iterations]	
		betaMutAttempts[betaValue]=[mutAttempts]	
		betaMutAttemptsPerIteration[betaValue]=[mutAttempts/iterations]
          if randomSeq:
            if betaValue in betaRandDictTime:
              betaRandDictTime[betaValue].append(time)
            else:
              betaRandDictTime[betaValue]=[time]
          else:
            if betaValue in betaSeqDictTime:
              betaSeqDictTime[betaValue].append(time)
            else:
              betaSeqDictTime[betaValue]=[time]


  #BUILD LIST OF MEANS & STDV FOR ITERATIONS AND MUTATTEMPTS
  mutAttemptsPerItMean, mutAttemptsPerItStd,mutAttemptsMean, mutAttemptsStd, iterationsMean,iterationsStd,betas =[],[],[],[],[],[],[]
  keyList=betaIterations.keys()
  keyList.sort()
  for key in keyList:
	betas.append(key)
	mutAttemptsPerItMean.append(np.mean(np.asarray(betaMutAttemptsPerIteration[key])))
	mutAttemptsPerItStd.append(np.std(np.asarray(betaMutAttemptsPerIteration[key])))
	mutAttemptsMean.append(np.mean(np.asarray(betaMutAttempts[key])))
	iterationsMean.append(np.mean(np.asarray(betaIterations[key])))
	mutAttemptsStd.append(np.std(np.asarray(betaMutAttempts[key])))
        iterationsStd.append(np.std(np.asarray(betaIterations[key])))
  #for i in range(len(betas)):
	#print mutAttemptsMean[i]

#  params = {
 #       'xlabel': u"Beta",
  #      'ylabel': u"Mutation Attempts - Total iterations",
   #     'meanIterations': iterationsMean,
   #     'meanMutAttempts': mutAttemptsMean,
   #     'stdIterations': iterationsStd,
   #     'stdMutAttempts': mutAttemptsStd,
   #     'betas': betas,
   #     'filename': basePath+'/beta-vs-iteration-length50.png',
   #     'xmax': 2.7,
   #     #'title': 'Largo secuencia=50'
   #     'title': ''
   # }
  #meanErrorBars(**params)

  params = {
        'xlabel': u"Accept rate when mutation increases score by 1 PATENA Unit",
        'ylabel': u"Count",
        #'xRandValues': xRandValues,
        #'xSeqValues': xSeqValues,
        #'yRandValues':yRandValues,
        #'ySeqValues':ySeqValues,
        'xMeanValuesRand': betas,
        'yMeanValuesRand': iterationsMean,
        'xMeanValuesSeq': betas,
        'yMeanValuesSeq': mutAttemptsMean,
        #'yMeanValuesSeq':mutAttemptsPerItMean,
	'yErrorValuesRand': iterationsStd,
        'yErrorValuesSeq': mutAttemptsStd,
        #'yErrorValuesSeq':mutAttemptsPerItStd,
	'filename': basePath+'/beta-vs-Mut-iterations.png',
        #'ymax':5000,
        'xmax': 2.7,
        #'title': 'Largo secuencia=50'
        'title': '',
    }
   
  meanErrorLines(**params)
 











###################################################
####    PROCESS BETA TESTS RESULTS AND PLOT: ######
####	BETA(x)   vs   EXEC.TIME(y)log?  ##########
####	MEAN TIMES, INCLUDES ERROR	###########
###################################################

def makeBetaVsTime(basePath):
  betaSeqDictTime,betaRandDictTime={},{}  #save pairs (beta-[list of times])
  iterations,mutAttempts,stepScores, colorValues=[],[],[],[]
  excludeList=[0.6,0.7,0.8,0.9,1.1,1.2,1.3,1.4,1.6,1.7,1.8,1.9,2.1,2.2,2.4]
  for files in os.listdir(basePath):
    randomSeq=False
    if not(files.endswith('.png')):
      with open(basePath+'/'+files,'r') as rawdata:
	betaValue=0.0
	time=200.0 #default value(in case the execution has not finished)
	
	#PROCESS FILE: SAVE BETA VALUE, RAND/NATURAL AND ELAPSED TIME
	for lines in rawdata.readlines():
	  cols=lines.split('\t')
	  #print cols
	  if cols[0]=='RAND' or cols[0]=='SEQ':
	    betaValue=float(cols[1])
	    if cols[0]=='RAND':
	      randomSeq=True
	    else:
	      randomSeq=False
	  if cols[0]=='END':
	    time=float(cols[1])/60.0
	    #if time>5000:
	      #time=5000
	
	#SAVE EXECUTION DATA IN DICTIONARY
	if betaValue not in excludeList:
	  if randomSeq:
	    if betaValue in betaRandDictTime:
	      betaRandDictTime[betaValue].append(time)
	    else:
	      betaRandDictTime[betaValue]=[time]
	  else:
	    if betaValue in betaSeqDictTime:
	      betaSeqDictTime[betaValue].append(time)
	    else:
	      betaSeqDictTime[betaValue]=[time]



  
  #BUILD X,Y LISTS OF EVERYTHING (VALUES, MEAN, STDEV )
  
  #RANDOM EXECUTIONS LISTS
  yMeanTimeValuesRand,yTimeValuesRand,yStdevTimeValuesRand=[],[],[]
  xMeanBetaValuesRand=[]  #mean and stdev x values are the same (length = different beta values)
  xBetaTimeValuesRand=[]  #one beta value for each execution (length = number of executions ) 
  
  #NATURAL SEQs EXECUTION LISTS	
  yMeanTimeValuesSeq,yTimeValuesSeq,yStdevTimeValuesSeq=[],[],[]
  xMeanBetaValuesSeq=[]  #mean and stdev x values are the same (one for each beta value)
  xBetaTimeValuesSeq=[]  #one beta value for each execution (length = number of executions ) 
  
  
  #ITERATE OVER THE DICTIONARIES AND FILL LISTS
  
  #RANDOM DICTTIONARIES
  keylist = betaRandDictTime.keys()
  keylist.sort()
  for key in keylist:
    xMeanBetaValuesRand.append(key)
    yMeanTimeValuesRand.append(np.mean(np.asarray(betaRandDictTime[key])))
    yStdevTimeValuesRand.append(np.std(np.asarray(betaRandDictTime[key])))
    for index in range(len(betaRandDictTime[key])):
      xBetaTimeValuesRand.append(key)	  				#append the key
      yTimeValuesRand.append(betaRandDictTime[key][index])		#append the value
 
  #NATURAL SEQs DICTIONARIES
  keylist = betaSeqDictTime.keys()
  keylist.sort()
  #for key in keylist:
  for key in keylist:
  #for key in betaSeqDictTime:
    xMeanBetaValuesSeq.append(key)
    yMeanTimeValuesSeq.append(np.mean(np.asarray(betaSeqDictTime[key])))
    yStdevTimeValuesSeq.append(np.std(np.asarray(betaSeqDictTime[key])))
    for index in range(len(betaSeqDictTime[key])):
      xBetaTimeValuesSeq.append(key)	  				#append the key
      yTimeValuesSeq.append(betaSeqDictTime[key][index])			#append the value

  params = {
	'xlabel': u"Accept rate when mutation increases score by 1 PATENA Unit",
	'ylabel': u"Execution time [min]",
	#'xRandValues': xRandValues,
	#'xSeqValues': xSeqValues,
	#'yRandValues':yRandValues,
	#'ySeqValues':ySeqValues,
	'xMeanValuesRand': xMeanBetaValuesRand,
	'yMeanValuesRand': yMeanTimeValuesRand,
	'xMeanValuesSeq': xMeanBetaValuesSeq,
	'yMeanValuesSeq': yMeanTimeValuesSeq,
	'yErrorValuesRand': yStdevTimeValuesRand,
	'yErrorValuesSeq': yStdevTimeValuesSeq,
	'filename': basePath+'/beta-vs-time-length50.png',
	#'ymax':5000,
	'xmax': 2.7,
	#'title': 'Largo secuencia=50'
	'title': ''
    }	
  meanErrorLines(**params)











###################################################
####  PROCESS BETA TESTS RESULTS AND PLOT:   ######
####       ITERATION NUMBER vs % ACEPTACION  ######
####   FOR EACH EXECUTION, MEAN  AND ERROR   ######
###################################################
def makeIterationVsScore(basePath):
  betaSeqDictTime,betaRandDictTime={},{}  #save pairs (beta-[list of times])
  
  betaList=[0.5,2.4]  #LIST OF BETAS TO PRINT
  #betaColourList=['red','green']
  betaSeqDictExecutions,betaRandDictExecutions={},{}  ##DICT OF EXECUTIONS BY BETA VALUE
  #betaValuesExecutionsRand=[]
  maxIterations=4050
  step=1
  #iterationList=range(0,10,1)+range(10,100,20)+range(200,1000,50)
  betaValues=[]
  random=[]
  executions=[]  # this lists saves the executions I want to print
  iterations,mutAttempts,stepScores, colorValues=[],[],[],[]
  for files in os.listdir(basePath):
    randomSeq=False
    if not(files.endswith('.png')):
      with open(basePath+'/'+files,'r') as rawdata:
	execution=[]  #list of %accepted per step
	betaValue=0.0
	time=15000.0 #default value(in case the execution has not finished)
	for lines in rawdata.readlines():
	  cols=lines.split('\t')
	  #print cols
	  if cols[0]=='RAND' or cols[0]=='SEQ':
	    if cols[0]=='RAND':
	      randomSeq=True
	    else:
	      randomSeq=False
	    betaValue=float(cols[1])
	  if cols[0]=='END':
	    time=float(cols[1])
	  if cols[0]=='LOOP1' or cols[0]=='LOOP2':
	    if betaValue in betaList:
	      iteration=int(cols[1])
	      #if iteration in iterationList:
	      if ((iteration%step)==0):
	      #if int(iteration) in np.logspace(0,3):
		#print iteration
		mutAttempts.append(int(cols[2]))
		stepScores.append(float(cols[3]))
		iterations.append(int(cols[1]))
		#acceptRate=(1/int(cols[2]))
		#acceptRate=((1.0/int(cols[2]))*100.0)
		#execution.append(acceptRate)
		#SAVE MUTATTEMPTS
		execution.append(int(cols[2]))
		#SAVE SCORES
		#execution.append(float(cols[3]))
	      #colorValues.append(int(betaValue*35))
	      #colorValues.append('red')
	      #the iteration time is stored in cols[4] 
	    #if betaValue==1.0:
	      #mutAttempts.append(int(cols[2]))
	      #stepScores.append(float(cols[3]))
	      #iterations.append(int(cols[1]))
	      ##colorValues.append(int(betaValue*35))
	      #colorValues.append('blue')
	    #if betaValue==1.5:
	      #mutAttempts.append(int(cols[2]))
	      #stepScores.append(float(cols[3]))
	      #iterations.append(int(cols[1]))
	      ##colorValues.append(int(betaValue*35))
	      #colorValues.append('green')
	    #if cols[0]=='LOOP2':
		#print 'AT LEAST 1 REACHED SECOND LOOP'
	#if time>7000:
	  #time=7000
	#if betaValue==0.4 and time>3000:
	  #print files1
	
	#SAVE WHOLE EXECUTION
	if betaValue in betaList:
	  #print files
	  betaValues.append(betaValue)
	  executions.append(execution)
	  #print betaValue
	  random.append(randomSeq)
	  
	  
	    
	#if randomSeq:
	  ##xRandValues.append(betaValue)	  
	  ##yRandValues.append(time) 
	  #if betaValue in betaRandDictTime:
	    #betaRandDictTime[betaValue].append(time)
	    #betaRandDictExecutions[betaValue].append(execution)
	    ##cantBetaRand[xRandValues[x]] += 1
	  #else:
	    #betaRandDictTime[betaValue]=[time]
	    #betaRandDictExecutions[betaValue][execution]
	    ##cantBetaRand[xRandValues[x]] = 1	
	#else:
	  ##xSeqValues.append(betaValue)
	  ##ySeqValues.append(time)
	  #if betaValue in betaSeqDictTime:
	    #betaSeqDictTime[betaValue].append(time)
	    #betaSeqDictExecutions[betaValue].append(execution)
	    ##cantBetaRand[xRandValues[x]] += 1
	  #else:
	    #betaSeqDictTime[betaValue]=[time]
	    #betaSeqDictExecutions=[execution]
	##if betaValue==0.0:
	  ##print files

 
  params = { 
      'executionsList':executions,
      'random':random,
      'beta':betaValues,
      'logScale': False,
      'maxIterations': maxIterations,
      'step': step,
      'xlabel':'Mutation',
      'ylabel':'Mutation attempts',
      #'ylabel': 'Score[PATENA Units]',
   }
 
  
  #iterationVsX(**params)	    
 
 
 
 
 
 
  #NOW PROCESS EXECUTIONS DATA TO GET MEAN AND STDEV 
  
  
  
  #FIRST MAKE DICT WITH LIST OF MUTATTEMPTS PER ITERATION #
  
  iterRandDict={}   
  iterSeqDict={}
  for exeIndex in range(len(executions)):
    #print exeIndex
    if random[exeIndex]:   #EXECUTION CORRESPONDS TO RANDOM SEQ
      if betaValues[exeIndex] in iterRandDict:   #ALREADY SAVED AN ENTRY AT RAND-LIST FOR THIS BETA 
	    iteration=0
	    while iteration<len(executions[exeIndex]) and iteration<maxIterations:
	      #AGREGO EL VALOR
	      iterRandDict[betaValues[exeIndex]][iteration].append(executions[exeIndex][iteration]) 
	      iteration+=1
	      
      else:   #IF IT IS THE FIRST EXECUTION FOR THIS BETA VALUE
	iterRandDict[betaValues[exeIndex]]= [[] for i in range(maxIterations)]
	iteration=0
	while iteration<len(executions[exeIndex]) and iteration<maxIterations:
	      #AGREGO EL VALOR
	      iterRandDict[betaValues[exeIndex]][iteration].append(executions[exeIndex][iteration]) 
	      iteration+=1
    
    
    else:    #EXECUTION CORRESPONDS TO NATURAL SEQ
      if betaValues[exeIndex] in iterSeqDict:
	    iteration=0
	    while iteration<len(executions[exeIndex]) and iteration<maxIterations:
	      #AGREGO EL VALOR
	      iterSeqDict[betaValues[exeIndex]][iteration].append(executions[exeIndex][iteration])
	      iteration+=1
	      
      else:   #IF IT IS THE FIRST EXECUTION FOR THIS BETA VALUE
	#print 'entro 1 vez'
	iterSeqDict[betaValues[exeIndex]]= [[] for i in range(maxIterations)]
	iteration=0
	while iteration<len(executions[exeIndex]) and iteration<maxIterations:
	      #AGREGO EL VALOR
	      iterSeqDict[betaValues[exeIndex]][iteration].append(executions[exeIndex][iteration])
	      iteration+=1
  
  
  #NOW PROCESS PREVIOUS LISTS TO GET MEANS AND STDEV
  meanRandDict,meanSeqDict,errorRandDict,errorSeqDict={},{},{},{}
  for betas in iterRandDict.keys():
    #if betas in betaList:
      #print betas
      meanRandDict[betas]=[]
      errorRandDict[betas]=[]
      iteration=0
      #print len(iterRandDict[betas])
      while iteration<len(iterRandDict[betas]) and iteration<maxIterations:
        #print iterRandDict[betas][iteration]
        if len(iterRandDict[betas][iteration]) > 0:
	  #print iteration
	  #print iterRandDict[betas][iteration]
	  #print len(iterRandDict[betas][iteration])
	  mean=np.mean(np.asarray(iterRandDict[betas][iteration]))
	  #if iteration==100:
	    #print mean
	  #print mean
	  std=np.std(np.asarray(iterRandDict[betas][iteration]))
	  #print std
	  meanRandDict[betas].append(mean)
	  errorRandDict[betas].append(std)
	iteration+=1
      
  for betas in iterSeqDict.keys():
    #if betas in betaList:
      meanSeqDict[betas]=[]
      errorSeqDict[betas]=[]
      iteration=0
      while iteration<len(iterSeqDict[betas]) and iteration<maxIterations:
	if len(iterSeqDict[betas][iteration]) > 0:
	  mean=np.mean(np.asarray(iterSeqDict[betas][iteration]))
	  #print iteration
	  #if iteration==100:
	    #print mean
	  #print mean
	  std=np.std(np.asarray(iterSeqDict[betas][iteration]))
	  #print std
	  meanSeqDict[betas].append(mean)
	  errorSeqDict[betas].append(std)
	iteration+=1
     
    
  betaValues, random, executionsMean, executionsError =[],[],[],[]
  for betas in meanRandDict.keys():
    betaValues.append(betas)
    random.append(True)
    executionsMean.append(meanRandDict[betas])
    executionsError.append(errorRandDict[betas])
    
  for betas in meanSeqDict.keys():
    betaValues.append(betas)
    random.append(False)
    executionsMean.append(meanSeqDict[betas])
    executionsError.append(errorSeqDict[betas])
  
  
  
  params = { 
      'executionsList':executionsMean,
      'executionsErrorList':executionsError,
      'random':random,
      'beta':betaValues,
      'logScale': True,
      'maxIterations': maxIterations,
      'step': step,
      #'ylabel': 'Score[PATENA Units]',
      'ylabel': 'Mutation attempts',
      'xlabel': 'Mutation'
    }
  
  iterationVsXError(**params)
  
  
  
   ##proceso los datos recolectados
    #betaMeanRand,cantBetaRand = {},{}
    #betaMeanNat,cantBetaNat = {},{}
    #for x in len(xRandValues)
      #if xRandValues[x] in :
	#betaMeanRand[xRandValues[x]].append(yRandValues[x])
	##cantBetaRand[xRandValues[x]] += 1
      #else:
	#betaMeanRand[xRandValues[x]]=[yRandValues[x]]
        ##cantBetaRand[xRandValues[x]] = 1	
    
    
    #for y in betaMeanRand:
      #betaMeanRand.append(mean(betaMeanRand[y]))
      #betaMeanStdv.append(pstdev(betaMeanRand[y]))
      ##betaMeanRand[y]=betaMeanRand[y]/cantBetaRand[y]
    
  #print 'paso todo'
  
  ##BUILD X,Y LISTS OF EVERYTHING (VALUES, MEAN, STDEV )
  #yMeanTimeValuesRand,yTimeValuesRand,yStdevTimeValuesRand=[],[],[]
  #xMeanBetaValuesRand,xBetaTimeValuesRand=[],[]  #mean and stdev x values are the same (one for each beta value)
  
  #yMeanTimeValuesSeq,yTimeValuesSeq,yStdevTimeValuesSeq=[],[],[]
  #xMeanBetaValuesSeq,xBetaTimeValuesSeq=[],[]  #mean and stdev x values are the same (one for each beta value)
  
  ##iterate over rand dict and get values together in a signle list
  
  #keylist = betaRandDictTime.keys()
  #keylist.sort()
  ##for key in keylist:
  #for key in keylist:
    #xMeanBetaValuesRand.append(key)
    #yMeanTimeValuesRand.append(np.mean(np.asarray(betaRandDictTime[key])))
    #yStdevTimeValuesRand.append(np.std(np.asarray(betaRandDictTime[key])))
    #for index in range(len(betaRandDictTime[key])):
      #xBetaTimeValuesRand.append(key)	  				#append the key
      #yTimeValuesRand.append(betaRandDictTime[key][index])		#append the value
  
  #keylist = betaSeqDictTime.keys()
  #keylist.sort()
  ##for key in keylist:
  #for key in keylist:
  ##for key in betaSeqDictTime:
    #xMeanBetaValuesSeq.append(key)
    #yMeanTimeValuesSeq.append(np.mean(np.asarray(betaSeqDictTime[key])))
    #yStdevTimeValuesSeq.append(np.std(np.asarray(betaSeqDictTime[key])))
    #for index in range(len(betaSeqDictTime[key])):
      #xBetaTimeValuesSeq.append(key)	  				#append the key
      #yTimeValuesSeq.append(betaSeqDictTime[key][index])			#append the value
  #print 'paso todo'

  #params = {
	#'xlabel': u"Beta value",
	#'ylabel': u"Total time [s]",
	##'xRandValues': xRandValues,
	##'xSeqValues': xSeqValues,
	##'yRandValues':yRandValues,
	##'ySeqValues':ySeqValues,
	#'xMeanValuesRand': xMeanBetaValuesRand,
	#'yMeanValuesRand': yMeanTimeValuesRand,
	#'xMeanValuesSeq': xMeanBetaValuesSeq,
	#'yMeanValuesSeq': yMeanTimeValuesSeq,
	#'yErrorValuesRand': yStdevTimeValuesRand,
	#'yErrorValuesSeq': yStdevTimeValuesSeq,
	#'filename': basePath+'/beta-vs-time-length50.png',
	##'ymax':5000,
	#'title': 'Sequence length=50'
    #}	
  #meanErrorLines(**params)
  #scatterGraphBinaryColour(**params)
  #params = {
	#'xlabel': u"Iteration number",
	#'ylabel': u"Score [patena Units]",
	#'xValues': iterations,
	#'yValues': stepScores,
	#'colorValues': colorValues ,
	#'filename': basePath+'/iterationNum-vs-score.png',
	#'title': ''
    #}	
  #scatterGraphNaryColour(**params)
  #params = {
	#'xlabel': u"Iteration number",
	#'ylabel': u"Mutation Attempts",
	#'xValues': iterations,
	#'yValues': mutAttempts,
	#'colorValues': colorValues ,
	#'filename': basePath+'/iterationNum-vs-mutAtt.png',
	#'title': ''
    #}	
  #scatterGraphNaryColour(**params)
  
  
 
def mutationsPerSite(basePath):
  seqLength=30
  mutPerSite=[[] for i in range(seqLength)]
  #for i in range(seqLength):
    #mutPerSite[i]=[]
  
  #NOW PROCESS ALL 
  for files in os.listdir(basePath):
    if (files.endswith('.log')):
      executionMutPerSite=[] #save mutations for each
      for i in range(seqLength):
	  executionMutPerSite.append(0)
      totalMutations=0.0
      with open(basePath+'/'+files,'r') as rawdata:
	for line in rawdata:
	    mutation=line.split('\t')[0]
	    if mutation != 'ISEQ' and mutation != 'END':
	      position=mutation.split('(')[0]
	      executionMutPerSite[int(position)]+=1
	      #print position
	      totalMutations+=1
      for i in range(seqLength):
        #print totalMutations
	executionMutPerSite[i]=(executionMutPerSite[i] / totalMutations)*100.0
        #print executionMutPerSite[i]
        mutPerSite[i].append(executionMutPerSite[i])
  meanPerSite=[]
  stdDevPerSite=[]
  index=[]
  #index=np.arange(seqLength)
  for i in range(seqLength):
    index.append(i+1)
    meanPerSite.append(np.mean(np.asarray(mutPerSite[i])))
    #print meanPerSite[i]
    stdDevPerSite.append(np.std(np.asarray(mutPerSite[i])))
    #print stdDevPerSite[i]
  #barsGraph(index,meanPerSite,stdDevPerSite)
  labelX='Residue position'
  labelY='Mutation %'
  #barsGraph(index,meanPerSite,stdDevPerSite)
  scatterGraphErrors(index,meanPerSite,stdDevPerSite,labelX,labelY)


####  OPEN ALL LOGS IN PATH AND ALIGN RESULT SEQUENCES 
####   SAVE RESULTS IN results FILE
def getDivergenceList(basePath):
   multiAlignment=open(basePath+'/resultsList','w')
   resultNumber=1
   for files in os.listdir(basePath):
    if (files.endswith('.log')):
       with open(basePath+'/'+files,'r') as rawdata:
	for line in rawdata:
	  pass
	last = line
	#print last
	resultSequence=last.split('\t')[2]
	#print resultSequence
	#multiAlignment.write('>RESULTSEQ_'+str(resultNumber) + '\n')
        multiAlignment.write(resultSequence)
        resultNumber+=1



def getIdentityPercent(seq1,seq2):
	#print seq1
	#print seq2
	hits=0
	for aa in seq1:
		if aa == seq2[seq1.index(aa)]:
			hits+=1
	if ((float(hits)/(len(seq1)))*100)>70.0:
		print float(hits)/float((len(seq1)))*100
	return (float(hits)/float((len(seq1))))*100


def processDivergenceTest(basePath):
	#getDivergenceList(basePath)
	sequenceList=[]
	initialSeq='MALWMRLLPLLALLALWGPDPAAAFVNQHL'
	#FIRST, LOAD SEQUENCE LIST FROM FILE
	#sequenceList = (with open(basePath+'/'+'resultsList','r')).read().splitlines()
	with open(basePath+'/'+'resultsList','r') as rawdata:
		for line in rawdata.readlines():
			sequenceList.append(line.rstrip())
	
	idPercentInitial, idPercentAll=[],[]
	
	#FIRST, GET IDENTITY % AGAINST INITIAL SEQUENCE:
	for seq in sequenceList:
		idPercentInitial.append(getIdentityPercent(initialSeq,seq))
	
		
	#print len(idPercentInitial)
	#plt.hist(np.asarray(idPercentInitial),12,alpha=0.5)
	#plt.title('Identity against starting sequence')	
	#plt.ylabel('Count')
	#plt.xlabel('Sequence identity %')	
	#plt.ylim(0,15)
	#plt.savefig('againstStart.png', bbox_inches='tight', frameon=True)
	#plt.show()
	
	
	#esto no esta probado, es para fittear una curva a los datos de identidad en set de secuencias random
	#valuesRandom son los valores de identidad de las secuencias random
	#getListRandomSeq(74,basePath)
	sequenceListRandom=[]
 	with open(basePath+'/'+'seqListRandom','r') as rawdata:
                for line in rawdata.readlines():
                        sequenceListRandom.append(line.rstrip())

        idPercentInitialRandom, idPercentAllRandom=[],[]
	for seqRandom in sequenceListRandom:
                idPercentInitialRandom.append(getIdentityPercent(initialSeq,seqRandom))
	
	for seq1Random in sequenceListRandom:
		for seq2Random in sequenceListRandom:
			if sequenceListRandom.index(seq1Random) != sequenceListRandom.index(seq2Random):
				idPercentAllRandom.append(getIdentityPercent(seq1Random,seq2Random))
	
	#my_pdf = gaussian_kde(idPercentAllRandom)
	#x = np.linspace(0,50,400)
	#y = []
	#for valoresX in x:
	#	if valoresX == 0.0:
	#		y.append(0)
	#	else:
	#		y.append(my_pdf(valoresX)*5*5402)
	#plt.plot(x,y,'r')
	#plt.plot(x,my_pdf(x)*5*5402,'r') 
	#plt.hist(np.asarray(idPercentInitialRandom),12,alpha=0.5)
	#plt.show()	

	#GET IDENTITY % ALL AGAINST ALL
	for seq1 in sequenceList:
        	for seq2 in sequenceList:
			if sequenceList.index(seq1) != sequenceList.index(seq2):
				idPercentAll.append(getIdentityPercent(seq1,seq2))
	
	#plt.hist((np.asarray(idPercentInitialRandom),np.asarray(idPercentInitial)),bins=[0,5,10,15, 20, 25,30,35,40,45,50],label=['Random','Results'],normed=1)
	plt.title('Identity between initial sequence and results')
	plt.ylabel('Frequency')
	plt.xlabel('Sequence identity %')
	#plt.savefig('againstInitial.png', bbox_inches='tight', frameon=True, dpi=180)
	plt.hist((np.asarray(idPercentAllRandom),np.asarray(idPercentAll)),bins=[0,5,10,15, 20, 25,30,35, 40,45, 50],label=['Random sequences','PATENA Results'],normed=1)
	plt.title('Identity between sequences')
	plt.xticks((np.arange(0,55,5)))
	plt.legend(loc='upper right')
	#plt.savefig('againstInitial.png', bbox_inches='tight', frameon=True, dpi=180)
	plt.savefig('againstAll.png', bbox_inches='tight', frameon=True, dpi=180) 
	#plt.show()




def getListRandomSeq(lengthList,path):
	freq=[("A",825), ("R",553),("N",406),("D",545),("C",137),("E",393),("Q",675),("G",707),("H",227),("I",596),("L",966),("K",548),("M",242),("F",386),("P",470),("S",656),("T",534),("W",108),("Y",292),("V",687) ]
	out=open(path+'/seqListRandom','w')
	url="http://web.expasy.org/cgi-bin/randseq/randseq.pl?size=" + str(30) + "&comp=average&output=fasta"
  	for x in range(lengthList):
    		response = urllib2.urlopen(url)
		html = response.read()
		i = html.index('\n')
		sequence = html[i+1:].replace('\n', '')
		out.write(sequence+'\n')	





##COMPARE EXPECTED FRECUENCIES WITH OBSERVED FREQUENCIES IN A SET OF RESULTING DESIGNS
def compareFrequencies(basePath):
	expectedFreq=[("A",8.25), ("R",5.53),("N",4.06),("D",5.45),("C",1.37),("E",3.93),("Q",6.75),("G",7.07),("H",2.27),("I",5.96),("L",9.66),("K",5.48),("M",2.42),("F",3.86),("P",4.70),("S",6.56),("T",5.34),("W",1.08),("Y",2.92),("V",6.87)]
	aaOcurrences=[("A",0), ("R",0),("N",0),("D",0),("C",0),("E",0),("Q",0),("G",0),("H",0),("I",0),("L",0),("K",0),("M",0),("F",0),("P",0),("S",0),("T",0),("W",0),("Y",0),("V",0)]
	aaOcurrencesDict=dict(aaOcurrences)
	expectedFreqDict=dict(expectedFreq)
	###
	###
	#getDivergenceList(basePath)		
	sequenceList=[]
	with open(basePath+'/'+'resultsList','r') as rawdata:
        	for line in rawdata.readlines():
                	sequenceList.append(line.rstrip())
	#iterate over seqList
	#get total number of residues for each AA
	#get total number of residues(len(seqList)*len(sequence))
	totalResidues=0.0
	for seq in sequenceList:
		for pos in range(len(seq)):
			aaOcurrencesDict[seq[pos]]+=1
			totalResidues+=1
	totalPercOcurr=0
	totalPercExpected=0
	for key in aaOcurrencesDict.keys():
		#print (aaOcurrencesDict[key]/totalResidues)*100
		aaOcurrencesDict[key]=(aaOcurrencesDict[key]/totalResidues)*100
		totalPercExpected+=expectedFreqDict[key]
		totalPercOcurr+=aaOcurrencesDict[key]
		
	#print totalPercOcurr
	#print totalPercExpected
	aminoacids=np.asarray(expectedFreqDict.keys())
	expectedArray=np.asarray(expectedFreqDict.values())
	observedArray=np.asarray(aaOcurrencesDict.values())	
	#for pos in range(len(aminoacids)):
	#	print   aminoacids.item(pos) + ' - ' + str(expectedArray.item(pos)) + ' - ' + str(observedArray.item(pos))	
	for i in range(len(aminoacids)):
    		plt.scatter(expectedArray[i], observedArray[i], marker=('$'+aminoacids[i]+'$'), s=200)
	#plt.scatter(expectedArray,observedArray)
	plt.xlabel('Background percent frequencies')
	plt.ylabel('Observed percent frequencies')
	x=np.arange(0,16,1)
	y=np.arange(0,16,1)
	plt.plot(x,y,linewidth=0.5,color='red',linestyle='--')
	plt.axis((0,15,0,15))
	#plt.gcf().set_size_inches(8, 8)
	#plt.gcf().set_dpi(300)
	#plt.figure(num=None,figsize=(8, 60), dpi=150)
	plt.savefig('holaaa',dpi=300)
	#plt.show()

#para comparar frecuencias usar datos de /home/ieguinoa/bioTesis/patena/tests/Results/test-divergence-1
#compareFrequencies(sys.argv[1])

#usar datos de /home/ieguinoa/results/beta0.1-2.5/ 
#makeBetaVsIteration(sys.argv[1])



#mutationsPerSite('/home/ieguinoa/bioTesis/patena/tests/Results/test-divergence-24395-beta-0.1')


#print iteration Vs score (or Vs mutation attempts)
makeIterationVsScore(sys.argv[1])


#usar /home/ieguinoa/results/beta0.1-2.5
#makeBetaVsTime(sys.argv[1])        

#getDivergenceList(sys.argv[1])


#usar datos de /home/ieguinoa/bioTesis/patena/tests/Results/test-divergence-1   (contiene la lista ya armada de sequencias resultantes y random)
#processDivergenceTest(sys.argv[1])


#processBetaTestResults('/home/ieguinoa/results/todos')    
#processBetaTestResults('/home/ieguinoa/results/beta-0.1-1.9')
#processBetaTestResults('/home/ieguinoa/results/beta-0.5-1.5-step-0.1')
#processTimeTestResults('/home/ieguinoa/results/timeTestBeta1')
#processBetaTestResults('/home/ieguinoa/results/betaTests')

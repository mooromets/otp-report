import codecs
import re
import datetime
import time
import os
import sys
import itertools

import money
import transaction
import places


#global declarations
patDate = "[0-9]{2}\.[0-9]{2}\.[0-9]{2}" # dd.mm.yy
patTime = "[0-9]{2}\:[0-9]{2}" # hh:mm
patOperDate = "(?P<oper_date>" + patDate + ")"
patOperTime = "(?P<oper_time>" + patTime + ")"
patChargeDate = "(?P<charge_date>" + patDate + ")"

patDateTimeDate = patOperDate + "\s+"+ patOperTime +"\s+"+ patChargeDate

patSum = "-?\d+,\d+" # -18,78
patCur = "UAH|USD|EUR|RUB" 
patSumOper = "(?P<oper_cur>"+ patCur +")\s*(?P<oper_sum>"+ patSum +")"
patSumAcc = "(?P<acc_cur>"+ patCur +")\s*(?P<acc_sum>"+ patSum +")"

patFirstComment = "(?P<comment1>.*)"
patSumComssision = "(.+UAH\s+(?P<com_sum>"+ patSum +"))?"
endString = '============' 

patCandidate = r"^" + patDateTimeDate

patCard = r".*(: ){1}(?P<card>[\w ]+[*]{6}\d{4})"

#regex https://docs.python.org/2/library/re.html

"""
internal transactions:
	(dateTime) (comment1) (sum1) [sum2]
	[comment2]
	[comment3]
spendings transactions:
	(dateTime) (comment1)
	(comment2) (sum1) (sum2)
	[(comment 3) (sum3)]

summary:	
	(dateTime) (comment1) (sum1) [sum2] [(comment 2) (sum3)]  
"""

patFull = r"^" + patDateTimeDate + patFirstComment + patSumOper + "\s+" + patSumAcc + patSumComssision

# is called on every couple of lines-candidates
def saveTransaction(line, tranList):
	line = line.replace('\r',"")
	line = line.replace('\n',"")
	matchFull = re.match(patFull, line)
	if matchFull:
		newTra = transaction.Transaction(line, matchFull.group('oper_date'), matchFull.group('oper_time'), matchFull.group('charge_date'), 
			money.Money(matchFull.group('oper_sum'), matchFull.group('oper_cur')),
			money.Money(matchFull.group('acc_sum'), matchFull.group('acc_cur')),
			matchFull.group('comment1'),
			money.Money(matchFull.group('com_sum'), 'UAH'))
		tranList.append(newTra)
		#print ("Match! ", time.strftime("%d-%m-%Y", newTra.myOperDate), newTra.myOperSum.myValue)
	#else :
		#print ("Not match!")
		#print (codecs.encode(line), 'utf8')	

def flo (x): return float(x.replace(',', '.'))
def sumstr (x,y) : return str ( flo(x) + flo(y) )		
		
		
# calc commissions
def transactionAddCommission(left, right):
	if (left.myCommision.myValue and right.myCommision.myValue):
		flo = lambda x : float(x.replace(',', '.'))
		sumstr = lambda x, y : str( flo(x) + flo(y))
		left.myAccSum.myValue = sumstr ( left.myAccSum.myValue, right.myAccSum.myValue )
		left.myCommision.myValue = sumstr(left.myCommision.myValue, right.myCommision.myValue)
	return left
		
# print list of transactions
def printTransactions(outFile, tranList):
	#sort
	tranList.sort(key=lambda x: x.myOperDate, reverse=False)	
	#print results
	for p in tranList:
		info = ""
		#find known placed
		for key in places.PlacesDict.keys():
			if key in p.myComment:
				info = places.PlacesDict[key]
				break
		#if place is unknown print comment otherwise
		if not info :
			info = "<<<"
			for word in p.myComment.split():
				try :
					print (word)
					info += " " + word
				except:
					continue
			info += ">>>"
		template = "{:11} {:>10}   {:30}"
		print (template.format(time.strftime("%d-%m-%Y", p.myOperDate),  p.myAccSum.myValue, info), file=outFile)
		if (p.myCommision.myValue):
			print ("\tComission: ", p.myCommision.myValue, file=outFile)
######################################################

#define filename
fname = "full.txt"
if len(sys.argv) == 2: # if directory specified 
	fname = sys.argv[1]
foutName = "out_" + fname	

f = codecs.open(fname, 'r', 'utf-8')
fout = open(foutName, 'w')

newTransaction = ""
AllTranList = []

#
print (patCard)
#

#read file and fill transaction list
line = f.readline()
re.UNICODE = True
while line:
	cardMatch = re.match(patCard, line)
	if (cardMatch):
		print (cardMatch.group('card'))
		print(cardMatch.group('card'), file=fout)
	if (re.match(patCandidate, line)): #string starts with date
		saveTransaction(newTransaction, AllTranList)
		newTransaction = line
	elif (line.startswith(endString)):
		saveTransaction(newTransaction, AllTranList)
		printTransactions(fout, AllTranList)
		print(endString, file=fout)
		#
		#commisions
		"""
		Sums = []
		Comms = []
		for t in AllTranList:
			if (t.myCommision.myValue):
				sum = float(t.myAccSum.myValue.replace(',', '.'))
				comms = float(t.myCommision.myValue.replace(',', '.'))
				Sums.append(sum)
				Comms.append(comms)
				print (time.strftime("%d-%m-%Y", t.myOperDate), sum, comms, comms/sum *100)
		"""
#		print (list(itertools.accumulate(Sums)))
#		print (list(itertools.accumulate(Comms)))
		
#		trans = list( itertools.accumulate(AllTranList, lambda left, right: left.myAccSum.myValue + right.myAccSum.myValue))	

#		trans = list( itertools.accumulate(AllTranList, transactionAddCommission))
#		print (trans[len(trans)-2].myAccSum.myValue, trans[len(trans)-2].myCommision.myValue)
		#

		
		
		AllTranList = []
		newTransaction = ""
	else :
		if (newTransaction != ""): #if we inside some Transaction
			newTransaction += line
	line = f.readline()
  
f.close()
fout.close()


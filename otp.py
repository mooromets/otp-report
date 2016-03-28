import codecs
import re
import datetime

places = {'ATM': "ATM"}
places['UZ.GOV.UA'] = "UZ tickets"
places['ALIBABA.COM'] = "Ali express"
places['20041103'] = "Dinner (cafe)"
places['WEST LINE'] = "WEST LINE"
places['S1K30P72'] = "suhofrukt15"
places['A0900140'] = "ATM"
places['A0900050'] = "ATM"
places['DOBROBUT'] = "DOBROBUT"
places['WWW.PORTMONE.COM.UA'] = "PORTMONE"
places['VARUS'] = "VARUS"
places['PLANETA-KINO'] = "PLANETA-KINO"
places['VITALUX'] = "Apteka VITALUX"
places['WOG'] = "WOG AZS"
places['Blizenko'] = "Blizenko Lvov"
places['BLYZENKO'] = "Blizenko Lvov"
places['EVERHOUR'] = "EVERHOUR"
places['Lego'] = "Lego"
places['Rukavichka'] = "Rukavichka Lvov"
places['CHICCO'] = "CHICCO"
places['MAGAZIN1035'] = "Novus"
places['S1LV0UAK'] = "Silpo"
places['DZHUNA'] = "Mega Market"
places['IZUMINKA'] = "Roshen"
places['NEXT'] = "NEXT"

#import sqlite3
#conn = sqlite3.connect('test.db')
#print ("Opened database successfully");

class Transaction:
	def __init__ (self, opDate, opDateProc, opSumm, opInfo):
		self.myDate = opDate
		self.myDateProcessed = opDateProc
		self.mySum = opSumm
		self.myInfo = opInfo

fname = "log.txt"

f = codecs.open(fname, 'r', 'utf8')

words1 = [] #first line
words2 = [] #second line
words3 = [] #third line
info = ""

trans = [] #transactions

for line in f:
	if re.search("[0-9]{2}\.[0-9]{2}\.[0-9]{2}", line): #first line of the transaction
		#save the last transaction
		if words1 and info:
			comission = 0.0
			if words3:
				comission = float(words3[len(words3)-1].replace(',','.'))
			tra = Transaction(words1[0], words1[2], float(words2[len(words2)-1].replace(',','.')) + comission, info)
			trans.append(tra)
		#new transaction
		words1 = line.split()
		words2 = []
		words3 = []
		info = ""
		continue
	if re.search("^[0-9]{6}", line): #second line of the transaction
		for key in places.keys():
			if key in line:
				info = places[key]
				break
		words2 = line.split()
		if not info:
			info = words2[1] +  "----"
		continue
	words3 = line.split()
	   
for p in trans: 
	if p.mySum > 0.0:
		print (p.myDateProcessed, p.mySum, p.myInfo)
	else :
		print (p.myDate, p.mySum, p.myInfo)
	
	   
f.close()


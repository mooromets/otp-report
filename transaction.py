import money
import time

class Transaction:
	def __init__ (self, transactionString, operDate, operTime, chargeDate, operSum, accSum, comment, commission):
		self.myTextBody = transactionString
		self.myOperDate = time.strptime(operDate, "%d.%m.%y" )
		self.myOperTime = operTime
		self.myChargeDate =  time.strptime(chargeDate, "%d.%m.%y" )
		self.myOperSum = operSum
		self.myAccSum = accSum
		self.myComment = comment
		self.myCommision = commission
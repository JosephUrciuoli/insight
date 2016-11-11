from collections import defaultdict
import math

# Constants
TRUSTED = "trusted"
UNVERIFIED = "unverified"

class Verification:
	"""docstring for ClassName"""
	def __init__(self):
		self.user_payments = defaultdict(list)

	def add_payment(self,id1,id2,amount):
		self.user_payments[id1].append(amount)
		self.user_payments[id2].append(amount)

	def check_within_standard_dev(self, amount, id1, id2):
		id1_amounts = self.user_payments[id1]
		id2_amounts = self.user_payments[id2]
		if len(id1_amounts) < 1 or len(id2_amounts) < 1:
			return UNVERIFIED
		id1_amounts, id2_amounts = [float(i) for i in id1_amounts],[float(i) for i in id2_amounts]
		means = mean(id1_amounts),mean(id2_amounts)
		standard_devs = standard_dev(id1_amounts,means[0]),standard_dev(id2_amounts,means[1])
		# check if the transaction is greater than two standard deviations of either user
		if amount > (means[0] + 2*standard_devs[0]) or amount > (means[1] + 2*standard_devs[1]):
			return UNVERIFIED
		else:
			return TRUSTED

def mean(amounts):
	return sum(amounts) / len(amounts)

def standard_dev(amounts, mean):
	if len(amounts) < 2:
		return mean * 1.477
	variance = map(lambda x: (x - mean)**2, amounts)
	standard_deviation = math.sqrt(sum(variance) / len(variance))
	return standard_deviation    
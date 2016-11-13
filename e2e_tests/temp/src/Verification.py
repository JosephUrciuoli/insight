__author__ = "joseph_urciuoli"
from collections import defaultdict
import math
import warnings


# Constants
TRUSTED = "trusted"
UNVERIFIED = "unverified"


# class Verification
# This class is used to manage a user's payments. It is also
# used to check if payments are within 2 standard deviations of
# user's previous payments. 2 Standard deviations was chosen because
# if a user's payments are from a normal distribution, 2 standard
# deviations away would mean that the transaction greater than 97% of their
# other transactions. We want to ensure user's are well aware of large transactions
# from their accounts
class Verification:
    def __init__(self):
        self.user_payments = defaultdict(list)

    # add_payment - add the transaction amount to each users payments
    def add_payment(self, id1, id2, amount):
        # Ensure that the type is a float and not a zero or negative value
        if float(amount) > 0 and id1 != id2:
            self.user_payments[id1].append(amount)
            self.user_payments[id2].append(amount)
        else:
            warnings.warn("Attempted to add a payment with improper parameters. Payment ignored.")

    # check_within_stand_dev - checks if the transaction is less than two standard deviations of
    # both user's previous transactions
    def check_within_standard_dev(self, amount, id1, id2):
        id1_amounts = self.user_payments[id1]
        id2_amounts = self.user_payments[id2]
        if len(id1_amounts) < 1 or len(id2_amounts) < 1:
            return UNVERIFIED
        # Convert to list of floats
        id1_amounts, id2_amounts = [float(i) for i in id1_amounts], [float(i) for i in id2_amounts]
        means = mean(id1_amounts), mean(id2_amounts)
        standard_devs = standard_dev(id1_amounts, means[0]), standard_dev(id2_amounts, means[1])
        # check if the transaction is greater than two standard deviations of either user
        if amount > (means[0] + 2 * standard_devs[0]) or amount > (means[1] + 2 * standard_devs[1]):
            return UNVERIFIED
        else:
            return TRUSTED


# mean - calculates the mean of a list of floats
def mean(amounts):
    # Simple mean: sum of the elements divided by the number of elements
    if not type(amounts) is list or len(amounts) < 1 or not type(amounts[0]) is float:
        warnings.warn("Attempted to find the mean of an invalid list. Returned 0.")
        return 0
    return sum(amounts) / float(len(amounts))


# standard_dev - calculates the population standard deviation of a list of floats
def standard_dev(amounts, mean):
    # simple type checking
    if len(amounts) < 1 or not type(amounts) is list or not type(mean) is float:
        warnings.warn("Attempted to find the standard deviation with invalid parameters. Returned 0.")
        return 0
    # The standard deviation of a single number is 0. It does not make it sense to treat it as 0
    # in this case. Because of this, we will just check to see if it is greater than twice the first transaction.
    if len(amounts) < 2:
        return mean * 2
    variance = map(lambda x: (x - mean) ** 2, amounts)
    standard_deviation = math.sqrt(sum(variance) / len(variance))
    return standard_deviation

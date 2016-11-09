__author__ = "joseph_urciuoli"


class Payment(object):
    def __init__(self, time, id1, id2, amount, message):
        self.time = time
        self.id1 = id1
        self.id2 = id2
        self.amount = amount
        self.message = message


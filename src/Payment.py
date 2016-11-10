import warnings

__author__ = "joseph_urciuoli"


class Payment(object):

    def __init__(self, time=None, id1=None, id2=None, amount=None, message=None):
        self.time = time
        self.id1 = id1
        self.id2 = id2
        self.amount = amount
        self.message = message

    def init_with_text(self, line):
        if type(line) == str:
            attr = line.split(",")
            if len(attr) > 4:
                self.time = attr[0]
                self.id1 = attr[1].strip()
                self.id2 = attr[2].strip()
                self.amount = attr[3].strip()
                self.message = attr[4].strip()
            else:
                warnings.warn("Attempted to initialize Payment with " \
                              "incorrect args. Attributes not added.")
        else:
            warnings.warn("Attempted to initialize Payment with " \
                          "incorrect data type. Attributes not added.")



__author__ = "joseph_urciuoli"
import warnings


# class Payment
# Used to organize and structure payment data from the input file
class Payment(object):

    def __init__(self, time=None, id1=None, id2=None, amount=None, message=None):
        self.time = time
        self.id1 = id1
        self.id2 = id2
        self.amount = amount
        self.message = message

    # ini_with_text - initialize the class with a line from the text file
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



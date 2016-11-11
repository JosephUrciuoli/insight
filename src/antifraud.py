import sys
from collections import defaultdict
from Payment import Payment
from Graph import Graph
from Verification import Verification
import warnings
from time import time
import math
import re

DATE_REGEX = "\d{4}[-/]\d{2}[-/]\d{2}[\s/](\d{2}[:/])*\d{2}"

def main(args, degrees, added_feature=False):
    # Implement the features in the challenge
    input_file = args[1]
    payments_graph,verification = process_input(file=input_file)
    for idx,degree in enumerate(degrees):
        print degree
        generate_output(degrees_of_separation=degree, \
            file=args[2], \
            output=args[3+idx], \
            graph=payments_graph)
    # Added feature
    output_added_feature(verification,file=args[2],output=args[6])

def output_added_feature(verification,file,output):
    try:
        f = open(file, 'rb')
    except IOError:
        print "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        try:
            with open(output, "w") as out_file:
                for line in lines[1:]:
                    if validate_line(line):
                        payment = Payment()
                        payment.init_with_text(line)
                        payment_status = verification.check_within_standard_dev(amount=float(payment.amount), \
                                id1=payment.id1, \
                                id2=payment.id2)
                        out_file.write(payment_status + "\n")
                    else:
                         warnings.warn("Read line with improper formatting. The line was dropped.")
        except IOError:
            print "Could not write to file: ", output
            sys.exit()
        else:
            out_file.close()


def generate_output(degrees_of_separation, file, output, graph):
    try:
        f = open(file, 'rb')
    except IOError:
        print "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        try:
            with open(output, "w") as out_file:
                for line in lines[1:]:
                    if validate_line(line):
                        payment = Payment()
                        payment.init_with_text(line)
                        payment_status = graph.is_within_network(payment.id1, \
                            payment.id2, \
                            degrees_of_separation)
                        out_file.write(payment_status + "\n")
                    else:
                         warnings.warn("Read line with improper formatting. The line was dropped.")
        except IOError:
            print "Could not write to file: ", output
            sys.exit()
        else:
            out_file.close()


def process_input(file):
    graph = Graph()
    verification = Verification()
    try:
        f = open(file, 'rb')
    except IOError:
        print "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        for line in lines[1:]:
            if validate_line(line):
                payment = Payment()
                payment.init_with_text(line)
                graph.add_node(payment.id1)
                graph.add_node(payment.id2)
                graph.add_edge(payment.id1,payment.id2)
                verification.add_payment(payment.id1,payment.id2,payment.amount)
            else:
                warnings.warn("Read line with improper formatting. The line was dropped.")
    return graph,verification

def validate_line(line):
    regex = re.compile(DATE_REGEX)
    return len(line.split(",")) > 4 and bool(regex.match(line.split(",")[0]))


if __name__ == "__main__":
    degrees = [1,2,4]
    main(args=sys.argv, degrees=degrees, added_feature=True)
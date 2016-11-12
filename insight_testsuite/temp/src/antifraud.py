__author__ = "joseph_urciuoli"
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


# main - kicks off all of the processing to generate the output files for all features
def main(args, degrees, added_feature=False):
    # Implement the features in the challenge
    if len(args) > 5:
        input_file = args[1]
        payments_graph, verification = process_input(file=input_file)
        for idx, degree in enumerate(degrees):
            generate_output(degrees_of_separation=degree, \
                            file=args[2], \
                            output=args[3 + idx], \
                            graph=payments_graph)
    else:
        warnings.warn("Improper arguments passed. Payments not processed.")
    # Added feature
    if len(args) > 6:
        output_added_feature(verification, file=args[2], output=args[6])
    else:
        warnings.warn("No output file location supplied for added feature. Processing not performed.")


# output_added_feature - outputs the added feature data to the supplied text file
def output_added_feature(verification, file, output):
    # Open the file that will be tested against
    try:
        f = open(file, 'rb')
    except IOError:
        print
        "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        try:
            # Open the file that will be output to
            with open(output, "w") as out_file:
                for line in lines[1:]:
                    if validate_line(line):
                        payment = Payment()
                        # create a Payment for each line in the text file
                        payment.init_with_text(line)
                        # Check if the payment amount is within 2 STDs of previous transactions
                        payment_status = verification.check_within_standard_dev(amount=float(payment.amount), \
                                                                                id1=payment.id1, \
                                                                                id2=payment.id2)
                        out_file.write(payment_status + "\n")
                    else:
                        warnings.warn("Read line with improper formatting. The line was dropped.")
        except IOError:
            print
            "Could not write to file: ", output
            sys.exit()
        else:
            out_file.close()


# generate_output - outputs the required features data to the supplied text file
def generate_output(degrees_of_separation, file, output, graph):
    # Open the file that will be tested against
    try:
        f = open(file, 'rb')
    except IOError:
        print
        "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        try:
            with open(output, "w") as out_file:
                for line in lines[1:]:
                    if validate_line(line):
                        payment = Payment()
                        # Create a payment for each line in the text file
                        payment.init_with_text(line)
                        # Check if the users are within each others network by DOS
                        payment_status = graph.is_within_network(payment.id1, \
                                                                 payment.id2, \
                                                                 degrees_of_separation)
                        out_file.write(payment_status + "\n")
                    else:
                        warnings.warn("Read line with improper formatting. The line was dropped.")
        except IOError:
            print
            "Could not write to file: ", output
            sys.exit()
        else:
            out_file.close()


# process_input - process the input from the text file to generate data structures
def process_input(file):
    # Graph is the DS for required feats., verification for the added feature
    graph = Graph()
    verification = Verification()
    # OPen the input file
    try:
        f = open(file, 'rb')
    except IOError:
        print
        "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        for line in lines[1:]:
            if validate_line(line):
                payment = Payment()
                # Create a payment from each line and add it to the graph
                # also add it to the verification.user_payment dictionary
                payment.init_with_text(line)
                graph.add_node(payment.id1)
                graph.add_node(payment.id2)
                graph.add_edge(payment.id1, payment.id2)
                verification.add_payment(payment.id1, payment.id2, payment.amount)
            else:
                warnings.warn("Read line with improper formatting. The line was dropped.")
    return graph, verification


# validate_line - ensure that the line read in from the text file is valid
'''
    TODO: some of the messages contain /n which causes them to move to the next line
    even though they're from the same transaction. Should handle this by combining the message
    to the previous valid transaction.  The message is not used for the features implemented,
    so they are simply discarded instead
'''
def validate_line(line):
    # check if there are a proper number of arguments and the first arg matches the date regex
    regex = re.compile(DATE_REGEX)
    return len(line.split(",")) > 4 and bool(regex.match(line.split(",")[0]))


if __name__ == "__main__":
    degrees = [1, 2, 4]
    main(args=sys.argv, degrees=degrees, added_feature=True)

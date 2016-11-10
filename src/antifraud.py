import sys
from collections import defaultdict
from Payment import Payment
from Graph import Graph
from time import time
import math
import re

DATE_REGEX = "\d{4}[-/]\d{2}[-/]\d{2}[\s/](\d{2}[:/])*\d{2}"

def main(args, degrees, added_feature=False):
    # Implement the features in the challenge
    input_file = args[1]
    payments_graph,amount_dict = process_input(file=input_file)
    # for idx,degree in enumerate(degrees):
    #     print degree
    #     generate_output(degrees_of_separation=degree, \
    #         file=args[2], \
    #         output=args[3+idx], \
    #         graph=payments_graph)
    # Added feature
    output_added_feature(amount_dict,file=args[2],output=args[6])

def output_added_feature(amount_dict,file,output):
    regex = re.compile(DATE_REGEX)
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
                    if len(line.split(",")) > 4 and bool(regex.match(line.split(",")[0])):
                        payment = Payment()
                        payment.init_with_text(line)
                        payment_status = check_within_standard_dev(amount=float(payment.amount), \
                                id1_amounts=amount_dict[payment.id1], \
                                id2_amounts=amount_dict[payment.id2])
                        out_file.write(payment_status + "\n")
                    else:
                        print "REGEX or crap line"
                        print line
        except IOError:
            print "Could not write to file: ", output
            sys.exit()
        else:
            out_file.close()

def check_within_standard_dev(amount, id1_amounts, id2_amounts):
    if len(id1_amounts) < 1 or len(id2_amounts) < 1:
        return "unverified"
    id1_amounts, id2_amounts = [float(i) for i in id1_amounts],[float(i) for i in id2_amounts]
    means = mean(id1_amounts),mean(id2_amounts)
    standard_devs = standard_dev(id1_amounts,means[0]),standard_dev(id2_amounts,means[1])
    # check if the transaction is greater than two standard deviations of either user
    if amount > (means[0] + 2*standard_devs[0]) or amount > (means[1] + 2*standard_devs[1]):
        return "unverified"
    else:
        return "trusted"


def standard_dev(amounts, mean):
    if len(amounts) < 2:
        return mean * 1.477
    variance = map(lambda x: (x - mean)**2, amounts)
    standard_deviation = math.sqrt(sum(variance) / len(variance))
    return standard_deviation

def mean(amounts):
    return sum(amounts) / len(amounts)


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
                    if len(line.split(",")) > 4:
                        payment = Payment()
                        payment.init_with_text(line)
                        payment_status = graph.is_within_network(payment.id1, \
                            payment.id2, \
                            degrees_of_separation)
                        out_file.write(payment_status + "\n")
        except IOError:
            print "Could not write to file: ", output
            sys.exit()
        else:
            out_file.close()


def process_input(file):
    graph = Graph()
    amount_dict = defaultdict(list)
    try:
        f = open(file, 'rb')
    except IOError:
        print "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        for line in lines[1:]:
            if len(line.split(",")) > 4:
                payment = Payment()
                payment.init_with_text(line)
                graph.add_node(payment.id1)
                graph.add_node(payment.id2)
                graph.add_edge(payment.id1,payment.id2)
                amount_dict[payment.id1].append(payment.amount)
                amount_dict[payment.id2].append(payment.amount)
    return graph,amount_dict


if __name__ == "__main__":
    degrees = [1,2,4]
    main(args=sys.argv, degrees=degrees, added_feature=True)
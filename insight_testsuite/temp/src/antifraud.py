import sys
from Payment import Payment
from Graph import Graph
from time import time


def main(args, degrees):
    input_file = args[1]
    payments_graph = process_input(file=input_file)
    t0 = time()
    print payments_graph.is_within_network("6659","3308",1)
    print time() - t0
    for idx,degree in enumerate(degrees):
        generate_output(degrees_of_separation=degree, \
            file=args[2], \
            output=args[3+idx], \
            graph=payments_graph)




def generate_output(degrees_of_separation, file, output, graph):
    print degrees_of_separation
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
    return graph


def process_input(file):
    graph = Graph()
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
    return graph


if __name__ == "__main__":
    degrees = [1,2,4]
    main(args=sys.argv, degrees=degrees)
__author__ = "joseph_urciuoli"
from collections import defaultdict
import warnings

# Constants
TRUSTED = "trusted"
UNVERIFIED = "unverified"


# class Graph
# Representation of the payment network fro users.  Nodes are
# users and edges represent a transaction between them.  This class
# is also responsible for checking if two users are within each others
# network to a certain degree of separation
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    # add_node - add a user to the network - will have no edges
    def add_node(self, node):
        self.nodes.add(node)

    # add_edge - add an edge between two users when they have a transaction
    # If the user is not in the network, add them
    def add_edge(self, from_node, to_node):
        # make sure were not adding edges back to own node
        # this is legal in graphs, but not useful in this domain
        if from_node != to_node:
            if from_node not in self.nodes:
                self.nodes.add(from_node)
            if to_node not in self.nodes:
                self.nodes.add(to_node)
            self.edges[from_node].add(to_node)
            self.edges[to_node].add(from_node)
        else:
            warnings.warn("Attempted to initialize Graph edge with " \
                          "the same node. Edge not added.")

    # is_within_network - Checks if two users are within the same network to a certain degree
    # of separation.  Uses bidirection BFS to find first intersection, and counts the hops to each
    # TODO: Benchmark multithreaded solution. Investigate use of dynamic programming
    def is_within_network(self,id1,id2,degrees_of_separation):
        if degrees_of_separation < 1:
            warnings.warn("Attempted to check if node was within less than 1 degrees " \
                          "of separation. Returned unverified.")
            return UNVERIFIED

        # Use bidirectional BFS to compute the shortest path
        visited_start, visited_end, queue_start, queue_finish = set(), set(), [id1], [id2]

        # initialize the visited nodes to the two user's nodes
        visited_start.add(id1)
        visited_end.add(id2)

        # bound the number of iterations
        degrees = 0

        # if there are neighbors to visit and we haven't explored past the degrees of separation
        while (queue_start or queue_finish) and degrees <= degrees_of_separation:
            # Walk over all of the neighbors from the starting node
            if len(queue_start) > 0:
                degrees += 1
                to_visit = queue_start
                queue_start = []
                # visit each neighbor in this layer if we have not already visited it
                # if it was visited by the search from the end, we have a path
                while len(to_visit) > 0:
                    vertex = to_visit.pop(0)
                    for neighbor in self.edges[vertex]:
                        if neighbor not in visited_start:
                            visited_start.add(neighbor)
                            queue_start.append(neighbor)
                        if neighbor in visited_end:
                            if degrees <= degrees_of_separation:
                                return TRUSTED
                            else:
                                return UNVERIFIED

            # Walk over all of the neighbors from the ending node
            if len(queue_finish) > 0:
                degrees += 1
                to_visit = queue_finish
                queue_finish = []
                # visit each neighbor in this layer if we have not already visited it
                # if it was visited by the search from the beginning, we have a path
                while len(to_visit) > 0:
                    vertex = to_visit.pop(0)
                    for neighbor in self.edges[vertex]:
                        if neighbor not in visited_end:
                            visited_end.add(neighbor)
                            queue_finish.append(neighbor)
                        if neighbor in visited_start:
                            if degrees <= degrees_of_separation:
                                return TRUSTED
                            else:
                                return UNVERIFIED
        # No path was found
        return UNVERIFIED

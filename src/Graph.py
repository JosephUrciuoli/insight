__author__ = "joseph_urciuoli"
from collections import defaultdict
import warnings

# Constants
TRUSTED = "trusted"
UNVERIFIED = "unverified"

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node):
        # make sure were not adding edges back to own node
        # this is legal in graphs, but not useful in this domain
        if from_node != to_node:
            # if node not in nodes, add it
            if from_node not in self.nodes:
                self.nodes.add(from_node)
            if to_node not in self.nodes:
                self.nodes.add(to_node)
            self.edges[from_node].add(to_node)
            self.edges[to_node].add(from_node)
        else:
            warnings.warn("Attempted to initialize Graph edge with " \
                          "the same node. Edge not added.")

    def is_within_network(self,id1,id2,degrees_of_separation):
        if degrees_of_separation < 1:
            warnings.warn("Attempted to check if node was within less than 1 degrees " \
                          "of separation. Returned unverified.")
            return UNVERIFIED
        # Use bidirectional BFS to compute the shortest path
        visited_start, visited_end, queue_start, queue_finish = set(), set(), [id1], [id2]

        shortest_distance = float("inf")
        visited_start.add(id1)
        visited_end.add(id2)

        # bound the number of iterations
        degrees = 0

        while (queue_start or queue_finish) and degrees <= degrees_of_separation:
            # Walk over all of the neighbors
            if len(queue_start) > 0:
                degrees = degrees + 1
                to_visit = queue_start
                queue_start = []
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

            if len(queue_finish) > 0:
                degrees = degrees + 1
                to_visit = queue_finish
                queue_finish = []
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

        return UNVERIFIED

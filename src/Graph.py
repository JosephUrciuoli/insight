__author__ = "joseph_urciuoli"
from collections import defaultdict
import math

class Graph:
    def __init__(self):
        self.nodes = set()
        self.vertices = defaultdict(list)

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)

    def is_within_network(self,id1,id2,degrees_of_separation):
        # Use Djikstra's Algorithm to compute the shortest path

        # Each list index contains the shortest distance from id1 to i
        distances = dict.fromkeys(self.nodes, math.inf)
        shortest_path_tree = dict.fromkeys(self.nodes, False)

        # Set the distance of the source vertex to 0
        distances[id1] = 0

        # find the shortest path for all vertices
        for _ in range(0,len(self.nodes)):
            min_node = find_min_distance(distances,shortest_path_tree)
            shortest_path_tree[node] = True

            # update the distances when the node is not in the shortest path
            # and there is an edge from min_node to node
            for node,distance in distances:
                if not shortest_path_tree[node] and \
                    node in self.edges[min_node]:
                    distances[node] = distances[min_node] + 1


def find_min_distance(distances, shortest_path_tree):
    min = math.inf
    min_node = None
    # go through nodes in shortest path tree
    for node,visited in shortest_path_tree:
        # iterate over non-processed nodes
        if not visited:
            if distances[node] < min:
                min = distances[node]
                min_node = node
    return min_node









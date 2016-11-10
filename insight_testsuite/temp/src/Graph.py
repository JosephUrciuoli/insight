__author__ = "joseph_urciuoli"
from collections import defaultdict

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node):
        self.edges[from_node].add(to_node)
        self.edges[to_node].add(from_node)

    def is_within_network(self,id1,id2,degrees_of_separation):
        if degrees_of_separation < 1:
            return False
        # Use bidirectional BFS to compute the shortest path
        visited_start, visited_end, queue_start, queue_finish = set(), set(), [id1], [id2]

        # Each index contains the shortest distance from id1 to i
        distances_start = dict.fromkeys(self.nodes, float("inf"))
        distances_finish = dict.fromkeys(self.nodes, float("inf"))

        distances_start[id1] = 0
        distances_finish[id2] = 0

        shortest_distance = float("inf")

        # bound the number of iterations
        degrees = 0

        while (queue_start or queue_finish) and degrees <= degrees_of_separation:
            # Add the distances from the start
            if len(queue_start) > 0:
                vertex = queue_start.pop(0)
                visited_start.add(vertex)
                degrees = degrees + 1
                for neighbor in self.edges[vertex]:
                    if neighbor not in visited_start:
                        distances_start[neighbor] = distances_start[vertex] + 1
                        queue_start.append(neighbor)

                    if neighbor in visited_end:
                        shortest_distance = distances_start[neighbor] + distances_finish[neighbor]
                        if shortest_distance <= degrees_of_separation:
                            return "trusted"
                        else:
                            return "unverified"
                        
            
            # Add the distances from the finish
            if len(queue_finish) > 0:
                vertex = queue_finish.pop(0)
                visited_end.add(vertex)
                degrees = degrees + 1
                for neighbor in self.edges[vertex]:
                    if neighbor not in visited_end:
                        distances_finish[neighbor] = distances_finish[vertex] + 1
                        queue_finish.append(neighbor)

                    if neighbor in visited_start:
                        shortest_distance = distances_start[neighbor] + distances_finish[neighbor]
                        if shortest_distance <= degrees_of_separation:
                            return "trusted"
                        else:
                            return "unverified"

        return "unverified"

import unittest
from .Payment import Payment
from .Graph import Graph
from collections import defaultdict

class GraphTestCases(unittest.TestCase):
    def test_instantiation(self):
        # Ensure datatypes are instantiated properly and are empty
        # also ensure data structures are empty
        graph = Graph()
        self.assertEqual(type(graph.nodes), type(set()))
        self.assertEqual(type(graph.edges), type(defaultdict(set)))
        self.assertEqual(len(graph.nodes), 0)
        self.assertEqual(len(graph.edges), 0)

    def test_adding_nodes(self):
        # Ensure adding nodes works as expected
        graph = Graph()
        graph.add_node("123")
        self.assertTrue("123" in graph.nodes)
        # Test adding multiples - should not add duplicates
        graph.add_node("123")
        self.assertEqual(len(graph.nodes), 1)
        # Add several nodes
        graph.add_node("456")
        graph.add_node("789")
        self.assertEqual(len(graph.nodes), 3)
        self.assertTrue("456" in graph.nodes)
        self.assertTrue("789" in graph.nodes)

    def test_adding_edges(self):
        # Ensure that edges are added to both dictionaries
        graph = Graph()
        graph.add_edge("1","2")
        self.assertTrue("2" in graph.edges["1"], "Edges added to both dictionaries - 2 in 1")
        self.assertTrue("1" in graph.edges["2"], "Edges added to both dictionaries - 1 in 2")
        # also ensure that nodes with edges are in nodes set
        self.assertTrue("2" in graph.nodes, "Nodes includes any added edges. 2 in nodes")
        self.assertTrue("1" in graph.nodes, "Nodes includes any added edges. 1 in nodes")

        # Ensure no duplicate edges
        graph.add_edge("2", "1")
        self.assertEqual(len(graph.edges["1"]),1, "Duplicate Edges")
        self.assertEqual(len(graph.edges["2"]), 1, "Duplicate Edges")

        # Ensure we can't add an edge with the same node
        graph.add_edge("3","3")
        self.assertFalse("3" in graph.edges.keys(), "Adding recursive edge does not add edge")
        self.assertFalse("3" in graph.nodes, "Adding recursive edge does not add node to nodes")

    def test_degrees_of_separation(self):
        graph = Graph()
        graph.add_node("1")
        graph.add_node("2")
        graph.add_edge("2","1")
        # Check degree of separation less than 1 - returns unverified
        self.assertEqual(graph.is_within_network("2","1",0), "unverified", "Degree of Separation LT 1")
        self.assertEqual(graph.is_within_network("2", "1", 1), "trusted", "Degree of Separation GTE 1")
        # Create the network in the README
        graph = Graph()
        nodes = ["A","B","C","D","E","F"]
        for idx,node in enumerate(nodes):
            graph.add_node(node)
            if idx > 0:
                graph.add_edge(prev,node)
            prev = node
        # Ensure it was created properly
        self.assertEqual(graph.nodes, set(nodes))
        self.assertTrue("B" in graph.edges["A"])
        self.assertTrue("A" in graph.edges["B"])
        self.assertFalse("F" in graph.edges["B"])
        self.assertFalse("A" in graph.edges["A"])
        self.assertTrue("E" in graph.edges["F"])

        #Feature 1 - Transaction with previous user
        # self.assertEquals(graph.is_within_network("A","B",1), "trusted")
        # self.assertEquals(graph.is_within_network("B", "A", 1), "trusted")
        # self.assertEquals(graph.is_within_network("C", "D", 1), "trusted")
        # self.assertEquals(graph.is_within_network("A", "C", 1), "unverified")
        # self.assertEquals(graph.is_within_network("D", "A", 1), "unverified")
        # self.assertEquals(graph.is_within_network("F", "A", 1), "unverified")

        # Feature 2 - transaction with 2nd degree user
        # self.assertEquals(graph.is_within_network("A", "B", 2), "trusted")
        # self.assertEquals(graph.is_within_network("B", "D", 2), "trusted")
        # self.assertEquals(graph.is_within_network("F", "D", 2), "trusted")
        # self.assertEquals(graph.is_within_network("A", "D", 2), "unverified")
        # self.assertEquals(graph.is_within_network("F", "A", 2), "unverified")
        # self.assertEquals(graph.is_within_network("E", "B", 2), "unverified")


        # add another edge for further testing
        graph.add_edge("G", "F")
        print graph.edges
        # Feature 3 - transaction with 4th degree user
        # self.assertEquals(graph.is_within_network("A", "E", 4), "trusted")
        self.assertEquals(graph.is_within_network("F", "B", 5), "trusted")
        # self.assertEquals(graph.is_within_network("C", "E", 4), "trusted")
        # self.assertEquals(graph.is_within_network("C", "G", 4), "trusted")
        # self.assertEquals(graph.is_within_network("A", "F", 4), "unverified")
        # self.assertEquals(graph.is_within_network("A", "G", 4), "unverified")
        # self.assertEquals(graph.is_within_network("B", "G", 4), "unverified")

class PaymentTestCases(unittest.TestCase):
    def test_instantiation(self):
        # initialize payment
        payment = Payment()
        self.assertEqual(payment.id1, None)
        self.assertEqual(payment.id2, None)
        self.assertEqual(payment.amount, None)
        self.assertEqual(payment.message, None)
        self.assertEqual(payment.time, None)

        # initialize with values
        payment = Payment(time="time", id1="id1", id2="id2", amount="amount", message="message")
        self.assertEqual(payment.id1, "id1")
        self.assertEqual(payment.id2, "id2")
        self.assertEqual(payment.amount, "amount")
        self.assertEqual(payment.message, "message")
        self.assertEqual(payment.time, "time")

    def test_string_input(self):
        # Test proper string input
        payment = Payment()
        payment.init_with_text("2016-11-02 09:38:53, 52349, 8552, 8552, Pitcher ")
        self.assertEqual(payment.id1, "52349")
        self.assertEqual(payment.id2, "8552")
        self.assertEqual(payment.amount, "8552")
        self.assertEqual(payment.message, "Pitcher")
        self.assertEqual(payment.time, "2016-11-02 09:38:53")

    def test_string_input_incorrect(self):
        # Test incorrect number of string params
        payment = Payment()
        payment.init_with_text("2016-11-02 09:38:53, 52349, 8552, 8552 Pitcher ")
        self.assertEqual(payment.id1, None)
        self.assertEqual(payment.id2, None)
        self.assertEqual(payment.amount, None)
        self.assertEqual(payment.message, None)
        self.assertEqual(payment.time, None)

        # Test wrong datatype
        payment.init_with_text(12345)
        self.assertEqual(payment.id1, None)
        self.assertEqual(payment.id2, None)
        self.assertEqual(payment.amount, None)
        self.assertEqual(payment.message, None)
        self.assertEqual(payment.time, None)


if __name__ == '__main__':
    unittest.main()

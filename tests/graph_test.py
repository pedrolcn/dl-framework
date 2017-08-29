"""
UnitTests for the interfaces of the Graph and Node Classes
"""
import unittest as ut
from graph import Graph, Node


class GraphInterfaces(ut.TestCase):

    def setUp(self):
        self.default_graph = Graph()

    def test_add_node(self):
        """
        Tests adding a node to the graph
        """
        self.test_node = Node(self.default_graph, name='test_node')
        self.assertEqual(self.default_graph.nodes['0'].name, 'test_node')

    def test_add_node_with_parents_explicit(self):
        """
        Tests adding a node having a parent node explicitly declared
        """
        self.test_node = Node(self.default_graph, name='test_node')
        self.child_node = Node(self.default_graph, name='child_node', parents=[0])
        self.assertEqual(self.default_graph.arcs['0'], 1)

if __name__ == '__main__':
    ut.main()

class Graph(object):
    """
    Implements a representation of a computational graph
    """

    def __init__(self):
        self.nodes = {}
        self.arcs = {}
        self.idx = 0

    def add_node(self, node):
        self.nodes[str(self.idx)] = node
        self.arcs[str(self.idx)] = []

        self.add_arcs(node.parents)

        self.idx += 1

    def add_arcs(self, parents):

        if type(parents) is list:
            for parent_node in parents:
                self.arcs[str(parent_node)] = self.idx

    def topologically_sort(self):
        raise NotImplementedError

    def execute(self, configs):
        raise NotImplementedError


class Node(object):
    """
    Implements a node class to describe the vertex of our graph, each node shall be defined by its type, parent nodes
    (if any), and operation
    """

    def __init__(self, graph=None, name='', node_type=None, parents=()):
        self.name = name
        self.node_type = node_type
        self.parents = parents
        self.cached_output = None

        if graph is not None:
            graph.add_node(self)

    def forward(self):
        raise NotImplementedError

    def backward(self):
        raise NotImplementedError

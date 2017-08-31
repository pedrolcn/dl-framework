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

        if type(parents) is list or type(parents) is tuple:
            for parent_node in parents:
                self.arcs[str(parent_node)].append(self.idx)

    def get_parents_by_var(self, inputs):
        parents = []
        for parameter in inputs:
            parents.append(list(self.nodes.keys())[list(self.nodes.values()).index(parameter)])

        return tuple(parents)

    def topologically_sort(self):
        raise NotImplementedError

    def forward_prop(self):
        raise NotImplementedError

    def backward_prop(self):
        raise NotImplementedError


class Node(object):
    """
    Implements a node class to describe the vertex of our graph, each node shall be defined by its type, parent nodes
    (if any), and operation
    """

    def __init__(self, graph=None, op=None, node_type=None, parents=(), cache=False, name=''):
        self.name = name
        self.op = op
        self.node_type = node_type
        self.parents = parents
        self.g = graph

        if cache:
            self.cached_output = []

        if graph is not None:
            graph.add_node(self)

    def get_cached_outputs_from_parents(self):
        cache = []
        for node in self.parents:
            cache.append(self.g.nodes[node].cached_output)

        return tuple(cache)

    def forward(self):
        raise NotImplementedError

    def backward(self):
        self.op.backward(self)

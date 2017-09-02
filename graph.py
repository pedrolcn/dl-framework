"""Base classes for building the computational graph"""


class Graph(object):
    """
    Representation of a computational graph. A computational graph is a directed Acyclic graph in which the
    nodes represent operations and the edges represent the flow of operands.

    This class uses the attributes Graph.nodes and Graph.arcs to represent the topology of the graph, together with an
    index Graph._idx which shall be a unique identifier of the Nodes as they are added.

    Graph.nodes and graph.arcs are dictionaries describing the topology of the computational graph with keys
    corresponding to str(_idx) of the node in Graph.nodes and to str(_idx) of the origin node of the arc in Graph.arcs.
    It shall be possible to topologically sort the graph based only on the information contained in Graph.Arcs

    This class interacts strongly with the Node class
    """
    def __init__(self):
        """
        Constructor method of the Graph class, initializes all the attributes, takes no arguments

        :return:
        """
        self.nodes = {}
        self.arcs = {}
        self._idx = 0

    @property
    def idx(self):
        """
        Returns the next index of the Graph
        :return:
        """
        return self._idx

    def add_node(self, node):
        """
        Method which adds a node to the graph, adding a key representing it to Graph.nodes and Graph.arcs, the parameter
        node is then added to Graph.nodes and if it has any parents, the relevant arcs are added to Graph.arcs.

        The rationale behind this interface is that a direct low-level call to this method shall very rarely (if ever)
        occur, instead it shall be more commonly called from the Node class constructor

        :param node:
        :return:
        """
        if not isinstance(node, Node):
            raise TypeError
        else:
            self.nodes[str(self._idx)] = node
            self.arcs[str(self._idx)] = []

            self.add_arcs(node.parents)

            self._idx += 1

    def add_arcs(self, parents):
        """
        Method to add the corresponding arcs to the graph  if a Node being added has parent nodes as entries in the
        Graph.arcs dict

        Is called from within graph.add_node if the node being added to the graph has parent nodes. Again, ad-hoc calls
        to this function from outside Graph.add_node (which itself shall more commonly be called from within the Node
        constructor) shall not be common.

        :param parents:
        :return:
        """
        if type(parents) is list or type(parents) is tuple:
            for parent_node in parents:
                self.arcs[str(parent_node)].append(self._idx)

    def get_parents_by_var(self, var_names):
        """
        Method called when instantiating a subclass of Node on which in the constructor's signature the parent nodes are
        specified as parameters via their variable names (the same way as is done in TensorFlow, eg. c = tf.add(a, b)).
        This method then takes the parameter's variable names and returns the keys corresponding to the relevant Nodes
        in the graph.

        :param var_names:
        :return:
        """
        parents = []
        for name in var_names:
            # dict inverse lookup, getting the key from the value
            parents.append(list(self.nodes.keys())[list(self.nodes.values()).index(name)])

        return tuple(parents)

    def topologically_sort(self):
        raise NotImplementedError

    def forward_prop(self):
        raise NotImplementedError

    def backward_prop(self):
        raise NotImplementedError


class Node(object):
    """
    A node abstract class describing the vertex of a graph. In a computational graph nodes are the main elements each
    node represents a operation to be  performed on the inputs defined by the arcs pointing towards it.It is flexible
    enough to encompass arithmetic operations, constants and variables declarations.

    This is an abstract class defining the overall interface of the Node objects, and its interactions with the Graph
    class with which it interacts strongly.
    """
    def __init__(self, graph=None, op=None, node_type=None, parents=(), cache=False, name=''):
        """
        Constructor of the Node class, takes as parameters the graph to which the Node shall be added, the operation op
        performed by the node on the inputs specified by the output of the nodes described in parents, there is the
        option to enable the node to cache the output of its operation which might be useful in computing the backward
        pass (eg. sigmoid function), there is also the option to name the node to give it an additional identifier

        :param graph:
        :param op:
        :param node_type:
        :param parents:
        :param cache:
        :param name:
        """
        self.name = name
        self.op = op
        self.node_type = node_type
        self.parents = parents
        self.g = graph

        if cache:
            self.cached_output = []
        if graph is not None:
            # Shall change in the future, the idea is that if no graph is specified, the node shall be added to a
            # default graph in the same fashion as is done in TensorFlow
            graph.add_node(self)

    def get_cached_outputs_from_parents(self):
        """
        Collects the values from the forward pass of the parent nodes to be taken as parameters for the Node.op
        operation forward pass

        :return:
        """
        cache = []
        for node in self.parents:
            cache.append(self.g.nodes[node].cached_output)

        return tuple(cache)

    def forward(self):
        raise NotImplementedError

    def backward(self):
        raise NotImplementedError

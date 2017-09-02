"""Abstract classes for math operations definition, and arithmetic operation classes"""

import numpy as np
from graph import Node


class BinaryOp(Node):
    """
    Abstract Wrapper for binary operations,subclasses Node, changes the constructor signature to accept two Node
    parameters as mandatory arguments, from which the operation's parameters shall be taken;
    """
    def __init__(self, a, b, bin_op, graph=None, name=None):
        """
        BinaryOp constructor, changes the signature of the Node constructor to accept two Node parameters a and b,
        which shall be nodes existing in the Graph given as parameter, the constructor calls Graph.get_parents_by_var
        to produce a tuple of the ids of the a and b nodes to be used as parameters for the constructor inherited from
        the Node class.

        :param a:
        :param b:
        :param bin_op:
        :param graph:
        :param name:
        """
        if a not in graph.nodes.values():
            raise NameError('Node %s not in the specified graph'.format(str(a)))
        elif b not in graph.nodes.values():
            raise NameError('Node %s not in the specified graph'.format(str(b)))
        else:
            parents = graph.get_parents_by_var((a, b))

        super().__init__(graph=graph, op=bin_op, node_type='op', parents=parents, cache=True, name=name)

    def forward(self):
        """
        forward propagation of the local node, caches the values from the parent nodes and executes the operation
        prescribed by 'op' and caches it

        :return:
        """

        input_values = self.get_cached_outputs_from_parents()
        self.cached_output = self.op(*input_values)

    def backward(self):
        raise NotImplementedError


class MathSum(BinaryOp):
    """
    Binary addition node, implements numpy.add
    Does not enforce shape checking, shall be changed in the future
    """

    def __init__(self, g, a, b, name=None):
        super().__init__(a=a, b=b, graph=g, bin_op=np.add, name=name)

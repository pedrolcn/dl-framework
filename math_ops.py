import numpy as np
from graph import Node


class BinaryOp(Node):
    """
    Abstract class for general binary operations
    """
    def __init__(self, a, b, bin_op, graph=None, name=None):
        if a not in graph.nodes.values():
            raise NameError('Node %s not in the specified graph'.format(a))
        elif b not in graph.nodes.values():
            raise NameError('Node %s not in the specified graph'.format(b))
        else:
            parents = graph.get_parents_by_var((a, b))

        super().__init__(graph=graph, op=bin_op, node_type='op', parents=parents, cache=True, name=name)

    def forward(self):

        input_values = self.get_cached_outputs_from_parents()
        self.cached_output = self.op(*input_values)


class MathSum(BinaryOp):

    def __init__(self,g, a, b, name=None):
        super().__init__(a=a, b=b, graph=g, bin_op=np.add, name=name)

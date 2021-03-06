from bzCompute.algorithms.postorder import Postorder
from bzCompute.graph import Operation
from bzCompute.graph import Variable
from bzCompute.graph import constant
from bzCompute.graph import placeholder

from bzCompute.graph import Graph

import numpy


class SequentialSession:

    def __init__(self):

        self.algorithm = Postorder

    def execute_graph(self, sequence, operation, feed_dict={}):

        executed = [False] * len(sequence)

        for i in range(len(sequence)):

            if executed[i]:
                continue

            node = sequence[i]

            if type(node) == placeholder:
                node.feed_value(feed_dict[node.name])
                node.output = node.value

            elif type(node) == Variable:

                node.output = node.input_value

            elif type(node) == constant:

                node.output = node.input_value

            else:

                inputs = [input_.output for input_ in node.inputs]

                node.output = node.compute(*inputs)

            executed[i] = True

        return operation.output

    def run(self, graph, operation, feed_dict={}):

        traversal_seq = self.algorithm(operation).run()

        return self.execute_graph(traversal_seq, operation, feed_dict)

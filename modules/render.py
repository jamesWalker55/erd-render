from graphviz import Graph

from modules.uid import new as uid


class ObjGraph:
    """a wrapper for graphviz.Graph that uses a unique id for all nodes to avoid name conflicts"""

    def __init__(self, *args, **kwargs):
        self.graph = Graph(*args, **kwargs)
        self.render = self.graph.render
        self.view = self.graph.view
        self.save = self.graph.save

    def node(self, label, **kwargs) -> str:
        """create a node then return its unique id"""
        node_id = uid()
        self.graph.node(node_id, label=label, **kwargs)
        return node_id

    def edge(self, node_a: str, node_b: str, label=None, **kwargs):
        """this takes 2 node ids as input, which are returned by the #node method"""
        self.graph.edge(node_a, node_b, label=label, **kwargs)

    def node_style(self, **kwargs):
        # set the node style
        self.graph.attr("node", **kwargs)

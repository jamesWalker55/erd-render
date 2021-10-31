from contextlib import contextmanager

from graphviz import Graph

from modules.uid import new as uid


class ObjGraph:
    """a wrapper for graphviz.Graph that uses a unique id for all nodes to avoid name conflicts"""

    def __init__(self, *args, **kwargs):
        self.graph = Graph(*args, **kwargs)
        self._node_styles = []

    def node(self, label, **kwargs) -> str:
        """create a node then return its unique id"""
        node_id = uid()
        self.graph.node(node_id, label=label, **kwargs)
        return node_id

    def edge(self, node_a: str, node_b: str, label=None, **kwargs):
        """this takes 2 node ids as input, which are returned by the #node method"""
        self.graph.edge(node_a, node_b, label=label, **kwargs)

    @contextmanager
    def node_style(self, **kwargs):
        # set the node style
        self.graph.attr("node", **kwargs)
        self._node_styles.append(kwargs)
        yield
        self._node_styles.pop()
        if len(self._node_styles) != 0:
            self.graph.attr("node", **self._node_styles[-1])

    def render(self, *args, **kwargs):
        self.graph.render(*args, **kwargs)

    def view(self, *args, **kwargs):
        self.graph.view(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.graph.save(*args, **kwargs)

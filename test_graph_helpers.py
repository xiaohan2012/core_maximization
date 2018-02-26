import pytest
from graph_tool import Graph, GraphView

from graph_helpers import edge_induced_subgraph, gt_int_nodes

@pytest.fixture
def g():
    """    
    """
    G = Graph()
    G.add_vertices(4)
    return G


def test_edge_induced_subgraph(g):
    edges1 = [(0, 1)]
    g1 = edge_induced_subgraph(g, edges1)
    assert gt_int_nodes(g1) == [0, 1]

    edges2 = [(0, 1), (2, 3)]
    g2 = edge_induced_subgraph(g, edges2)
    assert gt_int_nodes(g2) == [0, 1, 2, 3]

import pytest
from networkit import Graph as NGraph
from graph_tool import Graph
from util import complementary_edges


@pytest.fixture
def house_graph_nk():
    """
       0
      / \
     /   \
    /     \
    1 --- 2
    |    /|
    |   / |
    | /   |
    |/    |
    3 --- 4 --- 5

    node       : 0  1  2  3  4  5
    core number: 2  2  2  2  2  1
    """
    G = NGraph()
    for i in range(6):
        G.addNode()

    edges = [(0, 1), (0, 2), (1, 3), (2, 4),
             (1, 2), (3, 4), (2, 3), (4, 5)]
    for u, v in edges:
        G.addEdge(u, v)

    return G


@pytest.fixture
def house_graph():
    g = Graph(directed=False)
    g.add_vertex(6)

    edges = [(0, 1), (0, 2), (1, 3), (2, 4),
             (1, 2), (3, 4), (2, 3), (4, 5)]
    g.add_edge_list(edges)

    return g


@pytest.fixture
def cand_edges(g):
    return complementary_edges(g)

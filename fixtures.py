import pytest
from networkit import Graph
from util import complementary_edges


@pytest.fixture
def g():
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
    G = Graph()
    for i in range(6):
        G.addNode()

    edges = [(0, 1), (0, 2), (1, 3), (2, 4),
             (1, 2), (3, 4), (2, 3), (4, 5)]
    for u, v in edges:
        G.addEdge(u, v)

    return G


@pytest.fixture
def cand_edges(g):
    return complementary_edges(g)

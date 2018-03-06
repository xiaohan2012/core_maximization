import pytest
from graph_tool import Graph
from graph_tool.generation import complete_graph
from graph_tool.topology import kcore_decomposition

from fixtures import house_graph
from graph_helpers import (edge_induced_subgraph, node_induced_subgraph,
                           gt_int_nodes, gt_int_edges,
                           graph_equal, maximal_matching,
                           gt2nk, get_subcores,
                           get_degree_ge)

from test_subcore import get_input


@pytest.fixture
def g():
    """
    """
    G = Graph(directed=False)
    G.add_vertex(4)
    return G


@pytest.mark.parametrize("edges, nodes", [([(0, 1)], [0, 1]),
                                          ([(0, 1), (2, 3)], [0, 1, 2, 3])])
def test_edge_induced_subgraph(g, edges, nodes):
    old_g = Graph(g)  # copy it
    
    new_g = edge_induced_subgraph(g, edges)
    assert gt_int_nodes(new_g) == nodes
    assert gt_int_edges(new_g) == edges
    assert not new_g.is_directed()

    assert graph_equal(old_g, g)  # g is not changed


@pytest.mark.parametrize("nodes", [[0, 1],
                                   [2, 3]])
def test_node_induced_subgraph(g, nodes):
    old_g = Graph(g)  # copy it
    
    new_g = node_induced_subgraph(g, nodes)
    assert gt_int_nodes(new_g) == nodes
    assert not new_g.is_directed()

    assert graph_equal(old_g, g)  # g is not changed


def test_node_induced_subgraph_non_existing_nodes(g):
    # induce on nodes that does not exist
    new_g = node_induced_subgraph(g, [5, 6])
    assert gt_int_nodes(new_g) == []
    

@pytest.mark.parametrize("graph_edges, expected_edges, expected_unmatched",
                         [([(0, 1)], [(0, 1)], [2, 3]),
                          ([(0, 1), (2, 3)], [(0, 1), (2, 3)], []),
                          ([(0, 1), (1, 2), (2, 3)], [(0, 1), (2, 3)], []),
                          # case 4: inspired from house_graph
                          ([(0, 3), (1, 3)], [(0, 3)], [1, 2]),

                          # case 5:
                          # a case that greedy does not give maximum matching
                          # if starts by matching 1, then it should match all nodes
                          ([(0, 2), (0, 3, (1, 2))], [(0, 2)], [1, 3])
                         ])
def test_maximal_matching_simple(g, graph_edges, expected_edges, expected_unmatched):
    g.add_edge_list(graph_edges)
    actual_edges, unmatched = maximal_matching(g, return_unmatched=True)
    assert actual_edges == expected_edges
    assert expected_unmatched == unmatched


def test_gt2nk():
    gt_g = complete_graph(4)
    nk_g = gt2nk(gt_g)
    assert set(gt_int_nodes(gt_g)) == set(nk_g.nodes())
    assert set(gt_int_edges(gt_g)) == set(map(lambda e: tuple(sorted(e)), nk_g.edges()))
    assert gt_g.num_vertices() == nk_g.numberOfNodes()
    assert gt_g.num_edges() == nk_g.numberOfEdges()
    

@pytest.mark.parametrize("edges_to_add, expected",
                         [([], [{0, 1, 2, 3, 4}, {5}]),
                          ([(2, 5)], [{0, 1, 2, 3, 4, 5}])
                         ])
def test_get_subcores(house_graph, edges_to_add, expected):
    house_graph.add_edge_list(edges_to_add)
    kcore = kcore_decomposition(house_graph)
    subcores = get_subcores(house_graph, kcore)
    assert subcores == expected


@pytest.mark.parametrize("input_name, expected",
                         [('line', [1, 2, 2, 1]),
                          ('house', [2, 3, 4, 3, 2, 1])
                         ])
def test_get_degree_ge(input_name, expected):
    g, kcore, _, _ = get_input(input_name)
    degge = get_degree_ge(g, kcore)
    assert list(degge.a) == expected

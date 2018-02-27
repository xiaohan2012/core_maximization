import pytest
import numpy as np
from graph_tool import load_graph, Graph
from graph_tool.topology import kcore_decomposition
from subcore import (find_nodes_to_promote, partition_promotable_nodes,
                     promote_subcore_by_maximal_matching)


def karate_input():
    g = load_graph('data/karate.gml')
    core = kcore_decomposition(g)
    subcore_nodes = list(np.nonzero(core.a == 4)[0])
    return g, core, subcore_nodes


def line_input():
    g = Graph(directed=False)
    g.add_vertex(4)
    g.add_edge_list([(0, 1), (1, 2), (2, 3)])
    return g, kcore_decomposition(g), [0, 1, 2, 3]


def get_input(name):
    if name == 'karate':
        return karate_input()
    elif name == 'line':
        return line_input()


def test_find_nodes_to_promote():
    input_data = get_input('karate')
    g, core, subcore_nodes = input_data
    promotable_nodes_expected = {7, 30, 32, 33}

    promotable_nodes = find_nodes_to_promote(g, subcore_nodes, core)
    assert set(promotable_nodes) == promotable_nodes_expected


@pytest.fixture
def nodes():
    return [1, 2, 3, 4]


@pytest.mark.parametrize('cand_edges, expected_partition',
                         [
                             # case 1
                             ([(1, 2), (3, 4)],
                              ({1, 2, 3, 4}, set())),

                             # case 2
                             ([(1, 2)],
                              ({1, 2}, {3, 4}))])
def test_partition_promotable_nodes(nodes, cand_edges, expected_partition):
    partition = partition_promotable_nodes(nodes, cand_edges)
    assert partition == expected_partition


@pytest.mark.parametrize('cand_edges, selected_edges_true, unpromoted_true',
                         [
                             # case 1: promote success
                             ([(0, 3), (1, 3), (0, 2)],
                              [(0, 3)],
                              set()),
                             # case 2: impossible to promote
                             ([(1, 3), (0, 2)],
                              [],
                              {0, 3}),
                             # case 3: no edges
                             ([],
                              [],
                              {0, 3}),
                         ])
def test_promote_subcore_by_maximal_matching(cand_edges, selected_edges_true, unpromoted_true):
    input_data = get_input('line')
    g, kcore, subcore_nodes = input_data
    
    selected_edges, unpromoted = promote_subcore_by_maximal_matching(
        g, subcore_nodes, cand_edges, kcore)

    assert selected_edges == selected_edges_true
    assert unpromoted == unpromoted_true
    

import pytest
import numpy as np
from graph_tool import load_graph, Graph
from graph_tool.generation import complete_graph
from graph_tool.topology import kcore_decomposition

from graph_helpers import graph_equal, normalize_edges
from subcore import (find_nodes_to_promote, partition_promotable_nodes,
                     edges_to_promote_subcore_by_maximal_matching,
                     edges_to_promote_subcore)


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


def clique_input():
    g = complete_graph(3, directed=False)
    g.add_vertex()  # a singleton to attach edges
    return g, kcore_decomposition(g), [0, 1, 2]


def fake_input1():
    """
     --------
    |5-clique|   # node 0, 1, 2, 3, 4
     --------    # core number: 4
    
    5 ----- 6
    |       |   # the subcore sc
    |       |   # core number: 2
    7 ----- 8
    
    the goal is to promote sc to core 3
    """
    g = complete_graph(5, directed=False)
    g.add_vertex(4)
    g.add_edge_list([(5, 6), (5, 7), (6, 8), (7, 8)])
    core = kcore_decomposition(g)
    assert list(core.a) == [4, 4, 4, 4, 4, 2, 2, 2, 2]
    subcore_nodes = [5, 6, 7, 8]
    return g, core, subcore_nodes


def get_input(name):
    if name == 'karate':
        return karate_input()
    elif name == 'line':
        return line_input()
    elif name == 'clique':
        return clique_input()
    elif name == 'fake1':
        return fake_input1()


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
def test_edges_to_promote_subcore_by_maximal_matching(cand_edges, selected_edges_true, unpromoted_true):
    input_data = get_input('line')
    g, kcore, subcore_nodes = input_data
    old_g = Graph(g)  # copy it
    
    selected_edges, unpromoted = edges_to_promote_subcore_by_maximal_matching(
        g, subcore_nodes, cand_edges, kcore)

    assert selected_edges == selected_edges_true
    assert unpromoted == unpromoted_true
    assert graph_equal(old_g, g)  # graph unchanged


@pytest.mark.parametrize('input_name, cand_edges, expected_return',
                         [
                             # case 1: empty cand_edges, FAIL
                             ('line', [], None),
                             
                             # case 1: line graph, success
                             ('line', [(0, 3)], [(0, 3)]),

                             # case 2: line graph, FAIL
                             ('line', [(1, 3)], None),

                             # case 3: fake1, two intra-sc edges to promote
                             ('fake1', [(5, 8), (6, 7)], [(5, 8), (6, 7)]),

                             # case 4: fake1, two inter-sc edges to promote and one intra-sc edge
                             ('fake1', [(6, 7), (1, 5), (1, 6), (1, 7), (1, 8)], [(1, 5), (1, 8), (6, 7)]),
                             # case 5: fake1, four inter-sc edges to promote
                             ('fake1', [(1, 5), (1, 6), (1, 7), (1, 8)], [(1, 5), (1, 6), (1, 7), (1, 8)]),
                             # case 6: fake1, insufficient num. of edges
                             ('fake1', [(5, 8)], None),

                             # case 7: clique, impossible to promote with insufficient num. of edges
                             ('clique', [(0, 3), (1, 3)], None),

                             # case 8: clique, connect to a lower core node
                             ('clique', [(0, 3), (1, 3), (2, 3)], [(0, 3), (1, 3), (2, 3)])
                         ])
def test_edges_to_promote_subcore(input_name, cand_edges, expected_return):
    input_data = get_input(input_name)
    
    g, core, subcore_nodes = input_data

    old_g = Graph(g)  # copy it
    old_core_number = core[subcore_nodes[0]]

    ret = edges_to_promote_subcore(g, subcore_nodes, cand_edges, core)

    if ret is not None and expected_return is not None:
        assert normalize_edges(ret) == normalize_edges(expected_return)
    else:
        assert ret == expected_return
    
    # the input graph should be unchanged
    assert graph_equal(old_g, g)
        
    # add the selected edges, if succeeds
    # their core number indeeded increments
    if ret is not None:
        g.add_edge_list(ret)

        new_core = kcore_decomposition(g)
        for v in subcore_nodes:
            assert (new_core[v] - old_core_number) == 1
            

def test_subcore_greedy():
    pass

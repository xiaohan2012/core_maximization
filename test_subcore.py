import pytest
import numpy as np
from graph_tool import load_graph, Graph
from graph_tool.generation import complete_graph
from graph_tool.topology import kcore_decomposition

from graph_helpers import (graph_equal, normalize_edges,
                           complementary_edges, get_degree_ge)
from fixtures import house_graph
from subcore import (find_nodes_to_promote, partition_promotable_nodes,
                     edges_to_promote_subcore_by_maximal_matching,
                     edges_to_promote_subcore, subcore_greedy)


def karate_input():
    g = load_graph('data/karate.gml')
    core = kcore_decomposition(g)
    subcore_nodes = list(np.nonzero(core.a == 4)[0])
    return g, core, get_degree_ge(g, core), subcore_nodes


def line_input():
    g = Graph(directed=False)
    g.add_vertex(4)
    g.add_edge_list([(0, 1), (1, 2), (2, 3)])
    core = kcore_decomposition(g)
    return g, core, get_degree_ge(g, core), [0, 1, 2, 3]


def clique_input():
    g = complete_graph(3, directed=False)
    g.add_vertex()  # a singleton to attach edges
    core = kcore_decomposition(g)
    return g, core, get_degree_ge(g, core), [0, 1, 2]


def house_input():
    g = house_graph()
    core = kcore_decomposition(g)
    return g, core, get_degree_ge(g, core), [5]


def house_input_2():
    g = house_graph()
    core = kcore_decomposition(g)
    return g, core, get_degree_ge(g, core), [0, 1, 2, 3, 4]


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
    return g, core, get_degree_ge(g, core), subcore_nodes


def fake_input2():
    """
    
    0 -- 1 -- 2 -- 3 -- 5 -- 6
               \  /
                 4
    the goal is to promote sc to core 3
    """
    g = Graph(directed=False)
    g.add_vertex(7)
    g.add_edge_list([(0, 1), (1, 2), (2, 3), (2, 4),
                     (3, 4), (3, 5), (5, 6)])
    core = kcore_decomposition(g)
    assert list(core.a) == [1, 1, 2, 2, 2, 1, 1]
    subcore_nodes = [0, 1]
    return g, core, get_degree_ge(g, core), subcore_nodes
    

def get_input(name):
    if name == 'karate':
        return karate_input()
    elif name == 'line':
        return line_input()
    elif name == 'clique':
        return clique_input()
    elif name == 'fake1':
        return fake_input1()
    elif name == 'fake2':
        return fake_input2()
    elif name == 'house':
        return house_input()
    elif name == 'house2':
        return house_input_2()


@pytest.mark.parametrize('input_name, expected_output',
                         [
                             ('karate', {7, 30, 32, 33}),
                             ('house', {5}),
                             ('house2', {0, 4}),
                             ('fake2', {0})
                         ])
def test_find_nodes_to_promote(input_name, expected_output):
    input_data = get_input(input_name)
    g, core, degge, subcore_nodes = input_data

    promotable_nodes = find_nodes_to_promote(g, subcore_nodes, core, degge)
    assert set(promotable_nodes) == expected_output


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


@pytest.mark.parametrize('input_name, cand_edges, selected_edges_true, unpromoted_true',
                         [
                             # case 1: promote success
                             ('line',
                              [(0, 3), (1, 3), (0, 2)],
                              [(0, 3)],
                              set()),
                             # case 2: impossible to promote
                             ('line', [(1, 3), (0, 2)],
                              [],
                              {0, 3}),
                             # case 3: no edges
                             ('line', [],
                              [],
                              {0, 3}),

                             # case 4: house, subcore with one node
                             ('house', [(0, 5)], [], {5}),

                             # case 5: clique, all nodes are unpromotable
                             ('clique', [], [], {0, 1, 2}),

                             # case 6: fake input 2, not promotable by maximal matching
                             ('fake2', [(0, 2), (0, 3)], [], {0})
                         ])
def test_edges_to_promote_subcore_by_maximal_matching(
        input_name, cand_edges, selected_edges_true, unpromoted_true):
    input_data = get_input(input_name)
    g, kcore, degge, subcore_nodes = input_data
    old_g = Graph(g)  # copy it
    
    selected_edges, unpromoted = edges_to_promote_subcore_by_maximal_matching(
        g, subcore_nodes, cand_edges, kcore, degge)

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

                             # # case 8: clique, connect to a lower core node
                             # ('clique', [(0, 3), (1, 3), (2, 3)], [(0, 3), (1, 3), (2, 3)]),
                             # case 9: house, on the singleton subcore
                             ('house', [(0, 5)], [(0, 5)]),

                             # case 10, [(0, 6)] gives better result however,
                             # by subcore algorithm, (0, 2) is returned
                             ('fake2', [(0, 2), (0, 6)], [(0, 2)])
                             
                         ])
def test_edges_to_promote_subcore(input_name, cand_edges, expected_return):
    input_data = get_input(input_name)
    
    g, core, degge, subcore_nodes = input_data

    old_g = Graph(g)  # copy it
    old_core_number = core[subcore_nodes[0]]

    ret = edges_to_promote_subcore(g, subcore_nodes, cand_edges, core, degge)

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
            

@pytest.mark.parametrize('cand_edges, B, expected',
                         [
                             # case 1:
                             (None, 1, [(0, 4)]),

                             # case 2
                             (None, 2, [(0, 4), (5, 1)]),

                             # case 3
                             (None, 3, [(0, 4), (1, 4), (0, 3)]),
                         ])
def test_subcore_greedy(house_graph, cand_edges, B, expected):
    if cand_edges is None:  # by default, complement set
        cand_edges = complementary_edges(house_graph)
        cand_edges -= {(0, 5), (2, 5), (3, 5)}  # to avoid ambiguity
        # print('cand_edges', cand_edges)
        
    actual, log = subcore_greedy(house_graph, cand_edges, B, debug=True, log=True)
    print(log)
    assert set(actual) == set(expected)

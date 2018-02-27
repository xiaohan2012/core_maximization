import pytest
import numpy as np
from graph_tool import load_graph
from graph_tool.topology import kcore_decomposition
from subcore import find_nodes_to_promote, partition_promotable_nodes


def karate_input():
    g = load_graph('data/karate.gml')
    core = kcore_decomposition(g)
    subcore_nodes = list(np.nonzero(core.a == 4)[0])
    return g, core, subcore_nodes


def get_input(name):
    if name == 'karate':
        input_data = karate_input()
    return input_data


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

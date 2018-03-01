from greedy_noninc import do_greedy

from fixtures import house_graph_nk as g, cand_edges


def test_k1(g, cand_edges):
    assert do_greedy(g, 1, cand_edges) == [(0, 4)]


def test_k2(g, cand_edges):
    edges = do_greedy(g, 2, cand_edges)
    assert len(edges) == 2
    e1, e2 = edges
    assert e1 == (0, 4)
    assert e2[1] == 5
    assert e2[0] in set(range(5))


def test_k3(g, cand_edges):
    edges = do_greedy(g, 3, cand_edges)
    assert len(edges) == 3
    e1, e2, e3 = edges
    assert e1 == (0, 4)
    assert e2[1] == 5
    assert e2[0] in set(range(5))
    assert e3[1] == 5
    assert e3[0] in set(range(5))
    assert e3[0] != e2[0]


def test_states(g, cand_edges):
    """states are the same before/after calling do_greedy
    """
    cand_edges_prev = set(list(cand_edges))
    edges_prev = set(g.edges())

    do_greedy(g, 3, cand_edges)

    assert set(g.edges()) == edges_prev
    assert cand_edges_prev == cand_edges

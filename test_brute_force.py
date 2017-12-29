from fixtures import g, cand_edges
from brute_force import do_brute_force


def test_brute_force_1(g, cand_edges):
    edges = do_brute_force(g, 1, cand_edges)
    assert edges == {(0, 4)}


def test_brute_force_2(g, cand_edges):
    edges = do_brute_force(g, 2, cand_edges)
    assert len(edges) == 2
    assert (0, 5) in edges
    edges.remove((0, 5))
    u, v = list(edges)[0]
    assert v == 5
    assert u in {1, 2, 3}


def test_brute_force_3(g, cand_edges):
    edges = do_brute_force(g, 3, cand_edges)
    assert edges == {(0, 3), (0, 4), (1, 4)}

import os
import pickle as pkl
import pytest
from graph_tool import load_graph

from baselines import MFRecommender, RandomRecommender

os.environ['OPENBLAS_NUM_THREADS'] = '1'


graph_name = 'grqc'
    

@pytest.fixture
def g():
    return load_graph('data/{}/graph.gt'.format(graph_name))


@pytest.fixture
def cand_edges():
    return pkl.load(open('data/{}/recommended_edges_N10.pkl'.format(graph_name), 'rb'))


def test_mf_recommender(g, cand_edges):
    recommender = MFRecommender(g)
    recommender.train_model()
    rec_edges = recommender.get_top_k_edges(cand_edges, 100)
    assert len(rec_edges) == 100
    for e1, e2 in zip(rec_edges, rec_edges[1:]):
        assert recommender.get_edge_score(*e1) > recommender.get_edge_score(*e2)


def test_random_recommender(cand_edges):
    r = RandomRecommender()
    edges = r.get_top_k_edges(cand_edges, 10000)
    assert len(set(edges)) == 10000
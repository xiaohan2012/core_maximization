import numpy as np
import implicit
from graph_tool.spectral import adjacency
from operator import itemgetter
import networkx as nx

class MFRecommender():
    def __init__(self, g):
        self.g = g
        self.adj = adjacency(g)
        self.model = None
        
    def train_model(self, n_factors=50):
        self.model = implicit.als.AlternatingLeastSquares(factors=50)
        self.model.fit(self.adj)
        return self.model
    
    def get_edge_score(self, u, v):
        return np.dot(self.model.user_factors[u], self.model.item_factors[v])

    def recommend(self, u, k=10):
        return self.model.recommend(u, self.adj, k)
        
    def get_top_k_edges(self, cand_edges, k=100):
        return sorted(cand_edges, key=lambda e: self.get_edge_score(*e), reverse=True)[:k]


class RandomRecommender():
    def get_top_k_edges(self, cand_edges, k=100):
        cand_edges = list(cand_edges)
        ids = np.arange(len(cand_edges))
        sel_ids = np.random.choice(ids, k, replace=False)
        return [cand_edges[i] for i in sel_ids]
    

class CommonNeighbors():
    def __init__(self, g):
        self.g = g

    def get_top_k_edges(self, cand_edges, k=100):
        cand_edges = list(cand_edges)
        preds = nx.resource_allocation_index(self.g, cand_edges)
        # preds.sort(key=itemgetter(3), reverse=True)
        top = sorted(preds, key=itemgetter(2), reverse=True)
        return [(u, v) for u, v, p in top[:k]]

    
class AdamicAdar():
    def __init__(self, g):
        self.g = g

    def get_top_k_edges(self, cand_edges, k=100):
        cand_edges = list(cand_edges)
        preds = nx.adamic_adar_index(self.g, cand_edges)

        top = sorted(preds, key=itemgetter(2), reverse=True)
        #  preds.sort(key=itemgetter(3),reverse=True)
        return [(u, v) for u, v, p in top[:k]]


class Jaccard():
    def __init__(self, g):
        self.g = g

    def get_top_k_edges(self, cand_edges, k=100):
        cand_edges = list(cand_edges)
        preds = nx.jaccard_coefficient(self.g, cand_edges)
        
        top = sorted(preds, key=itemgetter(2), reverse=True)
        return [(u, v) for u, v, p in top[:k]]

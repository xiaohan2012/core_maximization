import numpy as np
import implicit
from graph_tool.spectral import adjacency


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
    


# coding: utf-8

# In[126]:


import os
import pickle as pkl
from graph_tool import load_graph
from subcore import subcore_greedy


graph_name = 'grqc'
budget = 100
g = load_graph('data/{}/graph.gt'.format(graph_name))

cand_edges = pkl.load(open('data/{}/recommended_edges_N10.pkl'.format(graph_name), 'rb'))

sel_edges = subcore_greedy(g, cand_edges, budget, debug=False, log=True, show_progress=True)


output_dir = 'output/{}/subcore'.format(graph_name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


pkl.dump(sel_edges,
         open(os.path.join(output_dir, 'B{}.pkl'.format(budget)), 'wb'))



# coding: utf-8

# In[71]:


import pickle as pkl
import os

from networkit import overview, Glist
from graph_tool import load_graph
from graph_tool.topology import kcore_decomposition
from greedy_noninc import do_greedy
from networkit.graphio import readGraph, Format


# In[59]:


graph_name = 'grqc'
budget = 100
g = readGraph('data/{}/graph.graphml'.format(graph_name), fileformat=Format.GraphML)
g_gt = load_graph('data/{}/graph.gt'.format(graph_name))


# In[62]:


kcore = kcore_decomposition(g_gt)
print('sum of core', sum(kcore.a))
print('num edges', g.numberOfEdges())


# In[50]:


glist = Glist(g)
prev_score = sum(glist.core)
print('prev_score={}'.format(sum(glist.core)))


# In[51]:


cand_edges = pkl.load(open('data/{}/recommended_edges_N10.pkl'.format(graph_name), 'rb'))


# In[53]:


greedy_edges = do_greedy(g, budget, cand_edges, debug=False, log=False, show_progress=True)


# In[72]:


output_dir = 'output/{}/greedy'.format(graph_name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
pkl.dump(greedy_edges, open(os.path.join(output_dir, 'B{}.pkl'.format(budget)), 'wb'))


# In[63]:


core_before = sum(kcore.a)


# In[65]:


g_gt.add_edge_list(greedy_edges)


# In[66]:


core_after = sum(kcore_decomposition(g_gt).a)


# In[69]:


print('core before/after', core_before, core_after)


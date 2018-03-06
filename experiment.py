
# coding: utf-8

# In[126]:


import os
import pickle as pkl
from graph_tool import load_graph
from graph_tool.topology import kcore_decomposition
from subcore import subcore_greedy


# In[120]:


graph_name = 'grqc'
g = load_graph('data/{}/graph.gt'.format(graph_name))


# In[121]:


cand_edges = pkl.load(open('data/{}/recommended_edges_N10.pkl'.format(graph_name), 'rb'))


# In[122]:


budget = 100


# In[123]:


sel_edges = subcore_greedy(g, cand_edges, budget, debug=False, log=True, show_progress=True)


# In[127]:


output_dir = 'output/{}/subcore'.format(graph_name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# In[129]:


pkl.dump([], open(os.path.join(output_dir, 'B{}.pkl'.format(budget)), 'wb'))


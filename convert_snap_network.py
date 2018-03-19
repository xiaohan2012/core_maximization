import os
import networkx as nx
from tqdm import tqdm

# 'livejournal', 
for dataset in tqdm(('condmat', 'enron')):
    output_path = 'data/{}/graph.graphml'.format(dataset)
    if os.path.exists(output_path):
        print('computed, skip')
        continue

    with open('data/{}/graph.txt'.format(dataset)) as f:
        g = nx.Graph()
        for l in f:
            u, v = map(int, l.split())
            g.add_edge(u, v)

        ccs = nx.connected_components(g)
        lcc = max(ccs, key=len)
        lcc_g = g.subgraph(lcc)
        lcc_g = nx.convert_node_labels_to_integers(lcc_g)
        # nx.write_gpickle(lcc_g, 'data/{}/graph.gpkl'.format(dataset))
        nx.write_graphml(lcc_g, output_path)

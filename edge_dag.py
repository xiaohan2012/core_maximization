import networkx as nx
from graph_helpers import get_kcore, sort_pair
from tqdm import tqdm


def get_edge_dag(original_g, cand_edges, iter_callback=None, verbose=True):
    g = original_g.copy()
    # old_core = get_kcore(g)
    pending_edges_g = nx.Graph()
    active_edges_g = nx.Graph()

    edge2meta_node = {}

    # pending_edges = set()
    # active_edges = set()

    edge_dag = nx.DiGraph()
    # meta_nodes = []
    # meta_edges = []
    
    for iter_i, (u, v) in tqdm(enumerate(cand_edges)):
        u, v = sort_pair([u, v])

        old_core = get_kcore(g)
        g.add_edge(u, v)
        new_core = get_kcore(g)
        core_increase = int((new_core - old_core).sum())

        affected_nodes = list((new_core != old_core).nonzero()[0])

        if affected_nodes:
            if verbose:
                print('adding ({}, {}) promotes {}'.format(u, v, affected_nodes))

            # get related pending edges
            # and create the meta node
            related_pending_edges = []
            for i in affected_nodes:
                if pending_edges_g.has_node(i):
                    for j in pending_edges_g[i]:
                        if new_core[i] >= new_core[j]:
                            related_pending_edges.append((i, j))

            related_pending_edges.append((u, v))
            # print('related pending edges', related_pending_edges)
            meta_node = tuple(set(sorted(map(sort_pair, related_pending_edges))))
            
            if verbose:
                print('new meta node:', meta_node)

            # create the indexing
            for e in meta_node:
                edge2meta_node[e] = meta_node

            # get meta nodes dependencies
            related_active_edges = []
            for i in affected_nodes:
                if active_edges_g.has_node(i):
                    for j in active_edges_g[i]:
                        if new_core[i] <= new_core[j]:  # only peer or higher-core neighbors
                            related_active_edges.append((i, j))

            related_active_edges = set(map(sort_pair, related_active_edges))
            # print('related active edges', related_active_edges)

            parent_meta_nodes = set()
            for e in related_active_edges:
                parent_meta_nodes.add(edge2meta_node[e])
            if verbose:
                print('parent meta nodes', parent_meta_nodes)

            # update the edge_dag
            attrs = {'local_gain': core_increase,
                     'local_weighted_gain': core_increase / len(meta_node)}
            edge_dag.add_node(
                meta_node,
                attrs)
            inc_edge_cost = len(meta_node)
            inc_gain = core_increase
            for n in parent_meta_nodes:
                edge_dag.add_edge(n, meta_node)
                inc_edge_cost += edge_dag.node[n]['inc_edge_cost']
                inc_gain += edge_dag.node[n]['inc_gain']
                inc_gain
            edge_dag.node[meta_node]['inc_edge_cost'] = inc_edge_cost
            edge_dag.node[meta_node]['inc_gain'] = inc_gain
            edge_dag.node[meta_node]['inc_weighted_gain'] = inc_gain / inc_edge_cost

            # these edges are not pending any more
            pending_edges_g.remove_edges_from(related_pending_edges)
            # these edges become active
            active_edges_g.add_edges_from(related_pending_edges)
        else:
            if verbose:
                print('adding ({}, {}) promotes nothing'.format(u, v))
            pending_edges_g.add_edge(u, v)

        if callable(iter_callback):
            new_core_num = (new_core[affected_nodes][0] if affected_nodes else None)
            iter_callback(g, iter_i, (u, v), affected_nodes, new_core_num, edge_dag)

        if verbose:
            print('-' * 10)
    return edge_dag

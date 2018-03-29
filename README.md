# core_maximization

# software dependency

- [graph_tool](https://graph-tool.skewed.de/)
  - takes a lot of time to compile, be patient!
- [networkit (modified by Han)](https://github.com/xiaohan2012/networkit/)
  - the main modification by Han is the addition of dynamic core maintenance using method by [this paper](https://arxiv.org/abs/1606.00200)
- pandas, numpy, implicit

## other version info

- Python 3.5

# important files

## preparing for data

note that for `grqc` and `condmat`, candidate edges are already prepared in `data/{dataset}/recommended_edges_N{num_edges_per_node}.pkl``

in case you need to generate it by yourself, use

- `get_candidate_edges_by_MF.py`: this recommend candidate edges by MF techniques

## algorithms

- `greedy_noninc.py`: greedy (non-incremental)
- `baselines.py`: random and MF
- `edge_dag_algorithm.ipynb`: the edge DAG algorithm (**inmature for now**)

## run experiments

- `experiment_greedy.py`: experiment using greedy
- `experiment_mf.py`: experiment using matrix factorization
- `experiment_random.py`: experiment using random edge selection

# evaluation

- `evaluation_plot.ipynb`: open it as Jupyter notebook!

# todo

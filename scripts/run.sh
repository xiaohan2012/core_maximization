#! /bin/zsh

budget=500
graphs=(grqc condmat)
N_list=(10)
baseline_methods=("adamicadar" "jaccard" "cn" "random" "mf" "greedy")

for baseline_method in ${baseline_methods}; do
    for graph in ${graphs}; do
	for N in ${N_list}; do
	    print "python3 experiment_${baseline_method}.py -g ${graph} -b ${budget} -n ${N}"
	done
    done
done

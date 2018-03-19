#! /bin/zsh

budget=10000
graphs=(grqc condmat enron)
N_list=(10 100)

for graph in ${graphs}; do
    for N in ${N_list}; do
	print "python3 experiment_greedy.py -g ${graph} -b ${budget} -n ${N}"
    done
done

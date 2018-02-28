# core_maximization


# todo

- [X] implement `PROMOTE-SUBCORE` (Algorithm 6)
- [ ] get the subcore list
- [ ] how to re-build networkit: https://networkit.iti.kit.edu/api/DevGuide.html#unit-tests-and-testing
- [ ] implement `SUBCORE-GREEDY` (Algorithm 7)
  - need to specifiy the  cache update mechanism (where "details omitted")
- [ ] cache usage and update for `GREEDY`
- experiment

# motivation of subcore algorithm

it's cheaper to promote a whole subcore for the following reason:

given a subcore, some of its nodes (call `V_1`) might already have enough edges, all they need to be promoted is that the other nodes (call `V_2`) in the subcore are promoted .

note that `V_1 | V_2 = V(subcore)` and `V_1 & V_2 = \emptyset`


[ ] to check:

1. `\sum |V_1| / \sum (|V_1| + |V_2|)`: saturation rate overall
2. `\mean (|V_1| / (|V_1| + |V_2|))`: average saturation rate
   - the higher the above ratios are, the fewer edges we need to promote subcores



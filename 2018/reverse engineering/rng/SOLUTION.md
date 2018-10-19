# RNG
## Solution
After reverse engineering this binary (sorry), the competitors should realize that this is an absorbing Markov chain. Now they have two options:

1. Solve the Absorbing Markov Chain. This can be achieved by solving for B = NR, where B is the probability of each transient state entering each absorbing state. Then, they can use this to solve the problem.

2. Generate a bajillion numbers and find the most frequent one. Then, generate enough so that the generation probability is accurate to ten digits. Theoretically this is possible, but I would definitely not recommend this approach.

Flag:

<center>

`hackgt{f10194618403}`

<center>
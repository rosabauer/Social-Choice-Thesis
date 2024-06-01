import matplotlib.pyplot as plt
import numpy as np
import scipy.special

'''Graph showing group accuracy as individual competency grows for a number of agents N'''

# Number of agents for which we want to show group accuracy
agent_numbers = [1,3,5,9,17,33,65]


# Function to determine probability that the majority of the group is correct
def condorcet(n, p):
    sum_result = 0
    for i in range((n // 2) + 1, n + 1):
        binom_coeff = scipy.special.comb(n, i)
        term = binom_coeff * (p ** i) * ((1 - p) ** (n - i))
        sum_result += term
    return sum_result

x = np.linspace(0,1)
fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(x, condorcet(x,0.6), label='0.6')

# For each N, create a subplot
ax.plot(x, condorcet(agent_numbers[0],x), label='N=1')
ax.plot(x,condorcet(agent_numbers[1],x), label='N=3')
ax.plot(x,condorcet(agent_numbers[2],x), label='N=5')
ax.plot(x,condorcet(agent_numbers[3],x), label= 'N=9')
ax.plot(x,condorcet(agent_numbers[4],x), label= 'N=17')
ax.plot(x,condorcet(agent_numbers[5],x), label= 'N=33')
ax.plot(x,condorcet(agent_numbers[6],x), label= 'N=65')

ax.set_xlabel('Individual competency')
ax.set_ylabel('Group competency')
ax.legend()

plt.show()
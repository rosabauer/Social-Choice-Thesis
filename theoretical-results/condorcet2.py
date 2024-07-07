import numpy as np
import matplotlib.pyplot as plt
import scipy.special

def condorcet(n, p):
    sum_result = 0
    for i in range((n // 2) + 1, n + 1):
        binom_coeff = scipy.special.comb(n, i)
        term = binom_coeff * (p ** i) * ((1 - p) ** (n - i))
        sum_result += term
    return sum_result

# Define the fixed probability p
p = 0.6

# Generate a range of n values
n_values = range(1, 21)  # For example, n from 1 to 20

# Calculate Condorcet function values for each n
condorcet_values = [condorcet(n, p) for n in n_values]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(n_values, condorcet_values, marker='o', linestyle='-', color='b')
plt.xlabel('n')
plt.ylabel('Condorcet Probability')
plt.title('Condorcet Probability for p = 0.6')
plt.grid(True)
plt.show()


'''NOTE: These were the simulation results for the same competency: 
Agents: 3, Condorcet Value: 0.648
Agents: 6, Condorcet Value: 0.54432
Agents: 9, Condorcet Value: 0.7334323199999999
Agents: 12, Condorcet Value: 0.6652085575679999
Agents: 15, Condorcet Value: 0.786896817389568
Agents: 18, Condorcet Value: 0.7368411690211737
Agents: 21, Condorcet Value: 0.8256221336382271
Agents: 24, Condorcet Value: 0.7869782010394586
Agents: 27, Condorcet Value: 0.85534823563728
Agents: 30, Condorcet Value: 0.8246309464931707
'''
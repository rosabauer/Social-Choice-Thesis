import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

def compute_function(a, b, p):
    result = 0
    for bi in range(b + 1):
        # Probability P(B = bi)
        P_B_eq_bi = binom.pmf(bi, b, p)
        # Binomial CDF F(bi; a, p)
        F_bi_a_p = binom.cdf(bi, a, p)
        # Summation
        result += P_B_eq_bi * F_bi_a_p
    return result

# Values for a and b
a = 5
b = 3

# Generate p values
p_vals = np.linspace(0, 1, 100)

# Calculate the results for each p value
results = [compute_function(a, b, p) for p in p_vals]

# Plot the function
plt.figure(figsize=(10, 6))
plt.plot(1-p_vals, results, label=f'Function for a={a}, b={b}')
plt.xlabel('p values')
plt.ylabel('Result')
plt.title('Function involving Binomial CDF and PMF')
plt.legend()
plt.grid(True)
plt.show()

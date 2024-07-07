import numpy as np
import matplotlib.pyplot as plt
from sympy import binomial

'''This has the same version of the function in it as evidence-probability-function, 
but with a scatter plot visualization instead of a continuous plot.

UPDATE: Function correctly modified, and visual was also broken. '''

# Define ranges for a, b, and p
a_vals = np.arange(0, 10)
b_vals = np.arange(0, 10)
p_val = 0.7  # Fixed p value

# Initialize an array to store the results
results = np.zeros((len(a_vals), len(b_vals)))

# Custom function to evaluate the expression
def lower_bound_func(a_val, b_val, p_val):
    a_val = int(a_val)
    b_val = int(b_val)
    
    result = 0
    
    for m in range(b_val+1):
        for k in range(a_val - m + 1):
            term = binomial(a_val, m + k) * binomial(b_val, m) * p_val**(2*m + k) * (1 - p_val)**(a_val + b_val - (2*m + k))
            result += term
    return result

# Compute the function values
for i, a_val in enumerate(a_vals):
    for j, b_val in enumerate(b_vals):
        results[i, j] = lower_bound_func(a_val, b_val, p_val)

# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Ensure correct reshaping and flattening
A, B = np.meshgrid(a_vals, b_vals, indexing='ij')
C = results.flatten()

ax.scatter(A.flatten(), B.flatten(), C, c=C, cmap='viridis')

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('Function Value')
plt.title('Winning Evidence Probability Plot for p=0.7')

# Test cases general
print(lower_bound_func(10, 1, 0.7))
print(lower_bound_func(1, 8, 0.7))
print(lower_bound_func(0, 8, 0.7))

# Testing for theorem calculations start here

print(lower_bound_func(6,4,0.7))

plt.show()
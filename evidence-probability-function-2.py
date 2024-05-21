import numpy as np
import matplotlib.pyplot as plt
from sympy import binomial

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
    for k in range(0, a_val - b_val + 1):
        term = binomial(a_val, b_val + k) * binomial(b_val, b_val) * p_val**(2*b_val + k) * (1 - p_val)**(a_val + b_val - (2*b_val + k))
        result += term
    return result

# Compute the function values
for i, a_val in enumerate(a_vals):
    for j, b_val in enumerate(b_vals):
        results[i, j] = lower_bound_func(a_val, b_val, p_val)

# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Plotting points where a and b are integers
A, B = np.meshgrid(a_vals, b_vals)
A = A.flatten()
B = B.flatten()
C = results.flatten()
ax.scatter(A, B, C, c=C, cmap='viridis')

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('Function Value')
plt.title('Winning Evidence Probability Plot for p=0.7')

plt.show()

print('This is a test.')
print(lower_bound_func(8, 1, 0.7))
print(lower_bound_func(1, 8, 0.7))
print(lower_bound_func(0, 8, 0.7))  # Makes sense, since a is the correct option

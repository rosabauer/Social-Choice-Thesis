import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, summation, binomial

# Define the symbols
a, b, bi, k, p = symbols('a b bi k p')

# Define the expression
expr = binomial(a, bi + k) * binomial(b, bi) * p**(2*bi + k) * (1 - p)**(a + b - (2*bi + k))

# Define the double summation
double_sum = summation(summation(expr, (k, 0, a - bi)), (bi, 0, b))

# Define ranges for a, b, and p
a_vals = np.arange(0, 10)
b_vals = np.arange(0, 10)
p_vals = np.linspace(0.5, 1, 100)  # p values greater than 0.5

# Initialize an array to store the results
results = np.zeros((len(a_vals), len(b_vals), len(p_vals)))

# Custom function to evaluate the expression
def func(a_val, b_val, p_val):
    result = 0
    for bi in range(0, b_val + 1):
        for k in range(0, a_val - bi + 1):
            term = binomial(a_val, bi + k) * binomial(b_val, bi) * p_val**(2*bi + k) * (1 - p_val)**(a_val + b_val - (2*bi + k))
            result += term
    return result

def lower_bound_func(a_val, b_val, p_val):
    result = 0

    for k in range(0, a_val - b_val + 1):
        term = binomial(a_val, b_val + k) * binomial(b_val, b_val) * p_val**(2*b_val + k) * (1 - p_val)**(a_val + b_val - (2*b_val + k))
        result += term
    return result

# Uncomment to show standard function
'''# Compute the function values
for i, a_val in enumerate(a_vals):
    for j, b_val in enumerate(b_vals):
        for k, p_val in enumerate(p_vals):
            results[i, j, k] = func(a_val, b_val, p_val)

# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
A, B = np.meshgrid(a_vals, b_vals)

# Plotting for a few values of p to avoid overcrowding the plot
for idx in range(0, len(p_vals), 10):  # Plot every 10th p_val
    ax.plot_surface(A, B, results[:, :, idx], alpha=0.3)

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('Function Value')
plt.title('Winning evidence probability plot')

# Workaround to display legends in 3D plot
legend_labels = [f'p={p_vals[idx]:.2f}' for idx in range(0, len(p_vals), 10)]
ax.text2D(0.05, 0.95, "Legends:\n" + "\n".join(legend_labels), transform=ax.transAxes)

print('This is a test.')
print(func(8,1,0.7))
print(func(1,8,0.7))
print(func(0,8, 0.7)) # Makes sense, since a is the correct option
#plt.show()'''

# Initialize an array to store the results
results = np.zeros((len(a_vals), len(b_vals), len(p_vals)))

# Compute the function values
for i, a_val in enumerate(a_vals):
    for j, b_val in enumerate(b_vals):
        for k, p_val in enumerate(p_vals):
            results[i, j, k] = lower_bound_func(a_val, b_val, p_val)

# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
A, B = np.meshgrid(a_vals, b_vals)

# Plotting for a few values of p to avoid overcrowding the plot
for idx in range(0, len(p_vals), 10):  # Plot every 10th p_val
    ax.plot_surface(A, B, results[:, :, idx], alpha=0.3)

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('Function Value')
plt.title('Winning evidence probability plot')

# Workaround to display legends in 3D plot
legend_labels = [f'p={p_vals[idx]:.2f}' for idx in range(0, len(p_vals), 10)]
ax.text2D(0.05, 0.95, "Legends:\n" + "\n".join(legend_labels), transform=ax.transAxes)

print('This is a test.')
print(lower_bound_func(8,1,0.7))
print(lower_bound_func(1,8,0.7))
print(lower_bound_func(0,8, 0.7)) # Makes sense, since a is the correct option
plt.show()

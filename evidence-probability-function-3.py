import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom

for i in range(5):
    print('hello')

def lower_bound_func(a_val, b_val, p_val):
    a_val = int(a_val)
    b_val = int(b_val)
    
    result = 0
    
    for m in range(b_val+1):
        for k in range(a_val - m+1):
            term = binom(a_val, m + k) * binom(b_val, m) * p_val**(2*m + k) * (1 - p_val)**(a_val + b_val - (2*m + k))
            result += term
    return result

def complex_function(a, b, p):
    result = 0
    for bi in range(b + 1):
        inner_sum = 0
        for k in range(a - bi + 1):
            inner_term = binom(a, bi + k) * (p**(bi + k)) * ((1 - p)**(a - bi - k))
            inner_sum += inner_term
        outer_term = binom(b, bi) * (p**bi) * ((1 - p)**(b - bi))
        result += inner_sum * outer_term
    return result

# Values for a and b
a = 5
b = 3

# Generate p values
p_vals = np.linspace(0, 1, 100)

# Calculate the results for each p value
results = [complex_function(a, b, p) for p in p_vals]

# Plot the function
plt.figure(figsize=(10, 6))
plt.plot(p_vals, results, label=f'Function for a={a}, b={b}')
plt.xlabel('p values')
plt.ylabel('Pr(a > b)')
plt.title('Competency of a single agent')
plt.legend()
plt.grid(True)
plt.show()

# Values for a and b
a_values = [2, 5, 6, 10, 100, 300]
b_values = [1, 3, 4, 5, 99, 299]

# Generate p values
p_vals = np.linspace(0, 1, 100)

# Plot the function for different values of a and b
plt.figure(figsize=(10, 6))

for a_val, b_val in zip(a_values, b_values):
    results = [lower_bound_func(a_val, b_val, p) for p in p_vals]
    plt.plot(p_vals, results, label=f'a={a_val}, b={b_val}')

plt.xlabel('p values')
plt.ylabel('Result')
plt.legend()
plt.grid(True)
plt.show()

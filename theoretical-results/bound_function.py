from math import comb
import matplotlib.pyplot as plt
import numpy as np
import scipy.special

def compute_expression(a, b, p):
    result = 0
    for b_i in range(b + 1):
        inner_sum_1 = 0
        for i in range(b_i + 1):
            inner_sum_1 += comb(a, i) * p**i * (1 - p)**(a - i)
        
        binomial_term = comb(b, b_i) * p**b_i * (1 - p)**(b - b_i)
        
        inner_sum_2 = 0
        for k in range(a - b_i + 1):
            inner_sum_2 += comb(a, b_i + k) * comb(b, b_i) * p**(2 * b_i + k) * (1 - p)**(a + b - (2 * b_i + k))
        
        result += (1 - inner_sum_1) * binomial_term - inner_sum_2
        
    return result

# Parameters
a_values = [5, 6]
b_values = [3, 4]
p_values = np.linspace(0, 1, 100)

# Plotting
plt.figure(figsize=(10, 6))

for a in a_values:
    for b in b_values:
        if a > b:
            y_values = [compute_expression(a, b, p) for p in p_values]
            plt.plot(p_values, y_values, label=f'a={a}, b={b}')

plt.xlabel('p')
plt.ylabel('Function Value')
plt.title('Plot of the function for different a and b combinations')
plt.legend()
plt.grid(True)
plt.show()

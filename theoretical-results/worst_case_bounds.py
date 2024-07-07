from class_structure import *
import matplotlib.pyplot as plt
import math
import numpy as np  

'''This simulation is meant to verify the claim that, as n grows, the number of agents for whom pA > B stays below n(q-1/2)'''

# SPECIAL METHOD (depleted) We generate n a-agents and see how much evidence they have
def a_agents_strong_competence(no_of_agents, competence, a_evidence, b_evidence):
    agents = []
    while len(agents) < no_of_agents:
        agent = Agent(a_evidence=a_evidence, b_evidence=b_evidence, p_competence=competence)
        if agent.es_A.count(1) > agent.es_B.count(1):
            agents.append(agent)  # Only add the agent if it has more evidence for A than B
    
    y_random_variable = 0

    for agent in agents:
        if competence * agent.es_A.count(1) > agent.es_B.count(1):
            y_random_variable += 1

    return y_random_variable

  # We generate n agents and give back the variable for how much evidence they have
def agents_strong_competence(no_of_agents, competence, a_evidence, b_evidence):
  agents = [Agent(a_evidence=a_evidence, b_evidence=b_evidence, p_competence=competence) for _ in range(no_of_agents)]
    
  y_random_variable = 0

  for agent in agents:
      if competence * agent.es_A.count(1) > agent.es_B.count(1):
          y_random_variable += 1

  return y_random_variable

def agents_wlln(no_of_agents, competence, a_evidence, b_evidence):
    agents = [Agent(a_evidence=a_evidence, b_evidence=b_evidence, p_competence=competence) for _ in range(no_of_agents)]
    
    evidence_A = []

    for agent in agents:
      evidence_A.append(agent.es_A.count(1))
      print(agent.es_A.count(1))

    return evidence_A

def binomial_coefficient(n, k):
    return math.comb(n, k)

def group_competency(a, b, p):
    total_sum = 0
    
    for bi in range(b + 1):
        for k in range(a - bi + 1):
            term = (binomial_coefficient(a, bi + k) *
                    binomial_coefficient(b, bi) *
                    p**(2 * bi + k) *
                    (1 - p)**(a + b - (2 * bi + k)))
            total_sum += term
    
    return total_sum

def wlln(a_evidence, p_competence, b_evidence):
    agent_numbers = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250, 300]
    results = {n: [] for n in agent_numbers}
    bounds = [p_competence * a_evidence] * len(agent_numbers)

    for n in agent_numbers:
        for _ in range(20):
            result = agents_wlln(n, p_competence, a_evidence, b_evidence)
            results[n].append(result)
  
    for n in agent_numbers:
        for i in range(20):
            plt.scatter([n] * len(results[n][i]), results[n][i], color='blue')

def statistical_wlln (a_evidence, p_competence, b_evidence):
    agent_numbers = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250, 300]
    means = []
    variances = []
    bounds = [p_competence * a_evidence] * len(agent_numbers)

    for n in agent_numbers:
        evidence_counts = []
        for _ in range(20):
            result = agents_wlln(n, p_competence, a_evidence, b_evidence)
            evidence_counts.extend(result)
        
        mean_evidence = np.mean(evidence_counts)
        variance_evidence = np.var(evidence_counts)
        
        means.append(mean_evidence)
        variances.append(variance_evidence)
  
    plt.figure(figsize=(12, 6))
    plt.errorbar(agent_numbers, means, yerr=np.sqrt(variances), fmt='o', color='blue', ecolor='lightgray', elinewidth=3, capsize=0, label='Mean Evidence A with Variance')
    plt.plot(agent_numbers, bounds, color='red', label='Bound Points')
    plt.xlabel('Number of Agents')
    plt.ylabel('Evidence A')
    plt.title('Mean and Variance of Evidence A')
    plt.legend()
    plt.show()

def generate_data(a_evidence, b_evidence, p_competence):
    agent_numbers = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250, 300]
    results = {n: [] for n in agent_numbers}
    bounds = []

    for n in agent_numbers:
        bound = n * (group_competency(a_evidence, b_evidence, p_competence) - 0.5)
        bounds.append(bound)
        
        for _ in range(20):  # Run the function 20 times for each number of agents
            result = agents_strong_competence(n, p_competence, a_evidence, b_evidence)
            results[n].append(result)
    
    # Plotting the results
    for n in agent_numbers:
        plt.scatter([n]*20, results[n], color='blue')  # Match the length of x and y
    
    plt.scatter(agent_numbers, bounds, color='red', label='Bound Points')
    plt.xlabel('Number of Agents')
    plt.ylabel('Value of Y')
    plt.title('Value of Y for Number of Agents')
    plt.legend()
    plt.show()

  
def generate_data_mean(a_evidence, b_evidence, p_competence):
  agent_numbers = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250, 300]
  results = {n: [] for n in agent_numbers}
  mean_values = []
  variances = []
  bounds = []

  for n in agent_numbers:
      agent_results = []
      for _ in range(20):  # Run the function 20 times for each number of agents
          result = agents_strong_competence(n, p_competence, a_evidence, b_evidence)
          agent_results.append(result)
        
      results[n] = agent_results
      mean_value = np.mean(agent_results)
      variance = np.var(agent_results)
      mean_values.append(mean_value)
      variances.append(variance)

      bound = n * (group_competency(a_evidence, b_evidence, p_competence) - 0.5)
      bounds.append(bound)
    
  # Plotting the results
  plt.errorbar(agent_numbers, mean_values, yerr=np.sqrt(variances), fmt='o', color='blue', label='Mean and Variance')
  plt.scatter(agent_numbers, bounds, color='red', label='Bound Points')
  plt.xlabel('Number of Agents')
  plt.ylabel('Value of Y')
  plt.title('Mean and Variance of Y for Number of Agents')
  plt.legend()
  plt.show()

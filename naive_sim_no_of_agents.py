
# Code for previous type of graphic

'''from class_structure import DeliberationSetting
import numpy as np
import matplotlib.pyplot as plt

# This code looks at the success rate in 5000 iterations with probabilistically generated 
# evidence sets relative to the competence parameter.
# It is a first step to assess whether constraints similar to the Jury Theorem 
# for the epistemic quality of group decision exist in this setting.

iterations_per_competency = 5000

# Discretely incremented competencies above 0.5 to 1.0 with a 0.05 step width
competencies = np.arange(0.1, 1.05, 0.05)  # 1.05 set because function excludes upper end of defined interval

# Array of different numbers of agents to test
agent_numbers = [5, 9, 25, 100]

# Plotting colors for different lines
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Plotting
plt.figure()

for idx, num_agents in enumerate(agent_numbers):
    # Array with values from 0 to 1.0 showing success rate corresponding to competencies array
    summary_success_rates = [None] * len(competencies)
    ties_per_round = [0] * len(competencies)

    for i in range(len(competencies)):  # For every competency
        ties = 0
        single_round_successes = []

        j = 0
        # Run specified number of times
        while j < iterations_per_competency:
            # Create new deliberation setting with the corresponding competence
            deliberation_setting = DeliberationSetting(no_of_agents=num_agents, p_competence=competencies[i])
            result = deliberation_setting.run_sim_keen()

            single_round_successes.append(result)
            j += 1

        # Calculate relative success
        success_rate = single_round_successes.count('A') / iterations_per_competency

        # Save success rate in the summary
        summary_success_rates[i] = success_rate
        ties_per_round[i] = ties
        print(f'Successes for competency {competencies[i]} with {num_agents} agents:', single_round_successes)
        print(f'{ties} tie rounds excluded for competency {competencies[i]} with {num_agents} agents')

    print(f'Summary of success rates for {num_agents} agents:', summary_success_rates)

    # Plotting
    plt.plot(competencies, summary_success_rates, marker='o', linestyle='-', color=colors[idx % len(colors)], label=f'{num_agents} agents')

plt.xlabel('Competencies from 0.1 to 1.0 in 0.05 increments')
plt.ylabel('Relative success rate in 5000 iterations with randomly generated evidence sets')
plt.title('Is this Jury-Theorem-worthy?')
plt.legend()
plt.show() '''


## Code for no_of_agents_dependent competency
# WATCH OUT: Too many operations for M1 as is
import numpy as np
import matplotlib.pyplot as plt
from class_structure import DeliberationSetting

iterations_per_agent = 5000
competence = 0.6
agent_counts = [3,6]  # Number of agents from 2 to 10

# Array with values showing success rate corresponding to number of agents
success_rates = []

for agents in agent_counts:
    single_round_successes = []
    ties = 0
    
    # Create new deliberation setting with the corresponding number of agents
    deliberation_setting = DeliberationSetting(no_of_agents=agents, p_competence=competence)
    
    j = 0
    # Run specified number of times
    while j < iterations_per_agent:
        result = deliberation_setting.run_sim_keen()
        
        if result is not None:
            single_round_successes.append(result)
            j += 1
        else:
            ties += 1
    
    # Calculate relative success
    success_rate = single_round_successes.count('A') / iterations_per_agent
    success_rates.append(success_rate)

# Generate the new plot with number of agents vs success rate
plt.figure(figsize=(8, 6))

plt.title("Success Rate vs Number of Agents for p = 0.6")
plt.xlabel("Number of Agents")
plt.ylabel("Success Rate")
plt.plot(agent_counts, success_rates, marker='o')

plt.tight_layout()
plt.show()

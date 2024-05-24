from class_structure import DeliberationSetting
import numpy as np
import matplotlib.pyplot as plt

'''This code looks at the success rate in 5000 iterations with probabilistically generated 
evidence sets relative to the competence parameter.

It is a first step to assess whether constraints similar to the Jury Theorem 
for the epistemic quality of group decision exist in this setting.'''

iterations_per_competency = 5000

##Runnning

# Discretely incremented competencies above 0.5 to 1.0 with a 0.05 step width
competencies = np.arange(0.5, 1.05, 0.05) # 1.05 set because function excludes upper end of defined interval

#Array with values from 0 to 1.0 showing succes rate corresponding to competencies array
summary_success_rates = [None] * len(competencies)

single_round_successes = []

for i in range(len(competencies)): # For every competency
    
    # Create new deliberation setting with the corresponding competence
    deliberation_setting = DeliberationSetting(no_of_agents=11, p_competence=competencies[i])

    # Run specified number of times
    for _ in range(iterations_per_competency):
        result = deliberation_setting.run_sim_keen()
        single_round_successes.append(result)

    # Calculate relative success
    success_rate = single_round_successes.count('A') / iterations_per_competency
    
    # Save success rate in the summary
    summary_success_rates[i] = success_rate



## Plotting

plt.plot(competencies, summary_success_rates, marker='o', linestyle='-')

plt.xlabel('Competencies from 0.5 to 1.0 in 0.05 increments')
plt.ylabel('Relative success rate in 5000 iterations with randomly generated evidence sets')
plt.title('Is this Jury-Theorem-worthy?')

plt.show()
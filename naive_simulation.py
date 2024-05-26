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
competencies = np.arange(0.1, 1.05, 0.05) # 1.05 set because function excludes upper end of defined interval

#Array with values from 0 to 1.0 showing succes rate corresponding to competencies array
summary_success_rates = [None] * len(competencies)
ties_per_round = [0]* len(competencies)

for i in range(len(competencies)): # For every competency
    
    ties = 0
    single_round_successes = []


    j = 0
    # Run specified number of times
    while j < iterations_per_competency:
         # Create new deliberation setting with the corresponding competence
        deliberation_setting = DeliberationSetting(no_of_agents=7, p_competence=competencies[i])
        result = deliberation_setting.run_sim_keen()

        # if result != None:
        single_round_successes.append(result)
        j += 1
        '''else:
            ties += 1'''
            
    # Calculate relative success
    success_rate = single_round_successes.count('A') / iterations_per_competency
    
    # Save success rate in the summary
    summary_success_rates[i] = success_rate
    ties_per_round[i] = ties
    print(f'Successes for {i} th competence:', single_round_successes)
    print(f'{ties} tie rounds excluded for the {i}th competence')

print('Summary of success rates:', summary_success_rates)




## Plotting

plt.plot(competencies, summary_success_rates, marker='o', linestyle='-')

plt.xlabel('Competencies from 0.5 to 1.0 in 0.05 increments')
plt.ylabel('Relative success rate in 5000 iterations with randomly generated evidence sets')
plt.title('Is this Jury-Theorem-worthy?')

plt.show()
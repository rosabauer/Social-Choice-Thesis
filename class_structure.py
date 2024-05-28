
## Imports

import random as rd
import matplotlib.pyplot as plt
import numpy as np

## Global variables

# Number of alternatives, denoted a, b, c, ..., n respectively
M_ALTERNATIVES = 2 

# Amount of evidence there is for a as well as b
A_EVIDENCE = 3 
B_EVIDENCE = 2 

# Global constant to adjust probability of gaining pieces of evidence
P_COMPETENCE = 0.6 

## Helper functions

def first_non_zero(arr):
    for element in arr:
        if element != 0:
            return element
    return None  # If all elements are zero, return None

## Defining Classes

class DeliberationSetting:
    def __init__(self, no_of_agents=5, a_evidence=3, b_evidence=2, p_competence=0.6):
        '''if no_of_agents % 2 == 0:
            raise ValueError("Behold, number of agents must be odd!")'''
        
        self.number_of_agents = no_of_agents
        self.A_EVIDENCE = a_evidence
        self.B_EVIDENCE = b_evidence
        self.P_COMPETENCE = p_competence

        self.crowd = Crowd(no_of_agents=self.number_of_agents, p_competence=self.P_COMPETENCE, a_evidence=self.A_EVIDENCE, b_evidence=self.B_EVIDENCE)
    
    def run_sim_keen(self):
        return self.crowd.deliberate_sim()
    

class Agent:

    def __init__(self, p_competence=0.6, a_evidence = 3, b_evidence = 2):
        
        self.P_COMPETENCE = p_competence
        self.A_EVIDENCE = a_evidence
        self.B_EVIDENCE = b_evidence
        
        self.es_A, self.es_B = self.sample_evidence() # Takes predefined evidence sets in, TBD adjust if necessary

        # Bool arrays to indicate whether a piece of evidence was learned from others or not
        self.es_A_acquired = [0] * self.A_EVIDENCE
        self.es_B_acquired = [0] * self.B_EVIDENCE

        self.update_top_keen() # Finds top alternative based on size of respective evidence sets
    
    def sample_evidence(self):
        evidence_for_a = [None] * self.A_EVIDENCE
        evidence_for_b = [None] * self.B_EVIDENCE
    
        # Fill evidence_for_a
        for i in range(len(evidence_for_a)):
            if rd.uniform(0, 1) <= self.P_COMPETENCE:
                evidence_for_a[i] = 1
            else:
                evidence_for_a[i] = 0

        # Fill evidence_for_b
        for i in range(len(evidence_for_b)):
            if rd.uniform(0, 1) <= self.P_COMPETENCE:
                evidence_for_b[i] = 1
            else:
                evidence_for_b[i] = 0

        return evidence_for_a, evidence_for_b 

    # Determines current favorite
    def update_top_keen(self):
        # Count the number of ones in each list
        count_a = self.es_A.count(1)
        count_b = self.es_B.count(1)
        
        # Set self.top based on which list has more ones
        if count_a > count_b:
            self.top = 'A'
        elif count_b > count_a:
            self.top = 'B'
        else:
            # Handle the undecided state when counts are equal
            #raise ValueError("Agent undecided! What to do now?")

            self.top = 'X' # Stands for indifference or equal evidence

    ''' # Learning new pieces of evidence: Increases evidence set for either option A or B
    def learn_for(self, option, evidence_index):
        if option in ['A', 'B']:
            # Construct the attribute name based on the input
            es_name = f'es_{option}'
            es_name_acquired = f'{es_name}_acquired'
            
            # Retrieve the attribute (list) using getattr
            attr_list = getattr(self, es_name)
            acquired_list = getattr(self, es_name_acquired)

            # Ensure the evidence index is within valid range (1-based to 0-based)
            if 1 <= evidence_index <= len(attr_list):
                zero_index = evidence_index - 1
                attr_list[zero_index] = 1  # Set the specific index to 1
                acquired_list[zero_index] = 1 # Sets acquired index for the corresponding element to 1
            else:
                print(f"Error: evidence_index {evidence_index} is out of range.")
            
            # Update preferred option
            self.update_top()
        else:
            # handle invalid input for A 
            print(f"Invalid option: {option}. Please choose 'A' or 'B'.")'''
  
class Crowd: # Some sort of dynamic process tracker / protocol initally, now a collective of agents
    
    def __init__(self, no_of_agents=5, p_competence=0.6, a_evidence=3, b_evidence=2):
        
        self.A_EVIDENCE = a_evidence
        self.B_EVIDENCE = b_evidence
        self.P_COMPETENCE = p_competence
        
        #if no_of_agents % 2 == 1:
        self.agents = [Agent(p_competence=self.P_COMPETENCE, a_evidence=self.A_EVIDENCE, b_evidence=self.B_EVIDENCE) for _ in range(no_of_agents)]
        #else:
           # raise ValueError("Number of agents must be odd.")
        
        self.public_evidence_A = [0] * len(self.agents[0].es_A)
        self.public_evidence_B = [0] * len(self.agents[0].es_B)    
    # In case anything goes wrong and number needs to be readjusted
    
    def set_no_of_agents(self, number):
        self.no_of_agents = number

    def generate_profile(self, agents):
        profile = [None] * len(agents)

        # For each agent, call their top-ranked alternative and save it in a index-corresponding array
        for i in range(len(agents)):
            profile[i] = getattr(agents[i], 'top')

        return profile

    
    def get_winner(self, profile):
        profile = profile

        count_a = 0
        count_b = 0

        # Iterate over the array to count occurrences
        for char in profile:

            if char == 'A':
                count_a += 1

            elif char == 'B':
                count_b += 1
            
            # ! In case of indifference: Do nothing
            elif char == 'X':
                continue
            else:
                raise ValueError("Input array should only contain 'A' and 'B'.")

        # Compare counts to determine which letter is more frequent
        if count_a > count_b:
            return 'A'
        elif count_b > count_a:
            return 'B'
        else:
            print("Tie! Adjust number of agents using set_no_of_agents.")
            return None

    # TBD: might be able to use this method for lazy dissenters as well and only ajust the update_top function of the agents    
    def dissenters_keen(self, profile):
        profile = profile
        winner = self.get_winner(profile) # This may be dangerous to do? Maybe control this variable outside the method.

        # Initialize boolean array to indicate whether agent dissents or not
        dissent = [0] * len(profile)

        i = 0
        while i < len(profile):
            if profile[i] != winner: # This works for keen dissenters, since 'X' is not 'A', so this loop would activate for indifference 
                dissent[i] = 1
            i += 1
        
        return dissent

    # Terminal plotter for evidence distribution
    def plot_agent_evidence(self, agents): 
         # Marker for each agent
         i = 1
         for agent in agents:
            print(i)
            i += 1

            es_A_own = 0
            es_B_own = 0

            # Count private evidence, which is in the evidence set but not in the acquired set 
            for j in range(len(agent.es_A)):
                if agent.es_A[j] == 1 and agent.es_A_acquired[j] == 0:
                    es_A_own += 1

            for k in range(len(agent.es_B)):
                if agent.es_B[k] == 1 and agent.es_B_acquired[k] == 0:
                    es_B_own += 1
            
            # Distinugish between private and acquired evidence
            print("Evidence A: " + "█" * es_A_own + "▒" * agent.es_A_acquired.count(1))
            print("Evidence B: " + "█" * es_B_own + "▒" * agent.es_B_acquired.count(1))
    
    def deliberate_sim(self):

        # Counts how many round of deliberation we have
        round = 0

        # Return reason for return statement
        ret_reason = None

        # Intialize important variables
        profile = self.generate_profile(self.agents)
        print(profile) # ___Printer___
        majority = self.get_winner(profile)
        minority = 'A' if majority == 'B' else 'B'
        revealed_in_round_A = [0] * A_EVIDENCE
        revealed_in_round_B = [0] * B_EVIDENCE

        # Initialize dissenters
        dissenters = self.dissenters_keen(profile)
        print('First dissenters:', dissenters)
        
        print('First majority vote:', majority) # ____Printer____
        print()

        while 1 in dissenters:

            # Start of a new round
            round += 1

            # Revelation marker: If there exists a piece of evidence that was revealed during a round, it is true. Otherwise, deliberation terminates.
            new_evidence_revealed = False
            
            # For all dissenters, add their evidence for the minority alternative into the revealed evidence sets
            minority_evidence = f'es_{minority}'
            print('The minority evidence: ', minority_evidence)
        
            for i, is_dissenter in enumerate(dissenters):
                if is_dissenter == 1:
                    # Get the set of evidence for the minority option from each dissenter
                    agent_evidence = getattr(self.agents[i], minority_evidence)
                    print(f'Agent {i} s agent_evidence for the minority {minority_evidence}: ', agent_evidence) # ___Printer___
                    
                    # Update the revealed_in_round sets to take on the minority_evidence (only one if-clause will be activated)
                    if minority == 'A':
                        for j in range(len(agent_evidence)):
                            if agent_evidence[j] == 1 and revealed_in_round_A[j] != 1:
                                revealed_in_round_A[j] = 1
                                new_evidence_revealed = True # Sets revealed marker to true

                                print(f'Revealing new evidence {j} for minority option {minority} from agent {i}') # ___Printer___
                    if minority == 'B':
                        for k in range(len(agent_evidence)):
                            if agent_evidence[k] == 1 and revealed_in_round_B[k] != 1:
                                revealed_in_round_B[k] = 1
                                new_evidence_revealed = True # Sets revealed marker to true

                                print(f'Revealing new evidence {k} for minority option {minority} from agent {i}') # ___Printer___

            # If no new evidence was revealed, break the loop
            if not new_evidence_revealed:
                ret_reason = 'No more evidence to reveal from dissenters.' 
                break
            
            # Add all the evidence to the public evidence sets for A and B cumulatively
            for i in range(len(revealed_in_round_A)):
                if revealed_in_round_A[i] == 1:
                    self.public_evidence_A[i] = 1
        
            for i in range(len(revealed_in_round_B)):
                if revealed_in_round_B[i] == 1:
                    self.public_evidence_B[i] = 1

            # Update the indivdual evidence sets of agents to take on the revealed evidence
            for agent in self.agents:

                # Update evidence for A with public evidence
                for i in range(len(self.public_evidence_A)):
                    if self.public_evidence_A[i] == 1 and agent.es_A[i] != 1:
                        agent.es_A[i] = 1
                        agent.es_A_acquired[i] = 1 # Mark as acquired information

                # Update evidence for B with public evidence
                for i in range(len(self.public_evidence_B)):
                    if self.public_evidence_B[i] == 1 and agent.es_B[i] != 1:
                        agent.es_B[i] = 1
                        agent.es_B_acquired[i] = 1 # Mark as acquired information

                agent.update_top_keen()  # Update each agents favorite option
            
            # Update profile, majority and minority
            self.profile = self.generate_profile(self.agents)
            print('New profile: ', self.profile) # ___Printer___

            majority = self.get_winner(self.profile)
            print('Newly assigned majority: ', majority) #___Printer___

            minority = 'A' if majority == 'B' else 'B'
            print('Newly assgined minority: ', minority) #___Printer___

            # Update dissenters
            dissenters = self.dissenters_keen(self.profile)
            print("Dissenters: ", dissenters) # ___Printer___

        print('Generating plot for deliberation end result...')
        self.plot_agent_evidence(self.agents)

        print(f'Termination at round {round}: No more dissenters.' if ret_reason == None else f'Termination at round {round}: {ret_reason}')
        return majority
        

# Running the simulations

test_crowd = Crowd()

test_crowd.deliberate_sim()
    
            







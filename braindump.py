
## Imports

import random as rd

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

def sample_evidence():
   evidence_for_a = [None] * A_EVIDENCE
   evidence_for_b = [None] * B_EVIDENCE

   # Random number generators: Rd generated numbers are smaller than constant -> use 1
   i = 0 
   while i < len(evidence_for_a):
    evidence_for_a[i] = 1 if P_COMPETENCE <= rd.uniform(0, 1) else 0
    i += 1

    j = 0
    while j < len(evidence_for_b):
        evidence_for_b[i] = 1 if P_COMPETENCE <= rd.uniform(0, 1) else 0
        j += 1

    return evidence_for_a, evidence_for_b 

class Agent:

    def __init__(self, es_A, es_B):
        self.es_A, self.es_B = sample_evidence() # Takes predefined evidence sets in, TBD adjust if necessary

        # Bool arrays to indicate whether a piece of evidence was learned from others or not
        #self.es_A_acquired = [0] * len(es_A) 
        # self.es_B_acquired = [0] * len(es_B)

        # Bool arrays to indicate whether evidence has been revealed or not
        # self.es_A_revealed = [0] * len(es_A)
        # self.es_B_revealed = [0] * len (es_B)

        self.top = self.update_top # Finds top alternative based on size of respective evidence sets
    
    # Determines current favorite
    def update_top(self):
        # Count the number of ones in each list
        count_a = self.es_A.count(1)
        count_b = self.es_B.count(1)
        # Set self.top based on which list has more ones

        try:
            if count_a > count_b:
                self.top = 'A'
            elif count_b > count_a:
                self.top = 'B'
        except:
            return ValueError("Agent undecided! What to do now?") #TBD: It is not yet defined what happens here by me/Adrian


    # Learning new pieces of evidence: Increases evidence set for either option A or B
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
            print(f"Invalid option: {option}. Please choose 'A' or 'B'.")


    
class Crowd: # Some sort of dynamic process tracker / protocol initally, now a collective of agents
    
    def __init__(self, no_of_agents):
        if no_of_agents % 2 == 1:
            self.agents = [Agent() for _ in range(no_of_agents)] # _ indicates throwaway variable
        else:
            raise ValueError("Number of agents must be odd.")
        self.public_evidence_A = [0] * len(self.agents[0].es_A)
        self.public_evidence_B = [0] * len(self.agents[0].es_B)    
    # In case anything goes wrong and number needs to be readjusted
    
    def set_no_of_agents(self, number):
        self.no_of_agents = number

    def generate_profile(self):
        
        profile = [None] * len(self.agents)

        # For each agent, call their top-ranked alternative and save it in a index-corresponding array
        i = 0
        while i < len(profile):
            profile[i] = self.agents[i].top
            i += 1
    
        return profile
    
    def get_winner(self):
        profile = self.get_profile

        count_a = 0
        count_b = 0

        # Iterate over the array to count occurrences
        for char in profile:
            if char == 'A':
                count_a += 1
            elif char == 'B':
                count_b += 1
            else:
                raise ValueError("Input array should only contain 'A' and 'B'.")

        # Compare counts to determine which letter is more frequent
        if count_a > count_b:
            return 'A'
        elif count_b > count_a:
            return 'B'
        else:
            print("Tie! Adjust number of agents using set_no_of_agents.")
            return "None"
        
    def dissenters_keen(self):
        profile = self.get_profile
        winner = self.get_winner

        # Initialize boolean array to indicate whether agent dissents or not
        dissent = [0] * len(profile)

        i = 0
        while i < len(profile):
            if profile[i] != winner:
                dissent[i] = 1
            i += 1
        
        return dissent       
    
    def deliberate_sim(self):

        # Intialize important variables
        profile = self.get_profile()
        majority = self.get_winner()
        minority = 'A' if majority == 'B' else 'B'
        revealed_in_round_A = [0] * A_EVIDENCE
        revealed_in_round_B = [0] * B_EVIDENCE

        # Initialize dissenters
        dissenters = self.dissenters_keen()
        
        print('Majority vote:', majority) # ____Printer____

        while 1 in dissenters:
            
            # For all dissenters, add their evidence for the minority alternative into the revealed evidence sets
            minority_evidence = f'es_{minority}'
            # 
            dissenters = self.dissenters_keen() # might be redundant
            for i, is_dissenter in enumerate(dissenters):
                if is_dissenter == 1:
                    # Get the set of evidence for the minority option from each dissenter
                    agent_evidence = getattr(self.agents[i], minority_evidence)
                    
                    # Update the revealed_in_round sets to take on the minority_evidence (only one if-clause will be activated)
                    if minority == 'A':
                        for i in range(len(agent_evidence)):
                            if agent_evidence[i] == 1:
                                revealed_in_round_A[i] = 1
                    if minority == 'B':
                        for i in range(len(agent_evidence)):
                            if agent_evidence[i] == 1:
                                revealed_in_round_B[i] = 1
            
            # Add all the evidence to the public evidence set
            self.public_evidence_A = revealed_in_round_A
            self.public_evidence_B = revealed_in_round_B

            # Update the indivdual evidence sets of agents to take on the revealed evidence
            for agent in self.agents:
                # Update evidence for A with public evidence
                for i in range(len(self.public_evidence_A)):
                    if self.public_evidence_A[i] == 1:
                        agent.learn_for('A', i)
                # Update evidence for B with public evidence
                for i in range(len(self.public_evidence_B)):
                    if self.public_evidence_B[i] == 1:
                        agent.learn_for('B', i)   # TBD: Make learn_for function do more for the structure of this protocol, so it works together more elegantly  
            
            # Update each agents favorite option
            for agent in self.agents:
                agent.update_top()
            
            # Update profile, majority and minority
            self.profile = self.generate_profile()
            print('New profile: ', self.profile) # ___Printer___

            majority = self.get_winner()
            print('Newly assigned majority: ', majority) #___Printer___

            minority = 'A' if majority == 'B' else 'B'
            print('Newly assgined minority: ', minority) #___Printer___

            # Update dissenters
            dissenters = self.dissenters_keen()
            print("Dissenters: ", dissenters)






        return None #TBD
        


# Deprecated
class Protocol:

    def __init__(self, no_of_agents):
        self.group = Crowd(no_of_agents)

    def deliberate(self):
        return None
    
    def dissenters(self):
        profile = self.group.getprofile()

    
            







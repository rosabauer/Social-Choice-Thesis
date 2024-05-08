
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

## Defining Classes

def sample_evidence():
   evidence_for_a = [None] * A_EVIDENCE
   evidence_for_b = [None] * B_EVIDENCE

   # Random number generators: Rd generated numbers are smaller than constant -> use 1
   i = 0 
   while i < len(evidence_for_a):
    evidence_for_a[i] = 1 if P_COMPETENCE <= rd.uniform(0, 1) else 0

    j = 0
    while j < len(evidence_for_b):
        evidence_for_b[i] = 1 if P_COMPETENCE <= rd.uniform(0, 1) else 0

    return evidence_for_a, evidence_for_b 

class Agent:

    def __init__(self, es_A, es_B):
        self.es_A, self.es_B = sample_evidence() # Takes predefined evidence sets in, TBD adjust if necessary
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
            return ValueError("Tie! What to do now?") #TBD: It is not yet defined what happens here by me/Adrian


    # Learning new pieces of evidence: Increases evidence set for either option A or B
    def learn_for(self, option, evidence_index):
        if option in ['A', 'B']:
            # Construct the attribute name based on the input
            es_name = f'es_{option}'
            
            # Retrieve the attribute (list) using getattr
            attr_list = getattr(self, es_name)

            # Ensure the evidence index is within valid range (1-based to 0-based)
            if 1 <= evidence_index <= len(attr_list):
                zero_index = evidence_index - 1
                attr_list[zero_index] = 1  # Set the specific index to 1
            else:
                print(f"Error: evidence_index {evidence_index} is out of range.")
            
            # Update preferred option
            self.update_top()
        else:
            # handle invalid input for A 
            print(f"Invalid option: {option}. Please choose 'A' or 'B'.")


    
class Crowd: # Some sort of dynmaic process tracker / protocol initally, now a collective of agents
    def __init__(self, no_of_agents):
        if no_of_agents % 2 == 1:
            self.agents = [Agent() for _ in range(no_of_agents)] # _ indicates throwaway variable
        else:
            raise ValueError("Number of agents must be odd.")
    
    # In case anything goes wrong and number needs to be readjusted
    def set_no_of_agents(self, number):
        self.set_no_of_agents = number


    def get_profile(self):
        
        profile = [None * len(self.agents)]

        # For each agent, call their top-ranked alternative and save it in a index-corresponding array
        i = 0
        while i < len(profile):
            profile[i] = self.agents[i].top
    
        return profile
    
    def get_winner(self):
        profile = self.get_profile

        count_a = 0
        count_b = 0

        # Iterate over the array to count occurrences
        for char in profile:
            if char == 'a':
                count_a += 1
            elif char == 'b':
                count_b += 1
            else:
                raise ValueError("Input array should only contain 'a' and 'b'.")

        # Compare counts to determine which letter is more frequent
        if count_a > count_b:
            return 'A'
        elif count_b > count_a:
            return 'B'
        else:
            print("Tie! Adjust number of agents using set_no_of_agents.")
            return "None"
        

class Protocol:

    def __init__(self):
        self.group = Crowd()

    def deliberate(self):
        return None

    
            







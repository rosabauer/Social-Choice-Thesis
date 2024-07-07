from pgmpy import models, factors, inference
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define the structure of the Bayesian Network
model = BayesianNetwork([
    ('E_A_1', 'top_1'), ('E_B_1', 'top_1'),
    ('E_A_2', 'top_2'), ('E_B_2', 'top_2'),
    # Add similar edges for all agents
    ('top_1', 'profile'), ('top_2', 'profile'), 
    # Add similar edges for all agents
    ('profile', 'winner')
])

# Define CPDs for each node
# Example CPD for evidence node (assuming binary evidence)
cpd_E_A_1 = TabularCPD(variable='E_A_1', variable_card=2, values=[[0.6], [0.4]])
cpd_E_B_1 = TabularCPD(variable='E_B_1', variable_card=2, values=[[0.4], [0.6]])

# Example CPD for preference node (top_1)
# Assume top_1 is determined based on E_A_1 and E_B_1
cpd_top_1 = TabularCPD(variable='top_1', variable_card=3, 
    values=[[0.5, 0.7, 0.1, 0.3],
            [0.3, 0.2, 0.7, 0.2],
            [0.2, 0.1, 0.2, 0.5]],
    evidence=['E_A_1', 'E_B_1'],
    evidence_card=[2, 2]
)

# Add CPDs for all nodes
model.add_cpds(cpd_E_A_1, cpd_E_B_1, cpd_top_1)
# Add CPDs for other agents and the profile, winner nodes similarly

# Validate the model
model.check_model()

# Perform inference
inference = VariableElimination(model)
result = inference.query(variables=['winner'])

print(result)

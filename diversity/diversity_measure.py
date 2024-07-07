from class_structure import *

def diversity(es_1, es_2):

    if len(es_1) != len(es_2):
        return ValueError('Evidence sets not of the same length')
    
    difference = 0

    for i in range(len(es_1)):
        if es_1[i] != es_2[i]:
            difference += 1
    
    es_1_evidence = es_1.count(1)
    es_2_evidence = es_2.count(1)

    result = difference - abs(es_1_evidence-es_2_evidence)**2

    return result


def crowd_diversity(crowd: Crowd):
    diversity_cum = 0
    num_agents = len(crowd.agents)
    
    for i in range(num_agents):
        for j in range(i + 1, num_agents):
            agent1 = crowd.agents[i]
            agent2 = crowd.agents[j]
            diversity_cum += diversity(agent1.es_A, agent2.es_A)
            diversity_cum += diversity(agent1.es_B, agent2.es_B)
    
    return diversity_cum

def diverse_deliberation(mindiversity = 0, maxdiversity = 100000):
    crowdsetting = DeliberationSetting()
    while crowd_diversity(crowdsetting.crowd) < mindiversity or crowd_diversity(crowdsetting.crowd) > maxdiversity:
        crowdsetting = DeliberationSetting()
    
    print('DIVERSITY SCORE OF THIS CROWD: ', crowd_diversity(crowdsetting.crowd))
    crowdsetting.run_sim_keen()

diverse_deliberation(mindiversity = 0, maxdiversity = 3)


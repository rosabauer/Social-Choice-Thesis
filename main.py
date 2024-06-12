from class_structure import DeliberationSetting
import numpy as np
import matplotlib.pyplot as plt



i = 100
results = []

while i != 0:
    setting = DeliberationSetting(a_evidence=9, b_evidence = 7, p_competence=0.3)
    deliberation_result = setting.run_sim_keen()
    results.append(deliberation_result)
    i -= 1

print('--------')
print('FINAL Result: ',results)

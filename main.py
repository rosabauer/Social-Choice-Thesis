from class_structure import DeliberationSetting
import numpy as np
import matplotlib.pyplot as plt

setting = DeliberationSetting()

deliberation_result = setting.run_sim_keen()
print('--------')
print('FINAL Result: ',deliberation_result)
####### This file is aimed at analyzing the low common mode voltage area
####### in the POD-PO PWM Type1 method.
####### and it considers three different variables:
####### X--modulation index;
####### Y--phase angle;
####### Z--zero-sequence voltage.
import numpy as np
import matplotlib.pyplot as plt

data1 = np.linspace(0, 1.01, 100) 
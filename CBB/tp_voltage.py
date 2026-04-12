####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseVoltage:
    def __init__(self, modulation_index, fre=50, start_angle=0):
        ##### set modulation index limitation 0~2/sqrt(3)
        modulation_index = max(0,modulation_index)
        modulation_index = min(2 / np.sqrt(3),modulation_index)
        self.modulation_index = modulation_index
        
        ##### set three-phase voltage parameters
        self.wt = np.linspace(0, 2*np.pi*fre*0.04, 10000)  # 50 Hz fundamental frequency
        self.start_anlge = start_angle # Starting phase angle
        self.Va = self.modulation_index * np.sin(self.wt + self.start_anlge)
        self.Vb = self.modulation_index * np.sin(self.wt - 2 * np.pi / 3 + self.start_anlge)
        self.Vc = self.modulation_index * np.sin(self.wt + 2 * np.pi / 3 + self.start_anlge)

    def Vzslimit_cal(self):
        ##### calculate zero-sequence voltage limitation
        umax = np.maximum(self.Va,np.maximum(self.Vb,self.Vc))
        umin = np.minimum(self.Va,np.minimum(self.Vb,self.Vc))
        
        Vzs_max = np.minimum(1 - umax,-umin)
        Vzs_min = np.maximum(-1 - umin,-umax)
        return Vzs_max,Vzs_min
    
if __name__ == "__main__":
    modulation_index = 0.90  # Example modulation index
    ClassThreePhaseVoltage = ThreePhaseVoltage(modulation_index)
    Vzs_max,Vzs_min = ClassThreePhaseVoltage.Vzslimit_cal()

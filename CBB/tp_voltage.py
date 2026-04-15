####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseVoltage:
    def __init__(self, modulation_index, fre=50, start_angle=0,time = 0.02):
        ##### use data_rest to initialize the three-phase voltage parameters
        self.data_reset(modulation_index, fre, start_angle,time)

    def data_reset(self, modulation_index=0.90, fre = 50,start_angle=0,time = 0.02):
        ##### set modulation index limitation 0~2/sqrt(3)
        modulation_index = max(0,modulation_index)
        modulation_index = min(2 / np.sqrt(3),modulation_index)
        self.modulation_index = modulation_index
        
        ##### set three-phase voltage parameters
        self.wt = np.linspace(0, 2*np.pi*fre*time, 1000)  # 50 Hz fundamental frequency
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
    
    def data_plot(self,*parameters,Picsize=(7, 4.3)):
        ##### plot three-phase voltage waveforms
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False      # fix negative sign display issue
        plt.rcParams['mathtext.fontset'] = 'stix'
        fig, ax = plt.subplots(figsize=Picsize)

        ##### plot the data waveforms
        for paramter in parameters:
            ax.plot(self.wt, paramter,linewidth=2.0)
              
        ##### set grid label font size and weight
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)  
            label.set_fontweight('bold')
        
        ##### set axis labels, limits, and grid    
        ax.set_xlabel(r'$\theta$ (rad)', fontsize=14,fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)', fontsize=14,fontweight='bold')
        ax.set_xlim(0,self.wt[-1])
        ax.grid(linestyle='--', alpha=0.3)
        plt.show()
    
if __name__ == "__main__":
    modulation_index = 0.90  # Example modulation index
    ClassThreePhaseVoltage = ThreePhaseVoltage(modulation_index)
    Vzs_max,Vzs_min = ClassThreePhaseVoltage.Vzslimit_cal()
    ClassThreePhaseVoltage.data_plot(ClassThreePhaseVoltage.Va,ClassThreePhaseVoltage.Vb,ClassThreePhaseVoltage.Vc,Vzs_max,Vzs_min)

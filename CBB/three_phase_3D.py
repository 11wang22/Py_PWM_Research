import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class Threephase3D:
    def __init__(self):
        self.wt = np.arange(0, 2 * np.pi / 3, 2e-3)
        self.Modu = np.arange(0, 2 / np.sqrt(3), 2e-3)
        self.X = np.zeros((len(self.Modu), len(self.wt)))
        self.Y = np.zeros((len(self.Modu), len(self.wt)))

    def DataCreate(self):
        X = self.wt
        Y = self.Modu
        X,Y = np.meshgrid(X,Y)
        self.X = X
        self.Y = Y
        [row,line] = self.X.shape
        self.vzmax = np.zeros((row,line))
        self.vzmin = np.zeros((row,line))
        
    def VzmaxCal(self,wt,Modu):
        ##### limit wt and Modu up and down
        wt = min(wt,2 * np.pi / 3)
        wt = max(wt,0)
        Modu = min(Modu,2 / np.sqrt(3))
        Modu = max(Modu,0)
        
        ##### calculate Vzmax
        division_cave = np.pi / 3
        umax = Modu * np.sin(wt + np.pi / 6)
        if wt < division_cave:
            umin = Modu * np.sin(wt - np.pi / 2)
        else:
            umin = Modu * np.sin(wt + 5 * np.pi / 6)
        
        Vzmax = min(1 - umax,-umin)
        return Vzmax
    
    def VzminCal(self,wt,Modu):
        ##### limit wt and Modu up and down
        wt = min(wt,2 * np.pi / 3)
        wt = max(wt,0)
        Modu = min(Modu,2 / np.sqrt(3))
        Modu = max(Modu,0)
        ##### calculate Vzmin
        division_cave = np.pi / 3
        umax = Modu * np.sin(wt + np.pi / 6)
        if wt < division_cave:
            umin = Modu * np.sin(wt - np.pi / 2)
        else:
            umin = Modu * np.sin(wt + 5 * np.pi / 6)
        Vzmin = max(-1 - umin,-umax)
        return Vzmin
    
    def DataCal(self):
        for i in range(self.vzmax.shape[0]):
            for j in range(self.vzmax.shape[1]):
                self.vzmax[i,j] = self.VzmaxCal(self.wt[j],self.Modu[i])
                self.vzmin[i,j] = self.VzminCal(self.wt[j],self.Modu[i])
                
        print(self.vzmax)
        print(self.vzmin)

    def Dataplot(self):
        plt.rcParams["font.family"] = "Times New Roman"  # 设置全局西文字体为 Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # 解决负号显示为方块的问题
        plt.rcParams['mathtext.fontset'] = 'stix'  # 让数学符号也匹配 Times 风格
        
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)  # cut some white space around the plot
        
        # ===================== axis settings =====================
        ##### set the projection type to orthographic for a more technical look
        ax.set_proj_type('ortho')  
        
        ##### set facecolor to white for a cleaner background
        ax.set_facecolor('white')
        # close the panes to make the plot cleaner
        ax.xaxis.pane.fill = False         
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        # set grid lines to a light gray for better visibility without overpowering the data
        grid_color = "#C0C0C0"
        ax.xaxis._axinfo['grid']['color'] = grid_color
        ax.yaxis._axinfo['grid']['color'] = grid_color
        ax.zaxis._axinfo['grid']['color'] = grid_color
        # set the axis lines to a darker gray for better contrast
        ax.xaxis.line.set_color('#666666')
        ax.yaxis.line.set_color('#666666')
        ax.zaxis.line.set_color('#666666')
        
        ##### set view angle for better visibility of the 3D structure
        ax.view_init(elev=20, azim=-45, roll=0)
        
        # ===================== colorbar settigns =====================
        cmap = cm.coolwarm  # 你可以换成 cm.plasma / cm.inferno / cm.Blues
        combined_data = np.concatenate([self.vzmax.ravel(), self.vzmin.ravel()])
        vmin, vmax = combined_data.min(), combined_data.max()
        
        # ===================== plot two surfaces =====================
        surf2 = ax.plot_surface(
            self.X, self.Y, self.vzmin,
            cmap=cmap, alpha=0.6, vmin=vmin, vmax=vmax,
            linewidth=0.2, edgecolor='k', rstride=20, cstride=20  # add grid lines for better visibility
        )
                
        surf1 = ax.plot_surface(
            self.X, self.Y, self.vzmax,
            cmap=cmap, alpha=0.6, vmin=vmin, vmax=vmax,
            linewidth=0.2, edgecolor='k', rstride=20, cstride=20  # add grid lines for better visibility
        )
        cbar = fig.colorbar(surf1, ax=ax, shrink=0.5, pad=0.1)

        # ===================== label fonts =====================
        ax.set_xlabel('Angle (rad)', fontweight='bold')
        ax.set_ylabel('Modulation Index', fontweight='bold')
        ax.set_zlabel('Zero-sequence Voltage (p.u.)', fontweight='bold')
        ax.set_box_aspect(None, zoom=0.95)

        # ===================== X axis label =====================
        xticks = [0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3]
        xtick_labels = [r'$0$', r'$\pi/6$', r'$\pi/3$', r'$\pi/2$',r'$2\pi/3$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    ClassTest = Threephase3D()
    ClassTest.DataCreate()
    ClassTest.DataCal()
    ClassTest.Dataplot()
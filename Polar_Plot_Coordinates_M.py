import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import glob
import os
plt.style.use('seaborn')
##d48
path = ('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Orientation/Trajectory_Orientation/')
excel_files = glob.glob(os.path.join(path, "*.xlsx"))

rad_frames=[]
for f in excel_files:
    # read the csv file
    excel = pd.read_excel(f)
    full_path = (f.split("\\")[-1])
    name=full_path[113:116]
    d48='d48_'
    folder=full_path[116:118]


# #Look at changing bin sizes
    def rose_plot(ax, angles, bins=16, density=False, offset=0, lab_unit="degrees",
                  start_zero=False, **param_dict):
        """
        Plot polar histogram of angles on ax. ax must have been created using
        subplot_kw=dict(projection='polar'). Angles are expected in radians.
        """
        # Wrap angles to [-pi, pi)
        angles = (angles + np.pi) % (2*np.pi) - np.pi
    
        # Set bins symetrically around zero
        if start_zero:
            # To have a bin edge at zero use an even number of bins
            if bins % 2:
                bins += 1
            bins = np.linspace(-np.pi, np.pi, num=bins+1)
    
        # Bin data and record counts
        count, bin = np.histogram(angles, bins=bins)
    
        # Compute width of each bin
        widths = np.diff(bin)
    
        # By default plot density (frequency potentially misleading)
        if density is None or density is True:
            # Area to assign each bin
            area = count / angles.size
            # Calculate corresponding bin radius
            radius = (area / np.pi)**.5
        else:
            radius = count
    
        # Plot data on ax
        ax.bar(bin[:-1], radius, zorder=1, align='edge', width=widths,
                edgecolor='C0', fill=False, linewidth=1)
    
        # Set the direction of the zero angle
        ax.set_theta_offset(offset)
    
        # Remove ylabels, they are mostly obstructive and not informative
        ax.set_yticks([])
    
        if lab_unit == "radians":
            label = ['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$',
                      r'$\pi$', r'$5\pi/4$', r'$3\pi/2$', r'$7\pi/4$']
            ax.set_xticklabels(label)
            
    excel_angle=int(excel.iloc[0,1])


    rad=(excel_angle* (math.pi/180))
    rad_frames.append(rad)

rad_frames= [rad_frames]
rads= pd.DataFrame(rad_frames).T
angles = rads
 

    # Visualise with polar histogram
fig, ax = plt.subplots(1, subplot_kw=dict(projection='polar'))
rose_plot(ax, angles)
fig.tight_layout()
image_name='Swimming Trajectory d48 (0-3 Sec)'#'Swimming Trajectory (deg) Unsuccessful Saturday (0-3 Sec)'
ax.title.set_text(image_name)
image_format='svg'

plt.savefig('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Polar_Plots/ '+image_name+'.svg', format=image_format, dpi=1260,bbox_inches= 'tight')
plt.show()





    
    








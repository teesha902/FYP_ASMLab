import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook


###############################################
###Import the CSV's file for d48 ###
###############################################
path = ('/Users/saoirselightbourne/Desktop/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48')
csv_files = glob.glob(os.path.join(path, "*12S_INTER_MM.csv" ))

fig, ax = plt.subplots(1, sharex=True, sharey=True)

for f in csv_files:
    # read the csv file
    csv = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    name=full_path[82:84]
    d48='d48_'
    folder=full_path[84:87]
############################
###Want to get 0-3 second###
############################
    three_s_mark_name=d48+name+folder
    three_s_mark_name=int(len(csv)/2)
    new_df='df_'+d48+name+folder
    new_df=pd.DataFrame(csv.iloc[:three_s_mark_name,:])


    #First Line
    first_x=new_df['Head_X.1'].iloc[0]
    first_y=new_df['Head_Y.1'].iloc[0]
    last_x=new_df['Head_X.1'].iloc[-1]
    last_y=new_df['Head_Y.1'].iloc[-1]
    ax.set_xlabel('X Coordinates (mm)', fontsize = 15)
    ax.set_ylabel('Y Coordinates (mm)', fontsize = 15)
    ax.set_xlim(left=0, right=350)
    ax.set_ylim(bottom=-600, top=0)
    ax.set_title('d48 Start & End Coordinates (0-3s)', fontsize = 25)
    ax.set_aspect('equal')
    ax.scatter(first_x,first_y,marker=".",color='green',s=150)
    ax.scatter(last_x,last_y,marker="D",color='red',s=50)
    #fig.set_figwidth(100)
    #fig.set_figheight(20)


image_format = 'png'
image_name = 'd48_Trajectory.png'
# #plt.show()
plt.savefig('/Users/saoirselightbourne/Desktop/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Dot_Plots/ '+image_name+'.svg', format=image_format)
plt.show()
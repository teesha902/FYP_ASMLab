
import math
from math import pi
import numpy as np
import pandas as pd
import glob
import os

#This calculates the swimming trajectory of the fish from one head coordinate to the next
path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48')
csv_files = glob.glob(os.path.join(path, "*.csv"))
data = []

for f in csv_files:
    csv = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    d48='d48_'
    name=full_path[51:54]
    folder=full_path[54:56]


    led_csv12=pd.read_csv('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48/d48_'+name+folder+'_12S_INTER_MM.csv')
    
    #Subset frame when LED turns on
    three_sec_mark=int(len(led_csv12)/2)
    #The original code was getting angle of the fish's body from tail to head @3 seconds
    #What he want is the angle between the fish's first and last head coordinate
    #At 0s- starting
    head_x_0s=led_csv12['Head_X.1'].loc[0]
    head_y_0s=led_csv12['Head_Y.1'].loc[0]
    #At 3s - end
    head_x_3s=led_csv12['Head_X.1'].loc[three_sec_mark]
    head_y_3s=led_csv12['Head_Y.1'].loc[three_sec_mark]
    
    
    head_0s= (head_x_0s,head_y_0s)
    head_3s=(head_x_3s,head_y_3s)
    #Calculate angle
    #centre at 0,0 by subtracting head_0s values from head_3s values
    centred_head_x=head_x_3s-head_x_0s
    centred_head_y=head_y_3s-head_y_0s
    
    centred_head_3s=(centred_head_x,centred_head_y)
    centred_head_0s=(0,0)
    
    def angle_between(p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return 360-np.rad2deg((ang1 - ang2) % (2 * np.pi))
    
    angle=angle_between(centred_head_0s,centred_head_3s)#angle_between(tail_0s,head_0s)
    data.append([name+folder, angle])
print (data)
#Write to excel 
results_df = pd.DataFrame(data, columns=["Fish Name", 'Trajectory Angle (deg)'])
print(results_df)
# file_data={'Fish Name':[name+folder],'Trajectory Angle (deg)':[angle]}

# file_data_df=pd.DataFrame.from_dict(file_data, orient='index').T

# writer = pd.ExcelWriter('/Users/asmlabuser1/Scripts_Ari/testing/d48_testing.xlsx')#('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Orientation/3sec/Trajectory_Orientation_3Sec_'+name+folder+'.xlsx')
# results_df.to_excel(writer,index=False,header=True,sheet_name=folder)
# writer.save()
# print("Ran:"+name +folder)
    
# /Users/asmlabuser1/Scripts_Ari/testing

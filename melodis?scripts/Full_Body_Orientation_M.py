import math
from math import pi
import numpy as np
import pandas as pd
import statistics
import glob
import os
from tqdm import tqdm

path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48')
csv_files = glob.glob(os.path.join(path, "*.csv"))[:10]
data = []

for f in (pbar:= tqdm(csv_files)):
    csv = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    d48='d48_'
    name=full_path[51:54]
    folder=full_path[54:56]
    pbar.set_postfix_str(name+folder)

    #Shows averahe way the fish was facing
    led_csv12=pd.read_csv('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48/d48_'+name+folder+'_12S_INTER_MM.csv')
    
    #Subset frame when LED turns on
    three_sec_mark=int(len(led_csv12)/2)
    
    head_x=led_csv12['Head_X.1'].loc[0:three_sec_mark]
    head_y=led_csv12['Head_Y.1'].loc[0:three_sec_mark]
    tail_x=led_csv12['Tail_X.1'].loc[0:three_sec_mark]
    tail_y=led_csv12['Tail_Y.1'].loc[0:three_sec_mark]
    
    head_0s= (head_x,head_y)
    tail_0s= (tail_x,tail_y)
    
    #Calculate angle
    #centre at 0,0 by subtracting tail values from head values
    centred_head_x_0s=head_x-tail_x
    centred_head_y_0s=head_y-tail_y
    
    centred_head_0s=(centred_head_x_0s,centred_head_y_0s)
    centred_tail_0s=(0,0)
    
    def angle_between(p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return 360-np.rad2deg((ang1 - ang2) % (2 * np.pi))
    
    angle=angle_between(centred_tail_0s,centred_head_0s)#angle_between(tail_0s,head_0s)
    med_angle= statistics.median(angle)
    data.append([name+folder, med_angle])
# print(data)
#Write to excel
results_df = pd.DataFrame(data, columns=["Fish Name", 'Median Body Angle (deg)'])

    # file_data={'Fish Name':[name+folder],'Median Body Angle (deg)':[med_angle]}
    
    # file_data_df=pd.DataFrame.from_dict(file_data, orient='index').T
    
# writer = pd.ExcelWriter('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Orientation/Body_Orientation/'+d48+name+folder+'.xlsx')
writer = pd.ExcelWriter('/Users/asmlabuser1/Scripts_Ari/testing/d48_medangle_testing.xlsx')#('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Orientation/3sec/Trajectory_Orientation_3Sec_'+name+folder+'.xlsx')

results_df.to_excel(writer,index=False,header=True,sheet_name=folder)
writer.save()
print("Ran:"+name +folder)
    

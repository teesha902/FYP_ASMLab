import math
from math import pi
import numpy as np
import pandas as pd
import os
import glob

path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48')
csv_files = glob.glob(os.path.join(path, "*.csv"))

for f in csv_files:
    csv = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    d48='d48_'
    name=full_path[51:54]
    folder=full_path[54:56]

    led_csv3=pd.read_csv('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48/d48_'+name+folder+'_3S_INTER_MM.csv')
    
    
    #Angle function
    def angle_between(p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return 360-np.rad2deg((ang1 - ang2) % (2 * np.pi))
    
    
    #Get coordinates
    first_head_x_0s=led_csv3['first_3_head_X'].loc[0]
    first_head_y_0s=led_csv3['first_3_head_Y'].loc[0]
    first_tail_x_0s=led_csv3['first_3_tail_X'].loc[0]
    first_tail_y_0s=led_csv3['first_3_tail_Y'].loc[0]
    first_head_0s= (first_head_x_0s,first_head_y_0s)
    first_tail_0s= (first_tail_x_0s,first_tail_y_0s)
    first_centred_head_x_0s=first_head_x_0s-first_tail_x_0s
    first_centred_head_y_0s=first_head_y_0s-first_tail_y_0s
    first_centred_head_0s=(first_centred_head_x_0s,first_centred_head_y_0s)
    first_centred_tail_0s=(0,0)
    first_angle=angle_between(first_centred_tail_0s,first_centred_head_0s)#angle_between(tail_0s,head_0s)
    
    
    second_head_x_0s=led_csv3['second__3_head_X'].loc[0]
    second_head_y_0s=led_csv3['second__3_head_Y'].loc[0]
    second_tail_x_0s=led_csv3['second_tail_3_X'].loc[0]
    second_tail_y_0s=led_csv3['second_tail_3_Y'].loc[0]
    second_head_0s= (second_head_x_0s,second_head_y_0s)
    second_tail_0s= (second_tail_x_0s,second_tail_y_0s)
    second_centred_head_x_0s=second_head_x_0s-second_tail_x_0s
    second_centred_head_y_0s=second_head_y_0s-second_tail_y_0s
    second_centred_head_0s=(second_centred_head_x_0s,second_centred_head_y_0s)
    second_centred_tail_0s=(0,0)
    second_angle=angle_between(second_centred_tail_0s,second_centred_head_0s)#angle_between(tail_0s,head_0s)
    
    
    
    third_head_x_0s=led_csv3['third_3_head_X'].loc[0]
    third_head_y_0s=led_csv3['third_3_head_Y'].loc[0]
    third_tail_x_0s=led_csv3['third_tail_3_X'].loc[0]
    third_tail_y_0s=led_csv3['third_tail_3_Y'].loc[0]
    third_head_0s= (third_head_x_0s,third_head_y_0s)
    third_tail_0s= (third_tail_x_0s,third_tail_y_0s)
    third_centred_head_x_0s=third_head_x_0s-third_tail_x_0s
    third_centred_head_y_0s=third_head_y_0s-third_tail_y_0s
    third_centred_head_0s=(third_centred_head_x_0s,third_centred_head_y_0s)
    third_centred_tail_0s=(0,0)
    third_angle=angle_between(third_centred_tail_0s,third_centred_head_0s)#angle_between(tail_0s,head_0s)
    
    
    fourth_head_x_0s=led_csv3['fourth_3_head_X'].loc[0]
    fourth_head_y_0s=led_csv3['fourth_3_head_Y'].loc[0]
    fourth_tail_x_0s=led_csv3['fourth_tail_3_X'].loc[0]
    fourth_tail_y_0s=led_csv3['fourth_tail_3_Y'].loc[0]
    fourth_head_0s= (fourth_head_x_0s,fourth_head_y_0s)
    fourth_tail_0s= (fourth_tail_x_0s,fourth_tail_y_0s)
    fourth_centred_head_x_0s=fourth_head_x_0s-fourth_tail_x_0s
    fourth_centred_head_y_0s=fourth_head_y_0s-fourth_tail_y_0s
    fourth_centred_head_0s=(fourth_centred_head_x_0s,fourth_centred_head_y_0s)
    fourth_centred_tail_0s=(0,0)
    fourth_angle=angle_between(fourth_centred_tail_0s,fourth_centred_head_0s)#angle_between(tail_0s,head_0s)
    
    fifth_head_x_0s=led_csv3['fifth_3_head_X'].loc[0]
    fifth_head_y_0s=led_csv3['fifth_3_head_Y'].loc[0]
    fifth_tail_x_0s=led_csv3['fifth_tail_3_X'].loc[0]
    fifth_tail_y_0s=led_csv3['fifth_tail_3_Y'].loc[0]
    fifth_head_0s= (fifth_head_x_0s,fifth_head_y_0s)
    fifth_tail_0s= (fifth_tail_x_0s,fifth_tail_y_0s)
    fifth_centred_head_x_0s=fifth_head_x_0s-fifth_tail_x_0s
    fifth_centred_head_y_0s=fifth_head_y_0s-fifth_tail_y_0s
    fifth_centred_head_0s=(fifth_centred_head_x_0s,fifth_centred_head_y_0s)
    fifth_centred_tail_0s=(0,0)
    fifth_angle=angle_between(fifth_centred_tail_0s,fifth_centred_head_0s)#angle_between(tail_0s,head_0s)
    
    
    sixth_head_x_0s=led_csv3['sixth_3_head_X'].loc[0]
    sixth_head_y_0s=led_csv3['sixth_3_head_Y'].loc[0]
    sixth_tail_x_0s=led_csv3['sixth_tail_3_X'].loc[0]
    sixth_tail_y_0s=led_csv3['sixth_tail_3_Y'].loc[0]
    sixth_head_0s= (sixth_head_x_0s,sixth_head_y_0s)
    sixth_tail_0s= (sixth_tail_x_0s,sixth_tail_y_0s)
    sixth_centred_head_x_0s=sixth_head_x_0s-sixth_tail_x_0s
    sixth_centred_head_y_0s=sixth_head_y_0s-sixth_tail_y_0s
    sixth_centred_head_0s=(sixth_centred_head_x_0s,sixth_centred_head_y_0s)
    sixth_centred_tail_0s=(0,0)
    sixth_angle=angle_between(sixth_centred_tail_0s,sixth_centred_head_0s)#angle_between(tail_0s,head_0s)
    
    #Average Angle
    av_angle= (first_angle+second_angle+third_angle+fourth_angle+fifth_angle+sixth_angle)/6
    
    # #Write to excel
    
    # file_data={'Fish Name':[name+folder],' First Trajectory Angle (deg)':[first_angle],' Second Trajectory Angle (deg)':[second_angle],
    #            ' Third Trajectory Angle (deg)':[third_angle],' Fourth Trajectory Angle (deg)':[fourth_angle],
    #            ' Fifth Trajectory Angle (deg)':[fifth_angle],' Sixth Trajectory Angle (deg)':[sixth_angle],
    #            ' Average Trajectory Angle (deg)':[av_angle]}
    
    # file_data_df=pd.DataFrame.from_dict(file_data, orient='index').T
    
    # writer = pd.ExcelWriter('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Orientation/Body_Orientation_Random_3s/d48_'+name+folder+'.xlsx')
    # file_data_df.to_excel(writer,index=False,header=True,sheet_name=folder)
    # writer.save()
    # print("Ran:"+name +folder)
    

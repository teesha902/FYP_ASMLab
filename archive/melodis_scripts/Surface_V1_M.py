#Read in csv
import pandas as pd
import openpyxl
from openpyxl import load_workbook
import os
import glob
import numpy as np
from tqdm import tqdm
path = "C:\\Users\\ASMLabUser1\\Desktop\\killifish\\videos\\analyzed\\38-M1\\og_results\\week_12\\with_led\\uroa\\1\\"
out_path = "C:\\Users\\ASMLabUser1\\killifish\\data\\output\\week_12\\uroa\\1\\"
out_out_path = "C:\\Users\\ASMLabUser1\\killifish\\data\\output\\week_12\\uroa\\1\\surface\\"
csv_files = glob.glob(os.path.join(path, "*.csv"))
data = []

for f in tqdm(csv_files):
    csv = pd.read_csv(f)
    full_path = f.split("\\")
    prefix = "week_12_"
    name=full_path[-1].split(".")[0]
    folder = str(full_path[-3]) + "_" + str(full_path[-2]) + "_"
    # d48=
    # name=full_path[51:54]
    # folder=full_path[54:56]
    file_location_raw= (f)
    csv_RAW = pd.read_csv(file_location_raw)
    exp_time =int(csv_RAW.iloc[0,22])
    exp_time_string= str(exp_time)+'s'

    raw_csv=pd.read_csv(out_path+prefix+folder+name+'_Raw_INTER_MM.csv')
    led_csv=pd.read_csv(out_path+prefix+folder+name+'_12S_INTER_MM.csv')
    
    
    three_sec_mark=int(len(led_csv)/2)
    
    #find frame number
    a=led_csv['Frames_Aft'].loc[three_sec_mark]
    frame_no_led=led_csv['Frames_Aft'].loc[three_sec_mark-7]
    raw_three_sec= raw_csv['Head_Y'].loc[frame_no_led:]

    
    
    #Find highest Y value
    objective_max= 340
    top_tank_whole = raw_csv["Head_Y"].max()
    top_tank_03=led_csv['Head_Y.1'].loc[0:(three_sec_mark-1)].max()
    top_tank_36=led_csv['Head_Y.1'].loc[(three_sec_mark-1):len(led_csv)].max()
    
    #Distance from surface
    
    #LED turns on
    dist_surface_0s_ob= objective_max-(led_csv['Head_Y.1'].loc[1])
    dist_surface_0s_whole= top_tank_whole-(led_csv['Head_Y.1'].loc[1])
    dist_surface_0s_03= top_tank_03-(led_csv['Head_Y.1'].loc[1])
    dist_surface_0s_36= top_tank_36-(led_csv['Head_Y.1'].loc[1])
    #LED turns off (food dispersed)
    dist_surface_3S_ob= objective_max-(led_csv['Head_Y.1'].loc[three_sec_mark-1])
    dist_surface_3S_whole= top_tank_whole-(led_csv['Head_Y.1'].loc[three_sec_mark-1])
    dist_surface_3S_03= top_tank_03-(led_csv['Head_Y.1'].loc[three_sec_mark-1])
    dist_surface_3S_36= top_tank_36-(led_csv['Head_Y.1'].loc[three_sec_mark-1])
    #6 Second mark (6 s after LED turns on)
    six_sec_mark=int(len(led_csv))
    dist_surface_6S_ob= objective_max-(led_csv['Head_Y.1'].loc[six_sec_mark-1])
    dist_surface_6S_whole= top_tank_whole-(led_csv['Head_Y.1'].loc[six_sec_mark-1])
    dist_surface_6S_03= top_tank_03-(led_csv['Head_Y.1'].loc[six_sec_mark-1])
    dist_surface_6S_36= top_tank_36-(led_csv['Head_Y.1'].loc[six_sec_mark-1])
    #Largest displacement
    max_dis_ob=objective_max -(raw_csv["Head_Y"].min())
    max_dis_whole=top_tank_whole -(raw_csv["Head_Y"].min())
    max_dis_03=top_tank_03 -(led_csv['Head_Y.1'].loc[0:(three_sec_mark-1)].min())
    max_dis_36=top_tank_36 -(led_csv['Head_Y.1'].loc[0:(three_sec_mark-1)].min())
    
    
    #Time where fish reaches highest point ahcived in 3-6 seconds
    
    raw_three_sec= pd.DataFrame(raw_three_sec)
    raw_three_sec.columns= ['Head_Y.1']
    
    s = pd.Series(raw_three_sec['Head_Y.1'].loc[0:len(raw_csv)])
    s_df=pd.DataFrame(s.between((objective_max-10),(objective_max+10)))
    frame_true=(s_df.index[s_df['Head_Y.1']].tolist())
    if len(frame_true) == 0:
        frame_true = [0,0,0]
    else:
        frame_true = frame_true
    
    first_frame_true= frame_true[0]
    
    
    
    # # convert to second
    frame_per_sec = len(raw_csv)/ int(exp_time)#Total frames/seconds
    frame_per_sec_r= round(frame_per_sec) #round frame per second to nearest whole number
    first_reach_food_sec=round(first_frame_true/frame_per_sec_r)
    
    if first_reach_food_sec == 0:
        first_reach_food_sec = exp_time
    else:
        first_reach_food_sec = first_reach_food_sec
    
    
    # # #Write to Excel
    data.append({'Fish Name':name+folder,'Video Length':exp_time,'Max Y (Objective)':objective_max,'Max Y (Entire Video)':top_tank_whole,'Max Y (0-3S)':top_tank_03,'Max Y (3-6S)':top_tank_36,
               "Displacement_LED_On_Objective_mm":dist_surface_0s_ob,"Displacement_LED_On_Whole_mm":dist_surface_0s_whole,"Displacement_LED_On_03_mm":dist_surface_3S_03,"Displacement_LED_On_36_mm":dist_surface_3S_36,
               "Displacement_LED_Off_Objective_mm":dist_surface_3S_ob,"Displacement_LED_Off_Whole_mm":dist_surface_3S_whole,"Displacement_LED_Off_03_mm":dist_surface_3S_03 ,"Displacement_LED_Off_36_mm":dist_surface_3S_36,
               "Displacement_6S_Objective_mm":dist_surface_6S_ob,"Displacement_6S_Whole_mm":dist_surface_6S_whole,"Displacement_LED_6S_03_mm":dist_surface_6S_03,"Displacement_LED_6S_36_mm":dist_surface_6S_36,
               "Maximum Displacement_Objective_mm":max_dis_ob,"Maximum Displacement_Whole_mm":max_dis_whole,"Maximum Displacement_03_mm":max_dis_03,"Maximum Displacement_36_mm":max_dis_36,"Time_Reach_Top_After_Food":first_reach_food_sec})
    
    # QUESTION: is Displacement_LED_On_03_mm and Displacement_LED_Off_03_mm supposed to be same??????

    # file_data_df=pd.DataFrame.from_dict(file_data, orient='index').T
    
results_df=pd.DataFrame(data)

writer = pd.ExcelWriter(out_out_path + folder + ".xlsx")#('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Orientation/3sec/Trajectory_Orientation_3Sec_'+name+folder+'.xlsx')
results_df.to_excel(writer,index=False,header=True,sheet_name=folder)
writer.save()
    
    # #Data frame with values
    
    # frames= (name+folder,exp_time,objective_max,top_tank_whole,top_tank_03,top_tank_36,
    #          dist_surface_0s_ob,dist_surface_0s_whole,dist_surface_3S_03,dist_surface_3S_36,
    #          dist_surface_3S_ob,dist_surface_3S_whole,dist_surface_3S_03,dist_surface_3S_36,
    #          dist_surface_6S_ob,dist_surface_6S_whole,dist_surface_6S_03,dist_surface_6S_36,
    #          max_dis_ob,max_dis_whole,max_dis_03,max_dis_36,first_reach_food_sec)
    
    # book = openpyxl.load_workbook('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Surface/'+d48+name+folder+'.xlsx')
    # sheet = book.active
    # rows = frames
    # sheet.append(rows)
    # book.save('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Surface/'+d48+name+folder+'.xlsx')
    # print("Ran:"+name +folder)

import os
import glob
import pandas as pd
import numpy as np
import random

path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48')
csv_files_raw = glob.glob(os.path.join(path, "*.csv"))

for f in csv_files_raw:
    # read the csv file
    csv_raw = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    raw_name=full_path[51:55]
    raw_folder=full_path[55:56]
    d48='d48_'
    

    last_row= csv_raw.iloc[:,1].index.get_loc(csv_raw.iloc[:, 1].last_valid_index())
    csv_raw= csv_raw.iloc[:(last_row+1),:]

    # Convert to float
    csv_float_raw = csv_raw.iloc[3:,[1,2,4,5,7,8,10,11,13,14]].astype('float')
    # Interpolate to fix missing data
    df_float_interpolate_raw= csv_float_raw.interpolate()
    df_float_interpolate_raw.columns= ['Tail_X','Tail_Y','Body1_X','Body1_Y','Body2_X','Body2_Y',
                                       "Body3_X","Body3_Y","Head_X","Head_Y"]

    #Convert to mm
    df_float_interpolate_raw["Tail_X"]=df_float_interpolate_raw ["Tail_X"]*0.28
    df_float_interpolate_raw["Body1_X"]=df_float_interpolate_raw ["Body1_X"]*0.28
    df_float_interpolate_raw["Body2_X"]=df_float_interpolate_raw ["Body2_X"]*0.28
    df_float_interpolate_raw["Body3_X"]=df_float_interpolate_raw ["Body3_X"]*0.28
    df_float_interpolate_raw["Head_X"]=df_float_interpolate_raw ["Head_X"]*0.28

    df_float_interpolate_raw["Tail_Y"]=df_float_interpolate_raw ["Tail_Y"]* -0.304
    df_float_interpolate_raw["Body1_Y"]=df_float_interpolate_raw ["Body1_Y"]* -0.304
    df_float_interpolate_raw["Body2_Y"]=df_float_interpolate_raw ["Body2_Y"]* -0.304
    df_float_interpolate_raw["Body3_Y"]=df_float_interpolate_raw ["Body3_Y"]* -0.304
    df_float_interpolate_raw["Head_Y"]=df_float_interpolate_raw ["Head_Y"]* -0.304

   # Write to excel
    df_float_interpolate_raw.to_csv('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48/'+d48+raw_name+raw_folder+'_Raw_INTER_MM.csv')

path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48')
csv_files_3 = glob.glob(os.path.join(path, "*_3S.csv"))

for f in csv_files_3:
        # read the csv file
    csv_3 = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    
    three_name = full_path[67:70]
    three_folder = full_path[70:72]


    last_row= csv_3.iloc[:,1].index.get_loc(csv_3.iloc[:, 1].last_valid_index())
    csv_3= csv_3.iloc[:(last_row+1),:]

    # Convert to float
    csv_float_3 = csv_3.astype('float')
    # Interpolate to fix missing data
    df_float_interpolate_3= csv_float_3.interpolate()
    df_float_interpolate_3=df_float_interpolate_3.iloc[:,1:]


    #3 SEC
    #1st
    df_float_interpolate_3 ["first_3_tail_X"]=df_float_interpolate_3 ["first_3_tail_X"]*0.28
    df_float_interpolate_3 ["first_3_body1_X"]=df_float_interpolate_3 ["first_3_body1_X"]*0.28
    df_float_interpolate_3 ["first_3_body2_X"]=df_float_interpolate_3 ["first_3_body2_X"]*0.28
    df_float_interpolate_3 ["first_3_body3_X"]=df_float_interpolate_3 ["first_3_body3_X"]*0.28
    df_float_interpolate_3 ["first_3_head_X"]=df_float_interpolate_3 ["first_3_head_X"]*0.28

    df_float_interpolate_3 ["first_3_tail_Y"]=df_float_interpolate_3 ["first_3_tail_Y"]* -0.304
    df_float_interpolate_3 ["first_3_body1_Y"]=df_float_interpolate_3 ["first_3_body1_Y"]* -0.304
    df_float_interpolate_3 ["first_3_body2_Y"]=df_float_interpolate_3 ["first_3_body2_Y"]* -0.304
    df_float_interpolate_3 ["first_3_body3_Y"]=df_float_interpolate_3 ["first_3_body3_Y"]* -0.304
    df_float_interpolate_3 ["first_3_head_Y"]=df_float_interpolate_3 ["first_3_head_Y"]* -0.304

    #2nd
    df_float_interpolate_3 ["second_tail_3_X"]=df_float_interpolate_3 ["second_tail_3_X"]*0.28
    df_float_interpolate_3 ["second_3_body1_X"]=df_float_interpolate_3 ["second_3_body1_X"]*0.28
    df_float_interpolate_3 ["second__3_body2_X"]=df_float_interpolate_3 ["second__3_body2_X"]*0.28
    df_float_interpolate_3 ["second__3_body3_X"]=df_float_interpolate_3 ["second__3_body3_X"]*0.28
    df_float_interpolate_3 ["second__3_head_X"]=df_float_interpolate_3 ["second__3_head_X"]*0.28

    df_float_interpolate_3 ["second_tail_3_Y"]=df_float_interpolate_3 ["second_tail_3_Y"]* -0.304
    df_float_interpolate_3 ["second__3_body1_Y"]=df_float_interpolate_3 ["second__3_body1_Y"]* -0.304
    df_float_interpolate_3 ["second__3_body2_Y"]=df_float_interpolate_3 ["second__3_body2_Y"]* -0.304
    df_float_interpolate_3 ["second__3_body3_Y"]=df_float_interpolate_3 ["second__3_body3_Y"]* -0.304
    df_float_interpolate_3 ["second__3_head_Y"]=df_float_interpolate_3 ["second__3_head_Y"]* -0.304

    #3rd
    df_float_interpolate_3 ["third_tail_3_X"]=df_float_interpolate_3 ["third_tail_3_X"]*0.28
    df_float_interpolate_3 ["third_3_body1_X"]=df_float_interpolate_3 ["third_3_body1_X"]*0.28
    df_float_interpolate_3 ["third_3_body2_X"]=df_float_interpolate_3 ["third_3_body2_X"]*0.28
    df_float_interpolate_3 ["third_3_body3_X"]=df_float_interpolate_3 ["third_3_body3_X"]*0.28
    df_float_interpolate_3 ["third_3_head_X"]=df_float_interpolate_3 ["third_3_head_X"]*0.28

    df_float_interpolate_3 ["third_tail_3_Y"]=df_float_interpolate_3 ["third_tail_3_Y"]* -0.304
    df_float_interpolate_3 ["third_3_body1_Y"]=df_float_interpolate_3 ["third_3_body1_Y"]* -0.304
    df_float_interpolate_3 ["third_3_body2_Y"]=df_float_interpolate_3 ["third_3_body2_Y"]* -0.304
    df_float_interpolate_3 ["third_3_body3_Y"]=df_float_interpolate_3 ["third_3_body3_Y"]* -0.304
    df_float_interpolate_3 ["third_3_head_Y"]=df_float_interpolate_3 ["third_3_head_Y"]* -0.304

    #4th
    df_float_interpolate_3 ["fourth_tail_3_X"]=df_float_interpolate_3 ["fourth_tail_3_X"]*0.28
    df_float_interpolate_3 ["fourth_3_body1_X"]=df_float_interpolate_3 ["fourth_3_body1_X"]*0.28
    df_float_interpolate_3 ["fourth_3_body2_X"]=df_float_interpolate_3 ["fourth_3_body2_X"]*0.28
    df_float_interpolate_3 ["fourth_3_body3_X"]=df_float_interpolate_3 ["fourth_3_body3_X"]*0.28
    df_float_interpolate_3 ["fourth_3_head_X"]=df_float_interpolate_3 ["fourth_3_head_X"]*0.28

    df_float_interpolate_3 ["fourth_tail_3_Y"]=df_float_interpolate_3 ["fourth_tail_3_Y"]* -0.304
    df_float_interpolate_3 ["fourth_3_body1_Y"]=df_float_interpolate_3 ["fourth_3_body1_Y"]* -0.304
    df_float_interpolate_3 ["fourth_3_body2_Y"]=df_float_interpolate_3 ["fourth_3_body2_Y"]* -0.304
    df_float_interpolate_3 ["fourth_3_body3_Y"]=df_float_interpolate_3 ["fourth_3_body3_Y"]* -0.304
    df_float_interpolate_3 ["fourth_3_head_Y"]=df_float_interpolate_3 ["fourth_3_head_Y"]* -0.304

    #5th
    df_float_interpolate_3 ["fifth_tail_3_X"]=df_float_interpolate_3 ["fifth_tail_3_X"]*0.28
    df_float_interpolate_3 ["fifth_3_body1_X"]=df_float_interpolate_3 ["fifth_3_body1_X"]*0.28
    df_float_interpolate_3 ["fifth_3_body2_X"]=df_float_interpolate_3 ["fifth_3_body2_X"]*0.28
    df_float_interpolate_3 ["fifth_3_body3_X"]=df_float_interpolate_3 ["fifth_3_body3_X"]*0.28
    df_float_interpolate_3 ["fifth_3_head_X"]=df_float_interpolate_3 ["fifth_3_head_X"]*0.28

    df_float_interpolate_3 ["fifth_tail_3_Y"]=df_float_interpolate_3 ["fifth_tail_3_Y"]* -0.304
    df_float_interpolate_3 ["fifth_3_body1_Y"]=df_float_interpolate_3 ["fifth_3_body1_Y"]* -0.304
    df_float_interpolate_3 ["fifth_3_body2_Y"]=df_float_interpolate_3 ["fifth_3_body2_Y"]* -0.304
    df_float_interpolate_3 ["fifth_3_body3_Y"]=df_float_interpolate_3 ["fifth_3_body3_Y"]* -0.304
    df_float_interpolate_3 ["fifth_3_head_Y"]=df_float_interpolate_3 ["fifth_3_head_Y"]* -0.304

    #6th
    df_float_interpolate_3 ["sixth_tail_3_X"]=df_float_interpolate_3 ["sixth_tail_3_X"]*0.28
    df_float_interpolate_3 ["sixth_3_body1_X"]=df_float_interpolate_3 ["sixth_3_body1_X"]*0.28
    df_float_interpolate_3 ["sixth_3_body2_X"]=df_float_interpolate_3 ["sixth_3_body2_X"]*0.28
    df_float_interpolate_3 ["sixth_3_body3_X"]=df_float_interpolate_3 ["sixth_3_body3_X"]*0.28
    df_float_interpolate_3 ["sixth_3_head_X"]=df_float_interpolate_3 ["sixth_3_head_X"]*0.28

    df_float_interpolate_3 ["sixth_tail_3_Y"]=df_float_interpolate_3 ["sixth_tail_3_Y"]* -0.304
    df_float_interpolate_3 ["sixth_3_body1_Y"]=df_float_interpolate_3 ["sixth_3_body1_Y"]* -0.304
    df_float_interpolate_3 ["sixth_3_body2_Y"]=df_float_interpolate_3 ["sixth_3_body2_Y"]* -0.304
    df_float_interpolate_3 ["sixth_3_body3_Y"]=df_float_interpolate_3 ["sixth_3_body3_Y"]* -0.304
    df_float_interpolate_3 ["sixth_3_head_Y"]=df_float_interpolate_3 ["sixth_3_head_Y"]* -0.304

    #3 sec
    df_float_interpolate_3.to_csv('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48/'+d48+three_name+three_folder+'_3S_INTER_MM.csv')

path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48')
csv_files_12 = glob.glob(os.path.join(path, "*_12S.csv"))

for f in csv_files_12:
    csv_12 = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    twelve_name = full_path[67:70]
    twelve_folder = full_path[70:72]
    last_row_12= csv_12.iloc[:,1].index.get_loc(csv_12.iloc[:, 1].last_valid_index())
    csv_12= csv_12.iloc[:(last_row_12+1),:]

    # Convert to float
    csv_float_12 = csv_12.astype('float')
    # Interpolate to fix missing data
    df_float_interpolate_12= csv_float_12.interpolate()
    df_float_interpolate_12=df_float_interpolate_12.iloc[:,1:]


    #convert to mm
    #12 SEC
    df_float_interpolate_12 ["Tail_X"]=df_float_interpolate_12 ["Tail_X"]*0.28
    df_float_interpolate_12 ["Body1_X"]=df_float_interpolate_12 ["Body1_X"]*0.28
    df_float_interpolate_12 ["Body2_X"]=df_float_interpolate_12 ["Body2_X"]*0.28
    df_float_interpolate_12 ["Body3_X"]=df_float_interpolate_12 ["Body3_X"]*0.28
    df_float_interpolate_12 ["Head_X"]=df_float_interpolate_12 ["Head_X"]*0.28
    df_float_interpolate_12 ["Tail_X.1"]=df_float_interpolate_12 ["Tail_X.1"]*0.28
    df_float_interpolate_12 ["Body1_X.1"]=df_float_interpolate_12 ["Body1_X.1"]*0.28
    df_float_interpolate_12 ["Body2_X.1"]=df_float_interpolate_12 ["Body2_X.1"]*0.28
    df_float_interpolate_12 ["Body3_X.1"]=df_float_interpolate_12 ["Body3_X.1"]*0.28
    df_float_interpolate_12 ["Head_X.1"]=df_float_interpolate_12 ["Head_X.1"]*0.28

    df_float_interpolate_12 ["Tail_Y"]=df_float_interpolate_12 ["Tail_Y"]* -0.304
    df_float_interpolate_12 ["Body1_Y"]=df_float_interpolate_12 ["Body1_Y"]* -0.304
    df_float_interpolate_12 ["Body2_Y"]=df_float_interpolate_12 ["Body2_Y"]* -0.304
    df_float_interpolate_12 ["Body3_Y"]=df_float_interpolate_12 ["Body3_Y"]* -0.304
    df_float_interpolate_12 ["Head_Y"]=df_float_interpolate_12 ["Head_Y"]* -0.304
    df_float_interpolate_12 ["Tail_Y.1"]=df_float_interpolate_12 ["Tail_Y.1"]* -0.304
    df_float_interpolate_12 ["Body1_Y.1"]=df_float_interpolate_12 ["Body1_Y.1"]* -0.304
    df_float_interpolate_12 ["Body2_Y.1"]=df_float_interpolate_12 ["Body2_Y.1"]* -0.304
    df_float_interpolate_12 ["Body3_Y.1"]=df_float_interpolate_12 ["Body3_Y.1"]* -0.304
    df_float_interpolate_12 ["Head_Y.1"]=df_float_interpolate_12 ["Head_Y.1"]* -0.304

    # Write to CSV
    # 12 sec
    df_float_interpolate_12.to_csv('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/d48/Cropped_CSV_d48/'+d48+twelve_name+twelve_folder+'_12S_INTER_MM.csv')
    
    print("Ran:"+twelve_name +twelve_folder)



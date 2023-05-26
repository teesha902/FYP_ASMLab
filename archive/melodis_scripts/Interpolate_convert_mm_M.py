import os
import glob
import pandas as pd
import numpy as np
import random

path = "C:\\Users\\ASMLabUser1\\Desktop\\killifish\\videos\\analyzed\\38-M1\\og_results\\week_12\\with_led\\uroa\\4\\"
out_path = "C:\\Users\\ASMLabUser1\\killifish\\data\\output\\week_12\\uroa\\4\\"
csv_files_raw = glob.glob(path + "*.csv")

for f in csv_files_raw:
    # read the csv file
    csv_raw = pd.read_csv(f)
    full_path = f.split("\\")
    raw_name=full_path[-1].split(".")[0]
    raw_folder = str(full_path[-3]) + "_" + str(full_path[-2]) + "_"
    prefix='week_12_'
    

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
    df_float_interpolate_raw.to_csv(out_path+prefix+raw_folder+raw_name+'_Raw_INTER_MM.csv')

csv_files_3 = glob.glob(os.path.join(out_path, "*_3S.csv"))
# print("csv files 3")
# print(csv_files_3)
for f in csv_files_3:
    # print(f)
    # read the csv file
    csv_3 = pd.read_csv(f)
    full_path = f.split("\\")
    
    three_name = full_path[-1].split(".")[0]
    # three_folder = str(full_path[-3]) + "_" + str(full_path[-2]) + "_"
    # print(three_name, three_folder)

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
    df_float_interpolate_3.to_csv(out_path+three_name+'_INTER_MM.csv')

csv_files_12 = glob.glob(os.path.join(out_path, "*_12S.csv"))
# print("csv_files_12")
# print(csv_files_12)
for f in csv_files_12:
    print(f)
    csv_12 = pd.read_csv(f)
    full_path = f.split("\\")
    twelve_name = full_path[-1].split(".")[0]
    # twelve_folder = str(full_path[-3]) + "_" + str(full_path[-2]) + "_"
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
    df_float_interpolate_12.to_csv(out_path+twelve_name+'_INTER_MM.csv')
    
    # print("Ran:"+twelve_folder+twelve_name)



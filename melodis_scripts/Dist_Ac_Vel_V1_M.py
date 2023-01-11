#Input csv files
import pandas as pd
from openpyxl import load_workbook
import numpy as np
import xlsxwriter
import random
import statistics
import io
import glob
import os
folder_name= 'd48'# could be d 77 etc
path = ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/'+folder_name)
csv_files = glob.glob(os.path.join(path, "*.csv"))

for f in csv_files:
    csv = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    #folder_name=folder_name+'_'
    name=full_path[51:54]
    folder=full_path[54:56]

    
    ##Read in raw csv file for exp time
    file_location_raw= ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/'+folder_name+'/'+folder_name+'_'+name+folder+'.csv')
    csv_RAW = pd.read_csv(file_location_raw)
    exp_time =int(csv_RAW.iloc[0,22])
    exp_time_string= str(exp_time)+'s'
    
    
    file_name= name+folder
    
    file_name_str = io.StringIO(file_name)
    file_name_df= pd.read_csv(file_name_str, sep=",")
    
    
    #Read in 3 second CSV file
    file_location= ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/'+folder_name+'/Cropped_CSV_'+folder_name+'/'+folder_name+'_'+name+folder+'_3S_INTER_MM.csv')
    csv_3 = pd.read_csv(file_location)
    
    
    
    #Read in 12 second CSV file
    file_location_12= ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/'+folder_name+'/Cropped_CSV_'+folder_name+'/'+folder_name+'_'+name+folder+'_12S_INTER_MM.csv')
    csv_12 = pd.read_csv(file_location_12)
    
    
    #Read in original csv file
    file_location_og= ('/Users/asmlabuser1/KF_SUMMER_2022/Raw_CSVs/'+folder_name+'/'+folder_name+'_'+name+folder+'.csv')
    csv = pd.read_csv(file_location_og)
    #calculate frame rate/frames per second
    n_row=3#no rows_before first row of data
    frame_per_sec = (len(csv)-n_row) / int(exp_time)#Total frames/seconds
    
    
    #File Data: Name & Experiment Length
    
    file_data={'Fish Name':[name +folder],'Experiment Length':[exp_time_string]}
    
    file_data_df=pd.DataFrame(file_data).T
    
    # writer_raw = pd.ExcelWriter('/Users/asmlabuser1/Scripts_Ari/testing/Dist_Ac_Vel/'+folder_name+'_'+name+folder+'.xlsx')
    
    # file_data_df.to_excel(writer_raw,index=True,header=False,sheet_name='Dist_03_36_mm')
    
    ##################
    #####DISTANCE#####
    ##################
    
    ##################
    ##first 3 second##
    ##################
    
    #Tail
    tail_x_1 = pd.DataFrame(csv_3.iloc[:, 2])
    tail_y_1 = pd.DataFrame(csv_3.iloc[:, 3])
    tail_x_y_1=[tail_x_1,tail_y_1]
    tail_x_y_1_df = pd.concat(tail_x_y_1, axis=1)
    tail_x_y_1_df.columns = ["Tail_X_1","Tail_Y_1"]
    dist_1_t=np.linalg.norm(tail_x_y_1_df.diff(axis=0), axis=1)#distance per frame
    dist_1_df_t = pd.DataFrame(dist_1_t)
    dist_1_df_t.replace(1,0)
    dist_1_df_t=dist_1_df_t.fillna(0)
    dist_1_df_t[dist_1_df_t > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_df_t_float= dist_1_df_t.astype('float')
    df_float_interpolate_t_1= dist_1_df_t_float.interpolate()#interpolate across NaN to fix tracking errors
    
    
    #body1
    body1_x_1 = pd.DataFrame(csv_3.iloc[:, 4])
    body1_y_1 = pd.DataFrame(csv_3.iloc[:, 5])
    body1_x_y_1=[body1_x_1,body1_y_1]
    body1_x_y_1_df = pd.concat(body1_x_y_1, axis=1)
    body1_x_y_1_df.columns = ["body1_X_1","body1_Y_1"]
    dist_1_b1=np.linalg.norm(body1_x_y_1_df.diff(axis=0), axis=1)#distance per frame
    dist_1_df_b1 = pd.DataFrame(dist_1_b1)
    dist_1_df_b1.replace(1,0)
    dist_1_df_b1=dist_1_df_b1.fillna(0)
    dist_1_df_b1[dist_1_df_b1 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_df_b1_float= dist_1_df_b1.astype('float')
    df_float_interpolate_b1_1= dist_1_df_b1_float.interpolate()#interpolate across NaN to fix tracking errors
    
    
    #body2
    body2_x_1 = pd.DataFrame(csv_3.iloc[:, 6])
    body2_y_1 = pd.DataFrame(csv_3.iloc[:, 7])
    body2_x_y_1=[body2_x_1,body2_y_1]
    body2_x_y_1_df = pd.concat(body2_x_y_1, axis=1)
    body2_x_y_1_df.columns = ["body2_X_1","body2_Y_1"]
    dist_1_b2=np.linalg.norm(body2_x_y_1_df.diff(axis=0), axis=1)#distance per frame
    dist_1_df_b2 = pd.DataFrame(dist_1_b2)
    dist_1_df_b2.replace(1,0)
    dist_1_df_b2=dist_1_df_b2.fillna(0)
    dist_1_df_b2[dist_1_df_b2 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_df_b2_float= dist_1_df_b2.astype('float')
    df_float_interpolate_b2_1= dist_1_df_b2_float.interpolate()#interpolate across NaN to fix tracking errors
    
    
    #body3
    body3_x_1 = pd.DataFrame(csv_3.iloc[:, 8])
    body3_y_1 = pd.DataFrame(csv_3.iloc[:, 9])
    body3_x_y_1=[body3_x_1,body3_y_1]
    body3_x_y_1_df = pd.concat(body3_x_y_1, axis=1)
    body3_x_y_1_df.columns = ["body3_X_1","body3_Y_1"]
    dist_1_b3=np.linalg.norm(body3_x_y_1_df.diff(axis=0), axis=1)#distance per frame
    dist_1_df_b3 = pd.DataFrame(dist_1_b3)
    dist_1_df_b3.replace(1,0)
    dist_1_df_b3=dist_1_df_b3.fillna(0)
    dist_1_df_b3[dist_1_df_b3 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_df_b3_float= dist_1_df_b3.astype('float')
    df_float_interpolate_b3_1= dist_1_df_b3_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #head
    head_x_1 = pd.DataFrame(csv_3.iloc[:, 10])
    head_y_1 = pd.DataFrame(csv_3.iloc[:, 11])
    head_x_y_1=[head_x_1,head_y_1]
    head_x_y_1_df = pd.concat(head_x_y_1, axis=1)
    head_x_y_1_df.columns = ["head_X_1","head_Y_1"]
    dist_1_h=np.linalg.norm(head_x_y_1_df.diff(axis=0), axis=1)#distance per frame
    dist_1_df_h = pd.DataFrame(dist_1_h)
    dist_1_df_h.replace(1,0)
    dist_1_df_h=dist_1_df_h.fillna(0)
    dist_1_df_h[dist_1_df_h > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_df_h_float= dist_1_df_h.astype('float')
    df_float_interpolate_h_1= dist_1_df_h_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #Summed Distances
    sum_df_float_interpolate_t_1=df_float_interpolate_t_1.sum()
    sum_df_float_interpolate_b1_1=df_float_interpolate_b1_1.sum()
    sum_df_float_interpolate_b2_1=df_float_interpolate_b2_1.sum()
    sum_df_float_interpolate_b3_1=df_float_interpolate_b3_1.sum()
    sum_df_float_interpolate_h_1=df_float_interpolate_h_1.sum()
    
    ##################
    ##second 3 second##
    ##################
    
    #Tail
    tail_x_2 = pd.DataFrame(csv_3.iloc[:, 13])
    tail_y_2 = pd.DataFrame(csv_3.iloc[:, 14])
    tail_x_y_2=[tail_x_2,tail_y_2]
    tail_x_y_2_df = pd.concat(tail_x_y_2, axis=1)
    tail_x_y_2_df.columns = ["Tail_X_2","Tail_Y_2"]
    dist_2_t=np.linalg.norm(tail_x_y_2_df.diff(axis=0), axis=1)#distance per frame
    dist_2_df_t = pd.DataFrame(dist_2_t)
    dist_2_df_t.replace(1,0)
    dist_2_df_t=dist_2_df_t.fillna(0)
    dist_2_df_t[dist_2_df_t > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_df_t_float= dist_2_df_t.astype('float')
    df_float_interpolate_t_2= dist_2_df_t_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body1
    body1_x_2 = pd.DataFrame(csv_3.iloc[:, 15])
    body1_y_2 = pd.DataFrame(csv_3.iloc[:, 16])
    body1_x_y_2=[body1_x_2,body1_y_2]
    body1_x_y_2_df = pd.concat(body1_x_y_2, axis=1)
    body1_x_y_2_df.columns = ["body1_X_2","body1_Y_2"]
    dist_2_b1=np.linalg.norm(body1_x_y_2_df.diff(axis=0), axis=1)#distance per frame
    dist_2_df_b1 = pd.DataFrame(dist_2_b1)
    dist_2_df_b1.replace(1,0)
    dist_2_df_b1=dist_2_df_b1.fillna(0)
    dist_2_df_b1[dist_2_df_b1 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_df_b1_float= dist_2_df_b1.astype('float')
    df_float_interpolate_b1_2= dist_2_df_b1_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body2
    body2_x_2 = pd.DataFrame(csv_3.iloc[:, 17])
    body2_y_2 = pd.DataFrame(csv_3.iloc[:, 18])
    body2_x_y_2=[body2_x_2,body2_y_2]
    body2_x_y_2_df = pd.concat(body2_x_y_2, axis=1)
    body2_x_y_2_df.columns = ["body2_X_2","body2_Y_2"]
    dist_2_b2=np.linalg.norm(body2_x_y_2_df.diff(axis=0), axis=1)#distance per frame
    dist_2_df_b2 = pd.DataFrame(dist_2_b2)
    dist_2_df_b2.replace(1,0)
    dist_2_df_b2=dist_2_df_b2.fillna(0)
    dist_2_df_b2[dist_2_df_b2 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_df_b2_float= dist_2_df_b2.astype('float')
    df_float_interpolate_b2_2= dist_2_df_b2_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body3
    body3_x_2 = pd.DataFrame(csv_3.iloc[:, 19])
    body3_y_2 = pd.DataFrame(csv_3.iloc[:, 20])
    body3_x_y_2=[body3_x_2,body3_y_2]
    body3_x_y_2_df = pd.concat(body3_x_y_2, axis=1)
    body3_x_y_2_df.columns = ["body3_X_2","body3_Y_2"]
    dist_2_b3=np.linalg.norm(body3_x_y_2_df.diff(axis=0), axis=1)#distance per frame
    dist_2_df_b3 = pd.DataFrame(dist_2_b3)
    dist_2_df_b3.replace(1,0)
    dist_2_df_b3=dist_2_df_b3.fillna(0)
    dist_2_df_b3[dist_2_df_b3 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_df_b3_float= dist_2_df_b3.astype('float')
    df_float_interpolate_b3_2= dist_2_df_b3_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #head
    head_x_2 = pd.DataFrame(csv_3.iloc[:, 21])
    head_y_2 = pd.DataFrame(csv_3.iloc[:, 22])
    head_x_y_2=[head_x_2,head_y_2]
    head_x_y_2_df = pd.concat(head_x_y_2, axis=1)
    head_x_y_2_df.columns = ["head_X_2","head_Y_2"]
    dist_2_h=np.linalg.norm(head_x_y_2_df.diff(axis=0), axis=1)#distance per frame
    dist_2_df_h = pd.DataFrame(dist_2_h)
    dist_2_df_h.replace(1,0)
    dist_2_df_h=dist_2_df_h.fillna(0)
    dist_2_df_h[dist_2_df_h > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_df_h_float= dist_2_df_h.astype('float')
    df_float_interpolate_h_2= dist_2_df_h_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #Summed Distances
    sum_df_float_interpolate_t_2 =df_float_interpolate_t_2.sum()
    sum_df_float_interpolate_b1_2=df_float_interpolate_b1_2.sum()
    sum_df_float_interpolate_b2_2=df_float_interpolate_b2_2.sum()
    sum_df_float_interpolate_b3_2=df_float_interpolate_b3_2.sum()
    sum_df_float_interpolate_h_2=df_float_interpolate_h_2.sum()
    
    ##################
    ##third 3 second##
    ##################
    
    #Tail
    tail_x_3 = pd.DataFrame(csv_3.iloc[:, 24])
    tail_y_3 = pd.DataFrame(csv_3.iloc[:, 25])
    tail_x_y_3=[tail_x_3,tail_y_3]
    tail_x_y_3_df = pd.concat(tail_x_y_3, axis=1)
    tail_x_y_3_df.columns = ["Tail_X_3","Tail_Y_3"]
    dist_3_t=np.linalg.norm(tail_x_y_3_df.diff(axis=0), axis=1)#distance per frame
    dist_3_df_t = pd.DataFrame(dist_3_t)
    dist_3_df_t.replace(1,0)
    dist_3_df_t=dist_3_df_t.fillna(0)
    dist_3_df_t[dist_3_df_t > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_df_t_float= dist_3_df_t.astype('float')
    df_float_interpolate_t_3= dist_3_df_t_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body1
    body1_x_3 = pd.DataFrame(csv_3.iloc[:, 26])
    body1_y_3 = pd.DataFrame(csv_3.iloc[:, 27])
    body1_x_y_3=[body1_x_3,body1_y_3]
    body1_x_y_3_df = pd.concat(body1_x_y_3, axis=1)
    body1_x_y_3_df.columns = ["body1_X_3","body1_Y_3"]
    dist_3_b1=np.linalg.norm(body1_x_y_3_df.diff(axis=0), axis=1)#distance per frame
    dist_3_df_b1 = pd.DataFrame(dist_3_b1)
    dist_3_df_b1.replace(1,0)
    dist_3_df_b1=dist_3_df_b1.fillna(0)
    dist_3_df_b1[dist_3_df_b1 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_df_b1_float= dist_3_df_b1.astype('float')
    df_float_interpolate_b1_3= dist_3_df_b1_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body2
    body2_x_3 = pd.DataFrame(csv_3.iloc[:, 28])
    body2_y_3 = pd.DataFrame(csv_3.iloc[:, 29])
    body2_x_y_3=[body2_x_3,body2_y_3]
    body2_x_y_3_df = pd.concat(body2_x_y_3, axis=1)
    body2_x_y_3_df.columns = ["body2_X_3","body2_Y_3"]
    dist_3_b2=np.linalg.norm(body2_x_y_3_df.diff(axis=0), axis=1)#distance per frame
    dist_3_df_b2 = pd.DataFrame(dist_3_b2)
    dist_3_df_b2.replace(1,0)
    dist_3_df_b2=dist_3_df_b2.fillna(0)
    dist_3_df_b2[dist_3_df_b2 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_df_b2_float= dist_3_df_b2.astype('float')
    df_float_interpolate_b2_3= dist_3_df_b2_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body3
    body3_x_3 = pd.DataFrame(csv_3.iloc[:, 30])
    body3_y_3 = pd.DataFrame(csv_3.iloc[:, 31])
    body3_x_y_3=[body3_x_3,body3_y_3]
    body3_x_y_3_df = pd.concat(body3_x_y_3, axis=1)
    body3_x_y_3_df.columns = ["body3_X_3","body3_Y_3"]
    dist_3_b3=np.linalg.norm(body3_x_y_3_df.diff(axis=0), axis=1)#distance per frame
    dist_3_df_b3 = pd.DataFrame(dist_3_b3)
    dist_3_df_b3.replace(1,0)
    dist_3_df_b3=dist_3_df_b3.fillna(0)
    dist_3_df_b3[dist_3_df_b3 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_df_b3_float= dist_3_df_b3.astype('float')
    df_float_interpolate_b3_3= dist_3_df_b3_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #head
    head_x_3 = pd.DataFrame(csv_3.iloc[:, 32])
    head_y_3 = pd.DataFrame(csv_3.iloc[:, 33])
    head_x_y_3=[head_x_3,head_y_3]
    head_x_y_3_df = pd.concat(head_x_y_3, axis=1)
    head_x_y_3_df.columns = ["head_X_3","head_Y_3"]
    dist_3_h=np.linalg.norm(head_x_y_3_df.diff(axis=0), axis=1)#distance per frame
    dist_3_df_h = pd.DataFrame(dist_3_h)
    dist_3_df_h.replace(1,0)
    dist_3_df_h=dist_3_df_h.fillna(0)
    dist_3_df_h[dist_3_df_h > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_df_h_float= dist_3_df_h.astype('float')
    df_float_interpolate_h_3= dist_3_df_h_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #Summed Distances
    sum_df_float_interpolate_t_3 =df_float_interpolate_t_3.sum()
    sum_df_float_interpolate_b1_3=df_float_interpolate_b1_3.sum()
    sum_df_float_interpolate_b2_3=df_float_interpolate_b2_3.sum()
    sum_df_float_interpolate_b3_3=df_float_interpolate_b3_3.sum()
    sum_df_float_interpolate_h_3=df_float_interpolate_h_3.sum()
    
    ##################
    ##fourth 3 second##
    ##################
    
    #Tail
    tail_x_4 = pd.DataFrame(csv_3.iloc[:, 35])
    tail_y_4 = pd.DataFrame(csv_3.iloc[:, 36])
    tail_x_y_4=[tail_x_4,tail_y_4]
    tail_x_y_4_df = pd.concat(tail_x_y_4, axis=1)
    tail_x_y_4_df.columns = ["Tail_X_4","Tail_Y_4"]
    dist_4_t=np.linalg.norm(tail_x_y_4_df.diff(axis=0), axis=1)#distance per frame
    dist_4_df_t = pd.DataFrame(dist_4_t)
    dist_4_df_t.replace(1,0)
    dist_4_df_t=dist_4_df_t.fillna(0)
    dist_4_df_t[dist_4_df_t > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_df_t_float= dist_4_df_t.astype('float')
    df_float_interpolate_t_4= dist_4_df_t_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body1
    body1_x_4 = pd.DataFrame(csv_3.iloc[:, 37])
    body1_y_4 = pd.DataFrame(csv_3.iloc[:, 38])
    body1_x_y_4=[body1_x_4,body1_y_4]
    body1_x_y_4_df = pd.concat(body1_x_y_4, axis=1)
    body1_x_y_4_df.columns = ["body1_X_4","body1_Y_4"]
    dist_4_b1=np.linalg.norm(body1_x_y_4_df.diff(axis=0), axis=1)#distance per frame
    dist_4_df_b1 = pd.DataFrame(dist_4_b1)
    dist_4_df_b1.replace(1,0)
    dist_4_df_b1=dist_4_df_b1.fillna(0)
    dist_4_df_b1[dist_4_df_b1 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_df_b1_float= dist_4_df_b1.astype('float')
    df_float_interpolate_b1_4= dist_4_df_b1_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body2
    body2_x_4 = pd.DataFrame(csv_3.iloc[:, 39])
    body2_y_4 = pd.DataFrame(csv_3.iloc[:, 40])
    body2_x_y_4=[body2_x_4,body2_y_4]
    body2_x_y_4_df = pd.concat(body2_x_y_4, axis=1)
    body2_x_y_4_df.columns = ["body2_X_4","body2_Y_4"]
    dist_4_b2=np.linalg.norm(body2_x_y_4_df.diff(axis=0), axis=1)#distance per frame
    dist_4_df_b2 = pd.DataFrame(dist_4_b2)
    dist_4_df_b2.replace(1,0)
    dist_4_df_b2=dist_4_df_b2.fillna(0)
    dist_4_df_b2[dist_4_df_b2 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_df_b2_float= dist_4_df_b2.astype('float')
    df_float_interpolate_b2_4= dist_4_df_b2_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body3
    body3_x_4 = pd.DataFrame(csv_3.iloc[:, 41])
    body3_y_4 = pd.DataFrame(csv_3.iloc[:, 42])
    body3_x_y_4=[body3_x_4,body3_y_4]
    body3_x_y_4_df = pd.concat(body3_x_y_4, axis=1)
    body3_x_y_4_df.columns = ["body3_X_4","body3_Y_4"]
    dist_4_b3=np.linalg.norm(body3_x_y_4_df.diff(axis=0), axis=1)#distance per frame
    dist_4_df_b3 = pd.DataFrame(dist_4_b3)
    dist_4_df_b3.replace(1,0)
    dist_4_df_b3=dist_4_df_b3.fillna(0)
    dist_4_df_b3[dist_4_df_b3 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_df_b3_float= dist_4_df_b3.astype('float')
    df_float_interpolate_b3_4= dist_4_df_b3_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #head
    head_x_4 = pd.DataFrame(csv_3.iloc[:, 43])
    head_y_4 = pd.DataFrame(csv_3.iloc[:, 44])
    head_x_y_4=[head_x_4,head_y_4]
    head_x_y_4_df = pd.concat(head_x_y_4, axis=1)
    head_x_y_4_df.columns = ["head_X_4","head_Y_4"]
    dist_4_h=np.linalg.norm(head_x_y_4_df.diff(axis=0), axis=1)#distance per frame
    dist_4_df_h = pd.DataFrame(dist_4_h)
    dist_4_df_h.replace(1,0)
    dist_4_df_h=dist_4_df_h.fillna(0)
    dist_4_df_h[dist_4_df_h > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_df_h_float= dist_4_df_h.astype('float')
    df_float_interpolate_h_4= dist_4_df_h_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #Summed Distances
    sum_df_float_interpolate_t_4 =df_float_interpolate_t_4.sum()
    sum_df_float_interpolate_b1_4=df_float_interpolate_b1_4.sum()
    sum_df_float_interpolate_b2_4=df_float_interpolate_b2_4.sum()
    sum_df_float_interpolate_b3_4=df_float_interpolate_b3_4.sum()
    sum_df_float_interpolate_h_4=df_float_interpolate_h_4.sum()
    
    
    ##################
    ##fifth 3 second##
    ##################
    
    
    #Tail
    tail_x_5 = pd.DataFrame(csv_3.iloc[:, 46])
    tail_y_5 = pd.DataFrame(csv_3.iloc[:, 47])
    tail_x_y_5=[tail_x_5,tail_y_5]
    tail_x_y_5_df = pd.concat(tail_x_y_5, axis=1)
    tail_x_y_5_df.columns = ["Tail_X_5","Tail_Y_5"]
    dist_5_t=np.linalg.norm(tail_x_y_5_df.diff(axis=0), axis=1)#distance per frame
    dist_5_df_t = pd.DataFrame(dist_5_t)
    dist_5_df_t.replace(1,0)
    dist_5_df_t=dist_5_df_t.fillna(0)
    dist_5_df_t[dist_5_df_t > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_df_t_float= dist_5_df_t.astype('float')
    df_float_interpolate_t_5= dist_5_df_t_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body1
    body1_x_5 = pd.DataFrame(csv_3.iloc[:, 48])
    body1_y_5 = pd.DataFrame(csv_3.iloc[:, 49])
    body1_x_y_5=[body1_x_5,body1_y_5]
    body1_x_y_5_df = pd.concat(body1_x_y_5, axis=1)
    body1_x_y_5_df.columns = ["body1_X_5","body1_Y_5"]
    dist_5_b1=np.linalg.norm(body1_x_y_5_df.diff(axis=0), axis=1)#distance per frame
    dist_5_df_b1 = pd.DataFrame(dist_5_b1)
    dist_5_df_b1.replace(1,0)
    dist_5_df_b1=dist_5_df_b1.fillna(0)
    dist_5_df_b1[dist_5_df_b1 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_df_b1_float= dist_5_df_b1.astype('float')
    df_float_interpolate_b1_5= dist_5_df_b1_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body2
    body2_x_5 = pd.DataFrame(csv_3.iloc[:, 50])
    body2_y_5 = pd.DataFrame(csv_3.iloc[:, 51])
    body2_x_y_5=[body2_x_5,body2_y_5]
    body2_x_y_5_df = pd.concat(body2_x_y_5, axis=1)
    body2_x_y_5_df.columns = ["body2_X_5","body2_Y_5"]
    dist_5_b2=np.linalg.norm(body2_x_y_5_df.diff(axis=0), axis=1)#distance per frame
    dist_5_df_b2 = pd.DataFrame(dist_5_b2)
    dist_5_df_b2.replace(1,0)
    dist_5_df_b2=dist_5_df_b2.fillna(0)
    dist_5_df_b2[dist_5_df_b2 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_df_b2_float= dist_5_df_b2.astype('float')
    df_float_interpolate_b2_5= dist_5_df_b2_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body3
    body3_x_5 = pd.DataFrame(csv_3.iloc[:, 52])
    body3_y_5 = pd.DataFrame(csv_3.iloc[:, 53])
    body3_x_y_5=[body3_x_5,body3_y_5]
    body3_x_y_5_df = pd.concat(body3_x_y_5, axis=1)
    body3_x_y_5_df.columns = ["body3_X_5","body3_Y_5"]
    dist_5_b3=np.linalg.norm(body3_x_y_5_df.diff(axis=0), axis=1)#distance per frame
    dist_5_df_b3 = pd.DataFrame(dist_5_b3)
    dist_5_df_b3.replace(1,0)
    dist_5_df_b3=dist_5_df_b3.fillna(0)
    dist_5_df_b3[dist_5_df_b3 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_df_b3_float= dist_5_df_b3.astype('float')
    df_float_interpolate_b3_5= dist_5_df_b3_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #head
    head_x_5 = pd.DataFrame(csv_3.iloc[:, 54])
    head_y_5 = pd.DataFrame(csv_3.iloc[:, 55])
    head_x_y_5=[head_x_5,head_y_5]
    head_x_y_5_df = pd.concat(head_x_y_5, axis=1)
    head_x_y_5_df.columns = ["head_X_5","head_Y_5"]
    dist_5_h=np.linalg.norm(head_x_y_5_df.diff(axis=0), axis=1)#distance per frame
    dist_5_df_h = pd.DataFrame(dist_5_h)
    dist_5_df_h.replace(1,0)
    dist_5_df_h=dist_5_df_h.fillna(0)
    dist_5_df_h[dist_5_df_h > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_df_h_float= dist_5_df_h.astype('float')
    df_float_interpolate_h_5= dist_5_df_h_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #Summed Distances
    sum_df_float_interpolate_t_5 =df_float_interpolate_t_5.sum()
    sum_df_float_interpolate_b1_5=df_float_interpolate_b1_5.sum()
    sum_df_float_interpolate_b2_5=df_float_interpolate_b2_5.sum()
    sum_df_float_interpolate_b3_5=df_float_interpolate_b3_5.sum()
    sum_df_float_interpolate_h_5=df_float_interpolate_h_5.sum()
    
    ##################
    ##sixth 3 second##
    ##################
    
    #Tail
    tail_x_6 = pd.DataFrame(csv_3.iloc[:, 57])
    tail_y_6 = pd.DataFrame(csv_3.iloc[:, 58])
    tail_x_y_6=[tail_x_6,tail_y_6]
    tail_x_y_6_df = pd.concat(tail_x_y_6, axis=1)
    tail_x_y_6_df.columns = ["Tail_X_6","Tail_Y_6"]
    dist_6_t=np.linalg.norm(tail_x_y_6_df.diff(axis=0), axis=1)#distance per frame
    dist_6_df_t = pd.DataFrame(dist_6_t)
    dist_6_df_t.replace(1,0)
    dist_6_df_t=dist_6_df_t.fillna(0)
    dist_6_df_t[dist_6_df_t > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_6_df_t_float= dist_6_df_t.astype('float')
    df_float_interpolate_t_6= dist_6_df_t_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body1
    body1_x_6 = pd.DataFrame(csv_3.iloc[:, 59])
    body1_y_6 = pd.DataFrame(csv_3.iloc[:, 60])
    body1_x_y_6=[body1_x_6,body1_y_6]
    body1_x_y_6_df = pd.concat(body1_x_y_6, axis=1)
    body1_x_y_6_df.columns = ["body1_X_6","body1_Y_6"]
    dist_6_b1=np.linalg.norm(body1_x_y_6_df.diff(axis=0), axis=1)#distance per frame
    dist_6_df_b1 = pd.DataFrame(dist_6_b1)
    dist_6_df_b1.replace(1,0)
    dist_6_df_b1=dist_6_df_b1.fillna(0)
    dist_6_df_b1[dist_6_df_b1 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_6_df_b1_float= dist_6_df_b1.astype('float')
    df_float_interpolate_b1_6= dist_6_df_b1_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body2
    body2_x_6 = pd.DataFrame(csv_3.iloc[:, 61])
    body2_y_6 = pd.DataFrame(csv_3.iloc[:, 62])
    body2_x_y_6=[body2_x_6,body2_y_6]
    body2_x_y_6_df = pd.concat(body2_x_y_6, axis=1)
    body2_x_y_6_df.columns = ["body2_X_6","body2_Y_6"]
    dist_6_b2=np.linalg.norm(body2_x_y_6_df.diff(axis=0), axis=1)#distance per frame
    dist_6_df_b2 = pd.DataFrame(dist_6_b2)
    dist_6_df_b2.replace(1,0)
    dist_6_df_b2=dist_6_df_b2.fillna(0)
    dist_6_df_b2[dist_6_df_b2 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_6_df_b2_float= dist_6_df_b2.astype('float')
    df_float_interpolate_b2_6= dist_6_df_b2_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #body3
    body3_x_6 = pd.DataFrame(csv_3.iloc[:, 63])
    body3_y_6 = pd.DataFrame(csv_3.iloc[:, 64])
    body3_x_y_6=[body3_x_6,body3_y_6]
    body3_x_y_6_df = pd.concat(body3_x_y_6, axis=1)
    body3_x_y_6_df.columns = ["body3_X_6","body3_Y_6"]
    dist_6_b3=np.linalg.norm(body3_x_y_6_df.diff(axis=0), axis=1)#distance per frame
    dist_6_df_b3 = pd.DataFrame(dist_6_b3)
    dist_6_df_b3.replace(1,0)
    dist_6_df_b3=dist_6_df_b3.fillna(0)
    dist_6_df_b3[dist_6_df_b3 > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_6_df_b3_float= dist_6_df_b3.astype('float')
    df_float_interpolate_b3_6= dist_6_df_b3_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #head
    head_x_6 = pd.DataFrame(csv_3.iloc[:, 65])
    head_y_6 = pd.DataFrame(csv_3.iloc[:, 66])
    head_x_y_6=[head_x_6,head_y_6]
    head_x_y_6_df = pd.concat(head_x_y_6, axis=1)
    head_x_y_6_df.columns = ["head_X_6","head_Y_6"]
    dist_6_h=np.linalg.norm(head_x_y_6_df.diff(axis=0), axis=1)#distance per frame
    dist_6_df_h = pd.DataFrame(dist_6_h)
    dist_6_df_h.replace(1,0)
    dist_6_df_h=dist_6_df_h.fillna(0)
    dist_6_df_h[dist_6_df_h > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_6_df_h_float= dist_6_df_h.astype('float')
    df_float_interpolate_h_6= dist_6_df_h_float.interpolate()#interpolate across NaN to fix tracking errors
    
    #Summed Distances
    sum_df_float_interpolate_t_6 =df_float_interpolate_t_6.sum()
    sum_df_float_interpolate_b1_6=df_float_interpolate_b1_6.sum()
    sum_df_float_interpolate_b2_6=df_float_interpolate_b2_6.sum()
    sum_df_float_interpolate_b3_6=df_float_interpolate_b3_6.sum()
    sum_df_float_interpolate_h_6=df_float_interpolate_h_6.sum()
    
    ###########################################
    ## Average Distance for 3 second segments##
    ############################################
    
    total_average_dist= (sum_df_float_interpolate_t_6+sum_df_float_interpolate_b1_6+sum_df_float_interpolate_b2_6+
                            sum_df_float_interpolate_b3_6+sum_df_float_interpolate_h_6+
    
                            sum_df_float_interpolate_t_5+sum_df_float_interpolate_b1_5+sum_df_float_interpolate_b2_5+
                            sum_df_float_interpolate_b3_5+sum_df_float_interpolate_h_5+
    
                            sum_df_float_interpolate_t_4+sum_df_float_interpolate_b1_4+sum_df_float_interpolate_b2_4+
                            sum_df_float_interpolate_b3_4+sum_df_float_interpolate_h_4+
    
                           sum_df_float_interpolate_t_3+sum_df_float_interpolate_b1_3+sum_df_float_interpolate_b2_3+
                           sum_df_float_interpolate_b3_3+sum_df_float_interpolate_h_3+
    
                           sum_df_float_interpolate_t_2+sum_df_float_interpolate_b1_2+sum_df_float_interpolate_b2_2+
                           sum_df_float_interpolate_b3_2+sum_df_float_interpolate_h_2+
    
                           sum_df_float_interpolate_t_1+sum_df_float_interpolate_b1_1+sum_df_float_interpolate_b2_1+
                           sum_df_float_interpolate_b3_1+sum_df_float_interpolate_h_1)/30
    
    average_dist_list= [sum_df_float_interpolate_t_6,sum_df_float_interpolate_b1_6,sum_df_float_interpolate_b2_6,
                            sum_df_float_interpolate_b3_6,sum_df_float_interpolate_h_6,
    
                            sum_df_float_interpolate_t_5,sum_df_float_interpolate_b1_5,sum_df_float_interpolate_b2_5,
                            sum_df_float_interpolate_b3_5,sum_df_float_interpolate_h_5,
    
                            sum_df_float_interpolate_t_4,sum_df_float_interpolate_b1_4,sum_df_float_interpolate_b2_4,
                            sum_df_float_interpolate_b3_4,sum_df_float_interpolate_h_4,
    
                           sum_df_float_interpolate_t_3,sum_df_float_interpolate_b1_3,sum_df_float_interpolate_b2_3,
                           sum_df_float_interpolate_b3_3,sum_df_float_interpolate_h_3,
    
                           sum_df_float_interpolate_t_2,sum_df_float_interpolate_b1_2,sum_df_float_interpolate_b2_2,
                           sum_df_float_interpolate_b3_2,sum_df_float_interpolate_h_2,
    
                           sum_df_float_interpolate_t_1,sum_df_float_interpolate_b1_1,sum_df_float_interpolate_b2_1,
                           sum_df_float_interpolate_b3_1,sum_df_float_interpolate_h_1]
    
    average_dist_list_df= pd.DataFrame(average_dist_list)
    average_dist_list_df.columns=["average_dist"]
    average_dist_list_df_list= average_dist_list_df["average_dist"].tolist()
    
    SD_dist_3sec_seg= statistics.stdev(average_dist_list_df_list)
    
    # #Write to excel
    # # Average of the randomly generated 3 second segments
    # file_data_descriptive={'Fish Name':[name +folder],'Experiment Length':[exp_time_string]}
    # file_data_descriptive_df=pd.DataFrame(file_data_descriptive)
    # writer = pd.ExcelWriter('/Users/asmlabuser1/Scripts_Ari/testing/Descriptive_Data/'+folder_name+'_'+name+folder+'.xlsx')
    # file_data_descriptive_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow=1)
    
    
    
    # #Put titles and units
    # #Distance
    # file_data_dist={'Distance Travelled (mm)':[]}
    # file_data_dist_df=pd.DataFrame(file_data_dist).T
    # file_data_dist_df.to_excel(writer,index=True,header=False,sheet_name= folder,startrow=0 ,startcol=2)
    
    # #Velocity
    # file_data_vel={'Velocity (mm per second)':[]}
    # file_data_vel_df=pd.DataFrame(file_data_vel).T
    # file_data_vel_df.to_excel(writer,index=True,header=False,sheet_name= folder,startrow=0 ,startcol=21)
    
    # #Acceleration
    # file_data_acc={'Acceleration (mm per second per second)':[]}
    # file_data_acc_df=pd.DataFrame(file_data_acc).T
    # file_data_acc_df.to_excel(writer,index=True,header=False,sheet_name= folder,startrow= 0,startcol=37)
    
    
    # total_average_dist_data={"Average_Distance_3sec_segments":total_average_dist.tolist()}
    # total_average_dist_data_df=pd.DataFrame(total_average_dist_data)
    # total_average_dist_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1,startcol=2 )
    
    # SD_dist_3sec_seg_data= {'Average_Distance_SD_3sec_segments':[SD_dist_3sec_seg]}
    # SD_dist_3sec_seg_data_df=pd.DataFrame(SD_dist_3sec_seg_data)
    # SD_dist_3sec_seg_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1,startcol=3 )
    
    #12 second span
    #Subset xy coordinates after LED
    
    #Tail
    tail_x = csv_12["Tail_X.1"]
    tail_y = csv_12["Tail_Y.1"]
    
    tail_X_Y= [tail_x,tail_y]
    tail_X_Y_df = pd.concat(tail_X_Y, axis=1)
    
    
    #Body 1
    body1_x = csv_12["Body1_X.1"]
    body1_y = csv_12["Body1_Y.1"]
    
    body1_X_Y= [body1_x,body1_y]
    body1_X_Y_df = pd.concat(body1_X_Y, axis=1)
    
    #Body 2
    body2_x = csv_12["Body2_X.1"]
    body2_y = csv_12["Body2_Y.1"]
    
    body2_X_Y= [body2_x,body2_y]
    body2_X_Y_df = pd.concat(body2_X_Y, axis=1)
    
    
    #Body 3
    body3_x = csv_12["Body3_X.1"]
    body3_y = csv_12["Body3_Y.1"]
    
    body3_X_Y= [body3_x,body3_y]
    body3_X_Y_df = pd.concat(body3_X_Y, axis=1)
    
    #Head
    
    head_x = csv_12["Head_X.1"]
    head_y = csv_12["Head_Y.1"]
    head_X_Y= [head_x,head_y]
    head_X_Y_df = pd.concat(head_X_Y, axis=1)
    
    #Subset xy coordinates Before LED
    
    #Tail
    tail_x_bef = csv_12["Tail_X"]
    tail_y_bef = csv_12["Tail_Y"]
    
    tail_X_Y_bef= [tail_x_bef,tail_y_bef]
    tail_X_Y_bef_df = pd.concat(tail_X_Y_bef, axis=1)
    
    
    #Body 1
    body1_x_bef = csv_12["Body1_X"]
    body1_y_bef = csv_12["Body1_Y"]
    
    body1_X_Y_bef= [body1_x_bef,body1_y_bef]
    body1_X_Y_bef_df = pd.concat(body1_X_Y_bef, axis=1)
    
    #Body 2
    body2_x_bef = csv_12["Body2_X"]
    body2_y_bef = csv_12["Body2_Y"]
    
    body2_X_Y_bef= [body2_x_bef,body2_y_bef]
    body2_X_Y_bef_df = pd.concat(body2_X_Y_bef, axis=1)
    
    
    #Body 3
    body3_x_bef = csv_12["Body3_X"]
    body3_y_bef = csv_12["Body3_Y"]
    
    body3_X_Y_bef= [body3_x_bef,body3_y_bef]
    body3_X_Y_bef_df = pd.concat(body3_X_Y_bef, axis=1)
    
    #Head
    
    head_x_bef = csv_12["Head_X"]
    head_y_bef = csv_12["Head_Y"]
    head_X_Y_bef= [head_x_bef,head_y_bef]
    head_X_Y_bef_df = pd.concat(head_X_Y_bef, axis=1)
    
    #Subset 0-1seconds & calculate distance
    one_sec_mark=int(len(tail_X_Y_df)/6)
    
    #Tail
    d_0_1_tail=pd.DataFrame(tail_X_Y_df.iloc[0:one_sec_mark,:])
    dist_0_1_tail=np.linalg.norm(d_0_1_tail.diff(axis=0), axis=1)#distance per frame
    dist_0_1_tail_df = pd.DataFrame(dist_0_1_tail)
    dist_0_1_tail_df.columns = ["Dist_0_1S_tail"]
    dist_0_1_tail_df["Dist_0_1S_tail"] = dist_0_1_tail_df["Dist_0_1S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_0_1_tail_df = dist_0_1_tail_df.fillna(0)  # replace NA with 0
    dist_0_1_tail_df[dist_0_1_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_1_tail_df_float= dist_0_1_tail_df.astype('float')
    dist_0_1_tail_df_float_inter= dist_0_1_tail_df_float.interpolate()
    total_dist_0_1_tail =dist_0_1_tail_df_float_inter['Dist_0_1S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    d_0_1_body1=pd.DataFrame(body1_X_Y_df.iloc[0:one_sec_mark,:])
    dist_0_1_body1=np.linalg.norm(d_0_1_body1.diff(axis=0), axis=1)#distance per frame
    dist_0_1_body1_df = pd.DataFrame(dist_0_1_body1)
    dist_0_1_body1_df.columns = ["Dist_0_1S_body1"]
    dist_0_1_body1_df["Dist_0_1S_body1"] = dist_0_1_body1_df["Dist_0_1S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_1_body1_df = dist_0_1_body1_df.fillna(0)  # replace NA with 0
    dist_0_1_body1_df[dist_0_1_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_1_body1_df_float= dist_0_1_body1_df.astype('float')
    dist_0_1_body1_df_float_inter= dist_0_1_body1_df_float.interpolate()
    total_dist_0_1_body1 =dist_0_1_body1_df_float_inter['Dist_0_1S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    d_0_1_body2=pd.DataFrame(body2_X_Y_df.iloc[0:one_sec_mark,:])
    dist_0_1_body2=np.linalg.norm(d_0_1_body2.diff(axis=0), axis=1)#distance per frame
    dist_0_1_body2_df = pd.DataFrame(dist_0_1_body2)
    dist_0_1_body2_df.columns = ["Dist_0_1S_body2"]
    dist_0_1_body2_df["Dist_0_1S_body2"] = dist_0_1_body2_df["Dist_0_1S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_1_body2_df = dist_0_1_body2_df.fillna(0)  # replace NA with 0
    dist_0_1_body2_df[dist_0_1_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_1_body2_df_float= dist_0_1_body2_df.astype('float')
    dist_0_1_body2_df_float_inter= dist_0_1_body2_df_float.interpolate()
    total_dist_0_1_body2 =dist_0_1_body2_df_float_inter['Dist_0_1S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    d_0_1_body3=pd.DataFrame(body3_X_Y_df.iloc[0:one_sec_mark,:])
    dist_0_1_body3=np.linalg.norm(d_0_1_body3.diff(axis=0), axis=1)#distance per frame
    dist_0_1_body3_df = pd.DataFrame(dist_0_1_body3)
    dist_0_1_body3_df.columns = ["Dist_0_1S_body3"]
    dist_0_1_body3_df["Dist_0_1S_body3"] = dist_0_1_body3_df["Dist_0_1S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_1_body3_df = dist_0_1_body3_df.fillna(0)  # replace NA with 0
    dist_0_1_body3_df[dist_0_1_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_1_body3_df_float= dist_0_1_body3_df.astype('float')
    dist_0_1_body3_df_float_inter= dist_0_1_body3_df_float.interpolate()
    total_dist_0_1_body3 =dist_0_1_body3_df_float_inter['Dist_0_1S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    d_0_1_head=pd.DataFrame(head_X_Y_df.iloc[0:one_sec_mark,:])
    dist_0_1_head=np.linalg.norm(d_0_1_head.diff(axis=0), axis=1)#distance per frame
    dist_0_1_head_df = pd.DataFrame(dist_0_1_head)
    dist_0_1_head_df.columns = ["Dist_0_1S_head"]
    dist_0_1_head_df["Dist_0_1S_head"] = dist_0_1_head_df["Dist_0_1S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_1_head_df = dist_0_1_head_df.fillna(0)  # replace NA with 0
    dist_0_1_head_df[dist_0_1_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_1_head_df_float= dist_0_1_head_df.astype('float')
    dist_0_1_head_df_float_inter= dist_0_1_head_df_float.interpolate()
    total_dist_0_1_head =dist_0_1_head_df_float_inter['Dist_0_1S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_0_1=pd.Series((total_dist_0_1_tail+total_dist_0_1_body1+total_dist_0_1_body2+total_dist_0_1_body3+total_dist_0_1_head)/5)
    
    
    #Subset 1-2seconds & calculate distance
    two_sec_mark= (one_sec_mark)*2
    
    #Tail
    zero_one_tail=pd.DataFrame(tail_X_Y_df.iloc[one_sec_mark:two_sec_mark,:])
    dist_1_2_tail=np.linalg.norm(zero_one_tail.diff(axis=0), axis=1)#distance per frame
    dist_1_2_tail_df = pd.DataFrame(dist_1_2_tail)
    dist_1_2_tail_df.columns = ["Dist_1_2S_tail"]
    dist_1_2_tail_df["Dist_1_2S_tail"] = dist_1_2_tail_df["Dist_1_2S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_1_2_tail_df = dist_1_2_tail_df.fillna(0)  # replace NA with 0
    dist_1_2_tail_df[dist_1_2_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_2_tail_df_float= dist_1_2_tail_df.astype('float')
    dist_1_2_tail_df_float_inter= dist_1_2_tail_df_float.interpolate()
    total_dist_1_2_tail =dist_1_2_tail_df_float_inter['Dist_1_2S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_one_body1=pd.DataFrame(body1_X_Y_df.iloc[one_sec_mark:two_sec_mark,:])
    dist_1_2_body1=np.linalg.norm(zero_one_body1.diff(axis=0), axis=1)#distance per frame
    dist_1_2_body1_df = pd.DataFrame(dist_1_2_body1)
    dist_1_2_body1_df.columns = ["Dist_1_2S_body1"]
    dist_1_2_body1_df["Dist_1_2S_body1"] = dist_1_2_body1_df["Dist_1_2S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_1_2_body1_df = dist_1_2_body1_df.fillna(0)  # replace NA with 0
    dist_1_2_body1_df[dist_1_2_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_2_body1_df_float= dist_1_2_body1_df.astype('float')
    dist_1_2_body1_df_float_inter= dist_1_2_body1_df_float.interpolate()
    total_dist_1_2_body1 =dist_1_2_body1_df_float_inter['Dist_1_2S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_one_body2=pd.DataFrame(body2_X_Y_df.iloc[one_sec_mark:two_sec_mark,:])
    dist_1_2_body2=np.linalg.norm(zero_one_body2.diff(axis=0), axis=1)#distance per frame
    dist_1_2_body2_df = pd.DataFrame(dist_1_2_body2)
    dist_1_2_body2_df.columns = ["Dist_1_2S_body2"]
    dist_1_2_body2_df["Dist_1_2S_body2"] = dist_1_2_body2_df["Dist_1_2S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_1_2_body2_df = dist_1_2_body2_df.fillna(0)  # replace NA with 0
    dist_1_2_body2_df[dist_1_2_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_2_body2_df_float= dist_1_2_body2_df.astype('float')
    dist_1_2_body2_df_float_inter= dist_1_2_body2_df_float.interpolate()
    total_dist_1_2_body2 =dist_1_2_body2_df_float_inter['Dist_1_2S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_one_body3=pd.DataFrame(body3_X_Y_df.iloc[one_sec_mark:two_sec_mark,:])
    dist_1_2_body3=np.linalg.norm(zero_one_body3.diff(axis=0), axis=1)#distance per frame
    dist_1_2_body3_df = pd.DataFrame(dist_1_2_body3)
    dist_1_2_body3_df.columns = ["Dist_1_2S_body3"]
    dist_1_2_body3_df["Dist_1_2S_body3"] = dist_1_2_body3_df["Dist_1_2S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_1_2_body3_df = dist_1_2_body3_df.fillna(0)  # replace NA with 0
    dist_1_2_body3_df[dist_1_2_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_2_body3_df_float= dist_1_2_body3_df.astype('float')
    dist_1_2_body3_df_float_inter= dist_1_2_body3_df_float.interpolate()
    total_dist_1_2_body3 =dist_1_2_body3_df_float_inter['Dist_1_2S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_one_head=pd.DataFrame(head_X_Y_df.iloc[one_sec_mark:two_sec_mark,:])
    dist_1_2_head=np.linalg.norm(zero_one_head.diff(axis=0), axis=1)#distance per frame
    dist_1_2_head_df = pd.DataFrame(dist_1_2_head)
    dist_1_2_head_df.columns = ["Dist_1_2S_head"]
    dist_1_2_head_df["Dist_1_2S_head"] = dist_1_2_head_df["Dist_1_2S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_1_2_head_df = dist_1_2_head_df.fillna(0)  # replace NA with 0
    dist_1_2_head_df[dist_1_2_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_1_2_head_df_float= dist_1_2_head_df.astype('float')
    dist_1_2_head_df_float_inter= dist_1_2_head_df_float.interpolate()
    total_dist_1_2_head =dist_1_2_head_df_float_inter['Dist_1_2S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_1_2=pd.Series((total_dist_1_2_tail+total_dist_1_2_body1+total_dist_1_2_body2+total_dist_1_2_body3+total_dist_1_2_head)/5)
    
    #Subset 2-3seconds & calculate distance
    three_sec_mark= (one_sec_mark)*3
    
    #Tail
    zero_one_tail=pd.DataFrame(tail_X_Y_df.iloc[two_sec_mark:three_sec_mark,:])
    dist_2_3_tail=np.linalg.norm(zero_one_tail.diff(axis=0), axis=1)#distance per frame
    dist_2_3_tail_df = pd.DataFrame(dist_2_3_tail)
    dist_2_3_tail_df.columns = ["Dist_2_3S_tail"]
    dist_2_3_tail_df["Dist_2_3S_tail"] = dist_2_3_tail_df["Dist_2_3S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_2_3_tail_df = dist_2_3_tail_df.fillna(0)  # replace NA with 0
    dist_2_3_tail_df[dist_2_3_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_3_tail_df_float= dist_2_3_tail_df.astype('float')
    dist_2_3_tail_df_float_inter= dist_2_3_tail_df_float.interpolate()
    total_dist_2_3_tail =dist_2_3_tail_df_float_inter['Dist_2_3S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_one_body1=pd.DataFrame(body1_X_Y_df.iloc[two_sec_mark:three_sec_mark,:])
    dist_2_3_body1=np.linalg.norm(zero_one_body1.diff(axis=0), axis=1)#distance per frame
    dist_2_3_body1_df = pd.DataFrame(dist_2_3_body1)
    dist_2_3_body1_df.columns = ["Dist_2_3S_body1"]
    dist_2_3_body1_df["Dist_2_3S_body1"] = dist_2_3_body1_df["Dist_2_3S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_2_3_body1_df = dist_2_3_body1_df.fillna(0)  # replace NA with 0
    dist_2_3_body1_df[dist_2_3_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_3_body1_df_float= dist_2_3_body1_df.astype('float')
    dist_2_3_body1_df_float_inter= dist_2_3_body1_df_float.interpolate()
    total_dist_2_3_body1 =dist_2_3_body1_df_float_inter['Dist_2_3S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_one_body2=pd.DataFrame(body2_X_Y_df.iloc[two_sec_mark:three_sec_mark,:])
    dist_2_3_body2=np.linalg.norm(zero_one_body2.diff(axis=0), axis=1)#distance per frame
    dist_2_3_body2_df = pd.DataFrame(dist_2_3_body2)
    dist_2_3_body2_df.columns = ["Dist_2_3S_body2"]
    dist_2_3_body2_df["Dist_2_3S_body2"] = dist_2_3_body2_df["Dist_2_3S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_2_3_body2_df = dist_2_3_body2_df.fillna(0)  # replace NA with 0
    dist_2_3_body2_df[dist_2_3_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_3_body2_df_float= dist_2_3_body2_df.astype('float')
    dist_2_3_body2_df_float_inter= dist_2_3_body2_df_float.interpolate()
    total_dist_2_3_body2 =dist_2_3_body2_df_float_inter['Dist_2_3S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_one_body3=pd.DataFrame(body3_X_Y_df.iloc[two_sec_mark:three_sec_mark,:])
    dist_2_3_body3=np.linalg.norm(zero_one_body3.diff(axis=0), axis=1)#distance per frame
    dist_2_3_body3_df = pd.DataFrame(dist_2_3_body3)
    dist_2_3_body3_df.columns = ["Dist_2_3S_body3"]
    dist_2_3_body3_df["Dist_2_3S_body3"] = dist_2_3_body3_df["Dist_2_3S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_2_3_body3_df = dist_2_3_body3_df.fillna(0)  # replace NA with 0
    dist_2_3_body3_df[dist_2_3_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_3_body3_df_float= dist_2_3_body3_df.astype('float')
    dist_2_3_body3_df_float_inter= dist_2_3_body3_df_float.interpolate()
    total_dist_2_3_body3 =dist_2_3_body3_df_float_inter['Dist_2_3S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_one_head=pd.DataFrame(head_X_Y_df.iloc[two_sec_mark:three_sec_mark,:])
    dist_2_3_head=np.linalg.norm(zero_one_head.diff(axis=0), axis=1)#distance per frame
    dist_2_3_head_df = pd.DataFrame(dist_2_3_head)
    dist_2_3_head_df.columns = ["Dist_2_3S_head"]
    dist_2_3_head_df["Dist_2_3S_head"] = dist_2_3_head_df["Dist_2_3S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_2_3_head_df = dist_2_3_head_df.fillna(0)  # replace NA with 0
    dist_2_3_head_df[dist_2_3_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_2_3_head_df_float= dist_2_3_head_df.astype('float')
    dist_2_3_head_df_float_inter= dist_2_3_head_df_float.interpolate()
    total_dist_2_3_head =dist_2_3_head_df_float_inter['Dist_2_3S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_2_3=pd.Series((total_dist_2_3_tail+total_dist_2_3_body1+total_dist_2_3_body2+total_dist_2_3_body3+total_dist_2_3_head)/5)
    
    #Subset 3-4seconds & calculate distance
    four_sec_mark= (one_sec_mark)*4
    
    #Tail
    zero_one_tail=pd.DataFrame(tail_X_Y_df.iloc[three_sec_mark:four_sec_mark,:])
    dist_3_4_tail=np.linalg.norm(zero_one_tail.diff(axis=0), axis=1)#distance per frame
    dist_3_4_tail_df = pd.DataFrame(dist_3_4_tail)
    dist_3_4_tail_df.columns = ["Dist_3_4S_tail"]
    dist_3_4_tail_df["Dist_3_4S_tail"] = dist_3_4_tail_df["Dist_3_4S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_3_4_tail_df = dist_3_4_tail_df.fillna(0)  # replace NA with 0
    dist_3_4_tail_df[dist_3_4_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_4_tail_df_float= dist_3_4_tail_df.astype('float')
    dist_3_4_tail_df_float_inter= dist_3_4_tail_df_float.interpolate()
    total_dist_3_4_tail =dist_3_4_tail_df_float_inter['Dist_3_4S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_one_body1=pd.DataFrame(body1_X_Y_df.iloc[three_sec_mark:four_sec_mark,:])
    dist_3_4_body1=np.linalg.norm(zero_one_body1.diff(axis=0), axis=1)#distance per frame
    dist_3_4_body1_df = pd.DataFrame(dist_3_4_body1)
    dist_3_4_body1_df.columns = ["Dist_3_4S_body1"]
    dist_3_4_body1_df["Dist_3_4S_body1"] = dist_3_4_body1_df["Dist_3_4S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_4_body1_df = dist_3_4_body1_df.fillna(0)  # replace NA with 0
    dist_3_4_body1_df[dist_3_4_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_4_body1_df_float= dist_3_4_body1_df.astype('float')
    dist_3_4_body1_df_float_inter= dist_3_4_body1_df_float.interpolate()
    total_dist_3_4_body1 =dist_3_4_body1_df_float_inter['Dist_3_4S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_one_body2=pd.DataFrame(body2_X_Y_df.iloc[three_sec_mark:four_sec_mark,:])
    dist_3_4_body2=np.linalg.norm(zero_one_body2.diff(axis=0), axis=1)#distance per frame
    dist_3_4_body2_df = pd.DataFrame(dist_3_4_body2)
    dist_3_4_body2_df.columns = ["Dist_3_4S_body2"]
    dist_3_4_body2_df["Dist_3_4S_body2"] = dist_3_4_body2_df["Dist_3_4S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_4_body2_df = dist_3_4_body2_df.fillna(0)  # replace NA with 0
    dist_3_4_body2_df[dist_3_4_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_4_body2_df_float= dist_3_4_body2_df.astype('float')
    dist_3_4_body2_df_float_inter= dist_3_4_body2_df_float.interpolate()
    total_dist_3_4_body2 =dist_3_4_body2_df_float_inter['Dist_3_4S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_one_body3=pd.DataFrame(body3_X_Y_df.iloc[three_sec_mark:four_sec_mark,:])
    dist_3_4_body3=np.linalg.norm(zero_one_body3.diff(axis=0), axis=1)#distance per frame
    dist_3_4_body3_df = pd.DataFrame(dist_3_4_body3)
    dist_3_4_body3_df.columns = ["Dist_3_4S_body3"]
    dist_3_4_body3_df["Dist_3_4S_body3"] = dist_3_4_body3_df["Dist_3_4S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_4_body3_df = dist_3_4_body3_df.fillna(0)  # replace NA with 0
    dist_3_4_body3_df[dist_3_4_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_4_body3_df_float= dist_3_4_body3_df.astype('float')
    dist_3_4_body3_df_float_inter= dist_3_4_body3_df_float.interpolate()
    total_dist_3_4_body3 =dist_3_4_body3_df_float_inter['Dist_3_4S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_one_head=pd.DataFrame(head_X_Y_df.iloc[three_sec_mark:four_sec_mark,:])
    dist_3_4_head=np.linalg.norm(zero_one_head.diff(axis=0), axis=1)#distance per frame
    dist_3_4_head_df = pd.DataFrame(dist_3_4_head)
    dist_3_4_head_df.columns = ["Dist_3_4S_head"]
    dist_3_4_head_df["Dist_3_4S_head"] = dist_3_4_head_df["Dist_3_4S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_4_head_df = dist_3_4_head_df.fillna(0)  # replace NA with 0
    dist_3_4_head_df[dist_3_4_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_4_head_df_float= dist_3_4_head_df.astype('float')
    dist_3_4_head_df_float_inter= dist_3_4_head_df_float.interpolate()
    total_dist_3_4_head =dist_3_4_head_df_float_inter['Dist_3_4S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_3_4=pd.Series((total_dist_3_4_tail+total_dist_3_4_body1+total_dist_3_4_body2+total_dist_3_4_body3+total_dist_3_4_head)/5)
    
    #Subset 4-5seconds & calculate distance
    five_sec_mark= (one_sec_mark)*5
    
    #Tail
    zero_one_tail=pd.DataFrame(tail_X_Y_df.iloc[four_sec_mark:five_sec_mark,:])
    dist_4_5_tail=np.linalg.norm(zero_one_tail.diff(axis=0), axis=1)#distance per frame
    dist_4_5_tail_df = pd.DataFrame(dist_4_5_tail)
    dist_4_5_tail_df.columns = ["Dist_4_5S_tail"]
    dist_4_5_tail_df["Dist_4_5S_tail"] = dist_4_5_tail_df["Dist_4_5S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_4_5_tail_df = dist_4_5_tail_df.fillna(0)  # replace NA with 0
    dist_4_5_tail_df[dist_4_5_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_5_tail_df_float= dist_4_5_tail_df.astype('float')
    dist_4_5_tail_df_float_inter= dist_4_5_tail_df_float.interpolate()
    total_dist_4_5_tail =dist_4_5_tail_df_float_inter['Dist_4_5S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_one_body1=pd.DataFrame(body1_X_Y_df.iloc[four_sec_mark:five_sec_mark,:])
    dist_4_5_body1=np.linalg.norm(zero_one_body1.diff(axis=0), axis=1)#distance per frame
    dist_4_5_body1_df = pd.DataFrame(dist_4_5_body1)
    dist_4_5_body1_df.columns = ["Dist_4_5S_body1"]
    dist_4_5_body1_df["Dist_4_5S_body1"] = dist_4_5_body1_df["Dist_4_5S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_4_5_body1_df = dist_4_5_body1_df.fillna(0)  # replace NA with 0
    dist_4_5_body1_df[dist_4_5_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_5_body1_df_float= dist_4_5_body1_df.astype('float')
    dist_4_5_body1_df_float_inter= dist_4_5_body1_df_float.interpolate()
    total_dist_4_5_body1 =dist_4_5_body1_df_float_inter['Dist_4_5S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_one_body2=pd.DataFrame(body2_X_Y_df.iloc[four_sec_mark:five_sec_mark,:])
    dist_4_5_body2=np.linalg.norm(zero_one_body2.diff(axis=0), axis=1)#distance per frame
    dist_4_5_body2_df = pd.DataFrame(dist_4_5_body2)
    dist_4_5_body2_df.columns = ["Dist_4_5S_body2"]
    dist_4_5_body2_df["Dist_4_5S_body2"] = dist_4_5_body2_df["Dist_4_5S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_4_5_body2_df = dist_4_5_body2_df.fillna(0)  # replace NA with 0
    dist_4_5_body2_df[dist_4_5_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_5_body2_df_float= dist_4_5_body2_df.astype('float')
    dist_4_5_body2_df_float_inter= dist_4_5_body2_df_float.interpolate()
    total_dist_4_5_body2 =dist_4_5_body2_df_float_inter['Dist_4_5S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_one_body3=pd.DataFrame(body3_X_Y_df.iloc[four_sec_mark:five_sec_mark,:])
    dist_4_5_body3=np.linalg.norm(zero_one_body3.diff(axis=0), axis=1)#distance per frame
    dist_4_5_body3_df = pd.DataFrame(dist_4_5_body3)
    dist_4_5_body3_df.columns = ["Dist_4_5S_body3"]
    dist_4_5_body3_df["Dist_4_5S_body3"] = dist_4_5_body3_df["Dist_4_5S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_4_5_body3_df = dist_4_5_body3_df.fillna(0)  # replace NA with 0
    dist_4_5_body3_df[dist_4_5_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_5_body3_df_float= dist_4_5_body3_df.astype('float')
    dist_4_5_body3_df_float_inter= dist_4_5_body3_df_float.interpolate()
    total_dist_4_5_body3 =dist_4_5_body3_df_float_inter['Dist_4_5S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_one_head=pd.DataFrame(head_X_Y_df.iloc[four_sec_mark:five_sec_mark,:])
    dist_4_5_head=np.linalg.norm(zero_one_head.diff(axis=0), axis=1)#distance per frame
    dist_4_5_head_df = pd.DataFrame(dist_4_5_head)
    dist_4_5_head_df.columns = ["Dist_4_5S_head"]
    dist_4_5_head_df["Dist_4_5S_head"] = dist_4_5_head_df["Dist_4_5S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_4_5_head_df = dist_4_5_head_df.fillna(0)  # replace NA with 0
    dist_4_5_head_df[dist_4_5_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_4_5_head_df_float= dist_4_5_head_df.astype('float')
    dist_4_5_head_df_float_inter= dist_4_5_head_df_float.interpolate()
    total_dist_4_5_head =dist_4_5_head_df_float_inter['Dist_4_5S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_4_5=pd.Series((total_dist_4_5_tail+total_dist_4_5_body1+total_dist_4_5_body2+total_dist_4_5_body3+total_dist_4_5_head)/5)
    
    #Subset 4-5seconds & calculate distance
    six_sec_mark= (one_sec_mark)*6
    
    #Tail
    zero_one_tail=pd.DataFrame(tail_X_Y_df.iloc[five_sec_mark:six_sec_mark,:])
    dist_5_6_tail=np.linalg.norm(zero_one_tail.diff(axis=0), axis=1)#distance per frame
    dist_5_6_tail_df = pd.DataFrame(dist_5_6_tail)
    dist_5_6_tail_df.columns = ["Dist_5_6S_tail"]
    dist_5_6_tail_df["Dist_5_6S_tail"] = dist_5_6_tail_df["Dist_5_6S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_5_6_tail_df = dist_5_6_tail_df.fillna(0)  # replace NA with 0
    dist_5_6_tail_df[dist_5_6_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_6_tail_df_float= dist_5_6_tail_df.astype('float')
    dist_5_6_tail_df_float_inter= dist_5_6_tail_df_float.interpolate()
    total_dist_5_6_tail =dist_5_6_tail_df_float_inter['Dist_5_6S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_one_body1=pd.DataFrame(body1_X_Y_df.iloc[five_sec_mark:six_sec_mark,:])
    dist_5_6_body1=np.linalg.norm(zero_one_body1.diff(axis=0), axis=1)#distance per frame
    dist_5_6_body1_df = pd.DataFrame(dist_5_6_body1)
    dist_5_6_body1_df.columns = ["Dist_5_6S_body1"]
    dist_5_6_body1_df["Dist_5_6S_body1"] = dist_5_6_body1_df["Dist_5_6S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_5_6_body1_df = dist_5_6_body1_df.fillna(0)  # replace NA with 0
    dist_5_6_body1_df[dist_5_6_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_6_body1_df_float= dist_5_6_body1_df.astype('float')
    dist_5_6_body1_df_float_inter= dist_5_6_body1_df_float.interpolate()
    total_dist_5_6_body1 =dist_5_6_body1_df_float_inter['Dist_5_6S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_one_body2=pd.DataFrame(body2_X_Y_df.iloc[five_sec_mark:six_sec_mark,:])
    dist_5_6_body2=np.linalg.norm(zero_one_body2.diff(axis=0), axis=1)#distance per frame
    dist_5_6_body2_df = pd.DataFrame(dist_5_6_body2)
    dist_5_6_body2_df.columns = ["Dist_5_6S_body2"]
    dist_5_6_body2_df["Dist_5_6S_body2"] = dist_5_6_body2_df["Dist_5_6S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_5_6_body2_df = dist_5_6_body2_df.fillna(0)  # replace NA with 0
    dist_5_6_body2_df[dist_5_6_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_6_body2_df_float= dist_5_6_body2_df.astype('float')
    dist_5_6_body2_df_float_inter= dist_5_6_body2_df_float.interpolate()
    total_dist_5_6_body2 =dist_5_6_body2_df_float_inter['Dist_5_6S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_one_body3=pd.DataFrame(body3_X_Y_df.iloc[five_sec_mark:six_sec_mark,:])
    dist_5_6_body3=np.linalg.norm(zero_one_body3.diff(axis=0), axis=1)#distance per frame
    dist_5_6_body3_df = pd.DataFrame(dist_5_6_body3)
    dist_5_6_body3_df.columns = ["Dist_5_6S_body3"]
    dist_5_6_body3_df["Dist_5_6S_body3"] = dist_5_6_body3_df["Dist_5_6S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_5_6_body3_df = dist_5_6_body3_df.fillna(0)  # replace NA with 0
    dist_5_6_body3_df[dist_5_6_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_6_body3_df_float= dist_5_6_body3_df.astype('float')
    dist_5_6_body3_df_float_inter= dist_5_6_body3_df_float.interpolate()
    total_dist_5_6_body3 =dist_5_6_body3_df_float_inter['Dist_5_6S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_one_head=pd.DataFrame(head_X_Y_df.iloc[five_sec_mark:six_sec_mark,:])
    dist_5_6_head=np.linalg.norm(zero_one_head.diff(axis=0), axis=1)#distance per frame
    dist_5_6_head_df = pd.DataFrame(dist_5_6_head)
    dist_5_6_head_df.columns = ["Dist_5_6S_head"]
    dist_5_6_head_df["Dist_5_6S_head"] = dist_5_6_head_df["Dist_5_6S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_5_6_head_df = dist_5_6_head_df.fillna(0)  # replace NA with 0
    dist_5_6_head_df[dist_5_6_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_5_6_head_df_float= dist_5_6_head_df.astype('float')
    dist_5_6_head_df_float_inter= dist_5_6_head_df_float.interpolate()
    total_dist_5_6_head =dist_5_6_head_df_float_inter['Dist_5_6S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_5_6=pd.Series((total_dist_5_6_tail+total_dist_5_6_body1+total_dist_5_6_body2+total_dist_5_6_body3+total_dist_5_6_head)/5)
    
    
    #Subset 0-3 seconds & calculate distance
    three_sec_mark=int(len(tail_X_Y_df)/2)
    #Tail
    zero_three_tail=pd.DataFrame(tail_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_tail=np.linalg.norm(zero_three_tail.diff(axis=0), axis=1)#distance per frame
    dist_0_3_tail_df = pd.DataFrame(dist_0_3_tail)
    dist_0_3_tail_df.columns = ["Dist_0_3S_tail"]
    dist_0_3_tail_df["Dist_0_3S_tail"] = dist_0_3_tail_df["Dist_0_3S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_0_3_tail_df = dist_0_3_tail_df.fillna(0)  # replace NA with 0
    dist_0_3_tail_df[dist_0_3_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_tail_df_float= dist_0_3_tail_df.astype('float')
    dist_0_3_tail_df_float_inter= dist_0_3_tail_df_float.interpolate()
    total_dist_0_3_tail =dist_0_3_tail_df_float_inter['Dist_0_3S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_three_body1=pd.DataFrame(body1_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_body1=np.linalg.norm(zero_three_body1.diff(axis=0), axis=1)#distance per frame
    dist_0_3_body1_df = pd.DataFrame(dist_0_3_body1)
    dist_0_3_body1_df.columns = ["Dist_0_3S_body1"]
    dist_0_3_body1_df["Dist_0_3S_body1"] = dist_0_3_body1_df["Dist_0_3S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_3_body1_df = dist_0_3_body1_df.fillna(0)  # replace NA with 0
    dist_0_3_body1_df[dist_0_3_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_body1_df_float= dist_0_3_body1_df.astype('float')
    dist_0_3_body1_df_float_inter= dist_0_3_body1_df_float.interpolate()
    total_dist_0_3_body1 =dist_0_3_body1_df_float_inter['Dist_0_3S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_three_body2=pd.DataFrame(body2_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_body2=np.linalg.norm(zero_three_body2.diff(axis=0), axis=1)#distance per frame
    dist_0_3_body2_df = pd.DataFrame(dist_0_3_body2)
    dist_0_3_body2_df.columns = ["Dist_0_3S_body2"]
    dist_0_3_body2_df["Dist_0_3S_body2"] = dist_0_3_body2_df["Dist_0_3S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_3_body2_df = dist_0_3_body2_df.fillna(0)  # replace NA with 0
    dist_0_3_body2_df[dist_0_3_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_body2_df_float= dist_0_3_body2_df.astype('float')
    dist_0_3_body2_df_float_inter= dist_0_3_body2_df_float.interpolate()
    total_dist_0_3_body2 =dist_0_3_body2_df_float_inter['Dist_0_3S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_three_body3=pd.DataFrame(body3_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_body3=np.linalg.norm(zero_three_body3.diff(axis=0), axis=1)#distance per frame
    dist_0_3_body3_df = pd.DataFrame(dist_0_3_body3)
    dist_0_3_body3_df.columns = ["Dist_0_3S_body3"]
    dist_0_3_body3_df["Dist_0_3S_body3"] = dist_0_3_body3_df["Dist_0_3S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_3_body3_df = dist_0_3_body3_df.fillna(0)  # replace NA with 0
    dist_0_3_body3_df[dist_0_3_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_body3_df_float= dist_0_3_body3_df.astype('float')
    dist_0_3_body3_df_float_inter= dist_0_3_body3_df_float.interpolate()
    total_dist_0_3_body3 =dist_0_3_body3_df_float_inter['Dist_0_3S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_three_head=pd.DataFrame(head_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_head=np.linalg.norm(zero_three_head.diff(axis=0), axis=1)#distance per frame
    dist_0_3_head_df = pd.DataFrame(dist_0_3_head)
    dist_0_3_head_df.columns = ["Dist_0_3S_head"]
    dist_0_3_head_df["Dist_0_3S_head"] = dist_0_3_head_df["Dist_0_3S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_3_head_df = dist_0_3_head_df.fillna(0)  # replace NA with 0
    dist_0_3_head_df[dist_0_3_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_head_df_float= dist_0_3_head_df.astype('float')
    dist_0_3_head_df_float_inter= dist_0_3_head_df_float.interpolate()
    total_dist_0_3_head =dist_0_3_head_df_float_inter['Dist_0_3S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_0_3=pd.Series((total_dist_0_3_tail+total_dist_0_3_body1+total_dist_0_3_body2+total_dist_0_3_body3+total_dist_0_3_head)/5)
    
    #Subset 3-6 seconds & calculate distance
    
    #Tail
    three_six_tail=pd.DataFrame(tail_X_Y_df.iloc[three_sec_mark:len(tail_X_Y_df),:])
    dist_3_6_tail=np.linalg.norm(three_six_tail.diff(axis=0), axis=1)#distance per frame
    dist_3_6_tail_df = pd.DataFrame(dist_3_6_tail)
    dist_3_6_tail_df.columns = ["Dist_3_6S_tail"]
    dist_3_6_tail_df["Dist_3_6S_tail"] = dist_3_6_tail_df["Dist_3_6S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_3_6_tail_df = dist_3_6_tail_df.fillna(0)  # replace NA with 0
    dist_3_6_tail_df[dist_3_6_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_6_tail_df_float= dist_3_6_tail_df.astype('float')
    dist_3_6_tail_df_float_inter= dist_3_6_tail_df_float.interpolate()
    total_dist_3_6_tail =dist_3_6_tail_df_float_inter['Dist_3_6S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    three_six_body1=pd.DataFrame(body1_X_Y_df.iloc[three_sec_mark:len(tail_X_Y_df),:])
    dist_3_6_body1=np.linalg.norm(three_six_body1.diff(axis=0), axis=1)#distance per frame
    dist_3_6_body1_df = pd.DataFrame(dist_3_6_body1)
    dist_3_6_body1_df.columns = ["Dist_3_6S_body1"]
    dist_3_6_body1_df["Dist_3_6S_body1"] = dist_3_6_body1_df["Dist_3_6S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_6_body1_df = dist_3_6_body1_df.fillna(0)  # replace NA with 0
    dist_3_6_body1_df[dist_3_6_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_6_body1_df_float= dist_3_6_body1_df.astype('float')
    dist_3_6_body1_df_float_inter= dist_3_6_body1_df_float.interpolate()
    total_dist_3_6_body1 =dist_3_6_body1_df_float_inter['Dist_3_6S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    three_six_body2=pd.DataFrame(body2_X_Y_df.iloc[three_sec_mark:len(tail_X_Y_df),:])
    dist_3_6_body2=np.linalg.norm(three_six_body2.diff(axis=0), axis=1)#distance per frame
    dist_3_6_body2_df = pd.DataFrame(dist_3_6_body2)
    dist_3_6_body2_df.columns = ["Dist_3_6S_body2"]
    dist_3_6_body2_df["Dist_3_6S_body2"] = dist_3_6_body2_df["Dist_3_6S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_6_body2_df = dist_3_6_body2_df.fillna(0)  # replace NA with 0
    dist_3_6_body2_df[dist_3_6_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_6_body2_df_float= dist_3_6_body2_df.astype('float')
    dist_3_6_body2_df_float_inter= dist_3_6_body2_df_float.interpolate()
    total_dist_3_6_body2 =dist_3_6_body2_df_float_inter['Dist_3_6S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    three_six_body3=pd.DataFrame(body3_X_Y_df.iloc[three_sec_mark:len(tail_X_Y_df),:])
    dist_3_6_body3=np.linalg.norm(three_six_body3.diff(axis=0), axis=1)#distance per frame
    dist_3_6_body3_df = pd.DataFrame(dist_3_6_body3)
    dist_3_6_body3_df.columns = ["Dist_3_6S_body3"]
    dist_3_6_body3_df["Dist_3_6S_body3"] = dist_3_6_body3_df["Dist_3_6S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_6_body3_df = dist_3_6_body3_df.fillna(0)  # replace NA with 0
    dist_3_6_body3_df[dist_3_6_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_6_body3_df_float= dist_3_6_body3_df.astype('float')
    dist_3_6_body3_df_float_inter= dist_3_6_body3_df_float.interpolate()
    total_dist_3_6_body3 =dist_3_6_body3_df_float_inter['Dist_3_6S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    three_six_head=pd.DataFrame(head_X_Y_df.iloc[three_sec_mark:len(tail_X_Y_df),:])
    dist_3_6_head=np.linalg.norm(three_six_head.diff(axis=0), axis=1)#distance per frame
    dist_3_6_head_df = pd.DataFrame(dist_3_6_head)
    dist_3_6_head_df.columns = ["Dist_3_6S_head"]
    dist_3_6_head_df["Dist_3_6S_head"] = dist_3_6_head_df["Dist_3_6S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_3_6_head_df = dist_3_6_head_df.fillna(0)  # replace NA with 0
    dist_3_6_head_df[dist_3_6_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_3_6_head_df_float= dist_3_6_head_df.astype('float')
    dist_3_6_head_df_float_inter= dist_3_6_head_df_float.interpolate()
    total_dist_3_6_head =dist_3_6_head_df_float_inter['Dist_3_6S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_3_6=pd.Series((total_dist_3_6_tail+total_dist_3_6_body1+total_dist_3_6_body2+total_dist_3_6_body3+total_dist_3_6_head)/5)
    
    #Subset 0-6 seconds & calculate distance
    
    #Tail
    three_six_tail=pd.DataFrame(tail_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_tail=np.linalg.norm(three_six_tail.diff(axis=0), axis=1)#distance per frame
    dist_0_6_tail_df = pd.DataFrame(dist_0_6_tail)
    dist_0_6_tail_df.columns = ["Dist_0_6S_tail"]
    dist_0_6_tail_df["Dist_0_6S_tail"] = dist_0_6_tail_df["Dist_0_6S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1-> replace 1 with 0
    dist_0_6_tail_df = dist_0_6_tail_df.fillna(0)  # replace NA with 0
    dist_0_6_tail_df[dist_0_6_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_tail_df_float= dist_0_6_tail_df.astype('float')
    dist_0_6_tail_df_float_inter= dist_0_6_tail_df_float.interpolate()
    total_dist_0_6_tail =dist_0_6_tail_df_float_inter['Dist_0_6S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    three_six_body1=pd.DataFrame(body1_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_body1=np.linalg.norm(three_six_body1.diff(axis=0), axis=1)#distance per frame
    dist_0_6_body1_df = pd.DataFrame(dist_0_6_body1)
    dist_0_6_body1_df.columns = ["Dist_0_6S_body1"]
    dist_0_6_body1_df["Dist_0_6S_body1"] = dist_0_6_body1_df["Dist_0_6S_body1"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_6_body1_df = dist_0_6_body1_df.fillna(0)  # replace NA with 0
    dist_0_6_body1_df[dist_0_6_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_body1_df_float= dist_0_6_body1_df.astype('float')
    dist_0_6_body1_df_float_inter= dist_0_6_body1_df_float.interpolate()
    total_dist_0_6_body1 =dist_0_6_body1_df_float_inter['Dist_0_6S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    three_six_body2=pd.DataFrame(body2_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_body2=np.linalg.norm(three_six_body2.diff(axis=0), axis=1)#distance per frame
    dist_0_6_body2_df = pd.DataFrame(dist_0_6_body2)
    dist_0_6_body2_df.columns = ["Dist_0_6S_body2"]
    dist_0_6_body2_df["Dist_0_6S_body2"] = dist_0_6_body2_df["Dist_0_6S_body2"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_6_body2_df = dist_0_6_body2_df.fillna(0)  # replace NA with 0
    dist_0_6_body2_df[dist_0_6_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_body2_df_float= dist_0_6_body2_df.astype('float')
    dist_0_6_body2_df_float_inter= dist_0_6_body2_df_float.interpolate()
    total_dist_0_6_body2 =dist_0_6_body2_df_float_inter['Dist_0_6S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    three_six_body3=pd.DataFrame(body3_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_body3=np.linalg.norm(three_six_body3.diff(axis=0), axis=1)#distance per frame
    dist_0_6_body3_df = pd.DataFrame(dist_0_6_body3)
    dist_0_6_body3_df.columns = ["Dist_0_6S_body3"]
    dist_0_6_body3_df["Dist_0_6S_body3"] = dist_0_6_body3_df["Dist_0_6S_body3"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_6_body3_df = dist_0_6_body3_df.fillna(0)  # replace NA with 0
    dist_0_6_body3_df[dist_0_6_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_body3_df_float= dist_0_6_body3_df.astype('float')
    dist_0_6_body3_df_float_inter= dist_0_6_body3_df_float.interpolate()
    total_dist_0_6_body3 =dist_0_6_body3_df_float_inter['Dist_0_6S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    three_six_head=pd.DataFrame(head_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_head=np.linalg.norm(three_six_head.diff(axis=0), axis=1)#distance per frame
    dist_0_6_head_df = pd.DataFrame(dist_0_6_head)
    dist_0_6_head_df.columns = ["Dist_0_6S_head"]
    dist_0_6_head_df["Dist_0_6S_head"] = dist_0_6_head_df["Dist_0_6S_head"].replace(1, 0)#When distance = 0, formula prints 1-> replace 1 with 0
    dist_0_6_head_df = dist_0_6_head_df.fillna(0)  # replace NA with 0
    dist_0_6_head_df[dist_0_6_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_head_df_float= dist_0_6_head_df.astype('float')
    dist_0_6_head_df_float_inter= dist_0_6_head_df_float.interpolate()
    total_dist_0_6_head =dist_0_6_head_df_float_inter['Dist_0_6S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_0_6=pd.Series((total_dist_0_6_tail+total_dist_0_6_body1+total_dist_0_6_body2+total_dist_0_6_body3+total_dist_0_6_head)/5)
    
    #Subset -3-0 seconds & calculate distance
    minus_three_sec_mark=int(len(tail_X_Y_df)/2)
    #Tail
    minus_three_zero_tail=pd.DataFrame(tail_X_Y_bef_df.iloc[minus_three_sec_mark :len(tail_X_Y_df),:])
    dist_minus3_0_tail=np.linalg.norm(minus_three_zero_tail.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_tail_df = pd.DataFrame(dist_minus3_0_tail)
    dist_minus3_0_tail_df.columns = ["Dist_minus3_0S_tail"]
    dist_minus3_0_tail_df["Dist_minus3_0S_tail"] = dist_minus3_0_tail_df["Dist_minus3_0S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_minus3_0_tail_df = dist_minus3_0_tail_df.fillna(0)  # replace NA with 0
    dist_minus3_0_tail_df[dist_minus3_0_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_tail_df_float= dist_minus3_0_tail_df.astype('float')
    dist_minus3_0_tail_df_float_inter= dist_minus3_0_tail_df_float.interpolate()
    total_dist_minus3_0_tail =dist_minus3_0_tail_df_float_inter['Dist_minus3_0S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    minus_three_zero_body1=pd.DataFrame(body1_X_Y_bef_df.iloc[minus_three_sec_mark :len(tail_X_Y_df),:])
    dist_minus3_0_body1=np.linalg.norm(minus_three_zero_body1.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_body1_df = pd.DataFrame(dist_minus3_0_body1)
    dist_minus3_0_body1_df.columns = ["Dist_minus3_0S_body1"]
    dist_minus3_0_body1_df["Dist_minus3_0S_body1"] = dist_minus3_0_body1_df["Dist_minus3_0S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_body1_df = dist_minus3_0_body1_df.fillna(0)  # replace NA with 0
    dist_minus3_0_body1_df[dist_minus3_0_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_body1_df_float= dist_minus3_0_body1_df.astype('float')
    dist_minus3_0_body1_df_float_inter= dist_minus3_0_body1_df_float.interpolate()
    total_dist_minus3_0_body1 =dist_minus3_0_body1_df_float_inter['Dist_minus3_0S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    minus_three_zero_body2=pd.DataFrame(body2_X_Y_bef_df.iloc[minus_three_sec_mark :len(tail_X_Y_df),:])
    dist_minus3_0_body2=np.linalg.norm(minus_three_zero_body2.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_body2_df = pd.DataFrame(dist_minus3_0_body2)
    dist_minus3_0_body2_df.columns = ["Dist_minus3_0S_body2"]
    dist_minus3_0_body2_df["Dist_minus3_0S_body2"] = dist_minus3_0_body2_df["Dist_minus3_0S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_body2_df = dist_minus3_0_body2_df.fillna(0)  # replace NA with 0
    dist_minus3_0_body2_df[dist_minus3_0_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_body2_df_float= dist_minus3_0_body2_df.astype('float')
    dist_minus3_0_body2_df_float_inter= dist_minus3_0_body2_df_float.interpolate()
    total_dist_minus3_0_body2 =dist_minus3_0_body2_df_float_inter['Dist_minus3_0S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    minus_three_zero_body3=pd.DataFrame(body3_X_Y_bef_df.iloc[minus_three_sec_mark :len(tail_X_Y_df),:])
    dist_minus3_0_body3=np.linalg.norm(minus_three_zero_body3.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_body3_df = pd.DataFrame(dist_minus3_0_body3)
    dist_minus3_0_body3_df.columns = ["Dist_minus3_0S_body3"]
    dist_minus3_0_body3_df["Dist_minus3_0S_body3"] = dist_minus3_0_body3_df["Dist_minus3_0S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_body3_df = dist_minus3_0_body3_df.fillna(0)  # replace NA with 0
    dist_minus3_0_body3_df[dist_minus3_0_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_body3_df_float= dist_minus3_0_body3_df.astype('float')
    dist_minus3_0_body3_df_float_inter= dist_minus3_0_body3_df_float.interpolate()
    total_dist_minus3_0_body3 =dist_minus3_0_body3_df_float_inter['Dist_minus3_0S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    minus_three_zero_head=pd.DataFrame(head_X_Y_bef_df.iloc[minus_three_sec_mark :len(tail_X_Y_df),:])
    dist_minus3_0_head=np.linalg.norm(minus_three_zero_head.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_head_df = pd.DataFrame(dist_minus3_0_head)
    dist_minus3_0_head_df.columns = ["Dist_minus3_0S_head"]
    dist_minus3_0_head_df["Dist_minus3_0S_head"] = dist_minus3_0_head_df["Dist_minus3_0S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_head_df = dist_minus3_0_head_df.fillna(0)  # replace NA with 0
    dist_minus3_0_head_df[dist_minus3_0_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_head_df_float= dist_minus3_0_head_df.astype('float')
    dist_minus3_0_head_df_float_inter= dist_minus3_0_head_df_float.interpolate()
    total_dist_minus3_0_head =dist_minus3_0_head_df_float_inter['Dist_minus3_0S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_minus3_0=pd.Series((total_dist_minus3_0_tail+total_dist_minus3_0_body1+total_dist_minus3_0_body2+total_dist_minus3_0_body3+total_dist_minus3_0_head)/5)
    
    #Subset minus 3- minus 2 seconds & calculate distance
    minus_two_sec_mark=(int(len(tail_X_Y_df)/2))+ (int(len(tail_X_Y_df)/6))
    #Tail
    minus_three_minus_two_tail=pd.DataFrame(tail_X_Y_bef_df.iloc[minus_three_sec_mark: minus_two_sec_mark,:])
    dist_minus3_minus2_tail=np.linalg.norm(minus_three_minus_two_tail.diff(axis=0), axis=1)#distance per frame
    dist_minus3_minus2_tail_df = pd.DataFrame(dist_minus3_minus2_tail)
    dist_minus3_minus2_tail_df.columns = ["Dist_minus3_minus2S_tail"]
    dist_minus3_minus2_tail_df["Dist_minus3_minus2S_tail"] = dist_minus3_minus2_tail_df["Dist_minus3_minus2S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_minus3_minus2_tail_df = dist_minus3_minus2_tail_df.fillna(0)  # replace NA with 0
    dist_minus3_minus2_tail_df[dist_minus3_minus2_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_minus2_tail_df_float= dist_minus3_minus2_tail_df.astype('float')
    dist_minus3_minus2_tail_df_float_inter= dist_minus3_minus2_tail_df_float.interpolate()
    total_dist_minus3_minus2_tail =dist_minus3_minus2_tail_df_float_inter['Dist_minus3_minus2S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    minus_three_minus_two_body1=pd.DataFrame(body1_X_Y_bef_df.iloc[minus_three_sec_mark: minus_two_sec_mark,:])
    dist_minus3_minus2_body1=np.linalg.norm(minus_three_minus_two_body1.diff(axis=0), axis=1)#distance per frame
    dist_minus3_minus2_body1_df = pd.DataFrame(dist_minus3_minus2_body1)
    dist_minus3_minus2_body1_df.columns = ["Dist_minus3_minus2S_body1"]
    dist_minus3_minus2_body1_df["Dist_minus3_minus2S_body1"] = dist_minus3_minus2_body1_df["Dist_minus3_minus2S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_minus2_body1_df = dist_minus3_minus2_body1_df.fillna(0)  # replace NA with 0
    dist_minus3_minus2_body1_df[dist_minus3_minus2_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_minus2_body1_df_float= dist_minus3_minus2_body1_df.astype('float')
    dist_minus3_minus2_body1_df_float_inter= dist_minus3_minus2_body1_df_float.interpolate()
    total_dist_minus3_minus2_body1 =dist_minus3_minus2_body1_df_float_inter['Dist_minus3_minus2S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    minus_three_minus_two_body2=pd.DataFrame(body2_X_Y_bef_df.iloc[minus_three_sec_mark: minus_two_sec_mark,:])
    dist_minus3_minus2_body2=np.linalg.norm(minus_three_minus_two_body2.diff(axis=0), axis=1)#distance per frame
    dist_minus3_minus2_body2_df = pd.DataFrame(dist_minus3_minus2_body2)
    dist_minus3_minus2_body2_df.columns = ["Dist_minus3_minus2S_body2"]
    dist_minus3_minus2_body2_df["Dist_minus3_minus2S_body2"] = dist_minus3_minus2_body2_df["Dist_minus3_minus2S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_minus2_body2_df = dist_minus3_minus2_body2_df.fillna(0)  # replace NA with 0
    dist_minus3_minus2_body2_df[dist_minus3_minus2_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_minus2_body2_df_float= dist_minus3_minus2_body2_df.astype('float')
    dist_minus3_minus2_body2_df_float_inter= dist_minus3_minus2_body2_df_float.interpolate()
    total_dist_minus3_minus2_body2 =dist_minus3_minus2_body2_df_float_inter['Dist_minus3_minus2S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    minus_three_minus_two_body3=pd.DataFrame(body3_X_Y_bef_df.iloc[minus_three_sec_mark: minus_two_sec_mark,:])
    dist_minus3_minus2_body3=np.linalg.norm(minus_three_minus_two_body3.diff(axis=0), axis=1)#distance per frame
    dist_minus3_minus2_body3_df = pd.DataFrame(dist_minus3_minus2_body3)
    dist_minus3_minus2_body3_df.columns = ["Dist_minus3_minus2S_body3"]
    dist_minus3_minus2_body3_df["Dist_minus3_minus2S_body3"] = dist_minus3_minus2_body3_df["Dist_minus3_minus2S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_minus2_body3_df = dist_minus3_minus2_body3_df.fillna(0)  # replace NA with 0
    dist_minus3_minus2_body3_df[dist_minus3_minus2_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_minus2_body3_df_float= dist_minus3_minus2_body3_df.astype('float')
    dist_minus3_minus2_body3_df_float_inter= dist_minus3_minus2_body3_df_float.interpolate()
    total_dist_minus3_minus2_body3 =dist_minus3_minus2_body3_df_float_inter['Dist_minus3_minus2S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    minus_three_minus_two_head=pd.DataFrame(head_X_Y_bef_df.iloc[minus_three_sec_mark: minus_two_sec_mark,:])
    dist_minus3_minus2_head=np.linalg.norm(minus_three_minus_two_head.diff(axis=0), axis=1)#distance per frame
    dist_minus3_minus2_head_df = pd.DataFrame(dist_minus3_minus2_head)
    dist_minus3_minus2_head_df.columns = ["Dist_minus3_minus2S_head"]
    dist_minus3_minus2_head_df["Dist_minus3_minus2S_head"] = dist_minus3_minus2_head_df["Dist_minus3_minus2S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_minus2_head_df = dist_minus3_minus2_head_df.fillna(0)  # replace NA with 0
    dist_minus3_minus2_head_df[dist_minus3_minus2_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_minus2_head_df_float= dist_minus3_minus2_head_df.astype('float')
    dist_minus3_minus2_head_df_float_inter= dist_minus3_minus2_head_df_float.interpolate()
    total_dist_minus3_minus2_head =dist_minus3_minus2_head_df_float_inter['Dist_minus3_minus2S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_minus3_minus2=pd.Series((total_dist_minus3_minus2_tail+total_dist_minus3_minus2_body1+total_dist_minus3_minus2_body2+total_dist_minus3_minus2_body3+total_dist_minus3_minus2_head)/5)
    
    #Subset minus 2 - minus 1 seconds & calculate distance
    minus_one_sec_mark=(int(len(tail_X_Y_df)/2))+ ((int(len(tail_X_Y_df)/6))*2)
    #Tail
    minus_two_minus_one_tail=pd.DataFrame(tail_X_Y_bef_df.iloc[minus_two_sec_mark: minus_one_sec_mark,:])
    dist_minus2_minus1_tail=np.linalg.norm(minus_two_minus_one_tail.diff(axis=0), axis=1)#distance per frame
    dist_minus2_minus1_tail_df = pd.DataFrame(dist_minus2_minus1_tail)
    dist_minus2_minus1_tail_df.columns = ["Dist_minus2_minus1S_tail"]
    dist_minus2_minus1_tail_df["Dist_minus2_minus1S_tail"] = dist_minus2_minus1_tail_df["Dist_minus2_minus1S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_minus2_minus1_tail_df = dist_minus2_minus1_tail_df.fillna(0)  # replace NA with 0
    dist_minus2_minus1_tail_df[dist_minus2_minus1_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus2_minus1_tail_df_float= dist_minus2_minus1_tail_df.astype('float')
    dist_minus2_minus1_tail_df_float_inter= dist_minus2_minus1_tail_df_float.interpolate()
    total_dist_minus2_minus1_tail =dist_minus2_minus1_tail_df_float_inter['Dist_minus2_minus1S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    minus_two_minus_one_body1=pd.DataFrame(body1_X_Y_bef_df.iloc[minus_two_sec_mark: minus_one_sec_mark,:])
    dist_minus2_minus1_body1=np.linalg.norm(minus_two_minus_one_body1.diff(axis=0), axis=1)#distance per frame
    dist_minus2_minus1_body1_df = pd.DataFrame(dist_minus2_minus1_body1)
    dist_minus2_minus1_body1_df.columns = ["Dist_minus2_minus1S_body1"]
    dist_minus2_minus1_body1_df["Dist_minus2_minus1S_body1"] = dist_minus2_minus1_body1_df["Dist_minus2_minus1S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus2_minus1_body1_df = dist_minus2_minus1_body1_df.fillna(0)  # replace NA with 0
    dist_minus2_minus1_body1_df[dist_minus2_minus1_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus2_minus1_body1_df_float= dist_minus2_minus1_body1_df.astype('float')
    dist_minus2_minus1_body1_df_float_inter= dist_minus2_minus1_body1_df_float.interpolate()
    total_dist_minus2_minus1_body1 =dist_minus2_minus1_body1_df_float_inter['Dist_minus2_minus1S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    minus_two_minus_one_body2=pd.DataFrame(body2_X_Y_bef_df.iloc[minus_two_sec_mark: minus_one_sec_mark,:])
    dist_minus2_minus1_body2=np.linalg.norm(minus_two_minus_one_body2.diff(axis=0), axis=1)#distance per frame
    dist_minus2_minus1_body2_df = pd.DataFrame(dist_minus2_minus1_body2)
    dist_minus2_minus1_body2_df.columns = ["Dist_minus2_minus1S_body2"]
    dist_minus2_minus1_body2_df["Dist_minus2_minus1S_body2"] = dist_minus2_minus1_body2_df["Dist_minus2_minus1S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus2_minus1_body2_df = dist_minus2_minus1_body2_df.fillna(0)  # replace NA with 0
    dist_minus2_minus1_body2_df[dist_minus2_minus1_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus2_minus1_body2_df_float= dist_minus2_minus1_body2_df.astype('float')
    dist_minus2_minus1_body2_df_float_inter= dist_minus2_minus1_body2_df_float.interpolate()
    total_dist_minus2_minus1_body2 =dist_minus2_minus1_body2_df_float_inter['Dist_minus2_minus1S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    minus_two_minus_one_body3=pd.DataFrame(body3_X_Y_bef_df.iloc[minus_two_sec_mark: minus_one_sec_mark,:])
    dist_minus2_minus1_body3=np.linalg.norm(minus_two_minus_one_body3.diff(axis=0), axis=1)#distance per frame
    dist_minus2_minus1_body3_df = pd.DataFrame(dist_minus2_minus1_body3)
    dist_minus2_minus1_body3_df.columns = ["Dist_minus2_minus1S_body3"]
    dist_minus2_minus1_body3_df["Dist_minus2_minus1S_body3"] = dist_minus2_minus1_body3_df["Dist_minus2_minus1S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus2_minus1_body3_df = dist_minus2_minus1_body3_df.fillna(0)  # replace NA with 0
    dist_minus2_minus1_body3_df[dist_minus2_minus1_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus2_minus1_body3_df_float= dist_minus2_minus1_body3_df.astype('float')
    dist_minus2_minus1_body3_df_float_inter= dist_minus2_minus1_body3_df_float.interpolate()
    total_dist_minus2_minus1_body3 =dist_minus2_minus1_body3_df_float_inter['Dist_minus2_minus1S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    minus_two_minus_one_head=pd.DataFrame(head_X_Y_bef_df.iloc[minus_two_sec_mark: minus_one_sec_mark,:])
    dist_minus2_minus1_head=np.linalg.norm(minus_two_minus_one_head.diff(axis=0), axis=1)#distance per frame
    dist_minus2_minus1_head_df = pd.DataFrame(dist_minus2_minus1_head)
    dist_minus2_minus1_head_df.columns = ["Dist_minus2_minus1S_head"]
    dist_minus2_minus1_head_df["Dist_minus2_minus1S_head"] = dist_minus2_minus1_head_df["Dist_minus2_minus1S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus2_minus1_head_df = dist_minus2_minus1_head_df.fillna(0)  # replace NA with 0
    dist_minus2_minus1_head_df[dist_minus2_minus1_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus2_minus1_head_df_float= dist_minus2_minus1_head_df.astype('float')
    dist_minus2_minus1_head_df_float_inter= dist_minus2_minus1_head_df_float.interpolate()
    total_dist_minus2_minus1_head =dist_minus2_minus1_head_df_float_inter['Dist_minus2_minus1S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_minus2_minus1=pd.Series((total_dist_minus2_minus1_tail+total_dist_minus2_minus1_body1+total_dist_minus2_minus1_body2+total_dist_minus2_minus1_body3+total_dist_minus2_minus1_head)/5)
    
    
    #Subset minus 1 - 0 seconds & calculate distance
    minus_one_sec_mark=(int(len(tail_X_Y_df)/2))+ ((int(len(tail_X_Y_df)/6))*2)
    #Tail
    minus_one_0_tail=pd.DataFrame(tail_X_Y_bef_df.iloc[minus_one_sec_mark: len(tail_X_Y_df),:])
    dist_minus1_0_tail=np.linalg.norm(minus_one_0_tail.diff(axis=0), axis=1)#distance per frame
    dist_minus1_0_tail_df = pd.DataFrame(dist_minus1_0_tail)
    dist_minus1_0_tail_df.columns = ["Dist_minus1_0S_tail"]
    dist_minus1_0_tail_df["Dist_minus1_0S_tail"] = dist_minus1_0_tail_df["Dist_minus1_0S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_minus1_0_tail_df = dist_minus1_0_tail_df.fillna(0)  # replace NA with 0
    dist_minus1_0_tail_df[dist_minus1_0_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus1_0_tail_df_float= dist_minus1_0_tail_df.astype('float')
    dist_minus1_0_tail_df_float_inter= dist_minus1_0_tail_df_float.interpolate()
    total_dist_minus1_0_tail =dist_minus1_0_tail_df_float_inter['Dist_minus1_0S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    minus_one_0_body1=pd.DataFrame(body1_X_Y_bef_df.iloc[minus_one_sec_mark: len(tail_X_Y_df),:])
    dist_minus1_0_body1=np.linalg.norm(minus_one_0_body1.diff(axis=0), axis=1)#distance per frame
    dist_minus1_0_body1_df = pd.DataFrame(dist_minus1_0_body1)
    dist_minus1_0_body1_df.columns = ["Dist_minus1_0S_body1"]
    dist_minus1_0_body1_df["Dist_minus1_0S_body1"] = dist_minus1_0_body1_df["Dist_minus1_0S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus1_0_body1_df = dist_minus1_0_body1_df.fillna(0)  # replace NA with 0
    dist_minus1_0_body1_df[dist_minus1_0_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus1_0_body1_df_float= dist_minus1_0_body1_df.astype('float')
    dist_minus1_0_body1_df_float_inter= dist_minus1_0_body1_df_float.interpolate()
    total_dist_minus1_0_body1 =dist_minus1_0_body1_df_float_inter['Dist_minus1_0S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    minus_one_0_body2=pd.DataFrame(body2_X_Y_bef_df.iloc[minus_one_sec_mark: len(tail_X_Y_df),:])
    dist_minus1_0_body2=np.linalg.norm(minus_one_0_body2.diff(axis=0), axis=1)#distance per frame
    dist_minus1_0_body2_df = pd.DataFrame(dist_minus1_0_body2)
    dist_minus1_0_body2_df.columns = ["Dist_minus1_0S_body2"]
    dist_minus1_0_body2_df["Dist_minus1_0S_body2"] = dist_minus1_0_body2_df["Dist_minus1_0S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus1_0_body2_df = dist_minus1_0_body2_df.fillna(0)  # replace NA with 0
    dist_minus1_0_body2_df[dist_minus1_0_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus1_0_body2_df_float= dist_minus1_0_body2_df.astype('float')
    dist_minus1_0_body2_df_float_inter= dist_minus1_0_body2_df_float.interpolate()
    total_dist_minus1_0_body2 =dist_minus1_0_body2_df_float_inter['Dist_minus1_0S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    minus_one_0_body3=pd.DataFrame(body3_X_Y_bef_df.iloc[minus_one_sec_mark: len(tail_X_Y_df),:])
    dist_minus1_0_body3=np.linalg.norm(minus_one_0_body3.diff(axis=0), axis=1)#distance per frame
    dist_minus1_0_body3_df = pd.DataFrame(dist_minus1_0_body3)
    dist_minus1_0_body3_df.columns = ["Dist_minus1_0S_body3"]
    dist_minus1_0_body3_df["Dist_minus1_0S_body3"] = dist_minus1_0_body3_df["Dist_minus1_0S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus1_0_body3_df = dist_minus1_0_body3_df.fillna(0)  # replace NA with 0
    dist_minus1_0_body3_df[dist_minus1_0_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus1_0_body3_df_float= dist_minus1_0_body3_df.astype('float')
    dist_minus1_0_body3_df_float_inter= dist_minus1_0_body3_df_float.interpolate()
    total_dist_minus1_0_body3 =dist_minus1_0_body3_df_float_inter['Dist_minus1_0S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    minus_one_0_head=pd.DataFrame(head_X_Y_bef_df.iloc[minus_one_sec_mark: len(tail_X_Y_df),:])
    dist_minus1_0_head=np.linalg.norm(minus_one_0_head.diff(axis=0), axis=1)#distance per frame
    dist_minus1_0_head_df = pd.DataFrame(dist_minus1_0_head)
    dist_minus1_0_head_df.columns = ["Dist_minus1_0S_head"]
    dist_minus1_0_head_df["Dist_minus1_0S_head"] = dist_minus1_0_head_df["Dist_minus1_0S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus1_0_head_df = dist_minus1_0_head_df.fillna(0)  # replace NA with 0
    dist_minus1_0_head_df[dist_minus1_0_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus1_0_head_df_float= dist_minus1_0_head_df.astype('float')
    dist_minus1_0_head_df_float_inter= dist_minus1_0_head_df_float.interpolate()
    total_dist_minus1_0_head =dist_minus1_0_head_df_float_inter['Dist_minus1_0S_head'].sum()#total distance travelled in 3 sec
    
    #Average
    av_minus1_0=pd.Series((total_dist_minus1_0_tail+total_dist_minus1_0_body1+total_dist_minus1_0_body2+total_dist_minus1_0_body3+total_dist_minus1_0_head)/5)
    
    
    #total distance minus 6-0
    #Subset minus 6 - 0 seconds & calculate distance
    
    #Tail
    minus_six_0_tail=pd.DataFrame(tail_X_Y_bef_df.iloc[0: len(tail_X_Y_df),:])
    dist_minus6_0_tail=np.linalg.norm(minus_six_0_tail.diff(axis=0), axis=1)#distance per frame
    dist_minus6_0_tail_df = pd.DataFrame(dist_minus6_0_tail)
    dist_minus6_0_tail_df.columns = ["Dist_minus6_0S_tail"]
    dist_minus6_0_tail_df["Dist_minus6_0S_tail"] = dist_minus6_0_tail_df["Dist_minus6_0S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_minus6_0_tail_df = dist_minus6_0_tail_df.fillna(0)  # replace NA with 0
    dist_minus6_0_tail_df[dist_minus6_0_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus6_0_tail_df_float= dist_minus6_0_tail_df.astype('float')
    dist_minus6_0_tail_df_float_inter= dist_minus6_0_tail_df_float.interpolate()
    total_dist_minus6_0_tail =dist_minus6_0_tail_df_float_inter['Dist_minus6_0S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    minus_six_0_body1=pd.DataFrame(body1_X_Y_bef_df.iloc[0: len(tail_X_Y_df),:])
    dist_minus6_0_body1=np.linalg.norm(minus_six_0_body1.diff(axis=0), axis=1)#distance per frame
    dist_minus6_0_body1_df = pd.DataFrame(dist_minus6_0_body1)
    dist_minus6_0_body1_df.columns = ["Dist_minus6_0S_body1"]
    dist_minus6_0_body1_df["Dist_minus6_0S_body1"] = dist_minus6_0_body1_df["Dist_minus6_0S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus6_0_body1_df = dist_minus6_0_body1_df.fillna(0)  # replace NA with 0
    dist_minus6_0_body1_df[dist_minus6_0_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus6_0_body1_df_float= dist_minus6_0_body1_df.astype('float')
    dist_minus6_0_body1_df_float_inter= dist_minus6_0_body1_df_float.interpolate()
    total_dist_minus6_0_body1 =dist_minus6_0_body1_df_float_inter['Dist_minus6_0S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    minus_six_0_body2=pd.DataFrame(body2_X_Y_bef_df.iloc[0: len(tail_X_Y_df),:])
    dist_minus6_0_body2=np.linalg.norm(minus_six_0_body2.diff(axis=0), axis=1)#distance per frame
    dist_minus6_0_body2_df = pd.DataFrame(dist_minus6_0_body2)
    dist_minus6_0_body2_df.columns = ["Dist_minus6_0S_body2"]
    dist_minus6_0_body2_df["Dist_minus6_0S_body2"] = dist_minus6_0_body2_df["Dist_minus6_0S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus6_0_body2_df = dist_minus6_0_body2_df.fillna(0)  # replace NA with 0
    dist_minus6_0_body2_df[dist_minus6_0_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus6_0_body2_df_float= dist_minus6_0_body2_df.astype('float')
    dist_minus6_0_body2_df_float_inter= dist_minus6_0_body2_df_float.interpolate()
    total_dist_minus6_0_body2 =dist_minus6_0_body2_df_float_inter['Dist_minus6_0S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    minus_six_0_body3=pd.DataFrame(body3_X_Y_bef_df.iloc[0: len(tail_X_Y_df),:])
    dist_minus6_0_body3=np.linalg.norm(minus_six_0_body3.diff(axis=0), axis=1)#distance per frame
    dist_minus6_0_body3_df = pd.DataFrame(dist_minus6_0_body3)
    dist_minus6_0_body3_df.columns = ["Dist_minus6_0S_body3"]
    dist_minus6_0_body3_df["Dist_minus6_0S_body3"] = dist_minus6_0_body3_df["Dist_minus6_0S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus6_0_body3_df = dist_minus6_0_body3_df.fillna(0)  # replace NA with 0
    dist_minus6_0_body3_df[dist_minus6_0_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus6_0_body3_df_float= dist_minus6_0_body3_df.astype('float')
    dist_minus6_0_body3_df_float_inter= dist_minus6_0_body3_df_float.interpolate()
    total_dist_minus6_0_body3 =dist_minus6_0_body3_df_float_inter['Dist_minus6_0S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    minus_six_0_head=pd.DataFrame(head_X_Y_bef_df.iloc[0: len(tail_X_Y_df),:])
    dist_minus6_0_head=np.linalg.norm(minus_six_0_head.diff(axis=0), axis=1)#distance per frame
    dist_minus6_0_head_df = pd.DataFrame(dist_minus6_0_head)
    dist_minus6_0_head_df.columns = ["Dist_minus6_0S_head"]
    dist_minus6_0_head_df["Dist_minus6_0S_head"] = dist_minus6_0_head_df["Dist_minus6_0S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus6_0_head_df = dist_minus6_0_head_df.fillna(0)  # replace NA with 0
    dist_minus6_0_head_df[dist_minus6_0_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus6_0_head_df_float= dist_minus6_0_head_df.astype('float')
    dist_minus6_0_head_df_float_inter= dist_minus6_0_head_df_float.interpolate()
    total_dist_minus6_0_head =dist_minus6_0_head_df_float_inter['Dist_minus6_0S_head'].sum()#total distance travelled in 3 sec
    
    #Total
    total_minus6_0=pd.Series(total_dist_minus6_0_tail+total_dist_minus6_0_body1+total_dist_minus6_0_body2+total_dist_minus6_0_body3+total_dist_minus6_0_head)
    
    
    #total distance minus 3-0
    #Subset minus 3 - 0 seconds & calculate distance
    minus_three_sec_mark=int(len(tail_X_Y_df)/2)
    
    #Tail
    minus_three_0_tail=pd.DataFrame(tail_X_Y_bef_df.iloc[minus_three_sec_mark:len(tail_X_Y_df),:])
    dist_minus3_0_tail=np.linalg.norm(minus_three_0_tail.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_tail_df = pd.DataFrame(dist_minus3_0_tail)
    dist_minus3_0_tail_df.columns = ["Dist_minus3_0S_tail"]
    dist_minus3_0_tail_df["Dist_minus3_0S_tail"] = dist_minus3_0_tail_df["Dist_minus3_0S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_minus3_0_tail_df = dist_minus3_0_tail_df.fillna(0)  # replace NA with 0
    dist_minus3_0_tail_df[dist_minus3_0_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_tail_df_float= dist_minus3_0_tail_df.astype('float')
    dist_minus3_0_tail_df_float_inter= dist_minus3_0_tail_df_float.interpolate()
    total_dist_minus3_0_tail =dist_minus3_0_tail_df_float_inter['Dist_minus3_0S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    minus_three_0_body1=pd.DataFrame(body1_X_Y_bef_df.iloc[minus_three_sec_mark:len(tail_X_Y_df),:])
    dist_minus3_0_body1=np.linalg.norm(minus_three_0_body1.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_body1_df = pd.DataFrame(dist_minus3_0_body1)
    dist_minus3_0_body1_df.columns = ["Dist_minus3_0S_body1"]
    dist_minus3_0_body1_df["Dist_minus3_0S_body1"] = dist_minus3_0_body1_df["Dist_minus3_0S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_body1_df = dist_minus3_0_body1_df.fillna(0)  # replace NA with 0
    dist_minus3_0_body1_df[dist_minus3_0_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_body1_df_float= dist_minus3_0_body1_df.astype('float')
    dist_minus3_0_body1_df_float_inter= dist_minus3_0_body1_df_float.interpolate()
    total_dist_minus3_0_body1 =dist_minus3_0_body1_df_float_inter['Dist_minus3_0S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    minus_three_0_body2=pd.DataFrame(body2_X_Y_bef_df.iloc[minus_three_sec_mark:len(tail_X_Y_df),:])
    dist_minus3_0_body2=np.linalg.norm(minus_three_0_body2.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_body2_df = pd.DataFrame(dist_minus3_0_body2)
    dist_minus3_0_body2_df.columns = ["Dist_minus3_0S_body2"]
    dist_minus3_0_body2_df["Dist_minus3_0S_body2"] = dist_minus3_0_body2_df["Dist_minus3_0S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_body2_df = dist_minus3_0_body2_df.fillna(0)  # replace NA with 0
    dist_minus3_0_body2_df[dist_minus3_0_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_body2_df_float= dist_minus3_0_body2_df.astype('float')
    dist_minus3_0_body2_df_float_inter= dist_minus3_0_body2_df_float.interpolate()
    total_dist_minus3_0_body2 =dist_minus3_0_body2_df_float_inter['Dist_minus3_0S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    minus_three_0_body3=pd.DataFrame(body3_X_Y_bef_df.iloc[minus_three_sec_mark:len(tail_X_Y_df),:])
    dist_minus3_0_body3=np.linalg.norm(minus_three_0_body3.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_body3_df = pd.DataFrame(dist_minus3_0_body3)
    dist_minus3_0_body3_df.columns = ["Dist_minus3_0S_body3"]
    dist_minus3_0_body3_df["Dist_minus3_0S_body3"] = dist_minus3_0_body3_df["Dist_minus3_0S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_body3_df = dist_minus3_0_body3_df.fillna(0)  # replace NA with 0
    dist_minus3_0_body3_df[dist_minus3_0_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_body3_df_float= dist_minus3_0_body3_df.astype('float')
    dist_minus3_0_body3_df_float_inter= dist_minus3_0_body3_df_float.interpolate()
    total_dist_minus3_0_body3 =dist_minus3_0_body3_df_float_inter['Dist_minus3_0S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    minus_three_0_head=pd.DataFrame(head_X_Y_bef_df.iloc[minus_three_sec_mark:len(tail_X_Y_df),:])
    dist_minus3_0_head=np.linalg.norm(minus_three_0_head.diff(axis=0), axis=1)#distance per frame
    dist_minus3_0_head_df = pd.DataFrame(dist_minus3_0_head)
    dist_minus3_0_head_df.columns = ["Dist_minus3_0S_head"]
    dist_minus3_0_head_df["Dist_minus3_0S_head"] = dist_minus3_0_head_df["Dist_minus3_0S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_minus3_0_head_df = dist_minus3_0_head_df.fillna(0)  # replace NA with 0
    dist_minus3_0_head_df[dist_minus3_0_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_minus3_0_head_df_float= dist_minus3_0_head_df.astype('float')
    dist_minus3_0_head_df_float_inter= dist_minus3_0_head_df_float.interpolate()
    total_dist_minus3_0_head =dist_minus3_0_head_df_float_inter['Dist_minus3_0S_head'].sum()#total distance travelled in 3 sec
    
    #Total
    total_minus3_0=pd.Series(total_dist_minus3_0_tail+total_dist_minus3_0_body1+total_dist_minus3_0_body2+total_dist_minus3_0_body3+total_dist_minus3_0_head)
    
    #total distance 0-6
    #Subset 0 - 6 seconds & calculate distance
    #Tail
    zero_6_tail=pd.DataFrame(tail_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_tail=np.linalg.norm(zero_6_tail.diff(axis=0), axis=1)#distance per frame
    dist_0_6_tail_df = pd.DataFrame(dist_0_6_tail)
    dist_0_6_tail_df.columns = ["Dist_0_6S_tail"]
    dist_0_6_tail_df["Dist_0_6S_tail"] = dist_0_6_tail_df["Dist_0_6S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_0_6_tail_df = dist_0_6_tail_df.fillna(0)  # replace NA with 0
    dist_0_6_tail_df[dist_0_6_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_tail_df_float= dist_0_6_tail_df.astype('float')
    dist_0_6_tail_df_float_inter= dist_0_6_tail_df_float.interpolate()
    total_dist_0_6_tail =dist_0_6_tail_df_float_inter['Dist_0_6S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_6_body1=pd.DataFrame(body1_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_body1=np.linalg.norm(zero_6_body1.diff(axis=0), axis=1)#distance per frame
    dist_0_6_body1_df = pd.DataFrame(dist_0_6_body1)
    dist_0_6_body1_df.columns = ["Dist_0_6S_body1"]
    dist_0_6_body1_df["Dist_0_6S_body1"] = dist_0_6_body1_df["Dist_0_6S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_6_body1_df = dist_0_6_body1_df.fillna(0)  # replace NA with 0
    dist_0_6_body1_df[dist_0_6_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_body1_df_float= dist_0_6_body1_df.astype('float')
    dist_0_6_body1_df_float_inter= dist_0_6_body1_df_float.interpolate()
    total_dist_0_6_body1 =dist_0_6_body1_df_float_inter['Dist_0_6S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_6_body2=pd.DataFrame(body2_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_body2=np.linalg.norm(zero_6_body2.diff(axis=0), axis=1)#distance per frame
    dist_0_6_body2_df = pd.DataFrame(dist_0_6_body2)
    dist_0_6_body2_df.columns = ["Dist_0_6S_body2"]
    dist_0_6_body2_df["Dist_0_6S_body2"] = dist_0_6_body2_df["Dist_0_6S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_6_body2_df = dist_0_6_body2_df.fillna(0)  # replace NA with 0
    dist_0_6_body2_df[dist_0_6_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_body2_df_float= dist_0_6_body2_df.astype('float')
    dist_0_6_body2_df_float_inter= dist_0_6_body2_df_float.interpolate()
    total_dist_0_6_body2 =dist_0_6_body2_df_float_inter['Dist_0_6S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_6_body3=pd.DataFrame(body3_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_body3=np.linalg.norm(zero_6_body3.diff(axis=0), axis=1)#distance per frame
    dist_0_6_body3_df = pd.DataFrame(dist_0_6_body3)
    dist_0_6_body3_df.columns = ["Dist_0_6S_body3"]
    dist_0_6_body3_df["Dist_0_6S_body3"] = dist_0_6_body3_df["Dist_0_6S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_6_body3_df = dist_0_6_body3_df.fillna(0)  # replace NA with 0
    dist_0_6_body3_df[dist_0_6_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_body3_df_float= dist_0_6_body3_df.astype('float')
    dist_0_6_body3_df_float_inter= dist_0_6_body3_df_float.interpolate()
    total_dist_0_6_body3 =dist_0_6_body3_df_float_inter['Dist_0_6S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_6_head=pd.DataFrame(head_X_Y_df.iloc[0:len(tail_X_Y_df),:])
    dist_0_6_head=np.linalg.norm(zero_6_head.diff(axis=0), axis=1)#distance per frame
    dist_0_6_head_df = pd.DataFrame(dist_0_6_head)
    dist_0_6_head_df.columns = ["Dist_0_6S_head"]
    dist_0_6_head_df["Dist_0_6S_head"] = dist_0_6_head_df["Dist_0_6S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_6_head_df = dist_0_6_head_df.fillna(0)  # replace NA with 0
    dist_0_6_head_df[dist_0_6_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_6_head_df_float= dist_0_6_head_df.astype('float')
    dist_0_6_head_df_float_inter= dist_0_6_head_df_float.interpolate()
    total_dist_0_6_head =dist_0_6_head_df_float_inter['Dist_0_6S_head'].sum()#total distance travelled in 3 sec
    
    #Total
    total_0_6=pd.Series(total_dist_0_6_tail+total_dist_0_6_body1+total_dist_0_6_body2+total_dist_0_6_body3+total_dist_0_6_head)
    #total distance 0-3
    #Subset 0 - 6 seconds & calculate distance
    three_sec_mark= (one_sec_mark)*3
    #Tail
    zero_3_tail=pd.DataFrame(tail_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_tail=np.linalg.norm(zero_3_tail.diff(axis=0), axis=1)#distance per frame
    dist_0_3_tail_df = pd.DataFrame(dist_0_3_tail)
    dist_0_3_tail_df.columns = ["Dist_0_3S_tail"]
    dist_0_3_tail_df["Dist_0_3S_tail"] = dist_0_3_tail_df["Dist_0_3S_tail"].replace(1, 0)#When disatnce = 0, formula pritns 1minus> replace 1 with 0
    dist_0_3_tail_df = dist_0_3_tail_df.fillna(0)  # replace NA with 0
    dist_0_3_tail_df[dist_0_3_tail_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_tail_df_float= dist_0_3_tail_df.astype('float')
    dist_0_3_tail_df_float_inter= dist_0_3_tail_df_float.interpolate()
    total_dist_0_3_tail =dist_0_3_tail_df_float_inter['Dist_0_3S_tail'].sum()#total distance travelled in 3 sec
    
    #Body1
    zero_3_body1=pd.DataFrame(body1_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_body1=np.linalg.norm(zero_3_body1.diff(axis=0), axis=1)#distance per frame
    dist_0_3_body1_df = pd.DataFrame(dist_0_3_body1)
    dist_0_3_body1_df.columns = ["Dist_0_3S_body1"]
    dist_0_3_body1_df["Dist_0_3S_body1"] = dist_0_3_body1_df["Dist_0_3S_body1"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_3_body1_df = dist_0_3_body1_df.fillna(0)  # replace NA with 0
    dist_0_3_body1_df[dist_0_3_body1_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_body1_df_float= dist_0_3_body1_df.astype('float')
    dist_0_3_body1_df_float_inter= dist_0_3_body1_df_float.interpolate()
    total_dist_0_3_body1 =dist_0_3_body1_df_float_inter['Dist_0_3S_body1'].sum()#total distance travelled in 3 sec
    
    #Body2
    zero_3_body2=pd.DataFrame(body2_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_body2=np.linalg.norm(zero_3_body2.diff(axis=0), axis=1)#distance per frame
    dist_0_3_body2_df = pd.DataFrame(dist_0_3_body2)
    dist_0_3_body2_df.columns = ["Dist_0_3S_body2"]
    dist_0_3_body2_df["Dist_0_3S_body2"] = dist_0_3_body2_df["Dist_0_3S_body2"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_3_body2_df = dist_0_3_body2_df.fillna(0)  # replace NA with 0
    dist_0_3_body2_df[dist_0_3_body2_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_body2_df_float= dist_0_3_body2_df.astype('float')
    dist_0_3_body2_df_float_inter= dist_0_3_body2_df_float.interpolate()
    total_dist_0_3_body2 =dist_0_3_body2_df_float_inter['Dist_0_3S_body2'].sum()#total distance travelled in 3 sec
    
    #Body3
    zero_3_body3=pd.DataFrame(body3_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_body3=np.linalg.norm(zero_3_body3.diff(axis=0), axis=1)#distance per frame
    dist_0_3_body3_df = pd.DataFrame(dist_0_3_body3)
    dist_0_3_body3_df.columns = ["Dist_0_3S_body3"]
    dist_0_3_body3_df["Dist_0_3S_body3"] = dist_0_3_body3_df["Dist_0_3S_body3"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_3_body3_df = dist_0_3_body3_df.fillna(0)  # replace NA with 0
    dist_0_3_body3_df[dist_0_3_body3_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_body3_df_float= dist_0_3_body3_df.astype('float')
    dist_0_3_body3_df_float_inter= dist_0_3_body3_df_float.interpolate()
    total_dist_0_3_body3 =dist_0_3_body3_df_float_inter['Dist_0_3S_body3'].sum()#total distance travelled in 3 sec
    
    #Head
    zero_3_head=pd.DataFrame(head_X_Y_df.iloc[0:three_sec_mark,:])
    dist_0_3_head=np.linalg.norm(zero_3_head.diff(axis=0), axis=1)#distance per frame
    dist_0_3_head_df = pd.DataFrame(dist_0_3_head)
    dist_0_3_head_df.columns = ["Dist_0_3S_head"]
    dist_0_3_head_df["Dist_0_3S_head"] = dist_0_3_head_df["Dist_0_3S_head"].replace(1, 0)#When distance = 0, formula prints 1minus> replace 1 with 0
    dist_0_3_head_df = dist_0_3_head_df.fillna(0)  # replace NA with 0
    dist_0_3_head_df[dist_0_3_head_df > 88.4402052] = 'NaN'#replace 2SD with NA
    dist_0_3_head_df_float= dist_0_3_head_df.astype('float')
    dist_0_3_head_df_float_inter= dist_0_3_head_df_float.interpolate()
    total_dist_0_3_head =dist_0_3_head_df_float_inter['Dist_0_3S_head'].sum()#total distance travelled in 3 sec
    
    #Total
    total_0_3=pd.Series(total_dist_0_3_tail+total_dist_0_3_body1+total_dist_0_3_body2+total_dist_0_3_body3+total_dist_0_3_head)
    
    #Write to excel
    # av_0_1_data={"Average_Distance_0-1S":av_0_1.tolist()}
    # av_0_1_data_df=pd.DataFrame(av_0_1_data)
    # av_0_1_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=4 )
    
    # av_0_2_data={"Average_Distance_1-2S":av_1_2.tolist()}
    # av_0_2_data_df=pd.DataFrame(av_0_2_data)
    # av_0_2_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=5 )
    
    # av_0_3_data={"Average_Distance_2-3S":av_2_3.tolist()}
    # av_0_3_data_df=pd.DataFrame(av_0_3_data)
    # av_0_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=6 )
    
    # av_0_4_data={"Average_Distance_3-4S":av_3_4.tolist()}
    # av_0_4_data_df=pd.DataFrame(av_0_4_data)
    # av_0_4_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=7 )
    
    # av_0_5_data={"Average_Distance_4-5S":av_4_5.tolist()}
    # av_0_5_data_df=pd.DataFrame(av_0_5_data)
    # av_0_5_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=8 )
    
    # av_0_6_data={"Average_Distance_5-6S":av_0_6.tolist()}
    # av_0_6_data_df=pd.DataFrame(av_0_6_data)
    # av_0_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=9 )
    
    # av_0_3_data={"Average_Distance_0-3S":av_0_3.tolist()}
    # av_0_3_data_df=pd.DataFrame(av_0_3_data)
    # av_0_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=10 )
    
    # av_3_6_data={"Average_Distance_3-6S":av_3_6.tolist()}
    # av_3_6_data_df=pd.DataFrame(av_3_6_data)
    # av_3_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol= 11)
    
    # av_0_6_data={"Average_Distance_0-6S":av_0_6.tolist()}
    # av_0_6_data_df=pd.DataFrame(av_0_6_data)
    # av_0_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=12 )
    
    # av_minus3_0_data={"Average_Distance_minus3-0S":av_minus3_0.tolist()}
    # av_minus3_0_data_df=pd.DataFrame(av_minus3_0_data)
    # av_minus3_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=13)
    
    # av_minus3_minus2_data={"Average_Distance_minus3-minus2S":av_minus3_minus2.tolist()}
    # av_minus3_minus2_data_df=pd.DataFrame(av_minus3_minus2_data)
    # av_minus3_minus2_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=14)
    
    # av_minus2_minus1_data={"Average_Distance_minus2-minus1S":av_minus2_minus1.tolist()}
    # av_minus2_minus1_data_df=pd.DataFrame(av_minus2_minus1_data)
    # av_minus2_minus1_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=15)
    
    # av_minus1_0_data={"Average_Distance_minus1-0S":av_minus1_0.tolist()}
    # av_minus1_0_data_df=pd.DataFrame(av_minus1_0_data)
    # av_minus1_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=16)
    
    # total_minus6_0_data={"Total_Distance_minus6-0S":total_minus6_0.tolist()}
    # total_minus6_0_data_df=pd.DataFrame(total_minus6_0_data)
    # total_minus6_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=17)
    
    # total_minus3_0_data={"Total_Distance_minus3-0S":total_minus3_0.tolist()}
    # total_minus3_0_data_df=pd.DataFrame(total_minus3_0_data)
    # total_minus3_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=18)
    
    # total_0_6_data={"Total_Distance_0-6S":total_0_6.tolist()}
    # total_0_6_data_df=pd.DataFrame(total_0_6_data)
    # total_0_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=19)
    
    # total_0_3_data={"Total_Distance_0-3S":total_0_3.tolist()}
    # total_0_3_data_df=pd.DataFrame(total_0_3_data)
    # total_0_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=20)
    
    
    
    
    #Print dataframe to Raw_Excel
    #12 Seconds
    frames_dist_per_frame= [dist_0_3_tail_df_float_inter.squeeze(),dist_0_3_body1_df_float_inter.squeeze(),dist_0_3_body2_df_float_inter.squeeze(),
             dist_0_3_body3_df_float_inter.squeeze(),dist_0_3_head_df_float_inter.squeeze(),
             dist_3_6_tail_df_float_inter.squeeze(), dist_3_6_body1_df_float_inter.squeeze(), dist_3_6_body2_df_float_inter.squeeze(),
             dist_3_6_body3_df_float_inter.squeeze(), dist_3_6_head_df_float_inter.squeeze()]
    df_dist_per_frame= (pd.DataFrame(frames_dist_per_frame)).T
    # df_dist_per_frame.to_excel(writer_raw,index=False,sheet_name='Dist_03_36_mm',startrow= 3 )
    
    
    
    ##################
    #####Velocity#####
    ##################
    
    #distance per frame/ time
    
    vel_3_sec=(pd.DataFrame(average_dist_list))/3
    vel_3_sec_v = (vel_3_sec.sum()/30)
    vel_3_sec_v=float(vel_3_sec_v)
    vel_3_sec.columns= ["Av_vel"]
    SD_vel_3sec_seg= statistics.stdev(vel_3_sec["Av_vel"].tolist())
    
    vel_per_frame= df_dist_per_frame/(1/frame_per_sec)
    # vel_per_frame.to_excel(writer_raw,index=False,sheet_name='Vel_03_36_mm_per_s')
    
    
    vel_3_sec_data= {"Average_Velocity_3sec_segments":[vel_3_sec_v]}
    vel_3_sec_data_df= pd.DataFrame(vel_3_sec_data)
    # vel_3_sec_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=21)
    
    
    vel_3_sec_data_SD= {"Average_Velocity_SD_3sec_segments":[SD_vel_3sec_seg]}
    vel_3_sec_data_df_SD= pd.DataFrame(vel_3_sec_data_SD)
    # vel_3_sec_data_df_SD.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=22)
    
    
    
    #Avergae Velocity per second
    #0_1 S
    av_vel_0_1= pd.Series((total_dist_0_1_tail/1)+(total_dist_0_1_body1/1)+(total_dist_0_1_body2/1)+(total_dist_0_1_body3/1)+(total_dist_0_1_head/1))/5
    #1_2 S
    av_vel_1_2= pd.Series((total_dist_1_2_tail/1)+(total_dist_1_2_body1/1)+(total_dist_1_2_body2/1)+(total_dist_1_2_body3/1)+(total_dist_1_2_head/1))/5
    #2_3 S
    av_vel_2_3= pd.Series((total_dist_2_3_tail/1)+(total_dist_2_3_body1/1)+(total_dist_2_3_body2/1)+(total_dist_2_3_body3/1)+(total_dist_2_3_head/1))/5
    #3_4 S
    av_vel_3_4= pd.Series((total_dist_3_4_tail/1)+(total_dist_3_4_body1/1)+(total_dist_3_4_body2/1)+(total_dist_3_4_body3/1)+(total_dist_3_4_head/1))/5
    #4_5 S
    av_vel_4_5= pd.Series((total_dist_4_5_tail/1)+(total_dist_4_5_body1/1)+(total_dist_4_5_body2/1)+(total_dist_4_5_body3/1)+(total_dist_4_5_head/1))/5
    #5_6 S
    av_vel_5_6=pd.Series ((total_dist_5_6_tail/1)+(total_dist_5_6_body1/1)+(total_dist_5_6_body2/1)+(total_dist_5_6_body3/1)+(total_dist_5_6_head/1))/5
    #0_3 S
    av_vel_0_3= pd.Series((total_dist_0_3_tail/3)+(total_dist_0_3_body1/3)+(total_dist_0_3_body2/3)+(total_dist_0_3_body3/3)+(total_dist_0_3_head/3))/5
    #3_6 S
    av_vel_3_6= pd.Series((total_dist_3_6_tail/3)+(total_dist_3_6_body1/3)+(total_dist_3_6_body2/3)+(total_dist_3_6_body3/3)+(total_dist_3_6_head/3))/5
    #0_6 S
    av_vel_0_6= pd.Series((total_dist_0_6_tail/6)+(total_dist_0_6_body1/6)+(total_dist_0_6_body2/6)+(total_dist_0_6_body3/6)+(total_dist_0_6_head/6))/5
    #average 3 second segment
    av_vel_3sec= pd.Series(total_average_dist/3)
    
    #minus3_0 S
    av_vel_minus3_0= pd.Series((total_dist_minus3_0_tail/3)+(total_dist_minus3_0_body1/3)+(total_dist_minus3_0_body2/3)+(total_dist_minus3_0_body3/3)+(total_dist_minus3_0_head/3))/5
    #minus3_minus2 S
    av_vel_minus3_minus2= pd.Series((total_dist_minus3_minus2_tail/1)+(total_dist_minus3_minus2_body1/1)+(total_dist_minus3_minus2_body2/1)+(total_dist_minus3_minus2_body3/1)+(total_dist_minus3_minus2_head/1))/5
    #minus2_minus1S
    av_vel_minus2_minus1= pd.Series((total_dist_minus2_minus1_tail/1)+(total_dist_minus2_minus1_body1/1)+(total_dist_minus2_minus1_body2/1)+(total_dist_minus2_minus1_body3/1)+(total_dist_minus2_minus1_head/1))/5
    #minus1_0S
    av_vel_minus1_0= pd.Series((total_dist_minus1_0_tail/1)+(total_dist_minus1_0_body1/1)+(total_dist_minus1_0_body2/1)+(total_dist_minus1_0_body3/1)+(total_dist_minus1_0_head/1))/5
    
    #Write to excel
    # av_vel_0_1_data={"Average_Velocity_per_sec_0-1S":av_vel_0_1.tolist()}
    # av_vel_0_1_data_df=pd.DataFrame(av_vel_0_1_data)
    # av_vel_0_1_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=23 )
    
    # av_vel_1_2_data={"Average_Velocity_per_sec_1-2S":av_vel_1_2.tolist()}
    # av_vel_1_2_data_df=pd.DataFrame(av_vel_1_2_data)
    # av_vel_1_2_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=24 )
    
    # av_vel_2_3_data={"Average_Velocity_per_sec_2-3S":av_vel_2_3.tolist()}
    # av_vel_2_3_data_df=pd.DataFrame(av_vel_2_3_data)
    # av_vel_2_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=25 )
    
    # av_vel_3_4_data={"Average_Velocity_per_sec_3-4S":av_vel_3_4.tolist()}
    # av_vel_3_4_data_df=pd.DataFrame(av_vel_3_4_data)
    # av_vel_3_4_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=26 )
    
    # av_vel_4_5_data={"Average_Velocity_per_sec_4-5S":av_vel_4_5.tolist()}
    # av_vel_4_5_data_df=pd.DataFrame(av_vel_4_5_data)
    # av_vel_4_5_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=27 )
    
    # av_vel_5_6_data={"Average_Velocity_per_sec_5-6S":av_vel_5_6.tolist()}
    # av_vel_5_6_data_df=pd.DataFrame(av_vel_5_6_data)
    # av_vel_5_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=28 )
    
    # av_vel_0_3_data={"Average_Velocity_per_sec_0-3S":av_vel_0_3.tolist()}
    # av_vel_0_3_data_df=pd.DataFrame(av_vel_0_3_data)
    # av_vel_0_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=29 )
    
    # av_vel_3_6_data={"Average_Velocity_per_sec_3-6S":av_vel_3_6.tolist()}
    # av_vel_3_6_data_df=pd.DataFrame(av_vel_3_6_data)
    # av_vel_3_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=30 )
    
    # av_vel_0_6_data={"Average_Velocity_per_sec_0-6S":av_vel_0_6.tolist()}
    # av_vel_0_6_data_df=pd.DataFrame(av_vel_0_6_data)
    # av_vel_0_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=31)
    
    # av_vel_3sec_data={"Average_Velocity_per_sec_3sec_Segments":av_vel_3sec.tolist()}
    # av_vel_3sec_data_df=pd.DataFrame(av_vel_3sec_data)
    # av_vel_3sec_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=32)
    
    # av_vel_minus3_0_data={"Average_Velocity_per_sec_minus3-0S":av_vel_minus3_0.tolist()}
    # av_vel_minus3_0_data_df=pd.DataFrame(av_vel_minus3_0_data)
    # av_vel_minus3_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=33)
    
    # av_vel_minus3_minus2_data={"Average_Velocity_per_sec_minus3-minus2S":av_vel_minus3_minus2.tolist()}
    # av_vel_minus3_minus2_data_df=pd.DataFrame(av_vel_minus3_minus2_data)
    # av_vel_minus3_minus2_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=34 )
    
    # av_vel_minus2_minus1_data={"Average_Velocity_per_sec_minus2-minus1S":av_vel_minus2_minus1.tolist()}
    # av_vel_minus2_minus1_data_df=pd.DataFrame(av_vel_minus2_minus1_data)
    # av_vel_minus2_minus1_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=35)
    
    # av_vel_minus1_0_data={"Average_Velocity_per_sec_minus1-0S":av_vel_minus1_0.tolist()}
    # av_vel_minus1_0_data_df=pd.DataFrame(av_vel_minus1_0_data)
    # av_vel_minus1_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=36)
    
    
    
    
    ##################
    ###ACCELERATION###
    ##################
    
    ##first 3 second##
    
    ac_t_1=(df_float_interpolate_t_1.diff())/(1/frame_per_sec)
    ac_b1_1=(df_float_interpolate_b1_1.diff())/(1/frame_per_sec)
    ac_b2_1=(df_float_interpolate_b2_1.diff())/(1/frame_per_sec)
    ac_b3_1=(df_float_interpolate_b3_1.diff())/(1/frame_per_sec)
    ac_h_1=(df_float_interpolate_h_1.diff())/(1/frame_per_sec)
    
    #Average ac/s
    
    av_ac_t_1= (ac_b1_1.sum())/3
    av_ac_b1_1=(ac_b1_1.sum())/3
    av_ac_b2_1=(ac_b2_1.sum())/3
    av_ac_b3_1= (ac_b3_1.sum())/3
    av_ac_h_1= (ac_h_1.sum())/3
    
    ##Second 3 second##
    
    ac_t_2=(df_float_interpolate_t_2.diff())/(1/frame_per_sec)
    ac_b1_2=(df_float_interpolate_b1_2.diff())/(1/frame_per_sec)
    ac_b2_2=(df_float_interpolate_b2_2.diff())/(1/frame_per_sec)
    ac_b3_2=(df_float_interpolate_b3_2.diff())/(1/frame_per_sec)
    ac_h_2=(df_float_interpolate_h_2.diff())/(1/frame_per_sec)
    #Average ac/s
    
    av_ac_t_2= (ac_b1_2.sum())/3
    av_ac_b1_2=(ac_b1_2.sum())/3
    av_ac_b2_2=(ac_b2_2.sum())/3
    av_ac_b3_2= (ac_b3_2.sum())/3
    av_ac_h_2= (ac_h_2.sum())/3
    
    
    ##Third 3 second##
    
    ac_t_3=(df_float_interpolate_t_3.diff())/(1/frame_per_sec)
    ac_b1_3=(df_float_interpolate_b1_3.diff())/(1/frame_per_sec)
    ac_b2_3=(df_float_interpolate_b2_3.diff())/(1/frame_per_sec)
    ac_b3_3=(df_float_interpolate_b3_3.diff())/(1/frame_per_sec)
    ac_h_3=(df_float_interpolate_h_3.diff())/(1/frame_per_sec)
    #Average ac/s
    
    av_ac_t_3= (ac_b1_3.sum())/3
    av_ac_b1_3=(ac_b1_3.sum())/3
    av_ac_b2_3=(ac_b2_3.sum())/3
    av_ac_b3_3= (ac_b3_3.sum())/3
    av_ac_h_3= (ac_h_3.sum())/3
    
    ##Fourth 3 second##
    
    ac_t_4=(df_float_interpolate_t_4.diff())/(1/frame_per_sec)
    ac_b1_4=(df_float_interpolate_b1_4.diff())/(1/frame_per_sec)
    ac_b2_4=(df_float_interpolate_b2_4.diff())/(1/frame_per_sec)
    ac_b3_4=(df_float_interpolate_b3_4.diff())/(1/frame_per_sec)
    ac_h_4=(df_float_interpolate_h_4.diff())/(1/frame_per_sec)
    #Average ac/s
    
    av_ac_t_4= (ac_b1_4.sum())/3
    av_ac_b1_4=(ac_b1_4.sum())/3
    av_ac_b2_4=(ac_b2_4.sum())/3
    av_ac_b3_4= (ac_b3_4.sum())/3
    av_ac_h_4= (ac_h_4.sum())/3
    
    
    ##Fifth 3 second##
    
    ac_t_5=(df_float_interpolate_t_5.diff())/(1/frame_per_sec)
    ac_b1_5=(df_float_interpolate_b1_5.diff())/(1/frame_per_sec)
    ac_b2_5=(df_float_interpolate_b2_5.diff())/(1/frame_per_sec)
    ac_b3_5=(df_float_interpolate_b3_5.diff())/(1/frame_per_sec)
    ac_h_5=(df_float_interpolate_h_5.diff())/(1/frame_per_sec)
    
    #Average ac/s
    
    av_ac_t_5= (ac_b1_5.sum())/3
    av_ac_b1_5=(ac_b1_5.sum())/3
    av_ac_b2_5=(ac_b2_5.sum())/3
    av_ac_b3_5= (ac_b3_5.sum())/3
    av_ac_h_5= (ac_h_5.sum())/3
    
    
    ##Sixth 3 second##
    
    ac_t_6=(df_float_interpolate_t_6.diff())/(1/frame_per_sec)
    ac_b1_6=(df_float_interpolate_b1_6.diff())/(1/frame_per_sec)
    ac_b2_6=(df_float_interpolate_b2_6.diff())/(1/frame_per_sec)
    ac_b3_6=(df_float_interpolate_b3_6.diff())/(1/frame_per_sec)
    ac_h_6=(df_float_interpolate_h_6.diff())/(1/frame_per_sec)
    
    #Average ac/s
    
    av_ac_t_6= (ac_b1_6.sum())/3
    av_ac_b1_6=(ac_b1_6.sum())/3
    av_ac_b2_6=(ac_b2_6.sum())/3
    av_ac_b3_6= (ac_b3_6.sum())/3
    av_ac_h_6= (ac_h_6.sum())/3
    
    #Average acceleration per second for all
    
    total_av_ac=[(av_ac_t_1),(av_ac_b1_1),(av_ac_b2_1),(av_ac_b3_1),(av_ac_h_1
                  ),(av_ac_t_2),(av_ac_b1_2),(av_ac_b2_2),(av_ac_b3_2),(av_ac_h_2),
                  (av_ac_t_3),(av_ac_b1_3),(av_ac_b2_3),(av_ac_b3_3),(av_ac_h_3),
                  (av_ac_t_4),(av_ac_b1_4),(av_ac_b2_4),(av_ac_b3_4),(av_ac_h_4
                  ),(av_ac_t_5),(av_ac_b1_5),(av_ac_b2_5),(av_ac_b3_5),(av_ac_h_5
                  ),(av_ac_t_6),(av_ac_b1_6),(av_ac_b2_6),(av_ac_b3_6),(av_ac_h_6)]
    total_av_ac_df=pd.DataFrame(total_av_ac)
    total_av_ac_df.columns=["Av_AC"]
    
    
    total_av_ac_mean=((av_ac_t_1)+(av_ac_b1_1)+(av_ac_b2_1)+(av_ac_b3_1)+(av_ac_h_1
                  )+(av_ac_t_2)+(av_ac_b1_2)+(av_ac_b2_2)+(av_ac_b3_2)+(av_ac_h_2)+
                  (av_ac_t_3)+(av_ac_b1_3)+(av_ac_b2_3)+(av_ac_b3_3)+(av_ac_h_3)+
                  (av_ac_t_4)+(av_ac_b1_4)+(av_ac_b2_4)+(av_ac_b3_4)+(av_ac_h_4
                  )+(av_ac_t_5)+(av_ac_b1_5)+(av_ac_b2_5)+(av_ac_b3_5)+(av_ac_h_5
                  )+(av_ac_t_6)+(av_ac_b1_6)+(av_ac_b2_6)+(av_ac_b3_6)+(av_ac_h_6))/30
    total_av_ac_mean=total_av_ac_mean
    total_av_ac_mean_SD=float(total_av_ac_mean)
    
    total_av_ac_SD= statistics.stdev(total_av_ac_df["Av_AC"].tolist())
    
    Average_Acceleration_3sec_segments_sd_data= {'Average_Acceleration_3sec_segments':[total_av_ac_mean]}
    Average_Acceleration_3sec_segments_sd_data_df=pd.DataFrame(Average_Acceleration_3sec_segments_sd_data)
    # Average_Acceleration_3sec_segments_sd_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=37)
    
    Average_Acceleration_SD_3sec_segments_data= {'Average_Acceleration_SD_3sec_segments':[total_av_ac_SD]}
    Average_Acceleration_SD_3sec_segments_data_df=pd.DataFrame(Average_Acceleration_SD_3sec_segments_data)
    # Average_Acceleration_SD_3sec_segments_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=38)
    
    #0-1
    ac_0_1_tail=( dist_0_1_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_0_1_body1 =( dist_0_1_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_0_1_body2=( dist_0_1_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_0_1_body3=( dist_0_1_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_0_1_head=( dist_0_1_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #1_2
    ac_1_2_tail=( dist_1_2_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_1_2_body1 =( dist_1_2_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_1_2_body2=( dist_1_2_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_1_2_body3=( dist_1_2_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_1_2_head=( dist_1_2_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #2_3
    ac_2_3_tail=( dist_2_3_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_2_3_body1 =( dist_2_3_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_2_3_body2=( dist_2_3_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_2_3_body3=( dist_2_3_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_2_3_head=( dist_2_3_head_df_float_inter.diff())/(1/frame_per_sec)
    #3_4
    ac_3_4_tail=( dist_3_4_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_3_4_body1 =( dist_3_4_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_3_4_body2=( dist_3_4_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_3_4_body3=( dist_3_4_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_3_4_head=( dist_3_4_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #4_5
    ac_4_5_tail=( dist_4_5_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_4_5_body1 =( dist_4_5_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_4_5_body2=( dist_4_5_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_4_5_body3=( dist_4_5_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_4_5_head=( dist_4_5_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #5_6
    ac_5_6_tail=( dist_5_6_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_5_6_body1 =( dist_5_6_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_5_6_body2=( dist_5_6_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_5_6_body3=( dist_5_6_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_5_6_head=( dist_5_6_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #0-3
    ac_0_3_tail=( dist_0_3_tail_df_float_inter.diff())/(3/frame_per_sec)
    ac_0_3_body1 =( dist_0_3_body1_df_float_inter.diff())/(3/frame_per_sec)
    ac_0_3_body2=( dist_0_3_body2_df_float_inter.diff())/(3/frame_per_sec)
    ac_0_3_body3=( dist_0_3_body3_df_float_inter.diff())/(3/frame_per_sec)
    ac_0_3_head=( dist_0_3_head_df_float_inter.diff())/(3/frame_per_sec)
    
    #3-6
    ac_3_6_tail=( dist_3_6_tail_df_float_inter.diff())/(3/frame_per_sec)
    ac_3_6_body1 =( dist_3_6_body1_df_float_inter.diff())/(3/frame_per_sec)
    ac_3_6_body2=( dist_3_6_body2_df_float_inter.diff())/(3/frame_per_sec)
    ac_3_6_body3=( dist_3_6_body3_df_float_inter.diff())/(3/frame_per_sec)
    ac_3_6_head=( dist_3_6_head_df_float_inter.diff())/(3/frame_per_sec)
    
    #0_6
    ac_0_6_tail=( dist_0_6_tail_df_float_inter.diff())/(6/frame_per_sec)
    ac_0_6_body1 =( dist_0_6_body1_df_float_inter.diff())/(6/frame_per_sec)
    ac_0_6_body2=( dist_0_6_body2_df_float_inter.diff())/(6/frame_per_sec)
    ac_0_6_body3=( dist_0_6_body3_df_float_inter.diff())/(6/frame_per_sec)
    ac_0_6_head=( dist_0_6_head_df_float_inter.diff())/(6/frame_per_sec)
    
    #minus3-0
    ac_minus3_0_tail=( dist_minus3_0_tail_df_float_inter.diff())/(3/frame_per_sec)
    ac_minus3_0_body1 =( dist_minus3_0_body1_df_float_inter.diff())/(3/frame_per_sec)
    ac_minus3_0_body2=( dist_minus3_0_body2_df_float_inter.diff())/(3/frame_per_sec)
    ac_minus3_0_body3=( dist_minus3_0_body3_df_float_inter.diff())/(3/frame_per_sec)
    ac_minus3_0_head=( dist_minus3_0_head_df_float_inter.diff())/(3/frame_per_sec)
    
    #minus3_minus2
    ac_minus3_minus2_tail=( dist_minus3_minus2_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus3_minus2_body1 =( dist_minus3_minus2_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus3_minus2_body2=( dist_minus3_minus2_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus3_minus2_body3=( dist_minus3_minus2_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus3_minus2_head=( dist_minus3_minus2_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #minus2_minus1
    ac_minus2_minus1_tail=( dist_minus2_minus1_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus2_minus1_body1 =( dist_minus2_minus1_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus2_minus1_body2=( dist_minus2_minus1_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus2_minus1_body3=( dist_minus2_minus1_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus2_minus1_head=( dist_minus2_minus1_head_df_float_inter.diff())/(1/frame_per_sec)
    
    #minus1_0
    ac_minus1_0_tail=( dist_minus1_0_tail_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus1_0_body1 =( dist_minus1_0_body1_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus1_0_body2=( dist_minus1_0_body2_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus1_0_body3=( dist_minus1_0_body3_df_float_inter.diff())/(1/frame_per_sec)
    ac_minus1_0_head=( dist_minus1_0_head_df_float_inter.diff())/(1/frame_per_sec)
    
    
    
    #Average Acceleration
    #0_1
    av_ac_0_1=pd.Series(float(ac_0_1_tail.sum()/1)+float(ac_0_1_body1.sum()/1)+float(ac_0_1_body2.sum()/1)+float(ac_0_1_body3.sum()/1)+float(ac_0_1_head.sum()/1))/5
    #1_2
    av_ac_1_2=pd.Series(float(ac_1_2_tail.sum()/1)+float(ac_1_2_body1.sum()/1)+float(ac_1_2_body2.sum()/1)+float(ac_1_2_body3.sum()/1)+float(ac_1_2_head.sum()/1))/5
    #2_3
    av_ac_2_3=pd.Series(float(ac_2_3_tail.sum()/1)+float(ac_2_3_body1.sum()/1)+float(ac_2_3_body2.sum()/1)+float(ac_2_3_body3.sum()/1)+float(ac_2_3_head.sum()/1))/5
    #3_4
    av_ac_3_4=pd.Series(float(ac_3_4_tail.sum()/1)+float(ac_3_4_body1.sum()/1)+float(ac_3_4_body2.sum()/1)+float(ac_3_4_body3.sum()/1)+float(ac_3_4_head.sum()/1))/5
    #4_5
    av_ac_4_5=pd.Series(float(ac_4_5_tail.sum()/1)+float(ac_4_5_body1.sum()/1)+float(ac_4_5_body2.sum()/1)+float(ac_4_5_body3.sum()/1)+float(ac_4_5_head.sum()/1))/5
    #5_6
    av_ac_5_6=pd.Series(float(ac_5_6_tail.sum()/1)+float(ac_5_6_body1.sum()/1)+float(ac_5_6_body2.sum()/1)+float(ac_5_6_body3.sum()/1)+float(ac_5_6_head.sum()/1))/5
    #0_3
    av_ac_0_3=pd.Series(float(ac_0_3_tail.sum()/3)+float(ac_0_3_body1.sum()/3)+float(ac_0_3_body2.sum()/3)+float(ac_0_3_body3.sum()/3)+float(ac_0_3_head.sum()/3))/5
    #3_6
    av_ac_3_6=pd.Series(float(ac_3_6_tail.sum()/3)+float(ac_3_6_body1.sum()/3)+float(ac_3_6_body2.sum()/3)+float(ac_3_6_body3.sum()/3)+float(ac_3_6_head.sum()/3))/5
    #0_6
    av_ac_0_6=pd.Series(float(ac_0_6_tail.sum()/6)+float(ac_0_6_body1.sum()/6)+float(ac_0_6_body2.sum()/6)+float(ac_0_6_body3.sum()/6)+float(ac_0_6_head.sum()/6))/5
    
    #minus3-0
    av_ac_minus3_0=pd.Series(float(ac_minus3_0_tail.sum()/3)+float(ac_minus3_0_body1.sum()/3)+float(ac_minus3_0_body2.sum()/3)+float(ac_minus3_0_body3.sum()/3)+float(ac_minus3_0_head.sum()/3))/5
    #minus3_minus2
    av_ac_minus3_minus2=pd.Series(float(ac_minus3_minus2_tail.sum()/1)+float(ac_minus3_minus2_body1.sum()/1)+float(ac_minus3_minus2_body2.sum()/1)+float(ac_minus3_minus2_body3.sum()/1)+float(ac_minus3_minus2_head.sum()/1))/5
    #minus2_minus1
    av_ac_minus2_minus1=pd.Series(float(ac_minus2_minus1_tail.sum()/1)+float(ac_minus2_minus1_body1.sum()/1)+float(ac_minus2_minus1_body2.sum()/1)+float(ac_minus2_minus1_body3.sum()/1)+float(ac_minus2_minus1_head.sum()/1))/5
    #minus1_0
    av_ac_minus1_0=pd.Series(float(ac_minus1_0_tail.sum()/1)+float(ac_minus1_0_body1.sum()/1)+float(ac_minus1_0_body2.sum()/1)+float(ac_minus1_0_body3.sum()/1)+float(ac_minus1_0_head.sum()/1))/5
    
    print(av_ac_0_1)
    print(folder)
    break

    # #Write to excel
    # av_ac_0_1_data={"Average_Acceleration_per_sec_0-1S":av_ac_0_1.tolist()}
    # av_ac_0_1_data_df=pd.DataFrame(av_ac_0_1_data)
    # av_ac_0_1_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=39 )
    
    # av_ac_1_2_data={"Average_Acceleration_per_sec_1-2S":av_ac_1_2.tolist()}
    # av_ac_1_2_data_df=pd.DataFrame(av_ac_1_2_data)
    # av_ac_1_2_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=40 )
    
    # av_ac_2_3_data={"Average_Acceleration_per_sec_2-3S":av_ac_2_3.tolist()}
    # av_ac_2_3_data_df=pd.DataFrame(av_ac_2_3_data)
    # av_ac_2_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=41 )
    
    # av_ac_3_4_data={"Average_Acceleration_per_sec_3-4S":av_ac_3_4.tolist()}
    # av_ac_3_4_data_df=pd.DataFrame(av_ac_3_4_data)
    # av_ac_3_4_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=42 )
    
    # av_ac_4_5_data={"Average_Acceleration_per_sec_4-5S":av_ac_4_5.tolist()}
    # av_ac_4_5_data_df=pd.DataFrame(av_ac_4_5_data)
    # av_ac_4_5_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=43 )
    
    # av_ac_5_6_data={"Average_Acceleration_per_sec_5-6S":av_ac_5_6.tolist()}
    # av_ac_5_6_data_df=pd.DataFrame(av_ac_5_6_data)
    # av_ac_5_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=44 )
    
    # av_ac_0_3_data={"Average_Acceleration_per_sec_0-3S":av_ac_0_3.tolist()}
    # av_ac_0_3_data_df=pd.DataFrame(av_ac_0_3_data)
    # av_ac_0_3_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=45)
    
    # av_ac_3_6_data={"Average_Acceleration_per_sec_3-6S":av_ac_3_6.tolist()}
    # av_ac_3_6_data_df=pd.DataFrame(av_ac_3_6_data)
    # av_ac_3_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=46)
    
    # av_ac_0_6_data={"Average_Acceleration_per_sec_0-6S":av_ac_0_6.tolist()}
    # av_ac_0_6_data_df=pd.DataFrame(av_ac_0_6_data)
    # av_ac_0_6_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=47)
    
    # av_ac_3sec_data={"Average_Acceleration_per_sec_3sec_Segments":total_av_ac_mean.tolist()}
    # av_ac_3sec_data_df=pd.DataFrame(av_ac_3sec_data)
    # av_ac_3sec_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=48)
    
    # av_ac_minus3_0_data={"Average_Acceleration_per_sec_minus3-0S":av_ac_minus3_0.tolist()}
    # av_ac_minus3_0_data_df=pd.DataFrame(av_ac_minus3_0_data)
    # av_ac_minus3_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=49)
    
    # av_ac_minus3_minus2_data={"Average_Acceleration_per_sec_minus3-minus2S":av_ac_minus3_minus2.tolist()}
    # av_ac_minus3_minus2_data_df=pd.DataFrame(av_ac_minus3_minus2_data)
    # av_ac_minus3_minus2_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=50)
    
    # av_ac_minus2_minus1_data={"Average_Acceleration_per_sec_minus2-minus1S":av_ac_minus2_minus1.tolist()}
    # av_ac_minus2_minus1_data_df=pd.DataFrame(av_ac_minus2_minus1_data)
    # av_ac_minus2_minus1_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=51)
    
    # av_ac_minus1_0_data={"Average_Acceleration_per_sec_minus1-0S":av_ac_minus1_0.tolist()}
    # av_ac_minus1_0_data_df=pd.DataFrame(av_ac_minus1_0_data)
    # av_ac_minus1_0_data_df.to_excel(writer,index=False,header=True,sheet_name= folder,startrow= 1, startcol=52)
    
    
    
    
    # #Print dataframe to Raw_Excel
    # frames_acceleration_per_frame= [ac_0_1_tail.squeeze(),ac_0_1_body1.squeeze(),ac_0_1_body2.squeeze(),
    #                                 ac_0_1_body3.squeeze(),ac_0_1_head.squeeze(),
    #                                 ac_0_3_tail.squeeze(), ac_0_3_body1.squeeze(), ac_0_3_body2.squeeze(),
    #                                 ac_0_3_body3.squeeze(), ac_0_3_head.squeeze(),
    #                                 ac_3_6_tail.squeeze(),ac_3_6_body1.squeeze(),ac_3_6_body2.squeeze(),
    #                                 ac_3_6_body3.squeeze(),ac_3_6_head.squeeze()]
    
    # df_acceleration_per_frame= (pd.DataFrame(frames_acceleration_per_frame)).T
    # df_acceleration_per_frame.columns= ['Acceleration_0_1S_tail','Acceleration_0_1S_body1','Acceleration_0_1S_body2',
    #                                     'Acceleration_0_1S_body3','Acceleration_0_1S_head',
    #                                     'Acceleration_0_3S_tail','Acceleration_0_3S_body1','Acceleration_0_3S_body2',
    #                                     'Acceleration_0_3S_body3','Acceleration_0_3S_head',
    #                                     'Acceleration_3_6S_tail','Acceleration_3_6S_body1',
    #                                     'Acceleration_3_6S_body2','Acceleration_3_6S_body3','Acceleration_3_6S_head']
    
    # df_acceleration_per_frame.to_excel(writer_raw,index=False,sheet_name='Acc_01_03_36_mm_per_s_per_s')
    
    
    # #Save both raw and output excel files
    # writer_raw.save()
    
    # writer.save()
    # print("Ran:"+name +folder)
    
    

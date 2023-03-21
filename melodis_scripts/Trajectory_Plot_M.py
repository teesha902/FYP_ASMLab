import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook

# upload results on nbox

###############################################
###Import the CSV's file for d48 ###
###############################################
path = "C:\\Users\\ASMLabUser1\\Desktop\\killifish\\videos\\analyzed\\38-M1\\og_results\\week_12\\with_led\\control\\1\\"
csv_files = glob.glob(os.path.join(path, "*S1_12S_INTER_MM.csv" ))

fig, ax = plt.subplots(1, sharex=True, sharey=True)

for f in csv_files:
    # read the csv file
    csv = pd.read_csv(f)
    full_path = (f.split("\\")[-1])
    name=full_path[67:70]
    d48='d48_'
    folder=full_path[70:72]
    print(name + folder)
############################
###Want to get 0-3 second###
############################
    three_s_mark_name=d48+name+folder
    three_s_mark_name=int(len(csv)/2)
    new_df='df_'+d48+name+folder
    new_df=pd.DataFrame(csv.iloc[:three_s_mark_name,:])


# #d48

    #First Line
    first_x=new_df['Head_X.1'].iloc[0]
    first_y=new_df['Head_Y.1'].iloc[0]
    last_x=new_df['Head_X.1'].iloc[-1]
    last_y=new_df['Head_Y.1'].iloc[-1]
    x = new_df['Head_X.1']
    y = new_df['Head_Y.1']
    # fig = plt.figure()
    ax.plot(x,y,label=d48+name+folder+'_Head',color='blue')
    ax.set_xlabel('X Coordinates (mm)', fontsize = 15)
    ax.set_ylabel('Y Coordinates (mm)', fontsize = 15)
    ax.set_xlim(left=0, right=350)
    ax.set_ylim(bottom=-600, top=0)
    ax.set_title('d48 Trajectory S1 (0-3s)', fontsize = 25)
    ax.set_aspect('equal')
    ax.scatter(first_x,first_y,marker=".",color='green',s=450)
    ax.scatter(last_x,last_y,marker="D",color='red',s=200)
    fig.set_figwidth(100)
    fig.set_figheight(20)

image_format = 'png'
image_name = 'd48_Trajectory.png'
plt.show()
# plt.savefig('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Trajectory_Plots/'+image_name, format=image_format, dpi=1040,bbox_inches= 'tight')

#plt.show()
#plt.savefig('/Users/asmlabuser1/KF_SUMMER_2022/KilliFish_Analysis_Output/Output_Melodi/Trajectory_Plots/'+image_name, format=image_format, dpi=1040,bbox_inches= 'tight')

# # #Second Line
# # first_x1=df_103_M['Head_X.1'].iloc[0]
# # first_y1=df_103_M['Head_Y.1'].iloc[0]
# # last_x1=df_103_M['Head_X.1'].iloc[-1]
# # last_y1=df_103_M['Head_Y.1'].iloc[-1]
# # x1 = df_103_M['Head_X.1']
# # y1 = df_103_M['Head_Y.1']
# # axes.plot(x1, y1,label='103_M_Head',color='gray')
# # axes.scatter(first_x1,first_y1,marker=".",color= 'gray',s=100)
# # axes.scatter(last_x1,last_y1,marker="D",color= 'gray',s=50)
# #
# # #Whird Line
# # first_x2=df_104_M['Head_X.1'].iloc[0]
# # first_y2=df_104_M['Head_Y.1'].iloc[0]
# # last_x2=df_104_M['Head_X.1'].iloc[-1]
# # last_y2=df_104_M['Head_Y.1'].iloc[-1]
# # x2 = df_104_M['Head_X.1']
# # y2 = df_104_M['Head_Y.1']
# # axes.plot(x2, y2,label='104_M_Head',color='brown')
# # axes.scatter(first_x2,first_y2,marker=".",color='brown',s=100)
# # axes.scatter(last_x2,last_y2,marker="D",color='brown',s=50)
# #
# # #Fourth Line
# # first_x3=df_105_M['Head_X.1'].iloc[0]
# # first_y3=df_105_M['Head_Y.1'].iloc[0]
# # last_x3=df_105_M['Head_X.1'].iloc[-1]
# # last_y3=df_105_M['Head_Y.1'].iloc[-1]
# # x3 = df_105_M['Head_X.1']
# # y3 = df_105_M['Head_Y.1']
# # axes.plot(x3, y3,label='105_M_Head',color='pink')
# # axes.scatter(first_x3,first_y3,marker=".",color='pink',s=100)
# # axes.scatter(last_x3,last_y3,marker="D",color='pink',s=50)
# #
# # # Fifth Line
# # first_x4=df_108_M['Head_X.1'].iloc[0]
# # first_y4=df_108_M['Head_Y.1'].iloc[0]
# # last_x4=df_108_M['Head_X.1'].iloc[-1]
# # last_y4=df_108_M['Head_Y.1'].iloc[-1]
# # x4 = df_108_M['Head_X.1']
# # y4 = df_108_M['Head_Y.1']
# # axes.plot(x4, y4,label='108_M_Head',color='orange')
# # axes.scatter(first_x4,first_y4,marker=".",color= 'orange',s=100)
# # axes.scatter(last_x4,last_y4,marker="D",color='orange',s=50)
# #
# # # Sixth Line
# # first_x5=df_113_T['Head_X.1'].iloc[0]
# # first_y5=df_113_T['Head_Y.1'].iloc[0]
# # last_x5=df_113_T['Head_X.1'].iloc[-1]
# # last_y5=df_113_T['Head_Y.1'].iloc[-1]
# # x5 = df_113_T['Head_X.1']
# # y5 = df_113_T['Head_Y.1']
# # axes.plot(x5, y5,label='113_T_Head',color='purple')
# # axes.scatter(first_x5,first_y5,marker=".",color='purple',s=100)
# # axes.scatter(last_x5,last_y5,marker="D",color='purple',s=50)
# #
# # #Seventh Line
# # first_x6=df_114_T['Head_X.1'].iloc[0]
# # first_y6=df_114_T['Head_Y.1'].iloc[0]
# # last_x6=df_114_T['Head_X.1'].iloc[-1]
# # last_y6=df_114_T['Head_Y.1'].iloc[-1]
# # x6 = df_114_T['Head_X.1']
# # y6 = df_114_T['Head_Y.1']
# # axes.plot(x6, y6,label='114_T_Head',color='red')
# # axes.scatter(first_x6,first_y6,marker=".",color='red',s=100)
# # axes.scatter(last_x6,last_y6,marker="D",color='red',s=50)
# #
# # # # Eigth Line
# # # first_x7=df_115_T['Head_X.1'].iloc[0]
# # # first_y7=df_115_T['Head_Y.1'].iloc[0]
# # # last_x7=df_115_T['Head_X.1'].iloc[-1]
# # # last_y7=df_115_T['Head_Y.1'].iloc[-1]
# # # x7 = df_115_T['Head_X.1']
# # # y7 = df_115_T['Head_Y.1']
# # # axes.plot(x7, y7,label='115_T_Head',color='blue')
# # # axes.scatter(first_x7,first_y7,marker=".",color= 'blue',s=100)
# # # axes.scatter(last_x7,last_y7,marker="D",color= 'blue',s=50)
# #
# # # #Ninth Line
# # first_x8=df_116_T['Head_X.1'].iloc[0]
# # first_y8=df_116_T['Head_Y.1'].iloc[0]
# # last_x8=df_116_T['Head_X.1'].iloc[-1]
# # last_y8=df_116_T['Head_Y.1'].iloc[-1]
# # x8 = df_116_T['Head_X.1']
# # y8 = df_116_T['Head_Y.1']
# # axes.plot(x8, y8,label='116_M_Head',color='green')
# # axes.scatter(first_x8,first_y8,marker=".",color= 'green',s=100)
# # axes.scatter(last_x8,last_y8,marker="D",color= 'green',s=50)
# #
# # #Wenth Line
# # first_x9=df_120_M['Head_X.1'].iloc[0]
# # first_y9=df_120_M['Head_Y.1'].iloc[0]
# # last_x9=df_120_M['Head_X.1'].iloc[-1]
# # last_y9=df_120_M['Head_Y.1'].iloc[-1]
# # x9 = df_120_M['Head_X.1']
# # y9 = df_120_M['Head_Y.1']
# # axes.plot(x9, y9,label='120_M_Head',color='black')
# # axes.scatter(first_x9,first_y9,marker=".",color= 'black',s=100)
# # axes.scatter(last_x9,last_y9,marker="D",color= 'black',s=50)

# # first_x10=df_121_M['Head_X.1'].iloc[0]
# # first_y10=df_121_M['Head_Y.1'].iloc[0]
# # last_x10=df_121_M['Head_X.1'].iloc[-1]
# # last_y10=df_121_M['Head_Y.1'].iloc[-1]
# # x10 = df_121_M['Head_X.1']
# # y10 = df_121_M['Head_Y.1']
# # axes.plot(x10, y10,label='121_M_Head',color='magenta')
# # axes.scatter(first_x10,first_y10,marker=".",color='magenta',s=100)
# # axes.scatter(last_x10,last_y10,marker="D",color='magenta',s=50)

# #Second Line
# first_x11=df_122_M['Head_X.1'].iloc[0]
# first_y11=df_122_M['Head_Y.1'].iloc[0]
# last_x11=df_122_M['Head_X.1'].iloc[-1]
# last_y11=df_122_M['Head_Y.1'].iloc[-1]
# x11 = df_122_M['Head_X.1']
# y11 = df_122_M['Head_Y.1']
# axes.plot(x11, y11,label='122_M_Head',color='gray')
# axes.scatter(first_x11,first_y11,marker=".",color= 'gray',s=100)
# axes.scatter(last_x11,last_y11,marker="D",color= 'gray',s=50)

# #Whird Line
# first_x12=df_125_M['Head_X.1'].iloc[0]
# first_y12=df_125_M['Head_Y.1'].iloc[0]
# last_x12=df_125_M['Head_X.1'].iloc[-1]
# last_y12=df_125_M['Head_Y.1'].iloc[-1]
# x12 = df_125_M['Head_X.1']
# y12 = df_125_M['Head_Y.1']
# axes.plot(x12, y12,label='125_M_Head',color='brown')
# axes.scatter(first_x12,first_y12,marker=".",color='brown',s=100)
# axes.scatter(last_x12,last_y12,marker="D",color='brown',s=50)

# #Fourth Line
# first_x13=df_126_M['Head_X.1'].iloc[0]
# first_y13=df_126_M['Head_Y.1'].iloc[0]
# last_x13=df_126_M['Head_X.1'].iloc[-1]
# last_y13=df_126_M['Head_Y.1'].iloc[-1]
# x13 = df_126_M['Head_X.1']
# y13 = df_126_M['Head_Y.1']
# axes.plot(x13, y13,label='126_M_Head',color='pink')
# axes.scatter(first_x13,first_y13,marker=".",color='pink',s=100)
# axes.scatter(last_x13,last_y13,marker="D",color='pink',s=50)

# # Fifth Line
# first_x14=df_128_M['Head_X.1'].iloc[0]
# first_y14=df_128_M['Head_Y.1'].iloc[0]
# last_x14=df_128_M['Head_X.1'].iloc[-1]
# last_y14=df_128_M['Head_Y.1'].iloc[-1]
# x14 = df_128_M['Head_X.1']
# y14 = df_128_M['Head_Y.1']
# axes.plot(x14, y14,label='128_M_Head',color='orange')
# axes.scatter(first_x14,first_y14,marker=".",color= 'orange',s=100)
# axes.scatter(last_x14,last_y14,marker="D",color='orange',s=50)

# # Six10th Line
# first_x15=df_129_M['Head_X.1'].iloc[0]
# first_y15=df_129_M['Head_Y.1'].iloc[0]
# last_x15=df_129_M['Head_X.1'].iloc[-1]
# last_y15=df_129_M['Head_Y.1'].iloc[-1]
# x15 = df_129_M['Head_X.1']
# y15 = df_129_M['Head_Y.1']
# axes.plot(x15, y15,label='129_M_Head',color='purple')
# axes.scatter(first_x15,first_y15,marker=".",color='purple',s=100)
# axes.scatter(last_x15,last_y15,marker="D",color='purple',s=50)

# #Seventh Line


# # # Eigth Line
# first_x17=df_133_M['Head_X.1'].iloc[0]
# first_y17=df_133_M['Head_Y.1'].iloc[0]
# last_x17=df_133_M['Head_X.1'].iloc[-1]
# last_y17=df_133_M['Head_Y.1'].iloc[-1]
# x17 = df_133_M['Head_X.1']
# y17 = df_133_M['Head_Y.1']
# axes.plot(x17, y17,label='133_M_Head',color='blue')
# axes.scatter(first_x17,first_y17,marker=".",color= 'blue',s=100)
# axes.scatter(last_x17,last_y17,marker="D",color= 'blue',s=50)


# #Wenth Line
# first_x19=df_137_M['Head_X.1'].iloc[0]
# first_y19=df_137_M['Head_Y.1'].iloc[0]
# last_x19=df_137_M['Head_X.1'].iloc[-1]
# last_y19=df_137_M['Head_Y.1'].iloc[-1]
# x19 = df_137_M['Head_X.1']
# y19 = df_137_M['Head_Y.1']
# axes.plot(x19, y19,label='137_M_Head',color='black')
# axes.scatter(first_x19,first_y19,marker=".",color= 'black',s=190)
# axes.scatter(last_x19,last_y19,marker="D",color= 'black',s=50)

# # #Ninth Line
# first_x20=df_139_M['Head_X.1'].iloc[0]
# first_y20=df_139_M['Head_Y.1'].iloc[0]
# last_x20=df_139_M['Head_X.1'].iloc[-1]
# last_y20=df_139_M['Head_Y.1'].iloc[-1]
# x20 = df_139_M['Head_X.1']
# y20 = df_139_M['Head_Y.1']
# axes.plot(x20, y20,label='139_M_Head',color='yellow')
# axes.scatter(first_x20,first_y20,marker=".",color= 'yellow',s=100)
# axes.scatter(last_x20,last_y20,marker="D",color= 'yellow',s=50)


# # #Ninth Line
# first_x21=df_142_M['Head_X.1'].iloc[0]
# first_y21=df_142_M['Head_Y.1'].iloc[0]
# last_x21=df_142_M['Head_X.1'].iloc[-1]
# last_y21=df_142_M['Head_Y.1'].iloc[-1]
# x21 = df_142_M['Head_X.1']
# y21 = df_142_M['Head_Y.1']
# axes.plot(x21, y21,label='142_M_Head',color='magenta')
# axes.scatter(first_x21,first_y21,marker=".",color= 'magenta',s=100)
# axes.scatter(last_x21,last_y21,marker="D",color= 'magenta',s=50)

# axes.title.set_text('Swimming Trajectory of Experimental_M when LED turns on (01s)')
# leg1= axes.legend(prop={'size': 8})
# scatter1 = axes.scatter(first_x19,first_y19,marker=".",color='black',s=80, label='Start')
# scatter2 = axes.scatter(last_x19,last_y19,marker="D",color= 'black',s=30, label='End')
# leg2 = axes.legend(handles=[scatter1, scatter2],loc= 'upper left',prop={'size': 8})
# axes.add_artist(leg1)
# axes.set_xlabel('X Coordinates (mm)')
# axes.set_ylabel('Y Coordinates (mm)')
# axes.set_xlim(left=0, right=200)
# axes.set_ylim(bottom=0, top=400)#First Line
# axes.set_aspect('equal')

# fig.set_figwidth(4)
# fig.set_figheight(8)
# image_format = 'svg'
# image_name = 'Experimental-M-01s_Head.svg'
# plt.savefig('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/svg_plots/Experimental/'+image_name, format=image_format, dpi=1040,bbox_inches= 'tight')
# #Excel
# frames = [x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x17,y17,x19,y19,x20,y20,x21,y21]
# df = pd.DataFrame(frames).T
# df.columns = ['X_122','Y_122','X_125','Y_125','X_126','Y_126','X_128','Y_128','X_129'
# ,'Y_129','X_133','Y_133','X_137','Y_137','X_139','Y_139','X_142','Y_142']

# # frames = [x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x8,y8,x9,y9]
# # df = pd.DataFrame(frames).T
# # df.columns = ['X_101','Y_101','X_103','Y_103','X_104','Y_104','X_105','Y_105','X_108','Y_108',
# #               'X_113','Y_113','X_114','Y_114','X_116','Y_116','X_120','Y_120']

# with pd.ExcelWriter('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Trajectory_Plot_Coordinates/X_Y_Coordinates_101-110.xlsx',engine="openpyxl",mode='a') as writer:
#     df.to_excel(writer, sheet_name='01s_M_Head',index=False)
# plt.show()
# #Tuesday
# fig, ax = plt.subplots()
# fig = plt.figure()
# axes = fig.add_subplot(111)
# #First Line
# # first_x=df_101_T['Head_X.1'].iloc[0]
# # first_y=df_101_T['Head_Y.1'].iloc[0]
# # last_x=df_101_T['Head_X.1'].iloc[-1]
# # last_y=df_101_T['Head_Y.1'].iloc[-1]
# # x = df_101_T['Head_X.1']
# # y = df_101_T['Head_Y.1']
# # axes.plot(x, y,label='101_T_Head',color='magenta')
# # axes.scatter(first_x,first_y,marker=".",color='magenta',s=100)
# # axes.scatter(last_x,last_y,marker="D",color='magenta',s=50)
# #
# #
# # #Second Line
# # first_x1=df_103_T['Head_X.1'].iloc[0]
# # first_y1=df_103_T['Head_Y.1'].iloc[0]
# # last_x1=df_103_T['Head_X.1'].iloc[-1]
# # last_y1=df_103_T['Head_Y.1'].iloc[-1]
# # x1 = df_103_T['Head_X.1']
# # y1 = df_103_T['Head_Y.1']
# # axes.plot(x1, y1,label='103_T_Head',color='gray')
# # axes.scatter(first_x1,first_y1,marker=".",color= 'gray',s=100)
# # axes.scatter(last_x1,last_y1,marker="D",color= 'gray',s=50)
# #
# # #Whird Line
# # first_x2=df_104_T['Head_X.1'].iloc[0]
# # first_y2=df_104_T['Head_Y.1'].iloc[0]
# # last_x2=df_104_T['Head_X.1'].iloc[-1]
# # last_y2=df_104_T['Head_Y.1'].iloc[-1]
# # x2 = df_104_T['Head_X.1']
# # y2 = df_104_T['Head_Y.1']
# # axes.plot(x2, y2,label='104_T_Head',color='brown')
# # axes.scatter(first_x2,first_y2,marker=".",color='brown',s=100)
# # axes.scatter(last_x2,last_y2,marker="D",color='brown',s=50)
# #
# # #Fourth Line
# # first_x3=df_105_T['Head_X.1'].iloc[0]
# # first_y3=df_105_T['Head_Y.1'].iloc[0]
# # last_x3=df_105_T['Head_X.1'].iloc[-1]
# # last_y3=df_105_T['Head_Y.1'].iloc[-1]
# # x3 = df_105_T['Head_X.1']
# # y3 = df_105_T['Head_Y.1']
# # axes.plot(x3, y3,label='105_T_Head',color='pink')
# # axes.scatter(first_x3,first_y3,marker=".",color='pink',s=100)
# # axes.scatter(last_x3,last_y3,marker="D",color='pink',s=50)
# #
# # # Fifth Line
# # first_x4=df_108_T['Head_X.1'].iloc[0]
# # first_y4=df_108_T['Head_Y.1'].iloc[0]
# # last_x4=df_108_T['Head_X.1'].iloc[-1]
# # last_y4=df_108_T['Head_Y.1'].iloc[-1]
# # x4 = df_108_T['Head_X.1']
# # y4 = df_108_T['Head_Y.1']
# # axes.plot(x4, y4,label='108_T_Head',color='orange')
# # axes.scatter(first_x4,first_y4,marker=".",color= 'orange',s=100)
# # axes.scatter(last_x4,last_y4,marker="D",color='orange',s=50)
# #
# # # Sixth Line
# # first_x5=df_113_W['Head_X.1'].iloc[0]
# # first_y5=df_113_W['Head_Y.1'].iloc[0]
# # last_x5=df_113_W['Head_X.1'].iloc[-1]
# # last_y5=df_113_W['Head_Y.1'].iloc[-1]
# # x5 = df_113_W['Head_X.1']
# # y5 = df_113_W['Head_Y.1']
# # axes.plot(x5, y5,label='113_W_Head',color='purple')
# # axes.scatter(first_x5,first_y5,marker=".",color='purple',s=100)
# # axes.scatter(last_x5,last_y5,marker="D",color='purple',s=50)
# #
# # # #Seventh Line
# # first_x6=df_114_W['Head_X.1'].iloc[0]
# # first_y6=df_114_W['Head_Y.1'].iloc[0]
# # last_x6=df_114_W['Head_X.1'].iloc[-1]
# # last_y6=df_114_W['Head_Y.1'].iloc[-1]
# # x6 = df_114_W['Head_X.1']
# # y6 = df_114_W['Head_Y.1']
# # axes.plot(x6, y6,label='114_W_Head',color='red')
# # axes.scatter(first_x6,first_y6,marker=".",color='red',s=100)
# # axes.scatter(last_x6,last_y6,marker="D",color='red',s=50)
# #
# # ##Eigth Line
# # # first_x7=df_115_W['Head_X.1'].iloc[0]
# # # first_y7=df_115_W['Head_Y.1'].iloc[0]
# # # last_x7=df_115_W['Head_X.1'].iloc[-1]
# # # last_y7=df_115_W['Head_Y.1'].iloc[-1]
# # # x7 = df_115_W['Head_X.1']
# # # y7 = df_115_W['Head_Y.1']
# # # axes.plot(x7, y7,label='115_W_Head',color='blue')
# # # axes.scatter(first_x7,first_y7,marker=".",color= 'blue',s=100)
# # # axes.scatter(last_x7,last_y7,marker="D",color= 'blue',s=50)
# #
# #
# # #Ninth Line
# # first_x8=df_116_T['Head_X.1'].iloc[0]
# # first_y8=df_116_T['Head_Y.1'].iloc[0]
# # last_x8=df_116_T['Head_X.1'].iloc[-1]
# # last_y8=df_116_T['Head_Y.1'].iloc[-1]
# # x8 = df_116_T['Head_X.1']
# # y8 = df_116_T['Head_Y.1']
# # axes.plot(x8, y8,label='116_T_Head',color='green')
# # axes.scatter(first_x8,first_y8,marker=".",color= 'green',s=100)
# # axes.scatter(last_x8,last_y8,marker="D",color= 'green',s=50)
# #
# # #Wenth Line
# # first_x9=df_120_T['Head_X.1'].iloc[0]
# # first_y9=df_120_T['Head_Y.1'].iloc[0]
# # last_x9=df_120_T['Head_X.1'].iloc[-1]
# # last_y9=df_120_T['Head_Y.1'].iloc[-1]
# # x9 = df_120_T['Head_X.1']
# # y9 = df_120_T['Head_Y.1']
# # axes.plot(x9, y9,label='120_T_Head',color='black')
# # axes.scatter(first_x9,first_y9,marker=".",color= 'black',s=100)
# # axes.scatter(last_x9,last_y9,marker="D",color= 'black',s=50)

# first_x10=df_121_T['Head_X.1'].iloc[0]
# first_y10=df_121_T['Head_Y.1'].iloc[0]
# last_x10=df_121_T['Head_X.1'].iloc[-1]
# last_y10=df_121_T['Head_Y.1'].iloc[-1]
# x10 = df_121_T['Head_X.1']
# y10 = df_121_T['Head_Y.1']
# axes.plot(x10, y10,label='121_T_Head',color='magenta')
# axes.scatter(first_x10,first_y10,marker=".",color='magenta',s=100)
# axes.scatter(last_x10,last_y10,marker="D",color='magenta',s=50)

# #Second Line
# first_x11=df_122_T['Head_X.1'].iloc[0]
# first_y11=df_122_T['Head_Y.1'].iloc[0]
# last_x11=df_122_T['Head_X.1'].iloc[-1]
# last_y11=df_122_T['Head_Y.1'].iloc[-1]
# x11 = df_122_T['Head_X.1']
# y11 = df_122_T['Head_Y.1']
# axes.plot(x11, y11,label='122_T_Head',color='gray')
# axes.scatter(first_x11,first_y11,marker=".",color= 'gray',s=100)
# axes.scatter(last_x11,last_y11,marker="D",color= 'gray',s=50)

# #Whird Line
# first_x12=df_125_T['Head_X.1'].iloc[0]
# first_y12=df_125_T['Head_Y.1'].iloc[0]
# last_x12=df_125_T['Head_X.1'].iloc[-1]
# last_y12=df_125_T['Head_Y.1'].iloc[-1]
# x12 = df_125_T['Head_X.1']
# y12 = df_125_T['Head_Y.1']
# axes.plot(x12, y12,label='125_T_Head',color='brown')
# axes.scatter(first_x12,first_y12,marker=".",color='brown',s=100)
# axes.scatter(last_x12,last_y12,marker="D",color='brown',s=50)

# #Fourth Line
# first_x13=df_126_T['Head_X.1'].iloc[0]
# first_y13=df_126_T['Head_Y.1'].iloc[0]
# last_x13=df_126_T['Head_X.1'].iloc[-1]
# last_y13=df_126_T['Head_Y.1'].iloc[-1]
# x13 = df_126_T['Head_X.1']
# y13 = df_126_T['Head_Y.1']
# axes.plot(x13, y13,label='126_T_Head',color='pink')
# axes.scatter(first_x13,first_y13,marker=".",color='pink',s=100)
# axes.scatter(last_x13,last_y13,marker="D",color='pink',s=50)

# # Fifth Line
# first_x14=df_128_T['Head_X.1'].iloc[0]
# first_y14=df_128_T['Head_Y.1'].iloc[0]
# last_x14=df_128_T['Head_X.1'].iloc[-1]
# last_y14=df_128_T['Head_Y.1'].iloc[-1]
# x14 = df_128_T['Head_X.1']
# y14 = df_128_T['Head_Y.1']
# axes.plot(x14, y14,label='128_T_Head',color='orange')
# axes.scatter(first_x14,first_y14,marker=".",color= 'orange',s=100)
# axes.scatter(last_x14,last_y14,marker="D",color='orange',s=50)

# # Six10th Line
# first_x15=df_129_T['Head_X.1'].iloc[0]
# first_y15=df_129_T['Head_Y.1'].iloc[0]
# last_x15=df_129_T['Head_X.1'].iloc[-1]
# last_y15=df_129_T['Head_Y.1'].iloc[-1]
# x15 = df_129_T['Head_X.1']
# y15 = df_129_T['Head_Y.1']
# axes.plot(x15, y15,label='129_T_Head',color='purple')
# axes.scatter(first_x15,first_y15,marker=".",color='purple',s=100)
# axes.scatter(last_x15,last_y15,marker="D",color='purple',s=50)

# #Seventh Line


# # # Eigth Line
# first_x17=df_133_T['Head_X.1'].iloc[0]
# first_y17=df_133_T['Head_Y.1'].iloc[0]
# last_x17=df_133_T['Head_X.1'].iloc[-1]
# last_y17=df_133_T['Head_Y.1'].iloc[-1]
# x17 = df_133_T['Head_X.1']
# y17 = df_133_T['Head_Y.1']
# axes.plot(x17, y17,label='133_T_Head',color='blue')
# axes.scatter(first_x17,first_y17,marker=".",color= 'blue',s=100)
# axes.scatter(last_x17,last_y17,marker="D",color= 'blue',s=50)

# # #Ninth Line


# #Wenth Line
# first_x19=df_137_T['Head_X.1'].iloc[0]
# first_y19=df_137_T['Head_Y.1'].iloc[0]
# last_x19=df_137_T['Head_X.1'].iloc[-1]
# last_y19=df_137_T['Head_Y.1'].iloc[-1]
# x19 = df_137_T['Head_X.1']
# y19 = df_137_T['Head_Y.1']
# axes.plot(x19, y19,label='137_T_Head',color='black')
# axes.scatter(first_x10,first_y10,marker=".",color= 'black',s=100)
# axes.scatter(last_x10,last_y10,marker="D",color= 'black',s=50)


# # #Ninth Line
# first_x20=df_139_T['Head_X.1'].iloc[0]
# first_y20=df_139_T['Head_Y.1'].iloc[0]
# last_x20=df_139_T['Head_X.1'].iloc[-1]
# last_y20=df_139_T['Head_Y.1'].iloc[-1]
# x20 = df_139_T['Head_X.1']
# y20 = df_139_T['Head_Y.1']
# axes.plot(x20, y20,label='139_T_Head',color='yellow')
# axes.scatter(first_x20,first_y20,marker=".",color= 'yellow',s=100)
# axes.scatter(last_x20,last_y20,marker="D",color= 'yellow',s=50)


# # #Ninth Line
# first_x21=df_142_T['Head_X.1'].iloc[0]
# first_y21=df_142_T['Head_Y.1'].iloc[0]
# last_x21=df_142_T['Head_X.1'].iloc[-1]
# last_y21=df_142_T['Head_Y.1'].iloc[-1]
# x21 = df_142_T['Head_X.1']
# y21 = df_142_T['Head_Y.1']
# axes.plot(x21, y21,label='142_T_Head',color='magenta')
# axes.scatter(first_x21,first_y21,marker=".",color= 'magenta',s=100)
# axes.scatter(last_x21,last_y21,marker="D",color= 'magenta',s=50)




# #set axes and title for  subplot

# axes.title.set_text('Swimming Trajectory of Experimental_T when LED turns on (01s)')
# leg1= axes.legend(prop={'size': 8})
# scatter1 = axes.scatter(first_x19,first_y19,marker=".",color='black',s=80, label='Start')
# scatter2 = axes.scatter(last_x19,last_y19,marker="D",color= 'black',s=30, label='End')
# leg2 = axes.legend(handles=[scatter1, scatter2],loc= 'upper left',prop={'size': 8})
# axes.add_artist(leg1)
# axes.set_xlabel('X Coordinates (mm)')
# axes.set_ylabel('Y Coordinates (mm)')
# axes.set_xlim(left=0, right=200)
# axes.set_ylim(bottom=0, top=400)
# axes.set_aspect('equal')

# fig.set_figwidth(4)
# fig.set_figheight(8)
# image_format = 'svg'
# image_name = 'Experimental-T-01s_Head.svg'
# plt.savefig('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/svg_plots/Experimental/'+image_name, format=image_format, dpi=1040,bbox_inches= 'tight')
# # Excel
# frames = [x10,y10,x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x17,y17,x19,y19,x20,y20,x21,y21]
# df = pd.DataFrame(frames).T
# df.columns = ['X_121','Y_121','X_122','Y_122','X_125','Y_125','X_126','Y_126','X_128','Y_128','X_129'
# ,'Y_129','X_133','Y_133','X_137','Y_137','X_139','Y_139','X_142','Y_142']

# # frames = [x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x8,y8,x9,y9]
# # df = pd.DataFrame(frames).T
# # df.columns = ['X_101','Y_101','X_103','Y_103','X_104','Y_104','X_105','Y_105','X_108','Y_108',
# #               'X_113','Y_113','X_114','Y_114','X_116','Y_116','X_120','Y_120']

# with pd.ExcelWriter('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Trajectory_Plot_Coordinates/X_Y_Coordinates_101-110.xlsx',
#                     engine="openpyxl", mode='a') as writer:
#     df.to_excel(writer, sheet_name='01s_T_Head', index=False)
# plt.show()
# #Friday
# fig, ax = plt.subplots()
# fig = plt.figure()
# axes = fig.add_subplot(111)
# #First Line
# # # first_x=df_101_F['Head_X.1'].iloc[0]
# # # first_y=df_101_F['Head_Y.1'].iloc[0]
# # # last_x=df_101_F['Head_X.1'].iloc[-1]
# # # last_y=df_101_F['Head_Y.1'].iloc[-1]
# # # x = df_101_F['Head_X.1']
# # # y = df_101_F['Head_Y.1']
# # # axes.plot(x, y,label='101_F_Head',color='magenta')
# # # axes.scatter(first_x,first_y,marker=".",color='magenta',s=100)
# # # axes.scatter(last_x,last_y,marker="D",color='magenta',s=50)
# #
# # #Second Line
# # first_x1=df_103_F['Head_X.1'].iloc[0]
# # first_y1=df_103_F['Head_Y.1'].iloc[0]
# # last_x1=df_103_F['Head_X.1'].iloc[-1]
# # last_y1=df_103_F['Head_Y.1'].iloc[-1]
# # x1 = df_103_F['Head_X.1']
# # y1 = df_103_F['Head_Y.1']
# # axes.plot(x1, y1,label='103_F_Head',color='gray')
# # axes.scatter(first_x1,first_y1,marker=".",color= 'gray',s=100)
# # axes.scatter(last_x1,last_y1,marker="D",color= 'gray',s=50)
# #
# # #Whird Line
# # # first_x2=df_104_F['Head_X.1'].iloc[0]
# # # first_y2=df_104_F['Head_Y.1'].iloc[0]
# # # last_x2=df_104_F['Head_X.1'].iloc[-1]
# # # last_y2=df_104_F['Head_Y.1'].iloc[-1]
# # # x2 = df_104_F['Head_X.1']
# # # y2 = df_104_F['Head_Y.1']
# # # axes.plot(x2, y2,label='104_F_Head',color='brown')
# # # axes.scatter(first_x2,first_y2,marker=".",color='brown',s=100)
# # # axes.scatter(last_x2,last_y2,marker="D",color='brown',s=50)
# #
# # #Fourth Line
# # first_x3=df_105_F['Head_X.1'].iloc[0]
# # first_y3=df_105_F['Head_Y.1'].iloc[0]
# # last_x3=df_105_F['Head_X.1'].iloc[-1]
# # last_y3=df_105_F['Head_Y.1'].iloc[-1]
# # x3 = df_105_F['Head_X.1']
# # y3 = df_105_F['Head_Y.1']
# # axes.plot(x3, y3,label='105_F_Head',color='pink')
# # axes.scatter(first_x3,first_y3,marker=".",color='pink',s=100)
# # axes.scatter(last_x3,last_y3,marker="D",color='pink',s=50)
# #
# # # # Fifth Line
# # # first_x4=df_108_F['Head_X.1'].iloc[0]
# # # first_y4=df_108_F['Head_Y.1'].iloc[0]
# # # last_x4=df_108_F['Head_X.1'].iloc[-1]
# # # last_y4=df_108_F['Head_Y.1'].iloc[-1]
# # # x4 = df_108_F['Head_X.1']
# # # y4 = df_108_F['Head_Y.1']
# # # axes.plot(x4, y4,label='108_F_Head',color='orange')
# # # axes.scatter(first_x4,first_y4,marker=".",color= 'orange',s=100)
# # # axes.scatter(last_x4,last_y4,marker="D",color='orange',s=50)
# #
# # # Sixth Line
# # first_x5=df_113_S['Head_X.1'].iloc[0]
# # first_y5=df_113_S['Head_Y.1'].iloc[0]
# # last_x5=df_113_S['Head_X.1'].iloc[-1]
# # last_y5=df_113_S['Head_Y.1'].iloc[-1]
# # x5 = df_113_S['Head_X.1']
# # y5 = df_113_S['Head_Y.1']
# # axes.plot(x5, y5,label='113_S_Head',color='purple')
# # axes.scatter(first_x5,first_y5,marker=".",color='purple',s=100)
# # axes.scatter(last_x5,last_y5,marker="D",color='purple',s=50)
# #
# # #Seventh Line
# # first_x6=df_114_S['Head_X.1'].iloc[0]
# # first_y6=df_114_S['Head_Y.1'].iloc[0]
# # last_x6=df_114_S['Head_X.1'].iloc[-1]
# # last_y6=df_114_S['Head_Y.1'].iloc[-1]
# # x6 = df_114_S['Head_X.1']
# # y6 = df_114_S['Head_Y.1']
# # axes.plot(x6, y6,label='114_S_Head',color='red')
# # axes.scatter(first_x6,first_y6,marker=".",color='red',s=100)
# # axes.scatter(last_x6,last_y6,marker="D",color='red',s=50)
# #
# # # #Eigth Line
# # # first_x7=df_115_S['Head_X.1'].iloc[0]
# # # first_y7=df_115_S['Head_Y.1'].iloc[0]
# # # last_x7=df_115_S['Head_X.1'].iloc[-1]
# # # last_y7=df_115_S['Head_Y.1'].iloc[-1]
# # # x7 = df_115_S['Head_X.1']
# # # y7 = df_115_S['Head_Y.1']
# # # axes.plot(x7, y7,label='115_S_Head',color='blue')
# # # axes.scatter(first_x7,first_y7,marker=".",color= 'blue',s=100)
# # # axes.scatter(last_x7,last_y7,marker="D",color= 'blue',s=50)
# #
# # #Ninth Line
# # first_x8=df_116_S['Head_X.1'].iloc[0]
# # first_y8=df_116_S['Head_Y.1'].iloc[0]
# # last_x8=df_116_S['Head_X.1'].iloc[-1]
# # last_y8=df_116_S['Head_Y.1'].iloc[-1]
# # x8 = df_116_S['Head_X.1']
# # y8 = df_116_S['Head_Y.1']
# # axes.plot(x8, y8,label='116_S_Head',color='green')
# # axes.scatter(first_x8,first_y8,marker=".",color= 'green',s=100)
# # axes.scatter(last_x8,last_y8,marker="D",color= 'green',s=50)
# #
# # #Wenth Line
# # first_x9=df_120_F['Head_X.1'].iloc[0]
# # first_y9=df_120_F['Head_Y.1'].iloc[0]
# # last_x9=df_120_F['Head_X.1'].iloc[-1]
# # last_y9=df_120_F['Head_Y.1'].iloc[-1]
# # x9 = df_120_F['Head_X.1']
# # y9 = df_120_F['Head_Y.1']
# # axes.plot(x9, y9,label='120_F_Head',color='black')
# # axes.scatter(first_x9,first_y9,marker=".",color= 'black',s=100)
# # axes.scatter(last_x9,last_y9,marker="D",color= 'black',s=50)


# first_x10=df_121_F['Head_X.1'].iloc[0]
# first_y10=df_121_F['Head_Y.1'].iloc[0]
# last_x10=df_121_F['Head_X.1'].iloc[-1]
# last_y10=df_121_F['Head_Y.1'].iloc[-1]
# x10 = df_121_F['Head_X.1']
# y10 = df_121_F['Head_Y.1']
# axes.plot(x10, y10,label='121_F_Head',color='magenta')
# axes.scatter(first_x10,first_y10,marker=".",color='magenta',s=100)
# axes.scatter(last_x10,last_y10,marker="D",color='magenta',s=50)

# #Second Line
# first_x11=df_122_F['Head_X.1'].iloc[0]
# first_y11=df_122_F['Head_Y.1'].iloc[0]
# last_x11=df_122_F['Head_X.1'].iloc[-1]
# last_y11=df_122_F['Head_Y.1'].iloc[-1]
# x11 = df_122_F['Head_X.1']
# y11 = df_122_F['Head_Y.1']
# axes.plot(x11, y11,label='122_F_Head',color='gray')
# axes.scatter(first_x11,first_y11,marker=".",color= 'gray',s=100)
# axes.scatter(last_x11,last_y11,marker="D",color= 'gray',s=50)

# #Whird Line
# first_x12=df_125_F['Head_X.1'].iloc[0]
# first_y12=df_125_F['Head_Y.1'].iloc[0]
# last_x12=df_125_F['Head_X.1'].iloc[-1]
# last_y12=df_125_F['Head_Y.1'].iloc[-1]
# x12 = df_125_F['Head_X.1']
# y12 = df_125_F['Head_Y.1']
# axes.plot(x12, y12,label='125_F_Head',color='brown')
# axes.scatter(first_x12,first_y12,marker=".",color='brown',s=100)
# axes.scatter(last_x12,last_y12,marker="D",color='brown',s=50)

# #Fourth Line
# first_x13=df_126_F['Head_X.1'].iloc[0]
# first_y13=df_126_F['Head_Y.1'].iloc[0]
# last_x13=df_126_F['Head_X.1'].iloc[-1]
# last_y13=df_126_F['Head_Y.1'].iloc[-1]
# x13 = df_126_F['Head_X.1']
# y13 = df_126_F['Head_Y.1']
# axes.plot(x13, y13,label='126_F_Head',color='pink')
# axes.scatter(first_x13,first_y13,marker=".",color='pink',s=100)
# axes.scatter(last_x13,last_y13,marker="D",color='pink',s=50)

# # Fifth Line
# first_x14=df_128_F['Head_X.1'].iloc[0]
# first_y14=df_128_F['Head_Y.1'].iloc[0]
# last_x14=df_128_F['Head_X.1'].iloc[-1]
# last_y14=df_128_F['Head_Y.1'].iloc[-1]
# x14 = df_128_F['Head_X.1']
# y14 = df_128_F['Head_Y.1']
# axes.plot(x14, y14,label='128_F_Head',color='orange')
# axes.scatter(first_x14,first_y14,marker=".",color= 'orange',s=100)
# axes.scatter(last_x14,last_y14,marker="D",color='orange',s=50)

# # Six10th Line
# first_x15=df_129_F['Head_X.1'].iloc[0]
# first_y15=df_129_F['Head_Y.1'].iloc[0]
# last_x15=df_129_F['Head_X.1'].iloc[-1]
# last_y15=df_129_F['Head_Y.1'].iloc[-1]
# x15 = df_129_F['Head_X.1']
# y15 = df_129_F['Head_Y.1']
# axes.plot(x15, y15,label='129_F_Head',color='purple')
# axes.scatter(first_x15,first_y15,marker=".",color='purple',s=100)
# axes.scatter(last_x15,last_y15,marker="D",color='purple',s=50)

# #Seventh Line


# # # Eigth Line
# first_x17=df_133_F['Head_X.1'].iloc[0]
# first_y17=df_133_F['Head_Y.1'].iloc[0]
# last_x17=df_133_F['Head_X.1'].iloc[-1]
# last_y17=df_133_F['Head_Y.1'].iloc[-1]
# x17 = df_133_F['Head_X.1']
# y17 = df_133_F['Head_Y.1']
# axes.plot(x17, y17,label='133_F_Head',color='blue')
# axes.scatter(first_x17,first_y17,marker=".",color= 'blue',s=100)
# axes.scatter(last_x17,last_y17,marker="D",color= 'blue',s=50)

# # #Ninth Line

# #Wenth Line
# first_x19=df_137_F['Head_X.1'].iloc[0]
# first_y19=df_137_F['Head_Y.1'].iloc[0]
# last_x19=df_137_F['Head_X.1'].iloc[-1]
# last_y19=df_137_F['Head_Y.1'].iloc[-1]
# x19 = df_137_F['Head_X.1']
# y19 = df_137_F['Head_Y.1']
# axes.plot(x19, y19,label='137_F_Head',color='black')
# axes.scatter(first_x10,first_y10,marker=".",color= 'black',s=100)
# axes.scatter(last_x10,last_y10,marker="D",color= 'black',s=50)

# # #Ninth Line
# first_x20=df_139_F['Head_X.1'].iloc[0]
# first_y20=df_139_F['Head_Y.1'].iloc[0]
# last_x20=df_139_F['Head_X.1'].iloc[-1]
# last_y20=df_139_F['Head_Y.1'].iloc[-1]
# x20 = df_139_F['Head_X.1']
# y20 = df_139_F['Head_Y.1']
# axes.plot(x20, y20,label='139_F_Head',color='yellow')
# axes.scatter(first_x20,first_y20,marker=".",color= 'yellow',s=100)
# axes.scatter(last_x20,last_y20,marker="D",color= 'yellow',s=50)


# # #Ninth Line
# first_x21=df_142_F['Head_X.1'].iloc[0]
# first_y21=df_142_F['Head_Y.1'].iloc[0]
# last_x21=df_142_F['Head_X.1'].iloc[-1]
# last_y21=df_142_F['Head_Y.1'].iloc[-1]
# x21 = df_142_F['Head_X.1']
# y21 = df_142_F['Head_Y.1']
# axes.plot(x21, y21,label='142_F_Head',color='magenta')
# axes.scatter(first_x21,first_y21,marker=".",color= 'magenta',s=100)
# axes.scatter(last_x21,last_y21,marker="D",color= 'magenta',s=50)



# #set axes and title for  subplot

# axes.title.set_text('Swimming Trajectory of Experimental_F when LED turns on (01s)')
# leg1= axes.legend(prop={'size': 8})
# scatter1 = axes.scatter(first_x19,first_y19,marker=".",color='black',s=80, label='Start')
# scatter2 = axes.scatter(last_x19,last_y19,marker="D",color= 'black',s=30, label='End')
# leg2 = axes.legend(handles=[scatter1, scatter2],loc= 'upper left',prop={'size': 8})
# axes.add_artist(leg1)
# axes.set_xlabel('X Coordinates (mm)')
# axes.set_ylabel('Y Coordinates (mm)')
# axes.set_xlim(left=0, right=200)
# axes.set_ylim(bottom=0, top=400)
# axes.set_aspect('equal')

# fig.set_figwidth(4)
# fig.set_figheight(8)
# image_format = 'svg'
# image_name = 'Experimental-F-01s_Head.svg'
# plt.savefig('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/svg_plots/Experimental/'+image_name, format=image_format, dpi=1040,bbox_inches= 'tight')
# # Excel
# frames = [x10,y10,x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x17,y17,x19,y19,x20,y20,x21,y21]
# df = pd.DataFrame(frames).T
# df.columns = ['X_121','Y_121','X_122','Y_122','X_125','Y_125','X_126','Y_126','X_128','Y_128','X_129'
# ,'Y_129','X_133','Y_133','X_137','Y_137','X_139','Y_139','X_142','Y_142']

# # frames = [x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x8,y8,x9,y9]
# # df = pd.DataFrame(frames).T
# # df.columns = ['X_101','Y_101','X_103','Y_103','X_104','Y_104','X_105','Y_105','X_108','Y_108',
# #               'X_113','Y_113','X_114','Y_114','X_116','Y_116','X_120','Y_120']
# plt.show()
# with pd.ExcelWriter('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Trajectory_Plot_Coordinates/X_Y_Coordinates_101-110.xlsx',
#                     engine="openpyxl", mode='a') as writer:
#     df.to_excel(writer, sheet_name='01s_F_Head', index=False)

# #Saturday
# fig, ax = plt.subplots()
# fig = plt.figure()
# axes = fig.add_subplot(111)
# #First Line
# # first_x=df_101_S['Head_X.1'].iloc[0]
# # first_y=df_101_S['Head_Y.1'].iloc[0]
# # last_x=df_101_S['Head_X.1'].iloc[-1]
# # last_y=df_101_S['Head_Y.1'].iloc[-1]
# # x = df_101_S['Head_X.1']
# # y = df_101_S['Head_Y.1']
# # axes.plot(x, y,label='101_S_Head',color='magenta')
# # axes.scatter(first_x,first_y,marker=".",color='magenta',s=100)
# # axes.scatter(last_x,last_y,marker="D",color='magenta',s=50)
# #
# # #Second Line
# # first_x1=df_103_S['Head_X.1'].iloc[0]
# # first_y1=df_103_S['Head_Y.1'].iloc[0]
# # last_x1=df_103_S['Head_X.1'].iloc[-1]
# # last_y1=df_103_S['Head_Y.1'].iloc[-1]
# # x1 = df_103_S['Head_X.1']
# # y1 = df_103_S['Head_Y.1']
# # axes.plot(x1, y1,label='103_S_Head',color='gray')
# # axes.scatter(first_x1,first_y1,marker=".",color= 'gray',s=100)
# # axes.scatter(last_x1,last_y1,marker="D",color= 'gray',s=50)
# #
# # #Whird Line
# # first_x2=df_104_S['Head_X.1'].iloc[0]
# # first_y2=df_104_S['Head_Y.1'].iloc[0]
# # last_x2=df_104_S['Head_X.1'].iloc[-1]
# # last_y2=df_104_S['Head_Y.1'].iloc[-1]
# # x2 = df_104_S['Head_X.1']
# # y2 = df_104_S['Head_Y.1']
# # axes.plot(x2, y2,label='104_S_Head',color='brown')
# # axes.scatter(first_x2,first_y2,marker=".",color='brown',s=100)
# # axes.scatter(last_x2,last_y2,marker="D",color='brown',s=50)
# #
# # #Fourth Line
# # first_x3=df_105_S['Head_X.1'].iloc[0]
# # first_y3=df_105_S['Head_Y.1'].iloc[0]
# # last_x3=df_105_S['Head_X.1'].iloc[-1]
# # last_y3=df_105_S['Head_Y.1'].iloc[-1]
# # x3 = df_105_S['Head_X.1']
# # y3 = df_105_S['Head_Y.1']
# # axes.plot(x3, y3,label='105_S_Head',color='pink')
# # axes.scatter(first_x3,first_y3,marker=".",color='pink',s=100)
# # axes.scatter(last_x3,last_y3,marker="D",color='pink',s=50)
# #
# # # # Fifth Line
# # first_x4=df_108_S['Head_X.1'].iloc[0]
# # first_y4=df_108_S['Head_Y.1'].iloc[0]
# # last_x4=df_108_S['Head_X.1'].iloc[-1]
# # last_y4=df_108_S['Head_Y.1'].iloc[-1]
# # x4 = df_108_S['Head_X.1']
# # y4 = df_108_S['Head_Y.1']
# # axes.plot(x4, y4,label='108_S_Head',color='orange')
# # axes.scatter(first_x4,first_y4,marker=".",color= 'orange',s=100)
# # axes.scatter(last_x4,last_y4,marker="D",color='orange',s=50)
# #
# # # Sixth Line
# # first_x5=df_113_SU['Head_X.1'].iloc[0]
# # first_y5=df_113_SU['Head_Y.1'].iloc[0]
# # last_x5=df_113_SU['Head_X.1'].iloc[-1]
# # last_y5=df_113_SU['Head_Y.1'].iloc[-1]
# # x5 = df_113_SU['Head_X.1']
# # y5 = df_113_SU['Head_Y.1']
# # axes.plot(x5, y5,label='113_SU_Head',color='purple')
# # axes.scatter(first_x5,first_y5,marker=".",color='purple',s=100)
# # axes.scatter(last_x5,last_y5,marker="D",color='purple',s=50)
# #
# # #SUeventh Line
# # first_x6=df_114_SU['Head_X.1'].iloc[0]
# # first_y6=df_114_SU['Head_Y.1'].iloc[0]
# # last_x6=df_114_SU['Head_X.1'].iloc[-1]
# # last_y6=df_114_SU['Head_Y.1'].iloc[-1]
# # x6 = df_114_SU['Head_X.1']
# # y6 = df_114_SU['Head_Y.1']
# # axes.plot(x6, y6,label='114_SU_Head',color='red')
# # axes.scatter(first_x6,first_y6,marker=".",color='red',s=100)
# # axes.scatter(last_x6,last_y6,marker="D",color='red',s=50)
# #
# # # #Eigth Line
# # # first_x7=df_115_SU['Head_X.1'].iloc[0]
# # # first_y7=df_115_SU['Head_Y.1'].iloc[0]
# # # last_x7=df_115_SU['Head_X.1'].iloc[-1]
# # # last_y7=df_115_SU['Head_Y.1'].iloc[-1]
# # # x7 = df_115_SU['Head_X.1']
# # # y7 = df_115_SU['Head_Y.1']
# # # axes.plot(x7, y7,label='115_SU_Head',color='blue')
# # # axes.scatter(first_x7,first_y7,marker=".",color= 'blue',s=100)
# # # axes.scatter(last_x7,last_y7,marker="D",color= 'blue',s=50)
# #
# #
# # #Ninth Line
# # first_x8=df_116_SU['Head_X.1'].iloc[0]
# # first_y8=df_116_SU['Head_Y.1'].iloc[0]
# # last_x8=df_116_SU['Head_X.1'].iloc[-1]
# # last_y8=df_116_SU['Head_Y.1'].iloc[-1]
# # x8 = df_116_SU['Head_X.1']
# # y8 = df_116_SU['Head_Y.1']
# # axes.plot(x8, y8,label='116_SU_Head',color='green')
# # axes.scatter(first_x8,first_y8,marker=".",color= 'green',s=100)
# # axes.scatter(last_x8,last_y8,marker="D",color= 'green',s=50)
# #
# # #Wenth Line
# # first_x9=df_120_S['Head_X.1'].iloc[0]
# # first_y9=df_120_S['Head_Y.1'].iloc[0]
# # last_x9=df_120_S['Head_X.1'].iloc[-1]
# # last_y9=df_120_S['Head_Y.1'].iloc[-1]
# # x9 = df_120_S['Head_X.1']
# # y9 = df_120_S['Head_Y.1']
# # axes.plot(x9, y9,label='120_S_Head',color='black')
# # axes.scatter(first_x9,first_y9,marker=".",color= 'black',s=100)
# # axes.scatter(last_x9,last_y9,marker="D",color= 'black',s=50)


# first_x10=df_121_S['Head_X.1'].iloc[0]
# first_y10=df_121_S['Head_Y.1'].iloc[0]
# last_x10=df_121_S['Head_X.1'].iloc[-1]
# last_y10=df_121_S['Head_Y.1'].iloc[-1]
# x10 = df_121_S['Head_X.1']
# y10 = df_121_S['Head_Y.1']
# axes.plot(x10, y10,label='121_S_Head',color='magenta')
# axes.scatter(first_x10,first_y10,marker=".",color='magenta',s=100)
# axes.scatter(last_x10,last_y10,marker="D",color='magenta',s=50)

# #Second Line
# first_x11=df_122_S['Head_X.1'].iloc[0]
# first_y11=df_122_S['Head_Y.1'].iloc[0]
# last_x11=df_122_S['Head_X.1'].iloc[-1]
# last_y11=df_122_S['Head_Y.1'].iloc[-1]
# x11 = df_122_S['Head_X.1']
# y11 = df_122_S['Head_Y.1']
# axes.plot(x11, y11,label='122_S_Head',color='gray')
# axes.scatter(first_x11,first_y11,marker=".",color= 'gray',s=100)
# axes.scatter(last_x11,last_y11,marker="D",color= 'gray',s=50)

# #Whird Line
# first_x12=df_125_S['Head_X.1'].iloc[0]
# first_y12=df_125_S['Head_Y.1'].iloc[0]
# last_x12=df_125_S['Head_X.1'].iloc[-1]
# last_y12=df_125_S['Head_Y.1'].iloc[-1]
# x12 = df_125_S['Head_X.1']
# y12 = df_125_S['Head_Y.1']
# axes.plot(x12, y12,label='125_S_Head',color='brown')
# axes.scatter(first_x12,first_y12,marker=".",color='brown',s=100)
# axes.scatter(last_x12,last_y12,marker="D",color='brown',s=50)

# #Sourth Line
# first_x13=df_126_S['Head_X.1'].iloc[0]
# first_y13=df_126_S['Head_Y.1'].iloc[0]
# last_x13=df_126_S['Head_X.1'].iloc[-1]
# last_y13=df_126_S['Head_Y.1'].iloc[-1]
# x13 = df_126_S['Head_X.1']
# y13 = df_126_S['Head_Y.1']
# axes.plot(x13, y13,label='126_S_Head',color='pink')
# axes.scatter(first_x13,first_y13,marker=".",color='pink',s=100)
# axes.scatter(last_x13,last_y13,marker="D",color='pink',s=50)

# # Sifth Line
# first_x14=df_128_S['Head_X.1'].iloc[0]
# first_y14=df_128_S['Head_Y.1'].iloc[0]
# last_x14=df_128_S['Head_X.1'].iloc[-1]
# last_y14=df_128_S['Head_Y.1'].iloc[-1]
# x14 = df_128_S['Head_X.1']
# y14 = df_128_S['Head_Y.1']
# axes.plot(x14, y14,label='128_S_Head',color='orange')
# axes.scatter(first_x14,first_y14,marker=".",color= 'orange',s=100)
# axes.scatter(last_x14,last_y14,marker="D",color='orange',s=50)

# # Six10th Line
# first_x15=df_129_S['Head_X.1'].iloc[0]
# first_y15=df_129_S['Head_Y.1'].iloc[0]
# last_x15=df_129_S['Head_X.1'].iloc[-1]
# last_y15=df_129_S['Head_Y.1'].iloc[-1]
# x15 = df_129_S['Head_X.1']
# y15 = df_129_S['Head_Y.1']
# axes.plot(x15, y15,label='129_S_Head',color='purple')
# axes.scatter(first_x15,first_y15,marker=".",color='purple',s=100)
# axes.scatter(last_x15,last_y15,marker="D",color='purple',s=50)


# # # Eigth Line
# first_x17=df_133_S['Head_X.1'].iloc[0]
# first_y17=df_133_S['Head_Y.1'].iloc[0]
# last_x17=df_133_S['Head_X.1'].iloc[-1]
# last_y17=df_133_S['Head_Y.1'].iloc[-1]
# x17 = df_133_S['Head_X.1']
# y17 = df_133_S['Head_Y.1']
# axes.plot(x17, y17,label='133_S_Head',color='blue')
# axes.scatter(first_x17,first_y17,marker=".",color= 'blue',s=100)
# axes.scatter(last_x17,last_y17,marker="D",color= 'blue',s=50)



# #Wenth Line
# first_x19=df_137_S['Head_X.1'].iloc[0]
# first_y19=df_137_S['Head_Y.1'].iloc[0]
# last_x19=df_137_S['Head_X.1'].iloc[-1]
# last_y19=df_137_S['Head_Y.1'].iloc[-1]
# x19 = df_137_S['Head_X.1']
# y19 = df_137_S['Head_Y.1']
# axes.plot(x19, y19,label='137_S_Head',color='black')
# axes.scatter(first_x10,first_y10,marker=".",color= 'black',s=100)
# axes.scatter(last_x10,last_y10,marker="D",color= 'black',s=50)


# # #Ninth Line
# first_x20=df_139_S['Head_X.1'].iloc[0]
# first_y20=df_139_S['Head_Y.1'].iloc[0]
# last_x20=df_139_S['Head_X.1'].iloc[-1]
# last_y20=df_139_S['Head_Y.1'].iloc[-1]
# x20 = df_139_S['Head_X.1']
# y20 = df_139_S['Head_Y.1']
# axes.plot(x20, y20,label='139_S_Head',color='yellow')
# axes.scatter(first_x20,first_y20,marker=".",color= 'yellow',s=100)
# axes.scatter(last_x20,last_y20,marker="D",color= 'yellow',s=50)


# # #Ninth Line
# first_x21=df_142_S['Head_X.1'].iloc[0]
# first_y21=df_142_S['Head_Y.1'].iloc[0]
# last_x21=df_142_S['Head_X.1'].iloc[-1]
# last_y21=df_142_S['Head_Y.1'].iloc[-1]
# x21 = df_142_S['Head_X.1']
# y21 = df_142_S['Head_Y.1']
# axes.plot(x21, y21,label='142_S_Head',color='magenta')
# axes.scatter(first_x21,first_y21,marker=".",color= 'magenta',s=100)
# axes.scatter(last_x21,last_y21,marker="D",color= 'magenta',s=50)


# #set axes and title for  subplot

# axes.title.set_text('Swimming Trajectory of Experimental_S when LED turns on (01s)')
# leg1= axes.legend(prop={'size': 8})
# scatter1 = axes.scatter(first_x19,first_y19,marker=".",color='black',s=80, label='Start')
# scatter2 = axes.scatter(last_x19,last_y19,marker="D",color= 'black',s=30, label='End')
# leg2 = axes.legend(handles=[scatter1, scatter2],loc= 'upper left',prop={'size': 8})
# axes.add_artist(leg1)
# axes.set_xlabel('X Coordinates (mm)')
# axes.set_ylabel('Y Coordinates (mm)')
# axes.set_xlim(left=0, right=200)
# axes.set_ylim(bottom=0, top=400)
# axes.set_aspect('equal')

# fig.set_figwidth(4)
# fig.set_figheight(8)
# image_format = 'svg'
# image_name = 'Experimental-S-01s_Head.svg'

# plt.show()
# plt.savefig('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/svg_plots/Experimental/'+image_name, format=image_format, dpi=1040,bbox_inches= 'tight')
# # Excel
# # frames = [x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x8,y8,x9,y9]
# # df = pd.DataFrame(frames).T
# # df.columns = ['X_101','Y_101','X_103','Y_103','X_104','Y_104','X_105','Y_105','X_108','Y_108',
# #               'X_113','Y_113','X_114','Y_114','X_116','Y_116','X_120','Y_120']

# frames = [x10,y10,x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x17,y17,x19,y19,x20,y20,x21,y21]
# df = pd.DataFrame(frames).T
# df.columns = ['X_121','Y_121','X_122','Y_122','X_125','Y_125','X_126','Y_126','X_128','Y_128','X_129'
# ,'Y_129','X_133','Y_133','X_137','Y_137','X_139','Y_139','X_142','Y_142']

# with pd.ExcelWriter('/Users/saoirselightbourne/Desktop/KilliFish_Analysis_Output/Trajectory_Plot_Coordinates/X_Y_Coordinates_101-110.xlsx',
#                     engine="openpyxl", mode='a') as writer:
#     df.to_excel(writer, sheet_name='01s_S_Head', index=False)

# plt.show()








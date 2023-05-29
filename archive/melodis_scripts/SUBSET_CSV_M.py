#subset 12 second span: 6 seconds before and after the LED light turns on
#subset 6 randomly generated 3 second spans, may be overlapping
import random
import numpy as np
import pandas as pd
import os
import glob
from pathlib import Path
#Read in CSV file
path = "C:\\Users\\ASMLabUser1\\Desktop\\killifish\\videos\\analyzed\\38-M1\\og_results\\week_12\\with_led\\uroa\\4\\"
out_path = "C:\\Users\\ASMLabUser1\\killifish\\data\\output\\week_12\\uroa\\4\\"
csv_files = glob.glob(path + "*.csv")
# print(path)
# print(csv_files)
for f in csv_files:
    # read the csv file
    csv = pd.read_csv(f)
    # print(csv.head(5))
    # print(f)
    full_path = f.split("\\")
    # print(full_path)
    name=full_path[-1].split(".")[0]
    prefix='week_12_'
    # folder=full_path[-4:-2]
    folder = str(full_path[-3]) + "_" + str(full_path[-2]) + "_"
    print(folder + name)
    # print(name)
    exp_time =int(csv.iloc[0,22])
    LED= int(csv.iloc[0,23])
    # print(LED, exp_time)

    #calculate frame rate/frames per second
    n_row=3
    frame_per_sec = (len(csv)-n_row) / int(exp_time)
    frame_per_sec_r= round(frame_per_sec)
    # print(frame_per_sec_r)

    #Find frame where LED light turns on
    n_column= 1
    last_column= 16
    LED_Frame= (int(LED)*frame_per_sec_r)+n_row+1
    print(LED_Frame)

    #Subset data frame to extract 6 seconds before LED light turns on (-6 to 0) and 6 seconds after (0 to 6)
    before_LED = pd.DataFrame(csv.iloc[LED_Frame-(frame_per_sec_r*6):LED_Frame,n_column:last_column])
    first_bef= before_LED.index.values[0]
    last_bef=before_LED.index.values[0] + (6*frame_per_sec_r)
    frame_order_bef = pd.Series(np.arange((first_bef-n_row), (last_bef-n_row), 1))

    after_LED = pd.DataFrame(csv.iloc[LED_Frame:(LED_Frame+(frame_per_sec_r * 6)),n_column:last_column])
    first_aft = after_LED.index.values[0]
    last_aft = after_LED.index.values[0] + (6 * frame_per_sec_r)
    frame_order_aft = pd.Series(np.arange((first_aft+n_row), (last_aft+n_row), 1))

    #create CSV for 12 second span
    #Combine the two data frames
    twelve_span=[frame_order_bef,before_LED,frame_order_aft,after_LED]
    twelve_span_df = pd.concat(twelve_span, axis=1)

    twelve_span_df.columns = ["Frames_bef","Tail_X","Tail_Y",'Tail_L',
                              'Body1_X','Body1_Y','Body1_L',
                              'Body2_X','Body2_Y','Body2_L',
                              'Body3_X','Body3_Y','Body3_L',
                              'Head_X','Head_Y','Head_L',

                              "Frames_Aft","Tail_X","Tail_Y",'Tail_L',
                              'Body1_X','Body1_Y','Body1_L',
                              'Body2_X','Body2_Y','Body2_L',
                              'Body3_X','Body3_Y','Body3_L',
                              'Head_X','Head_Y','Head_L']#32 "Frames_bef","Frames_Aft"
    # To shift cells to top
    frame_bef= twelve_span_df.iloc[:, 0].index.get_loc(twelve_span_df.iloc[:, 0].first_valid_index())
    twelve_span_df.iloc[:, 0] = twelve_span_df.iloc[:, 0].shift(-(frame_bef))

    a = twelve_span_df.iloc[:, 1].index.get_loc(twelve_span_df.iloc[:, 1].first_valid_index())
    twelve_span_df.iloc[:, 1] = twelve_span_df.iloc[:, 1].shift(-(a))

    b = twelve_span_df.iloc[:, 2].index.get_loc(twelve_span_df.iloc[:, 2].first_valid_index())
    twelve_span_df.iloc[:, 2] = twelve_span_df.iloc[:, 2].shift(-(b))

    c = twelve_span_df.iloc[:, 3].index.get_loc(twelve_span_df.iloc[:, 3].first_valid_index())
    twelve_span_df.iloc[:, 3] = twelve_span_df.iloc[:, 3].shift(-(c))

    d= twelve_span_df.iloc[:, 4].index.get_loc(twelve_span_df.iloc[:, 4].first_valid_index())
    twelve_span_df.iloc[:, 4] = twelve_span_df.iloc[:, 4].shift(-(d))

    e = twelve_span_df.iloc[:, 5].index.get_loc(twelve_span_df.iloc[:, 5].first_valid_index())
    twelve_span_df.iloc[:, 5] = twelve_span_df.iloc[:, 5].shift(-(e))

    f = twelve_span_df.iloc[:, 6].index.get_loc(twelve_span_df.iloc[:, 6].first_valid_index())
    twelve_span_df.iloc[:, 6] = twelve_span_df.iloc[:, 6].shift(-(f))

    g = twelve_span_df.iloc[:, 7].index.get_loc(twelve_span_df.iloc[:, 7].first_valid_index())
    twelve_span_df.iloc[:, 7] = twelve_span_df.iloc[:, 7].shift(-(g))

    h = twelve_span_df.iloc[:, 8].index.get_loc(twelve_span_df.iloc[:, 8].first_valid_index())
    twelve_span_df.iloc[:, 8] = twelve_span_df.iloc[:, 8].shift(-(h))

    i= twelve_span_df.iloc[:, 9].index.get_loc(twelve_span_df.iloc[:, 9].first_valid_index())
    twelve_span_df.iloc[:, 9] = twelve_span_df.iloc[:, 9].shift(-(i))

    j= twelve_span_df.iloc[:, 10].index.get_loc(twelve_span_df.iloc[:, 10].first_valid_index())
    twelve_span_df.iloc[:, 10] = twelve_span_df.iloc[:, 10].shift(-(j))

    k = twelve_span_df.iloc[:, 11].index.get_loc(twelve_span_df.iloc[:, 11].first_valid_index())
    twelve_span_df.iloc[:, 11] = twelve_span_df.iloc[:, 11].shift(-(k))

    l = twelve_span_df.iloc[:, 12].index.get_loc(twelve_span_df.iloc[:, 12].first_valid_index())
    twelve_span_df.iloc[:, 12] = twelve_span_df.iloc[:, 12].shift(-(l))

    m = twelve_span_df.iloc[:, 13].index.get_loc(twelve_span_df.iloc[:, 13].first_valid_index())
    twelve_span_df.iloc[:, 13] = twelve_span_df.iloc[:, 13].shift(-(m))

    n = twelve_span_df.iloc[:, 14].index.get_loc(twelve_span_df.iloc[:, 14].first_valid_index())
    twelve_span_df.iloc[:, 14] = twelve_span_df.iloc[:, 14].shift(-(n))

    o = twelve_span_df.iloc[:, 15].index.get_loc(twelve_span_df.iloc[:, 15].first_valid_index())
    twelve_span_df.iloc[:, 15] = twelve_span_df.iloc[:, 15].shift(-(o))

    p = twelve_span_df.iloc[:, 16].index.get_loc(twelve_span_df.iloc[:, 16].first_valid_index())
    twelve_span_df.iloc[:, 16] = twelve_span_df.iloc[:, 16].shift(-(p))

    q= twelve_span_df.iloc[:, 17].index.get_loc(twelve_span_df.iloc[:, 17].first_valid_index())
    twelve_span_df.iloc[:, 17] = twelve_span_df.iloc[:, 17].shift(-(q))

    r = twelve_span_df.iloc[:, 18].index.get_loc(twelve_span_df.iloc[:, 18].first_valid_index())
    twelve_span_df.iloc[:, 18] = twelve_span_df.iloc[:, 18].shift(-(r))

    s = twelve_span_df.iloc[:, 19].index.get_loc(twelve_span_df.iloc[:, 19].first_valid_index())
    twelve_span_df.iloc[:, 19] = twelve_span_df.iloc[:, 19].shift(-(s))

    t = twelve_span_df.iloc[:, 20].index.get_loc(twelve_span_df.iloc[:, 20].first_valid_index())
    twelve_span_df.iloc[:, 20] = twelve_span_df.iloc[:, 20].shift(-(t))

    u = twelve_span_df.iloc[:, 21].index.get_loc(twelve_span_df.iloc[:, 21].first_valid_index())
    twelve_span_df.iloc[:, 21] = twelve_span_df.iloc[:, 21].shift(-(u))

    v = twelve_span_df.iloc[:, 22].index.get_loc(twelve_span_df.iloc[:, 22].first_valid_index())
    twelve_span_df.iloc[:, 22] = twelve_span_df.iloc[:, 22].shift(-(v))

    x = twelve_span_df.iloc[:, 23].index.get_loc(twelve_span_df.iloc[:, 23].first_valid_index())
    twelve_span_df.iloc[:, 23] = twelve_span_df.iloc[:, 23].shift(-(x))

    y = twelve_span_df.iloc[:, 24].index.get_loc(twelve_span_df.iloc[:, 24].first_valid_index())
    twelve_span_df.iloc[:, 24] = twelve_span_df.iloc[:, 24].shift(-(y))

    z = twelve_span_df.iloc[:, 25].index.get_loc(twelve_span_df.iloc[:, 25].first_valid_index())
    twelve_span_df.iloc[:, 25] = twelve_span_df.iloc[:, 25].shift(-(z))

    a1 = twelve_span_df.iloc[:, 26].index.get_loc(twelve_span_df.iloc[:, 26].first_valid_index())
    twelve_span_df.iloc[:, 26] = twelve_span_df.iloc[:, 26].shift(-(a1))

    a2 = twelve_span_df.iloc[:, 27].index.get_loc(twelve_span_df.iloc[:, 27].first_valid_index())
    twelve_span_df.iloc[:, 27] = twelve_span_df.iloc[:, 27].shift(-(a2))

    a3 = twelve_span_df.iloc[:, 28].index.get_loc(twelve_span_df.iloc[:, 28].first_valid_index())
    twelve_span_df.iloc[:, 28] = twelve_span_df.iloc[:, 28].shift(-(a3))

    a4 = twelve_span_df.iloc[:, 29].index.get_loc(twelve_span_df.iloc[:, 29].first_valid_index())
    twelve_span_df.iloc[:, 29] = twelve_span_df.iloc[:, 29].shift(-(a4))

    a5 = twelve_span_df.iloc[:, 30].index.get_loc(twelve_span_df.iloc[:, 30].first_valid_index())
    twelve_span_df.iloc[:, 30] = twelve_span_df.iloc[:, 30].shift(-(a5))

    a6 = twelve_span_df.iloc[:, 31].index.get_loc(twelve_span_df.iloc[:, 31].first_valid_index())
    twelve_span_df.iloc[:, 31] = twelve_span_df.iloc[:, 31].shift(-(a6))

    # #write to new CSV
    twelve_span_df.to_csv(out_path+ prefix +folder+ name + '_12S.csv')#('/Users/saoirselightbourne/Desktop/Cropped_CSV/12_sec/'+big_folder+'/'+big_folder+'-'+folder+'/'+name +folder+ '_12S.csv')


    # #Subset random 3 second segments

    #create a data frame of data from which you wish to create the random 3 second segments
    start_time= 1
    end_time=(LED)
    subset_time_span= pd.DataFrame(csv.iloc[((start_time*frame_per_sec_r)-n_row):((end_time*frame_per_sec_r)-n_row),n_column:last_column])
    step= int(3*frame_per_sec_r)

    #generate 6 randomly generated non overlapping 3 second segmets
    randomlist = set()
    sampleSize = 6
    answerSize = 0

    while answerSize < sampleSize:
        r = random.randrange(start_time, end_time)
        if r not in randomlist:
            answerSize += 1
            randomlist.add(r)

    randomlist= list(randomlist)
    #randomlist= list(random.sample(range(start_time, end_time),6))#list(random.sample(range(start_time, end_time,6),6))


    #subset the data frame for 6 randomly generated 3 second segments

    first_3s = pd.DataFrame(subset_time_span.iloc[(randomlist[0]-1):(randomlist[0]+step-1),[0,1,3,4,6,7 ,9,10,12,13]])
    second_3s = pd.DataFrame(subset_time_span.iloc[(randomlist[1]-1):(randomlist[1]+step-1),[0,1,3,4,6,7 ,9,10,12,13]])
    third_3s = pd.DataFrame(subset_time_span.iloc[(randomlist[2]-1):(randomlist[2]+step-1),[0,1,3,4,6,7 ,9,10,12,13]])
    fourth_3s = pd.DataFrame(subset_time_span.iloc[(randomlist[3]-1):(randomlist[3]+step-1),[0,1,3,4,6,7 ,9,10,12,13]])
    fifth_3s = pd.DataFrame(subset_time_span.iloc[(randomlist[4]-1):(randomlist[4]+step-1),[0,1,3,4,6,7 ,9,10,12,13]])
    sixth_3s = pd.DataFrame(subset_time_span.iloc[(randomlist[5]-1):(randomlist[5]+step-1),[0,1,3,4,6,7 ,9,10,12,13]])

    # Create CSV for the 6 3 second segments

    #extract frame numbers
    frame_oder_1 = pd.Series(np.arange((randomlist[0]), (randomlist[0]+step), 1))
    frame_oder_2 = pd.Series(np.arange((randomlist[1]), (randomlist[1]+step), 1))
    frame_oder_3 = pd.Series(np.arange((randomlist[2]), (randomlist[2]+step), 1))
    frame_oder_4 = pd.Series(np.arange((randomlist[3]), (randomlist[3]+step), 1))
    frame_oder_5 = pd.Series(np.arange((randomlist[4]), (randomlist[4]+step), 1))
    frame_oder_6 = pd.Series(np.arange((randomlist[5]), (randomlist[5]+step), 1))

    # calculate average velocity across the 3 seconds

    #calculate distance travelled in the 3 seconds
    #first 3 sec
    tail_x_y_1= pd.DataFrame(first_3s.iloc[:,[0,1]])
    tail_x_y_1.columns= ["X","Y"]
    tail_x_y_1["X"] = pd.to_numeric(tail_x_y_1["X"], downcast="float")
    tail_x_y_1["Y"] = pd.to_numeric(tail_x_y_1["Y"], downcast="float")


    body1_x_y_1= pd.DataFrame(first_3s.iloc[:,[2,3]])
    body1_x_y_1.columns= ["X","Y"]
    body1_x_y_1["X"] = pd.to_numeric(body1_x_y_1["X"], downcast="float")
    body1_x_y_1["Y"] = pd.to_numeric(body1_x_y_1["Y"], downcast="float")


    body2_x_y_1= pd.DataFrame(first_3s.iloc[:,[4,5]])
    body2_x_y_1.columns= ["X","Y"]
    body2_x_y_1["X"] = pd.to_numeric(body2_x_y_1["X"], downcast="float")
    body2_x_y_1["Y"] = pd.to_numeric(body2_x_y_1["Y"], downcast="float")


    body3_x_y_1= pd.DataFrame(first_3s.iloc[:,[6,7]])
    body3_x_y_1.columns= ["X","Y"]
    body3_x_y_1["X"] = pd.to_numeric(body3_x_y_1["X"], downcast="float")
    body3_x_y_1["Y"] = pd.to_numeric(body3_x_y_1["Y"], downcast="float")


    head_x_y_1= pd.DataFrame(first_3s.iloc[:,[8,9]])
    head_x_y_1.columns= ["X","Y"]
    head_x_y_1["X"] = pd.to_numeric(body3_x_y_1["X"], downcast="float")
    head_x_y_1["Y"] = pd.to_numeric(body3_x_y_1["Y"], downcast="float")



    #second 3 sec

    tail_x_y_2= pd.DataFrame(second_3s.iloc[:,[0,1]])
    tail_x_y_2.columns= ["X","Y"]
    tail_x_y_2["X"] = pd.to_numeric(tail_x_y_2["X"], downcast="float")
    tail_x_y_2["Y"] = pd.to_numeric(tail_x_y_2["Y"], downcast="float")



    body1_x_y_2= pd.DataFrame(second_3s.iloc[:,[2,3]])
    body1_x_y_2.columns= ["X","Y"]
    body1_x_y_2["X"] = pd.to_numeric(body1_x_y_2["X"], downcast="float")
    body1_x_y_2["Y"] = pd.to_numeric(body1_x_y_2["Y"], downcast="float")


    body2_x_y_2= pd.DataFrame(second_3s.iloc[:,[4,5]])
    body2_x_y_2.columns= ["X","Y"]
    body2_x_y_2["X"] = pd.to_numeric(body2_x_y_2["X"], downcast="float")
    body2_x_y_2["Y"] = pd.to_numeric(body2_x_y_2["Y"], downcast="float")


    body3_x_y_2= pd.DataFrame(second_3s.iloc[:,[6,7]])
    body3_x_y_2.columns= ["X","Y"]
    body3_x_y_2["X"] = pd.to_numeric(body3_x_y_2["X"], downcast="float")
    body3_x_y_2["Y"] = pd.to_numeric(body3_x_y_2["Y"], downcast="float")


    head_x_y_2= pd.DataFrame(second_3s.iloc[:,[8,9]])
    head_x_y_2.columns= ["X","Y"]
    head_x_y_2["X"] = pd.to_numeric(body3_x_y_2["X"], downcast="float")
    head_x_y_2["Y"] = pd.to_numeric(body3_x_y_2["Y"], downcast="float")


    #third 3 sec

    tail_x_y_3= pd.DataFrame(third_3s.iloc[:,[0,1]])
    tail_x_y_3.columns= ["X","Y"]
    tail_x_y_3["X"] = pd.to_numeric(tail_x_y_3["X"], downcast="float")
    tail_x_y_3["Y"] = pd.to_numeric(tail_x_y_3["Y"], downcast="float")



    body1_x_y_3= pd.DataFrame(third_3s.iloc[:,[2,3]])
    body1_x_y_3.columns= ["X","Y"]
    body1_x_y_3["X"] = pd.to_numeric(body1_x_y_3["X"], downcast="float")
    body1_x_y_3["Y"] = pd.to_numeric(body1_x_y_3["Y"], downcast="float")


    body2_x_y_3= pd.DataFrame(third_3s.iloc[:,[4,5]])
    body2_x_y_3.columns= ["X","Y"]
    body2_x_y_3["X"] = pd.to_numeric(body2_x_y_3["X"], downcast="float")
    body2_x_y_3["Y"] = pd.to_numeric(body2_x_y_3["Y"], downcast="float")


    body3_x_y_3= pd.DataFrame(third_3s.iloc[:,[6,7]])
    body3_x_y_3.columns= ["X","Y"]
    body3_x_y_3["X"] = pd.to_numeric(body3_x_y_3["X"], downcast="float")
    body3_x_y_3["Y"] = pd.to_numeric(body3_x_y_3["Y"], downcast="float")


    head_x_y_3= pd.DataFrame(third_3s.iloc[:,[8,9]])
    head_x_y_3.columns= ["X","Y"]
    head_x_y_3["X"] = pd.to_numeric(body3_x_y_3["X"], downcast="float")
    head_x_y_3["Y"] = pd.to_numeric(body3_x_y_3["Y"], downcast="float")


    #fourth 3 sec

    tail_x_y_4= pd.DataFrame(fourth_3s.iloc[:,[0,1]])
    tail_x_y_4.columns= ["X","Y"]
    tail_x_y_4["X"] = pd.to_numeric(tail_x_y_4["X"], downcast="float")
    tail_x_y_4["Y"] = pd.to_numeric(tail_x_y_4["Y"], downcast="float")



    body1_x_y_4= pd.DataFrame(fourth_3s.iloc[:,[2,3]])
    body1_x_y_4.columns= ["X","Y"]
    body1_x_y_4["X"] = pd.to_numeric(body1_x_y_4["X"], downcast="float")
    body1_x_y_4["Y"] = pd.to_numeric(body1_x_y_4["Y"], downcast="float")


    body2_x_y_4= pd.DataFrame(fourth_3s.iloc[:,[4,5]])
    body2_x_y_4.columns= ["X","Y"]
    body2_x_y_4["X"] = pd.to_numeric(body2_x_y_4["X"], downcast="float")
    body2_x_y_4["Y"] = pd.to_numeric(body2_x_y_4["Y"], downcast="float")


    body3_x_y_4= pd.DataFrame(fourth_3s.iloc[:,[6,7]])
    body3_x_y_4.columns= ["X","Y"]
    body3_x_y_4["X"] = pd.to_numeric(body3_x_y_4["X"], downcast="float")
    body3_x_y_4["Y"] = pd.to_numeric(body3_x_y_4["Y"], downcast="float")


    head_x_y_4= pd.DataFrame(fourth_3s.iloc[:,[8,9]])
    head_x_y_4.columns= ["X","Y"]
    head_x_y_4["X"] = pd.to_numeric(body3_x_y_4["X"], downcast="float")
    head_x_y_4["Y"] = pd.to_numeric(body3_x_y_4["Y"], downcast="float")




    #fifth 3 sec


    tail_x_y_5= pd.DataFrame(fifth_3s.iloc[:,[0,1]])
    tail_x_y_5.columns= ["X","Y"]
    tail_x_y_5["X"] = pd.to_numeric(tail_x_y_5["X"], downcast="float")
    tail_x_y_5["Y"] = pd.to_numeric(tail_x_y_5["Y"], downcast="float")


    body1_x_y_5= pd.DataFrame(fifth_3s.iloc[:,[2,3]])
    body1_x_y_5.columns= ["X","Y"]
    body1_x_y_5["X"] = pd.to_numeric(body1_x_y_5["X"], downcast="float")
    body1_x_y_5["Y"] = pd.to_numeric(body1_x_y_5["Y"], downcast="float")


    body2_x_y_5= pd.DataFrame(fifth_3s.iloc[:,[4,5]])
    body2_x_y_5.columns= ["X","Y"]
    body2_x_y_5["X"] = pd.to_numeric(body2_x_y_5["X"], downcast="float")
    body2_x_y_5["Y"] = pd.to_numeric(body2_x_y_5["Y"], downcast="float")


    body3_x_y_5= pd.DataFrame(fifth_3s.iloc[:,[6,7]])
    body3_x_y_5.columns= ["X","Y"]
    body3_x_y_5["X"] = pd.to_numeric(body3_x_y_5["X"], downcast="float")
    body3_x_y_5["Y"] = pd.to_numeric(body3_x_y_5["Y"], downcast="float")


    head_x_y_5= pd.DataFrame(fifth_3s.iloc[:,[8,9]])
    head_x_y_5.columns= ["X","Y"]
    head_x_y_5["X"] = pd.to_numeric(body3_x_y_5["X"], downcast="float")
    head_x_y_5["Y"] = pd.to_numeric(body3_x_y_5["Y"], downcast="float")


    #sixth 3 sec

    tail_x_y_6= pd.DataFrame(sixth_3s.iloc[:,[0,1]])
    tail_x_y_6.columns= ["X","Y"]
    tail_x_y_6["X"] = pd.to_numeric(tail_x_y_6["X"], downcast="float")
    tail_x_y_6["Y"] = pd.to_numeric(tail_x_y_6["Y"], downcast="float")



    body1_x_y_6= pd.DataFrame(sixth_3s.iloc[:,[2,3]])
    body1_x_y_6.columns= ["X","Y"]
    body1_x_y_6["X"] = pd.to_numeric(body1_x_y_6["X"], downcast="float")
    body1_x_y_6["Y"] = pd.to_numeric(body1_x_y_6["Y"], downcast="float")


    body2_x_y_6= pd.DataFrame(sixth_3s.iloc[:,[4,5]])
    body2_x_y_6.columns= ["X","Y"]
    body2_x_y_6["X"] = pd.to_numeric(body2_x_y_6["X"], downcast="float")
    body2_x_y_6["Y"] = pd.to_numeric(body2_x_y_6["Y"], downcast="float")


    body3_x_y_6= pd.DataFrame(sixth_3s.iloc[:,[6,7]])
    body3_x_y_6.columns= ["X","Y"]
    body3_x_y_6["X"] = pd.to_numeric(body3_x_y_6["X"], downcast="float")
    body3_x_y_6["Y"] = pd.to_numeric(body3_x_y_6["Y"], downcast="float")


    head_x_y_6= pd.DataFrame(sixth_3s.iloc[:,[8,9]])
    head_x_y_6.columns= ["X","Y"]
    head_x_y_6["X"] = pd.to_numeric(body3_x_y_6["X"], downcast="float")
    head_x_y_6["Y"] = pd.to_numeric(body3_x_y_6["Y"], downcast="float")


    #Combine the data frames


    three_sec_seg= [frame_oder_1,first_3s,
                    frame_oder_2,second_3s,
                    frame_oder_3,third_3s,
                    frame_oder_4,fourth_3s,
                    frame_oder_5,fifth_3s,
                    frame_oder_6,sixth_3s]
    three_sec_seg_df = pd.concat(three_sec_seg, axis=1)
    three_sec_seg_df.columns = ["Frames","first_3_tail_X","first_3_tail_Y","first_3_body1_X","first_3_body1_Y",
                                "first_3_body2_X","first_3_body2_Y","first_3_body3_X","first_3_body3_Y","first_3_head_X","first_3_head_Y",


                                "Frames","second_tail_3_X","second_tail_3_Y","second_3_body1_X","second__3_body1_Y",
                                "second__3_body2_X","second__3_body2_Y","second__3_body3_X","second__3_body3_Y","second__3_head_X","second__3_head_Y",


                                "Frames","third_tail_3_X","third_tail_3_Y","third_3_body1_X","third_3_body1_Y",
                                "third_3_body2_X","third_3_body2_Y","third_3_body3_X","third_3_body3_Y","third_3_head_X","third_3_head_Y",


                                "Frames","fourth_tail_3_X","fourth_tail_3_Y","fourth_3_body1_X","fourth_3_body1_Y",
                                "fourth_3_body2_X","fourth_3_body2_Y","fourth_3_body3_X","fourth_3_body3_Y","fourth_3_head_X","fourth_3_head_Y",


                                "Frames","fifth_tail_3_X","fifth_tail_3_Y","fifth_3_body1_X","fifth_3_body1_Y",
                                "fifth_3_body2_X","fifth_3_body2_Y","fifth_3_body3_X","fifth_3_body3_Y","fifth_3_head_X","fifth_3_head_Y",


                                "Frames","sixth_tail_3_X","sixth_tail_3_Y","sixth_3_body1_X","sixth_3_body1_Y",
                                "sixth_3_body2_X","sixth_3_body2_Y","sixth_3_body3_X","sixth_3_body3_Y","sixth_3_head_X","sixth_3_head_Y"]


    #Shift cells up
    aa= three_sec_seg_df.iloc[:, 1].index.get_loc(three_sec_seg_df.iloc[:, 1].first_valid_index())
    three_sec_seg_df.iloc[:, 1:11] = three_sec_seg_df.iloc[:, 1:11].shift(-(aa))

    ab= three_sec_seg_df.iloc[:, 12].index.get_loc(three_sec_seg_df.iloc[:, 12].first_valid_index())
    three_sec_seg_df.iloc[:, 12:22] = three_sec_seg_df.iloc[:, 12:22].shift(-(ab))


    ac= three_sec_seg_df.iloc[:, 23].index.get_loc(three_sec_seg_df.iloc[:, 23].first_valid_index())
    three_sec_seg_df.iloc[:, 23:33] = three_sec_seg_df.iloc[:, 23:33].shift(-(ac))

    ad= three_sec_seg_df.iloc[:, 34].index.get_loc(three_sec_seg_df.iloc[:, 34].first_valid_index())
    three_sec_seg_df.iloc[:, 34:44] = three_sec_seg_df.iloc[:, 34:44].shift(-(ad))

    ae= three_sec_seg_df.iloc[:, 45].index.get_loc(three_sec_seg_df.iloc[:, 45].first_valid_index())
    three_sec_seg_df.iloc[:, 45:55] = three_sec_seg_df.iloc[:, 45:55].shift(-(ae))

    af= three_sec_seg_df.iloc[:, 56].index.get_loc(three_sec_seg_df.iloc[:, 56].first_valid_index())
    three_sec_seg_df.iloc[:, 56:66] = three_sec_seg_df.iloc[:, 56:66].shift(-(af))


    #write to new CSV
    three_sec_seg_df.to_csv(out_path+prefix+folder+ name+ '_3S.csv')
    print("Ran:"+name +folder)




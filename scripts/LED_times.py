"""
The if name == main runs the script when called from command line.

Parser is used to take in arguments from command line.
--vis flag is used to visualise background mask, and current mask while LED is detected. 
--video_path can be used to provide path to a folder containing videos if not in data/videos. 
--output_path can be used to provide output path for csv if not data/output

create_mask() creates a mask given the image/frame. it converts frame to LAB color format and applies a small gaussian blur to decrease noise, before applying a threshold on L for luminance(brightness), and the other 2 channels for filtering the red color. 

In the main() function, we use video path to find all video files. 
LED_times array saves the final result for each video before saving that data in a csv. 
the for loop is the main code. for each video, a progress bar is initiated. 
a capture object is opened to process each frame using opencv. 
bg flag tracks if a background mask has been created or not, which is done on the first frame. 
the small bg if loop stores the background mask in bg_mask variable and then turns flag to false. 
Next, we go through all the frames wherein a mask for the frame is created, 
after which we subtract background mask from the current frame's mask. 
we store all the timestamps at which LED is observed, 
and append the max and the min of this along with the video name to LED_times. 
After all the videos are processed, this array is saved to a csv in data/output folder.

There is a small check for the time difference between the first and last LED observation.
If the difference is more than 7s, the program prints the video name and the time difference.
Created by: Aritejh
"""

import numpy as np
import argparse
import cv2
from pathlib import Path
from tqdm import tqdm

def create_mask(frame):
  frame_LAB = cv2.cvtColor(cv2.GaussianBlur(frame,(5,5),0), cv2.COLOR_BGR2Lab)
  lower_threshold = (27*2.55, 25+128, -20+128)
  upper_threshold = (100*2.55, 128+128, 40+128)
  mask = cv2.inRange(frame_LAB, lower_threshold, upper_threshold)
  return mask

def main(video_path, vis, debug):
    # Creating the list of videos and initialising arrays
    vid_list = list(video_path.glob("*.mp4"))
    print(f' total videos found are {len(vid_list)}')
    print(f' Videos to be processed are {[i.name for i in vid_list]}') if debug else None
    LED_times = [["name", "start time(s)", "end time(s)", "start frame", "end frame", "fps"]]

    problem_vids = []
    
    #Looping over videos
    for video_path in vid_list:
        video = cv2.VideoCapture(str(video_path))
        print(video_path.name)
        
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = tqdm(total=total_frames)
        
        time_for_video=[]
        frame_for_video=[]
        bg = True
        mask_bg = []
        
        # Read until video is completed
        while(video.isOpened()):
            # Capture frame-by-frame
            ret, frame = video.read()

            if bg == True:
                mask_bg = create_mask(frame)
                bg = False
                print("bg created") if debug else None
                if vis == True: 
                    cv2.imshow(f'{video_path.name} bg',mask_bg)
            if ret == True:  
            # Press Q on keyboard to  exit, for visualization
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                
                mask_frame = create_mask(frame)
                mask_bw = mask_frame - mask_bg
                #find number of non-zero pixels and print timestamp and pixels count if nonzero pixels > 2500
                if np.count_nonzero(mask_bw) > 2500:
                    time_for_video.append(video.get(cv2.CAP_PROP_POS_MSEC))
                    frame_for_video.append(video.get(cv2.CAP_PROP_POS_FRAMES))
                    # print timestamp of video frame
                    print(min(time_for_video), max(time_for_video), min(frame_for_video), max(frame_for_video)) if debug else None
                    # EXPERIMENT IF ERODE AND DILATE IS NEEDED
                    if vis == True:  
                        mask_dilate = cv2.dilate(mask_bw, None, iterations=3)
                        mask_erode = cv2.erode(mask_dilate, None, iterations=4)
                        cv2.imshow(f'{video_path.name} mask',mask_erode)
                progress_bar.update(1)
                # Break the loop
            else: 
                break
        try:
            LED_times.append([str(video_path.name), f"{min(time_for_video)/1000:.2f}", f"{max(time_for_video)/1000:.2f}", min(frame_for_video), max(frame_for_video), cv2.CAP_PROP_FPS ])        
        except:
            print(f"LED not found in {video_path.name}")
            problem_vids.append(video_path.name)


        # When everything done, release the video capture object, progress bar, and close frames
        video.release()
        progress_bar.close()
        print(LED_times[-1])
        cv2.destroyAllWindows()
    return problem_vids, LED_times

if __name__ == "__main__":
    
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", default = "./data/videos/", help="the filepath to video files if not default")
    parser.add_argument("--output_path", default = "./data/output/", help="the filepath to output csv if not default")
    parser.add_argument("--debug", action="store_true", default = False, help="debug mode (default is false)")
    parser.add_argument("--vis", action="store_true", default = False, help="visualise (default is false)")
    args = parser.parse_args()
    video_path = Path(args.video_path) 
    out_path = Path(args.output_path) 
    vis = args.vis
    debug = args.debug

    #main process
    problem_vids, LED_times = main(video_path, vis, debug)

    # output verification and error handling
    if len(problem_vids) > 0:
        print(f'No LED found in {problem_vids}')
    for i in LED_times:
        if i[2]-i[1] > 7:
            print(f'problem detected in {i[0]}. time difference is {i[2]-i[1]}')

    # saving to csv        
    csv_path = Path(out_path, "LED_times.csv")
    print(f'saving to {csv_path}')
    np.savetxt(csv_path, LED_times, delimiter=',', fmt = "%s" )
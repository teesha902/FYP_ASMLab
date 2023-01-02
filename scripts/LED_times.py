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

def main(video_path, out_path, vis):
    # Creating the list of videos and initialising arrays
    vid_list = list(video_path.glob("*.mp4"))
    print(f' Videos to be processed are {[i.name for i in vid_list]}')
    LED_times = [["name", "start time(s)", "end time(s)"]]
    
    #Looping over videos
    for video_path in vid_list:
        video = cv2.VideoCapture(str(video_path))
        print(video_path.name)
        
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = tqdm(total=total_frames)
        
        time_for_video=[]
        bg = True
        mask_bg = []
        
        # Read until video is completed
        while(video.isOpened()):
            # Capture frame-by-frame
            ret, frame = video.read()

            if bg == True:
                mask_bg = create_mask(frame)
                bg = False
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
                    # print timestamp of video frame
                    # print(video.get(cv2.CAP_PROP_POS_MSEC))
                    # EXPERIMENT IF ERODE AND DILATE IS NEEDED
                    if vis == True:  
                        mask_dilate = cv2.dilate(mask_bw, None, iterations=3)
                        mask_erode = cv2.erode(mask_dilate, None, iterations=4)
                        cv2.imshow(f'{video_path.name} mask',mask_erode)
                progress_bar.update(1)
                # Break the loop
            else: 
                break
            
        LED_times.append([str(video_path.name), "{:.2f}".format(min(time_for_video)/1000), "{:.2f}".format(max(time_for_video)/1000)])        
        
        # When everything done, release the video capture object, progress bar, and close frames
        video.release()
        progress_bar.close()
        cv2.destroyAllWindows()
    return LED_times

if __name__ == "__main__":
    
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", default = "./data/videos/", help="the filepath to video files if not default")
    parser.add_argument("--output_path", default = "./data/output/", help="the filepath to output csv if not default")

    parser.add_argument("--vis", action="store_true", default = False, help="visualise (default is false)")
    args = parser.parse_args()
    video_path = Path(args.video_path) 
    out_path = Path(args.output_path) 
    vis = args.vis
    LED_times = main(video_path, out_path, vis)

    np.savetxt(Path(out_path, "LED_times.csv"),LED_times, delimiter=',', fmt = "%s" )
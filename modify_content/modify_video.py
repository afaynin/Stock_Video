import ffmpeg
import os

def convert_ratio(video, video_path, convert_to = [2560, 1440]):
    if video["videos"][0]["width"] != convert_to[0] or video["videos"][0]["width"] != convert_to[1]:
        convert(video_path, convert_to)
    

def convert(video_path, ratio):
    (
        ffmpeg
        .input(video_path)
        .filter('scale', ratio[0], ratio[1])
        .output(f"{video_path.split(".")[0]}_modified.mp4") #removes and readds .mp4
        .run(overwrite_output=True)
    )
    #complete conversion
    os.remove(video_path)
    os.rename((f"{video_path.split(".")[0]}_modified.mp4"), video_path)


convert("temp/temp2.mp4", [2560, 1440])
import ffmpeg
import os
from moviepy.editor import *

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

def convert_all(video_dir, ratio = [2560, 1440]):
    for vid in os.listdir(video_dir):
        convert(vid, ratio)

def trim_video_add_audio(video:str, audio:str, path):
    vid_path = video
    aud_path = audio
    video = VideoFileClip(video)
    audio = AudioFileClip(audio)
    trimmed_video = video.subclip(0, audio.duration)
    # For whatever reason set_audio does not work
    trimmed_video.set_audio(audio)
    trimmed_video.write_videofile(f"{path}.mp4", codec="libx264", audio_codec="aac")
    os.system(f"ffmpeg -i {f"{path}.mp4"} -i {aud_path} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {path}_final.mp4")
    os.remove(f"{path}.mp4")
    # os.remove(vid_path)
    os.rename(f"{path}_final.mp4", f"{path}.mp4")
    video.close()
    audio.close()
    trimmed_video.close()

trim_video_add_audio("temp/temp2.mp4", "temp/temp.mp3", "temp/temp22")
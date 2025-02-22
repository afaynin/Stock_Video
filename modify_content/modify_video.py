import ffmpeg
import os
from moviepy.editor import * #change this
#then again if i cared about efficiency i would be running ffmpeg only no moviepy

def concatenate_mp4_reencode(video_list: list[str], output_file: str):
    # Concatenate clips
    video_list = [VideoFileClip(video) for video in video_list]
    final_clip = concatenate_videoclips(video_list, method="compose")
    # Write the output file
    final_clip.write_videofile(f"{output_file}.mp4", codec="libx264", fps=30)
    return f"{output_file}.mp3"

def concatenate_mp3(audio_list: list[str], directory):
    # Concatenate clips
    audio_list= [AudioFileClip(os.path.join(directory, audio)) for audio in audio_list]
    final_audio = concatenate_audioclips(audio_list)
    # Write the output file
    final_audio.write_audiofile(os.path.join(directory, "audio_final.mp3"), codec="libmp3lame")
    return "audio_final.mp3"

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
    os.remove(vid_path)
    os.rename(f"{path}_final.mp4", f"{path}.mp4")
    video.close()
    audio.close()
    trimmed_video.close()

def clean_out(directory: str):
    for file in os.listdir(directory):
        if not (file.endswith("final.mp4") or file.endswith("accreditation.txt")):
            os.remove(os.path.join(directory, file))
# trim_video_add_audio("temp/temp2.mp4", "temp/temp.mp3", "temp/temp22")
# concatenate_mp4_reencode(["temp/temp2.mp4", "temp/temp3.mp4", "temp/temp4.mp4"], "temp/final.mp4")
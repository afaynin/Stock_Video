import ffmpeg
import os
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip 

#remember to close the audio and video streams to prevent memory leak
def concatenate_mp4_reencode(video_list: list[str], output_file: str):
    # Concatenate clips
    video_list = [VideoFileClip(video) for video in video_list]
    final_clip = concatenate_videoclips(video_list, method="compose")
    # Write the output file
    final_clip.write_videofile(f"{output_file}.mp4", codec="libx264", fps=30, audio=False)
    for vid in video_list:
        vid.close()
    final_clip.close() 
    return f"{output_file}.mp4"

# def concatenate_final(video_paths, output_path):
#     """
#     Concatenates multiple MP4 videos into a single video using FFmpeg.
    
#     Parameters:
#         video_paths (list): List of video file paths to be concatenated.
#         output_path (str): Output file path for the concatenated video.
    
#     Returns:
#         str: Path of the final concatenated video.
#     """
#     # Create a temporary file listing all videos
#     list_file = "video_list.txt"
#     with open(list_file, "w") as f:
#         for video in video_paths:
#             f.write(f"file '{video}'\n")

#     # Run FFmpeg concat command
#     command = f"ffmpeg -f concat -safe 0 -i {list_file} -c copy {f"{output_path}.mp4"}"
#     subprocess.run(command, shell=True, check=True)

#     # Clean up
#     os.remove(list_file)

    # return output_path


def reencode_video(input_path, output_path, target_resolution=(3840, 2160), target_fps=30):
    """
    Re-encodes a video to ensure format consistency for concatenation.
    
    Parameters:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the re-encoded video.
        target_resolution (tuple): The resolution to standardize (width, height).
        target_fps (int): The frame rate to standardize.
    
    Returns:
        str: Path of the re-encoded video.
    """
    command = (
        f"ffmpeg -i {input_path} "
        f"-vf 'scale={target_resolution[0]}:{target_resolution[1]},fps={target_fps},format=yuv420p' "  # Standardize resolution, FPS, pixel format
        f"-c:v libx264 -crf 23 -preset fast "  # Standardize video codec and compression
        f"-g {target_fps} "  # Standardize GOP (keyframe interval)
        f"-c:a aac -b:a 192k -ar 44100 "  # Standardize audio codec and sample rate
        f"-movflags +faststart "  # Enable fast seeking
        f"{output_path}"
    )
    
    subprocess.run(command, shell=True, check=True)
    return output_path

def concatenate_final(video_paths, output_path):
    """
    Concatenates multiple MP4 videos into a single video using FFmpeg.
    
    Parameters:
        video_paths (list): List of video file paths to be concatenated.
        output_path (str): Output file path for the concatenated video.
    
    Returns:
        str: Path of the final concatenated video.
    """
    temp_files = []
    for i, video in enumerate(video_paths):
        temp_output = f"temp_video_{i}.mp4"
        reencode_video(video, temp_output)
        temp_files.append(temp_output)

    # Create list file for FFmpeg concat
    list_file = "video_list.txt"
    with open(list_file, "w") as f:
        for video in temp_files:
            f.write(f"file '{video}'\n")

    # Run FFmpeg concat command
    final_output = f"{output_path}.mp4"
    command = f"ffmpeg -f concat -safe 0 -i {list_file} -c copy {final_output}"
    subprocess.run(command, shell=True, check=True)

    # Clean up temp files
    for file in temp_files:
        os.remove(file)
    os.remove(list_file)

    return final_output
# def concatenate_mp4_reencode(video_list: list[str], output_file: str):
#     video_clips = []
#     audio_clips = []
#     for video in video_list:
#         clip = VideoFileClip(video)
#         video_clips.append(clip)
#         if clip.audio is not None:
#             audio_clips.append(clip.audio)
#     final_video = concatenate_videoclips(video_clips, method="compose")
#     if audio_clips:
#         final_audio = CompositeAudioClip(audio_clips)
#         final_video = final_video.set_audio(final_audio)

#     final_video.write_videofile(f"{output_file}.mp4", codec="libx264", audio_codec="libmp3lame", fps=30)
#     for clip in video_clips:
#         clip.close()
    
#     if audio_clips:
#         for audio in audio_clips:
#             audio.close()

    # return f"{output_file}.mp4"
# fix this eventually, totally unecessary to have to reencode the videos over and over again

# def concatenate_mp4_final(video_list: list[str], output_file: str):
#     # Concatenate clips
#     video_list = [VideoFileClip(video) for video in video_list]
#     final_clip = concatenate_videoclips(video_list,"compose")
#     # Write the output file
#     final_clip.write_videofile(f"{output_file}.mp4", codec="copy", fps=video_list[0].fps)

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

def aud_duration(audio):
    return AudioFileClip(audio).duration

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
    return f"{path}.mp4"

def clean_out(directory: str):
    for file in os.listdir(directory):
        if not (file.endswith("final.mp4") or file.endswith("accreditation.txt")):
            os.remove(os.path.join(directory, file))
# trim_video_add_audio("temp/temp2.mp4", "temp/temp.mp3", "temp/temp22")
# concatenate_mp4_reencode(["temp/temp2.mp4", "temp/temp3.mp4", "temp/temp4.mp4"], "temp/final.mp4")
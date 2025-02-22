from request_content.request_audio import generate_audio_files
from request_content.request_videos import make_vid
from modify_content.categorize import seperate_text, represent_text
from modify_content.modify_video import concatenate_mp4_reencode, aud_duration, trim_video_add_audio,  concatenate_final
import argparse
import asyncio
import os

parser = argparse.ArgumentParser(description="Place your script which you want to have stock footage added to, more features coming soon!")
parser.add_argument("--script", type=str, help="Your script")
parser.add_argument("--seperator", type=str, help="How you would like your script seperated for visuals")
parser.add_argument("--directory", type=str, default="temp", help="directory to save video")
args = parser.parse_args()

seperated_text = seperate_text(args.script, args.seperator)
print(seperated_text)

print()
text_descriptors = represent_text(seperated_text)
print(text_descriptors)
audio_files = []
for i, segment in enumerate(seperated_text):
   audio_files.append(asyncio.run(generate_audio_files(segment, os.path.join(args.directory, f"temp{i}"), f"audio{i}")))
print(audio_files)
all_vid_paths = []
for i, audio in enumerate(audio_files):
   sub_dir = os.path.join(args.directory, f"temp{i}")
   all_vid_paths.append(make_vid(text_descriptors[i], args.directory, sub_dir, "video", aud_duration(os.path.join(sub_dir, audio_files[i]))))
print(all_vid_paths)
os.makedirs(os.path.join(args.directory, "final"))
final_vid_paths = []
#-2 is because the 'final' directory is added and the work accreditation.txt is added when really we only want to navigate the temp directories
for i in (range(len(os.listdir(args.directory))-2)):
   sub_dir = os.path.join(args.directory, f"temp{i}")
   vid_path = concatenate_mp4_reencode(all_vid_paths[i], os.path.join(sub_dir, "vid"))
   final_vid_paths.append(trim_video_add_audio(vid_path, os.path.join(args.directory, f"temp{i}", f"audio{i}.mp3"), os.path.join(args.directory, "final", f"final{i}")))
print(final_vid_paths)
   
concatenate_final(final_vid_paths, os.path.join(args.directory, "final"))




   # trim_video_add_audio()

# concatenate_mp3(audio_files, args.directory)
# request_timed_vid(f"{aud_duration(os.path.join(args.directory, "audio_final.mp3"))}", )






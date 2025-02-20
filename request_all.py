from request_content.request_audio import generate_audio_files
from request_content.request_videos import request_timed_vid
from modify_content.categorize import seperate_text, represent_text, split_text
from modify_content.modify_video import concatenate_mp4_reencode, concatenate_mp3
import argparse
import asyncio

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
   audio_files.append(asyncio.run(generate_audio_files(segment, args.directory, f"audio{i}")))
print(audio_files)
concatenate_mp3(audio_files, args.directory)



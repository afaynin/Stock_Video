import os
from edge_tts import Communicate

# Function to generate audio files from text segments
async def generate_audio_files(input_text, output_folder, filename="audio", voice = "en-US-AriaNeural"):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, f"{filename}.mp3")
    communicate = Communicate(text=input_text, voice=voice)
    await communicate.save(output_file)
    return f"{filename}.mp3"


# asyncio.run(generate_audio_files("hello there, do you have time to talk about your car's extended warrantly? uwu uwu uwuwwuw", "temp", "temp"))
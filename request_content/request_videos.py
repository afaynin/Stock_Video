import requests
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_video(query, per_page=1):
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns JSON response with video data
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_next_video(video):
    
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(video['next_page'], headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns JSON response with video data
    else:
        return f"Error: {response.status_code}, {response.text}"

def check16to9ratio(video):
    if video["videos"][0]["width"] % 16 != 0 or video["videos"][0]["width"] % 16 != 0:
        return False
    return True

def timeofvid(video):
    return(video["videos"][0]["duration"])
def request_timed_vid(required_length, query):
    stored_vids = []
    total_vid_time = 0
    vid = get_video(query)
    while total_vid_time < required_length:
        if check16to9ratio(vid):
            stored_vids.append(vid)
            total_vid_time += timeofvid(vid) 
        if total_vid_time < required_length:
            vid = get_next_video(vid)
    return stored_vids

# def downloadvid(video, directory = "temp"):
#     videourl = video["videos"][0]["video_files"][0]["link"]
#     with open("pexels_video.mp4", "wb") as file:
#         file.write(videourl.content)
def download_video(video, output_dir, filename):
    video_url = video["videos"][0]["video_files"][0]["link"]
    response = requests.get(video_url, stream=True)
    response.raise_for_status()  # Raise error for HTTP issues
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save video to file
    file_path = os.path.join(output_dir, f"{filename}.mp4")
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Video saved to {file_path}")


def create_work_accreditation_file(videos: list, directory: str):
    with open(f"{directory}/accreditation.txt", "w") as file:
        for i, vid in enumerate(videos):
            file.write(f"Video #{i} by: {["videos"][0]["user"]["name"]} at {["videos"][0]["user"]["url"]} \n")

def make_vid(input_text, output_dir, filename, time):
    vids = request_timed_vid(time, input_text)
    for i, vid in enumerate(vids):
        download_video(vid, output_dir, f"{filename}{i}")
# download_video(get_video("nature"), "temp", "temp")
make_vid("nature", "temp", "temp")
# Example Usage
# videos = get_videos("nature", 1)
# print(type(videos))
# print(videos["videos"])
# print(videos["videos"]["video_files"])
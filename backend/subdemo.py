import os
from yt_dlp import YoutubeDL
import whisper
import torch
import subprocess

# Ensure Whisper model runs on GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)

def download_audio_from_youtube(url, output_path='.'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/sample_%(id)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get("id", None)
        audio_file = f"{output_path}/sample_{video_id}.wav"
    
    return audio_file

def convert_audio_for_transcription(input_filename):
    output_filename = os.path.join(os.path.dirname(input_filename), "temp_converted.wav")
 

if __name__ == '__main__':
    # List of YouTube links
    youtube_links = [
        'https://www.youtube.com/watch?v=bfmFfD2RIcg',
        'https://www.youtube.com/watch?v=NrO0CJCbYLA',
    ]
    
    # Process each link and get the transcriptions
    transcriptions = process_youtube_links(youtube_links)
    
    # Output the result as a dictionary of YouTube link -> transcript
    print("\nTranscriptions:")
    for link, transcript in transcriptions.items():
        print(f"\n{link}:\n{transcript}")
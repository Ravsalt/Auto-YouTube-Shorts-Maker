import os
import re
import random
import urllib.parse
import requests
import unicodedata
import glob
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.crop as crop_vid
import json

# -------------------------- CONFIGS --------------------------
TEMPLATE_FOLDER = "templates"
OUTPUT_FOLDER = "generated"
GAMEPLAY_PATTERN = os.path.join(TEMPLATE_FOLDER, "short_*.mp4")


# -------------------- CLEANUP FUNCTION --------------------
def clean_script(text):
    # Remove [directions]
    text = re.sub(r"\[.*?\]", "", text)
    # Remove 'Voiceover' / 'Narrator' / tone indicators
    text = re.sub(r"^\s*(Voiceover|Narrator)?\s*\(?.*?\)?:\s*", "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"^\s*(Voiceover|Narrator)\s*[-:]?\s*", "", text, flags=re.IGNORECASE | re.MULTILINE)
    # Remove asterisks
    text = text.replace("*", "")
    # Normalize quotes and other characters
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # Strip extra whitespace
    return ' '.join(text.strip().split())


# ------------------ TEXT TO SPEECH WITH SCRIPT GENERATION -------------------
def generate_short_title(theme):
    # Remove common words and keep it concise
    words = theme.split()
    # Keep first 2-3 words, remove stop words
    stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
    title_words = [word for word in words if word.lower() not in stop_words][:3]
    # Capitalize and join
    return '_'.join(word.capitalize() for word in title_words)[:30]

def synthesize_speech_post(theme, out_path):
    # Clean and prepare the theme
    cleaned_theme = clean_script(theme)

    prompt = (
    "You’re making a TikTok Short (30 sec MAX) that fucks hard — it’s fast, raw, emotional, borderline psychotic, and makes people slam that like/follow out of pure fear and awe. "
    "Curse as much as possible starts with what the fuck is {theme}. For example, 'What the fuck is ankylosing spondylitis. It's a chronic inflammatory disease that mainly attacks your mine, turning you into a stiff, creaky motherfucker over time. That bitch runs from your lower back through your ass cheeks and all the way down both legs. What the fucking shit is acid reflux? How the fuck do they replace your hip?'"
    "NO lame-ass calls to action. Just obliterate the viewer with knowledge and chaos. "
    "Now rage-explain like maniac with this bastard of a topic like it owes you money — "
    ) + cleaned_theme


    # Encode the text for the URL
    encoded_text = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_text}?model=openai-audio&voice=onyx"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is an audio file
        if 'audio/mpeg' in response.headers.get('Content-Type', ''):
            with open(out_path, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved successfully as {out_path}")
            # Extract and clean the script from the response text
            script = clean_script(response.text.strip())
            print("\n📜 Generated Script:\n", script)
            return script
        else:
            print("Error: Expected audio response, received:")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error making TTS request: {e}")
        return None
    encoded_text = urllib.parse.quote(text)
    url = f"https://text.pollinations.ai/{encoded_text}?model=openai-audio&voice=nova"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is an audio file
        if 'audio/mpeg' in response.headers.get('Content-Type', ''):
            with open(out_path, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved successfully as {out_path}")
        else:
            print("Error: Expected audio response, received:")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error making TTS request: {e}")


# -------------- SELECT RANDOM GAMEPLAY ----------------
def get_random_gameplay_clip(duration_limit):
    gameplay_files = glob.glob(GAMEPLAY_PATTERN)
    if not gameplay_files:
        raise FileNotFoundError("No gameplay templates found in 'templates/'")
    selected = random.choice(gameplay_files)
    clip = VideoFileClip(selected)
    start = random.randint(0, max(1, int(clip.duration - duration_limit)))
    return clip.subclip(start, start + duration_limit)


# -------------- RESIZE TO 9:16 FORMAT ----------------
def resize_to_9_16(clip):
    w, h = clip.size
    target_ratio = 1080 / 1920
    if w / h > target_ratio:
        new_width = int(h * target_ratio)
        return crop_vid.crop(clip, width=new_width, height=h, x_center=w / 2, y_center=h / 2)
    else:
        new_height = int(w / target_ratio)
        return crop_vid.crop(clip, width=w, height=new_height, x_center=w / 2, y_center=h / 2)


# --------------- COMBINE AUDIO & VIDEO ----------------
def combine_clips(video_clip, audio_path):
    audio = AudioFileClip(audio_path)
    duration = min(audio.duration, video_clip.duration)
    trimmed_video = video_clip.subclip(0, duration)
    trimmed_audio = audio.subclip(0, duration)
    return trimmed_video.set_audio(trimmed_audio), duration


# ---------------------- MAIN ------------------------
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    theme = input("🎯 Enter topic for your short: ").strip()

    # Create speech and generate script via Pollinations API
    speech_path = os.path.join(OUTPUT_FOLDER, "speech.mp3")
    script = synthesize_speech_post(theme, speech_path)

    if script is None:
        # Fallback to manual script input if API fails
        script = clean_script(input("✍️ Enter your script manually: ").strip())
        title = input("🎬 Enter video title: ").strip().replace(" ", "_")
    else:
        # Use the auto-generated title
        title = generate_short_title(theme)

    try:
        # Load speech to determine exact duration
        speech_audio = AudioFileClip(speech_path)
        exact_duration = min(speech_audio.duration, 30.0)

        # Load gameplay to match speech
        gameplay_clip = get_random_gameplay_clip(exact_duration + 1.3)

        # Combine
        final_clip, actual_duration = combine_clips(gameplay_clip, speech_path)
        final_clip = resize_to_9_16(final_clip)

        # Output
        output_file = os.path.join(OUTPUT_FOLDER, f"{title}.mp4")
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac',
                                   temp_audiofile='temp-audio.m4a', remove_temp=True)

        print(f"\n✅ DONE. Video saved as: {output_file}")
    except Exception as e:
        print(f"💥 ERROR: {e}")

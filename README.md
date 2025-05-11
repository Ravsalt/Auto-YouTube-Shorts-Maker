# Auto YouTube Shorts Maker

🤖 Automatically generate YouTube shorts simply by running the script!

## Description
This script automates the creation of YouTube shorts, from generating a script and voiceover to editing the video. It's designed to be fast and easy to use.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Built Using](#built-using)

## Installation

### Prerequisites
1.  **Python 3.x**
2.  **Pip** (Python package installer)
3.  **Requests** - `pip install requests`
4.  **MoviePy** - `pip install moviepy`
5.  **Unidecode** - `pip install unidecode` (Often a dependency of other libraries, but good to ensure it's available for `unicodedata.normalize`)

### Installing
1.  Clone this repository or download it as a zip file.
    ```bash
    git clone https://github.com/Ravsalt/Auto-YouTube-Shorts-Maker.git
    cd Auto-YouTube-Shorts-Maker
    ```
2.  Install the required Python modules:
    ```bash
    pip install requests moviepy unidecode
    ```
    (Alternatively, a `requirements.txt` could be created and used with `pip install -r requirements.txt`)
3.  Create a folder named `templates` in the project directory.
4.  Add your gameplay video clips to the `templates` folder. These files should be named following the pattern `short_*.mp4` (e.g., `short_gameplay1.mp4`, `short_cool_moment.mp4`). The script will randomly pick one of these for each short.
5.  Create a folder named `generated` in the project directory. This is where the output videos will be saved.

## Usage

To use this script:
1.  Run the `shorts.py` Python file:
    ```bash
    python shorts.py
    ```
2.  When prompted, enter the topic or theme for your short.
3.  The script will then:
    *   Generate a script and voiceover using the Pollinations AI text-to-speech service.
    *   Select a random gameplay clip from your `templates` folder.
    *   Combine the audio and video.
    *   Resize the video to a 9:16 aspect ratio.
4.  Your completed short will be saved in the `generated/` directory with a title based on your theme.

## How it Works

### 1. Theme Input
The script starts by asking for a theme for the YouTube Short.

### 2. Script & Speech Generation
Using the provided theme, the script interacts with the Pollinations AI API to:
    *   Generate a "rage-explain" style script.
    *   Synthesize this script into an audio voiceover (MP3).
    The generated script is also printed to the console. If the API call fails, you'll be prompted to enter the script manually.

### 3. Video Assembly
    *   **Gameplay Selection**: A random gameplay video (matching `short_*.mp4`) is chosen from the `templates/` directory. A random segment of this clip is selected, matching the duration of the generated audio (up to 30 seconds).
    *   **Combining Clips**: The generated audio is combined with the selected gameplay video clip.
    *   **Resizing**: The combined video is resized to a 9:16 aspect ratio, suitable for YouTube Shorts.

### 4. Output
The final video is saved in the `generated/` folder with a filename derived from the input theme (e.g., `Your_Theme_Here.mp4`).

## Contributing

This script is a work in progress. Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.
Potential future enhancements:
*   Adding subtitles.
*   More sophisticated video editing options.
*   Support for different TTS voices or services.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Built Using

1.  **Pollinations AI** - For text-to-speech and script generation assistance.
2.  **MoviePy** - For video editing.
3.  **Requests** - For making HTTP requests to the API.

import os
from pydub import AudioSegment
from pydub.playback import play

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def play_files_in_order(root_directory, text_only=False):
    try:
        # Get a sorted list of directories by date (assuming directory names represent dates)
        directories = sorted([os.path.join(root_directory, d) for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d))])

        for directory in directories:

            txt_file = [f for f in os.listdir(directory) if f.endswith('.txt')][0]
            file_path = os.path.join(directory, txt_file)
            with open(file_path, "r") as transcription:
                print(f"{bcolors.OKGREEN}[{directory}]: {bcolors.OKBLUE}{transcription.read()}{bcolors.ENDC}")

            if not text_only:
                wav_file = [f for f in os.listdir(directory) if f.endswith('.wav')][0]
                file_path = os.path.join(directory, wav_file)
                audio = AudioSegment.from_wav(file_path)
                play(audio)

    except FileNotFoundError:
        print(f"File not found: {root_directory}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace 'root_directory' with the path to your root directory containing date-ordered subdirectories
    play_files_in_order('output/Feed1', text_only=True)

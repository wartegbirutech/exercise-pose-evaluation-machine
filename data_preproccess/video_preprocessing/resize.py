"""Resize and mute exercise videos to 720x404 with ffmpeg.

    uv run data_preproccess/video_preprocessing/resize.py [INPUT_DIR] [--output OUTPUT_DIR]

INPUT_DIR may hold videos directly, or one subfolder per exercise (push-up/, sit-up/, ...);
subfolders are kept in the output. Results go to OUTPUT_DIR/preprocessed_videos/.
Defaults: INPUT_DIR = $EPEM_DATA_DIR/Videos/Dataset, OUTPUT_DIR = $EPEM_DATA_DIR/Videos
(or INPUT_DIR itself when only INPUT_DIR is given).
"""
import argparse
import os
import subprocess

# Dataset folder (override with EPEM_DATA_DIR).
DATA_DIR = os.environ.get("EPEM_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))), "exercise-pose-data"))

# Define default paths for the dataset
base_path = os.path.join(DATA_DIR, "Videos/Dataset")
save_base_path = os.path.join(DATA_DIR, 'Videos')
OUTPUT_FOLDER = 'preprocessed_videos'


def transform_video(file_path, save_dir, filename):
    os.makedirs(save_dir, exist_ok=True)
    # Resize video to optimal size, drop audio
    save_path = os.path.join(save_dir, filename + '.mp4')
    subprocess.run(["ffmpeg", "-i", file_path, "-vf", "scale=720:404", "-an", save_path], check=True)
    print("Resized, muted and saved!")


def resize_all(base, save_base):
    output_root = os.path.join(save_base, OUTPUT_FOLDER)
    for entry in sorted(os.listdir(base)):
        path = os.path.join(base, entry)
        if os.path.abspath(path) == os.path.abspath(output_root):
            continue  # don't re-process our own output
        if os.path.isdir(path):
            # one folder per exercise
            for filename in sorted(os.listdir(path)):
                transform_video(os.path.join(path, filename), os.path.join(output_root, entry), filename)
        else:
            # videos directly in the input folder
            transform_video(path, output_root, entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_dir", nargs="?", help=f"folder with videos (default: {base_path})")
    parser.add_argument("--output", help="folder to write preprocessed_videos/ into")
    args = parser.parse_args()

    base = args.input_dir or base_path
    save_base = args.output or (args.input_dir if args.input_dir else save_base_path)
    resize_all(base, save_base)

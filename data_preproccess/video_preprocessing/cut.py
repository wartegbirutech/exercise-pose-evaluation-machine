import os
# Repo root and dataset folder (override with EPEM_ROOT / EPEM_DATA_DIR).
REPO_ROOT = os.environ.get("EPEM_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
DATA_DIR = os.environ.get("EPEM_DATA_DIR", os.path.join(os.path.dirname(REPO_ROOT), "exercise-pose-data"))
import os
from moviepy import VideoFileClip, vfx  # MoviePy 2 API

# Define base path for the dataset
base_path = os.path.join(DATA_DIR, "Bandicut/Uncut")
save_base_path = os.path.join(DATA_DIR, 'Bandicut')

def cut_video(folder, filename, count):
    # Get clip duration
    file_path = base_path + '/' + folder + '/' + filename
    clip = VideoFileClip(file_path)
    duration = clip.duration
    
    # Cut video
    clip = clip.with_section_cut_out(duration-5, duration)
    temp_clip = clip
    temp_count = count
    
    # Save processed clip
    # Define directory
    if not os.path.exists(save_base_path + '/Cut'):
        os.mkdir(save_base_path + '/Cut')
        print("Made Cut directory!")
    if not os.path.exists(save_base_path + '/Cut/' + folder):
        os.mkdir(save_base_path + '/Cut/' + folder)
        print("Made " + folder + " directory!")
    save_path = save_base_path + '/Cut/' + folder
        
    # Write video
    temp_clip.write_videofile(save_path + '/' + folder + str(temp_count) + '.mp4')
    temp_count+=1
    
    # Flip video
    temp_clip = temp_clip.with_effects([vfx.MirrorX()])

    # Write flipped video
    temp_clip.write_videofile(save_path + '/' + folder +  str(temp_count) + '.mp4')
    temp_count+=1
    
    # Save optimized clip
    # Speedup clip
    fin = 1
    if folder == 'push-up':
        fin = 1
    elif folder == 'plank':
        fin = 1
    elif folder == 'dumbell-curl':
        fin = 1
    else:
        fin = 2
    clip = clip.with_effects([vfx.MultiplySpeed(final_duration=fin)])

    # Define directory
    if not os.path.exists(save_base_path + '/Optimized'):
        os.mkdir(save_base_path + '/Optimized')
        print("Made Optimized directory!")
    if not os.path.exists(save_base_path + '/Optimized/' + folder):
        os.mkdir(save_base_path + '/Optimized/' + folder)
        print("Made " + folder + " directory!")
    save_path = save_base_path + '/Optimized/' + folder
        
    # Write video
    clip.write_videofile(save_path + '/' + folder + str(count) + '.mp4', fps=24)
    count+=1
    
    # Flip video
    clip = clip.with_effects([vfx.MirrorX()])

    # Write flipped video
    clip.write_videofile(save_path + '/' + folder +  str(count) + '.mp4', fps=24)
    count+=1

    return count

if __name__ == '__main__':
    
    # Get dataset folders
    dirs = os.listdir(base_path)

    # Loop in each folder
    for folder in dirs:
        files = os.listdir(base_path + '/' + folder)
        count = 7000
        for filename in files:
            count = cut_video(folder, filename, count)
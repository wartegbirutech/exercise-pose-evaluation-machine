import os
# Repo root and dataset folder (override with EPEM_ROOT / EPEM_DATA_DIR).
REPO_ROOT = os.environ.get("EPEM_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
DATA_DIR = os.environ.get("EPEM_DATA_DIR", os.path.join(os.path.dirname(REPO_ROOT), "exercise-pose-data"))
import os
import cv2

# Opens the Video file
path = os.path.join(DATA_DIR, 'exercise-videos')
files = os.listdir(path)
for vids in files:
    fname = os.path.splitext(vids)
    if fname[1] == "":
        continue
    fname = fname[0]

    cap = cv2.VideoCapture(f'{path}/{vids}')
    if not os.path.exists(f'{path}/pictures/{fname}'):
        os.mkdir(f'{path}/pictures/{fname}')

    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(f'{path}/pictures/{fname}/{fname}{str(i)}.jpg', frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()
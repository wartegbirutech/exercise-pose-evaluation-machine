# Exercise Pose Machine

Real time exercise pose evaluation in a crowded environtment using Long Short-Term Memory.

## Branches

- **`master`**: modernised for Python 3.11+ and TensorFlow 2 / Keras 3, managed with [uv](https://docs.astral.sh/uv/).
- **[`original`](../../tree/original)**: the code as it was in January 2021 (TensorFlow 1.15, Python ≤ 3.7, commit `96ea402`).

## Requirements

- Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/)
- **OpenPose** with its Python API (`pyopenpose`), built separately and placed in `openpose/`, with models in
  `openpose/models` (see `keypoints_extractor.py`). It's a C++ library and isn't installable with pip. See the
  [OpenPose installation guide](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md).
- **MongoDB** for the extracted keypoint datasets
- A CUDA GPU is recommended for OpenPose and training. On Linux, add GPU support with `uv pip install "tensorflow[and-cuda]"`.

```bash
uv sync
```

## Configuration

Hardcoded paths from the original machines were replaced by environment variables:

| Variable | Default | Used for |
|---|---|---|
| `EPEM_ROOT` | this repository | `models/`, logs, k-fold results |
| `EPEM_DATA_DIR` | `../exercise-pose-data` (next to the repo) | videos, images and datasets (`dataset/`, `initial-pose-data/`, …) |
| `MONGODB_URI` | `mongodb://127.0.0.1` | keypoint database (`PoseMachine`). If your server needs a login, put the username and password in the URI (the 2021 setup used `mongo` / `mongo`). |

## Running

```bash
uv run app/main.py                                   # full pipeline
uv run detectors_keras_api/lstm_model_keras.py       # train an exercise LSTM
uv run detectors_keras_api/stratified_k_fold_lstm_test_script.py
```

## What changed from `original`

- `requirements.txt` (TensorFlow 1.15, scikit-learn 0.21, OpenCV 4.2) replaced by `pyproject.toml` + `uv.lock`
  (TensorFlow 2.20 with Keras 3, NumPy 2, scikit-learn 1.9, MoviePy 2).
- Model code keeps using `tf.keras`. Every imported Keras name was checked against Keras 3. `.h5` save/load still works
  (Keras 3 treats it as a legacy format).
- Deep SORT:
  - The frozen feature-extractor graph now loads through `tf.compat.v1` with its own graph and session.
  - `freeze_model.py` runs in TF1-compatibility mode with `tf_slim`, because `tf.contrib.slim` is gone.
  - `sklearn.utils.linear_assignment_` (removed) was replaced by `scipy.optimize.linear_sum_assignment`.
- `np.float` / `np.int` (removed in NumPy) were replaced by `float` / `int`.
- `cut.py` was ported to the MoviePy 2 API (`with_section_cut_out`, `vfx.MirrorX`, `vfx.MultiplySpeed`).
- Hardcoded `/home/kevin/...`, `/home/binus/...` and `/mnt/c/...` paths, and the MongoDB credentials, are now configurable (see above).
- `is "..."` string comparisons became `==`, and a missing `import traceback` was added in `lstm_model_keras.py`.

### Verification status

Checked on a machine without AVX, so TensorFlow itself could not be imported there:

- all files compile, and the port introduced no undefined names;
- all 161 `tensorflow.keras` imports exist in Keras 3;
- Deep SORT tracking, the MoviePy 2 calls and the MongoDB module were run successfully.

**Not yet run:** model training and inference on TensorFlow 2, `generate_detections.py` with a real frozen graph, and the
OpenPose pipeline. These need a TensorFlow-capable machine, OpenPose and the dataset.

Known issues carried over from `original` (not changed): the `__main__` demo code in `initial_pose_detector_keras.py`
references undefined `kp_extractor` / `KeypointsExtractor`, and `keypoints_extractor.py` line 1182 references an undefined `keypoint`.

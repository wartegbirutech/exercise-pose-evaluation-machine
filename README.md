# Fitcam: Exercise Pose Evaluation Machine

## Introduction

This repository contains code for *Fitcam: detecting and counting repetitive exercises with deep learning*
([Journal of Big Data, 2024](https://doi.org/10.1186/s40537-024-00915-8)).

Fitcam watches a video stream, picks out the person who raises their right hand, recognises which exercise they start
(push-up, sit-up, squat or plank), and evaluates and counts their repetitions. Body keypoints come from
[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose), the person is followed through crowded scenes with
[Deep SORT](https://github.com/nwojke/deep_sort), and each exercise is evaluated by an LSTM network. The models reach
over 90% accuracy on all four exercises.

The code as it was for the paper (TensorFlow 1.15) is on the [`original`](../../tree/original) branch.

## Installation

Clone the repository and install the Python dependencies with [uv](https://docs.astral.sh/uv/):

```
git clone https://github.com/wartegbirutech/exercise-pose-evaluation-machine.git
cd exercise-pose-evaluation-machine
uv sync
```

You also need:

- **OpenPose** with its Python API, built from source and placed in `openpose/` (models in `openpose/models`).
  See the [OpenPose installation guide](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md).
- **Deep SORT's appearance model** `mars-small128.pb` in `deep_sort/model_data/`, from the
  [Deep SORT resources](https://github.com/nwojke/deep_sort#installation).
- **MongoDB**, which stores the extracted keypoints used for training.
- A CUDA GPU is recommended. On Linux, `uv pip install "tensorflow[and-cuda]"` adds GPU support.

Paths and the database are configured with environment variables:

| Variable | Default | Used for |
|---|---|---|
| `EPEM_DATA_DIR` | `../exercise-pose-data` | videos, images and datasets |
| `EPEM_ROOT` | this repository | trained models, logs and k-fold results |
| `MONGODB_URI` | `mongodb://127.0.0.1` | keypoint database (`PoseMachine`); include a username and password if your server needs one |

## Running Fitcam

```
uv run app/main.py
```

This runs the full pipeline on a video: detect the person raising their right hand, recognise the starting pose, then
evaluate and count repetitions on screen. The input videos per exercise are set in `VIDEO_PATHS` in `app/main.py`.
`app/only_exercise.py` skips the right-hand-up step and starts from the starting-pose detection.

## Preparing data and training

1. Preprocess the videos with the scripts in `data_preproccess/video_preprocessing/`, e.g.
   `uv run data_preproccess/video_preprocessing/resize.py path/to/videos`.
2. Extract keypoints into MongoDB with the scripts in `data_preproccess/data_extraction/` (`extract_kp_to_db.py` for exercise
   sequences, `extract_initial_pose_kp_to_db.py` and `extract_right_hand_up_kp_to_db.py` for the pose detectors).
3. Train the models in `detectors_keras_api/`. `lstm_model_keras.py` trains the exercise LSTMs, and the
   `stratified_k_fold_*.py` scripts run the paper's k-fold experiments for each model (right-hand-up detector,
   starting-pose classifier and LSTMs):

```
uv run detectors_keras_api/lstm_model_keras.py
uv run detectors_keras_api/stratified_k_fold_lstm_test_script.py
```

Results of the experiments in the paper are in `k_fold_results/` and `selected_result/`.

## Highlevel overview of source files

- `app/`: the Fitcam application (`main.py`) and a Tkinter version (`app/tkinter/`).
- `keypoints_extractor.py`: OpenPose wrapper, keypoint normalisation and Deep SORT tracking.
- `detectors_keras_api/`: the right-hand-up detector, starting-pose classifier and exercise LSTMs, with their
  training, prediction and k-fold scripts.
- `data_preproccess/`: video preprocessing and keypoint extraction into MongoDB (`db_entity.py`).
- `deep_sort/`: Deep SORT by Nicolai Wojke.

## License

[GPL-3.0](LICENSE), the same licence as the included Deep SORT code.

## Citing Fitcam

If you find this repository useful in your research, we'd really appreciate it if you cite our paper:

    @article{japhne2024fitcam,
      title={Fitcam: detecting and counting repetitive exercises with deep learning},
      author={Japhne, Ferdinandz and Janada, Kevin and Theodorus, Agustinus and Chowanda, Andry},
      journal={Journal of Big Data},
      volume={11},
      pages={101},
      year={2024},
      doi={10.1186/s40537-024-00915-8}
    }

GitHub's "Cite this repository" button gives the same in other formats. Fitcam builds on Deep SORT, so please consider
citing it too:

    @inproceedings{Wojke2017simple,
      title={Simple Online and Realtime Tracking with a Deep Association Metric},
      author={Wojke, Nicolai and Bewley, Alex and Paulus, Dietrich},
      booktitle={2017 IEEE International Conference on Image Processing (ICIP)},
      year={2017},
      pages={3645--3649},
      organization={IEEE},
      doi={10.1109/ICIP.2017.8296962}
    }

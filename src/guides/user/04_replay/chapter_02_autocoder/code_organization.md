# Code Organization

The tool uses a bunch of libraries, and the code is split into several files.

Table of contents:

- [Backend](#backend)
  - [uploads: main data folder](#uploads-main-data-folder)
  - [DATA TAB](#1-data-tab)
  - [SEGMENT TAB](#2-segment-tab)
  - [LABEL TAB](#3-label-tab)
  - [TRAIN TAB](#4-train-tab)
  - [APPLY TAB](#5-apply-tab)
- [Frontend](#frontend)


## Backend
The `flask` webserver is defined inside `main.py` with all the routes.

**Dependencies:**
- flask
- joblib
- numpy
- pandas
- polars-lts-cpu
- scikit-learn
- torch

### uploads: main data folder
1. Contains the uploaded datasets TSV files.
2. In addition, for each dataset_file a `<dataset_file>_models.json` file is created to store all the training experiments information.
3. And under `uploads/models` subdirectory, the models and preprocessors are stored (using joblib and torch).

### Detailed file structure
#### 1. DATA TAB

`dataset.py`
- Read the dataframe
- Get dataset info
- Get users list

`events.py`
- Create extended description for `event_name` column
- Filter by `event_name` column

#### 2. SEGMENT TAB

`segment.py`
- Manual and automatic segmenting, writing to `segment_id` column
- Get segments list for user_id

#### 3. LABEL TAB

`label.py`
- Labels rows, writing to `segment_labels` column

#### 4. TRAIN TAB

`ogd_features.py`
- Calculates OGD numeric features (float, int, bool)

`dim_reduction.py`
- Calculates PCA metrics with scaling as argument
- Calculates correlation matrix
- Autoselects features building a logistic regression with regularization to exclude useless features with zero coefficients.

`preprocess.py`
- One hot encodes the `event_name` column and calculates sum and average grouping by `user_id` and `segment_id`, so that we have 1 row for each segment.
- Adds more columns like `segment_duration` in seconds and `events_counts`.
- Merges the new dataframe with the OGD features.

`train.py`
- Train models (specific implementations are in `train_logistic.py`, `train_random_forest.py` and `train_neural_net.py`) with certain hyperparameters, saving the model and the results.

`metrics.py`
- Calculates evaluation metrics saved on training

#### 5. APPLY TAB

`inference.py`
- Loads existing models using the `*_models.json` from the `uploads` folder
- Applies selected model to get the label with max confidence (saved to `predicted_labels` and `prediction_confidence`).


## Frontend
- `static` folder for the assets
- `templates` folder for html templates

**Dependencies:**
- Bootstrap
    - Bootstrap icons
- jQuery
- Select2
- Chart.js
- DataTables with plugins
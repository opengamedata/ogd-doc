# Data Tab

In the data tab, you load data to use in the system.

Table of contents
- [Loading Datasets](#loading-datasets)
- [Dataset Info](#dataset-info)
- [Downloading Dataset](#downloading-dataset)

## Loading Datasets
**Load TSV** is for uploading data in TSV format to work with.

You can also **delete** the datasets, including all the associated files like models, preprocessors...

Datasets can be downloaded from any game **Raw Data** at the [OGD website](https://opengamedata.fielddaylab.wisc.edu). It should have the following columns:
- session_id
- app_id
- timestamp
- event_name
- event_data
- event_source
- app_version
- app_branch
- log_version
- offset
- user_id
- user_data
- game_state
- index

## Dataset Info

Presents the **filename**, the **date range** of the dataset and the **number of models** trained. And the table for number of rows, segments, users, sessions in the filtered (explained next) and original datasets.

### Event description
To provide a more informative event description, you can use the **Load Event Descriptions** button that allows you to upload a JSON file as follows: 
```json
[
    "switch_job": "switched from job '{event_data[prev_job_name]}' to job '{game_state[job_name]}'",
	"receive_fact": "received new fact: '{event_data[fact_id]}'",
    ...
]
```
That maps each value from `event_name` to a wrapping description, with replacement variables for `event_data` and `game_state` columns and writes the results to the `event_description` column

### Event Filtering
To **apply** the changes **Floppy Disk icon** needs to be pressed.

A new auxiliary column is added, `filtered_in`. Therefore, we can exclude rows with certain values for `event_name` column setting `filtered_in` = False. 

### Pie charts
**Labeling progress pie**: how many segments are not labels, and how many segments are excluded. (if not segmented)

**Labels count pie**: how many segments are inside each class (also available at the top as text).

## Downloading Dataset
If you ever want to "export" the dataset you have been working on, click the **Download** button.
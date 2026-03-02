## Process for Adding and Configuring Modeling Modules

This document outlines the step-by-step process for adding a new modeling module into the codebase and configuring it in a game’s JSON schema

### Adding a New Modeling Module

#### Implementing the Model Class

When creating a new model:

* Inherit from `PopulationModel` (from `ogd.core.generators.models.PopulationModel`).
* Review existing examples like:
  * `KMeansModel`
  * `LogisticRegressionModel`
  * `NeuralNetModel`
  * `RandomForestModel`

Steps:

1. Create the model file in: `ogd/games/<GAME>/models/<MyModel>.py`
2. Implement the following methods in the model class:
    * `__init__`: Set up internal lists, parameters, and objects (e.g., scalers, classifiers).
    * `_featureFilter(cls, mode)`: Return the **exact list** of feature names needed (must match schema file features).
    * `_updateFromFeatureData(self, feature)`: Handle and store incoming feature values.
    * `_train(self)`: Train the model using accumulated data.
    * `_apply(self, apply_to)`: Apply the model to new feature data for predictions.
    * `_render(self, save_path=None)`: Output charts, plots, or other reports.
    * `_modelInfo(self)`: Log metrics, statistics, feature importances, cluster summaries, etc.

#### Registering the Model

To enable the system to load the model at runtime from the JSON config:

* **Do not hard-code** into the loader, rely on `ModelRegistry` and `loader._loadConfiguredModels`.
* Ensure the name in the JSON **matches the class name exactly**.

Process:

1. Import the new model into the game’s code if required.
2. `ModelRegistry`:
    * Calls `_loadFromSchema()` to read models from the config.
    * Registers the model with the feature listener system.
3. Loader instantiates the model based on JSON config.

#### Integration Points

* Ensure `_featureFilter` matches schema-defined features exactly.
* Verify model handles correct data types (numeric, time durations, etc.).
* Output model results using the **same conventions** as other models for consistency.

### Configuring the Model in the JSON Schema File

Location: `ogd/games/<GAME>/schemas/<GAME>.json`
Example for BLOOM: `ogd/games/BLOOM/schemas/BLOOM.json`

#### Adding My Model to the Config

Example: KMeansModel for BLOOM

```json
"models": [
  {
    "name": "KMeansModel",
    "params": {
      "n_clusters": 6,
      "features": [
        "BuildCount",
        "CityInspectionCount",
        "DairyInspectionCount",
        "GrainInspectionCount",
        "AveragePhosphorusViewTime",
        "AverageEconomyViewTime"
      ]
    }
  }
]
```

Key Fields:

* `name` — Exact Python class name of the model.
* `params` — Optional parameters passed to `GeneratorParameters` in the model.
* `features` — Exact list from `_featureFilter`.

#### How the Loader Uses It

When running an export:

1. `GeneratorLoader` reads "`models`" from the schema.
2. Instantiates each model with provided parameters.
3. `ModelRegistry` registers them so they receive matching features.
4. `ModelManager` calls:
    * `TrainModels()` → `_train`
    * `GetModelInfo()` → `_modelInfo`
    * `RenderModels()` → `_render`

#### Special Configuration Rules

* All features in "`features`" must already exist in the "`features`" section of the schema.
* If the model needs new features:
  * Add them to the schema first, including **type** and **description**.
* Special hyperparameters (e.g., `hidden_layer_sizes` for neural nets) go under "`params`".

#### Another Example

Neural Network for BLOOM:

```json
"models": [
  {
    "name": "NeuralNetModel",
    "params": {
      "hidden_layer_sizes": [8],
      "activation": "relu"
    },
    "features": [
      "EconomyViewCount",
      "AlertReviewCount",
      "TotalPolicyChangeCount",
      "GameCompletionStatus"
    ]
  }
]
```

### End-to-End Workflow

Order of Steps:

1. Implement the model — subclass `PopulationModel`.
2. Test locally — verify:
    * `_updateFromFeatureData`
    * `_train`
    * `_apply`
3. Add config — insert model into "`models`" in the game’s JSON schema.
4. Run export — check:
    * Features are collected correctly.
    * Training logs appear.
    * Model metrics and outputs are generated.
5. (Optional) Visualize results in `_render`.

Summary:  
To add a new machine learning module to the OGD pipeline, you only need to:

1. Create one Python file for the model.
2. Update the game’s JSON schema.

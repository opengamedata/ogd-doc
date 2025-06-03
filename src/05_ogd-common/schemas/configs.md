## `Config` Categories and Classes

### `games` Configs

```{mermaid}
---
title: `games` Configs
---
classDiagram
    note "Showing subsets of public properties"
    class Config
    class GameGeneratorsConfig {
        + GameID
        + Detectors : DetectorMapConfig
        + Extractors : ExtractorMapConfig
        + LevelRange
        + OtherRanges : Dict[str, range]
    }
    class FeatureMapConfig {
        + AggregateFeatures
        + PerCountFeatures
        + LegacyPerLevelFeatures
        + LegacyMode : bool
    }
    class DetectorMapConfig {
        + AggregateDetectors
        + PerCountDetectors
        + PerLevelDetectors
    }
    class GeneratorConfig
    class FeatureConfig
    class DetectorConfig
    class SubfeatureConfig {
        + ReturnType
        + Description
    }
    class DetectorConfig {
        + Enabled
        + Description
        + ReturnType
        + Subfeatures
    }
    class AggregateConfig {
        + Enabled
        + Description
        + ReturnType
        + Subfeatures
    }
    class PerCountConfig {
        + Enabled
        + Description
        + Prefix
        + Count
        + ReturnType
        + Subfeatures
    }
    GameGeneratorsConfig *-- DetectorMapConfig
    GameGeneratorsConfig *-- FeatureMapConfig
    DetectorMapConfig o-- DetectorConfig
    FeatureMapConfig o-- AggregateConfig
    FeatureMapConfig o-- PerCountConfig
    GeneratorConfig <|-- DetectorConfig
    GeneratorConfig <|-- FeatureConfig
    FeatureConfig <|-- AggregateConfig
    FeatureConfig <|-- PerCountConfig
    AggregateConfig *-- SubfeatureConfig
    PerCountConfig *-- SubfeatureConfig
```

### `Config` Classes in OGD-Common Library

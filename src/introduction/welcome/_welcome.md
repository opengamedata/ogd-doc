## Welcome

Welcome to the OpenGameData Project!
This website will, at some point, describe all aspects of the OpenGameData tools for collecting, processing, analyzing, and distributing event-based data from educational games and game-like interactive digital media.

## Documentation Organization

The OpenGameData documentation is broken down into 3 *guides*, plus the library API reference docs.
Each guide has one more more units, each made up of several chapters.
Together, the guides describe all parts of the OpenGameData infrastructure.

The guides and units are as follows:

<!-- TODO : update links here -->

* [Introduction & Organization](../index.rst):  
    An overview of the OpenGameData project and documentation.
    1. [Getting Started](../getting_started/index.rst):
        Identify your use case, and which part of the documentation you should read.
* [User Guide](../../guides/user/index.rst):
    User-level documentation. Intended for researchers and analysts who want to use datasets and/or tooling from OpenGameData, without any additional programming work.
    1. [OpenGameData Core Basics](../../guides/user/core/index.rst):  
        The basics of using OpenGameData Core, including configuration and basic data exports.
    2. [Data Types and Logging](../../guides/user/logging/index.rst):  
        A discussion of the OpenGameData Event Schema, and the several software packages used to collect event data.
    3. [OpenGameData Web APIs](../../guides/user/apis/index.rst):  
        Documentation of the OpenGameData Web APIs for data storage and access.
    4. [Data Replay Tools](../../guides/user/replay/index.rst):  
        An introduction to OpenGameData-based tools for data replay.
    5. [Data Analysis & Visualization Tools](../../guides/user/visualization/index.rst):  
        An introduction to OpenGameData-based tools for data analysis, including Jupyter Notebook templates and data dashboards.
* [Game Producer Guide](../../guides/producer/index.rst):
    Documentation for game producers who want to use OpenGameData as a telemetry logging and analytics solution.
    This includes information on how to prepare for logging with your game, and ways for your team to use the collected data.
    1. [Event Logging](../../guides/producer/logging/index.rst):  
        How to identify the events that occur in your game, which can be logged with OpenGameData telemetry tools.
* [Game/Data Engineering Guide](../../guides/engineer/index.rst):
    Documentation for engineers who want to use OpenGameData libraries in their projects and products.
    This includes logging integration in games, and feature extraction modules for game data.
    1. [Event Logging](../../guides/engineer/logging/index.rst):  
        How to use the OpenGameData logging libraries to log telemetry from Unity or JavaScript projects.
    2. [Detectors & Feature Engineering](../../guides/engineer/generators/index.rst):  
        How to write data Generators in OpenGameData Core to create refined analytics from raw event data.
* [OGD Developer Guide](../../guides/developer/index.rst):
    Documentation for developers who want to work on the core OpenGameData libraries and software tools.
    1. [Core Architecture](../../guides/developer/core/index.rst):  
        A comprehensive review of the data processing architecture in OpenGameData Core, including how to integrate Core components into your own 3rd-party tool(s).
    2. [OGD ``Common'' Library](../../guides/developer/common/index.rst):  
        A comprehensive review of the library containing base classes and other utilities used across multiple parts of the OGD software ecosystem.
    3. [OpenGameData Web APIs](../../guides/developer/apis/index.rst):  
        Documentation of the OpenGameData Web APIs for data storage and access.
    4. [Meta-Documentation](../../guides/developer/docs/index.rst):  
        Documentation for contributors working on core OGD infrastructure and documentation, covering topics such as coding conventions and our software reference platform.
* [Core API Reference](../reference/index.rst):  
    API reference for the OpenGameData Core Python package.

## Problems with this Website?

If you encounter any issues with this documentation site, such as missing images or broken links, please feel free to report the issue on our documentation GitHub page:
[Submit an Issue Report](https://github.com/opengamedata/opengamedata-doc/issues/new?assignees=LswaN58&labels=bug&projects=&template=bug_report.md&title=)

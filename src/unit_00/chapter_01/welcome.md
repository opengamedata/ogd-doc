## Introduction

Welcome to the OpenGameData Documentation Project.
This website will, at some point, describe all aspects of the OpenGameData tools for collecting, processing, analyzing, and distributing event-based data from educational games and game-like interactive digital media.

We recommend you check the [getting started](./getting_started.md) page to determine which of the many use-cases supported by the OpenGameData tools apply to you, and by extension, which parts of this website you should read.
The rest of this chapter will introduce you to the structure of our documentation, and briefly introduce you to a few of the tools available from OpenGameData.

### Problems with this Website?

If you encounter any issues with this documentation site, such as missing images or broken links, please feel free to report the issue on our documentation GitHub page:
[Submit an Issue Report](https://github.com/opengamedata/opengamedata-doc/issues/new?assignees=LswaN58&labels=bug&projects=&template=bug_report.md&title=)

### Documentation Organization

The OpenGameData documentation is broken down into 9 *Units*, plus the "Unit 0" containing this introductory material.
Each unit is made up of several chapters.
Together, the units describe all parts of the OpenGameData infrastructure.

The units are as follows:

<!-- TODO : update links here -->

0. [Introduction & Organization](./index.rst):  
    An overview of the OpenGameData project and documentation.
1. [OpenGameData Core Basics](../01_core-basics/index.rst):  
    The basics of using OpenGameData Core, including configuration and basic data exports.
2. [Event Data](../02_events/index.rst):  
    A discussion of the OpenGameData Event Schema, and the several software packages used to collect event data.
3. [Detectors & Feature Engineering](../03_detectors-and-features/index.rst):  
    How to write data Generators in OpenGameData Core to create refined analytics from raw event data.
4. [Core Architecture](../04_core-architecture/index.rst):  
    A comprehensive review of the data processing architecture in OpenGameData Core, including how to integrate Core components into your own 3rd-party tool(s).
5. [OGD ``Common'' Library](../05_ogd-common/index.rst):  
    A comprehensive review of the library containing base classes and other utilities used across multiple parts of the OGD software ecosystem.
6. [OpenGameData Web APIs](../06_apis/index.rst):  
    Documentation of the OpenGameData Web APIs for data storage and access.
7. [Data Analysis & Visualization Tools](../07_analysis-and-visualization/index.rst):  
    An introduction to OpenGameData-based tools for data analysis, including Jupyter Notebook templates and data dashboards.
8. [Meta-Documentation](../08_meta-documentation/index.rst):  
    Documentation for contributors working on core OGD infrastructure and documentation, covering topics such as coding conventions and our software reference platform.
9. [Core API Reference](../reference/index.rst):  
    API reference for the OpenGameData Core Python package.

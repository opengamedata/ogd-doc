# Unit 7, Chapter 6 : Fun Historical Bits

This document just holds bits of historic trivia and code snippets that I find fun in looking back on the development of OpenGameData.

## Model Class Comment

Found this comment left-over from the "Model" class used in the original teacher dashboard, or a near descendant of that class.

```python
## @class Model
#  Abstract base class for session-level Wave features.
#  Models only have one public function, called Eval.
#  The Eval function takes a list of row data, computes some statistic, and returns a list of results.
#  If the model works on features from session data, it should calculate one result for each row (each row being a session).
#  If the model works on a raw list of recent events, it should calculate a single result (each row being an event).
```

Found it really interesting that at the time, it had the option of taking in rows of feature data.
Not sure if we ever really used this or not, but it's cool that we had some version of "second-order features" before we'd ever formalized that idea as something to be done as a main part of our "miniextractors" architecture.

## "Interface" PyProject

During a cleanup of one of the old server directories that once ran a copy of `opengamedata-core`, I rediscovered that at some point there was an attempt to set up a package for the OGD interface classes as its own separate package for inclusion in other projects, with a `setup.cfg` as shown below.
This would have pre-dated the "real," successful creation of the `OGDUtils` and `opengamedata-core` packages by a couple years - the `pyproject`-related files were dated 09/23/2021.

```toml
[metadata]
name = opengamedata-interfaces
version = 0.0.1
author = Luke Swanson
author_email = swansonl@cs.wisc.edu
description = Data Interfaces package for OpenGameData.
long_description = Data Interfaces package for OpenGameData.
url = https://github.com/opengamedata/opengamedata-core/tree/master/interfaces/
project_urls =
    Bug Tracker = https://github.com/opengamedata/opengamedata-core/issues
classifiers =
    Programming Langauage :: Python :: 3
    License :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find
python_requires = >= 3.6

[options.packages.find]
where = src
```

## Testing Structure for Python Projects

We use Python's built-in `unittest` library as our testing framework, as it gives us:

* Straightforward compatibility with base Python
* Clear class and function structures for organizing tests

In general, the structures we have to use for organizing our tests are as follows:

1. Folders & Files
2. `unittest` Classes (`TestBed` and `TestCase`)
3. Individual Test Methods

The rest of this section describes how we use map various Python/project entities to those testing structures.

### Folder & File Structure

Every project has a `src` folder containing the direct source code for the project, and a `tests` folder housing tests of that source code.
The `tests` folder should in turn have a standard set of subfolders:

```md
- tests
  - cases
  - config
  - data (optional)
```

* The `cases` folder contains all the code for individual test cases, test suites, etc.
* The `config` folder contains any configuration for the test harness, including any classes for configuring the tests.
For example, the an API project may have a custom configuration to set the API base URL for remote tests.
Both the config itself, and any custom class definitions (e.g. an `APIConfig.py` file), belong in `config`.
* The `data` folder is optional, and is the place to store any data loaded by the tests themselves.  
**Note**: in the case where we are writing tests for configuration classes, any config files loaded for the sake of testing belong in the `data` folder;
the `config` folder is reserved for configuration of the test harness itself.

Within `src`, our projects typically group Python code into a few folder levels, typically in accordance with inheritance trees.
Folders under `cases` should approximately mirror the folders under `src`.
For example, the `src` folder structure of `ogd-common` looks something like:

```md
- src
  - ogd
    - commmon
      - configs
      - filters
      - models
      - schemas
      - storage
        - connectors
        - interfaces
        - outerfaces
      - ... etc.
```

Then the folder structure for `cases` should have an identical structure, for ease of navigation; the exception is that we can omit the "singleton" folders that exist only for namespacing in the Python package:

```md
- tests
  - cases
    - configs
    - filters
    - models
    - schemas
    - storage
      - connectors
      - interfaces
      - outerfaces
    - ... etc.
  - config
  - data
```

The standards for file and folder structure _within_ this mirrored structure will be developed further in the remaining sections.
For the TL;DR version, jump straight to [Full Outline of Python Testing Structure](#full-outline-of-python-testing-structure)

### `unittest` Classes

The two major classes we can use for testing within the Python `unittest` framework are `TestSuite` and `TestCase`.

The `unittest` framework is apparently based on the [Beck Testing Framework](https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm), which broadly defines terms **Test Fixture** as a single configuration of a software module, and **Test Case** as a "stimulus" of a **Fixture**.
Beck conceptualizes a `TestCase` class, which is subclassed for each **Fixture** one wishes to test.
The **Test Fixture** is implemented by setting instance variables (roughly equivalent to a constructor), and each **Test Case** stimulus is implemented as a method of the `TestCase` subclass (with one or more **Checks** at the end of the method).

In `unittest`, then, we use `TestCase` subclasses to create **Fixtures**, and functions within the subclasses to implement **Cases**.
Then we use `TestSuite` to collect together multiple `TestCase`s.
The `unittest` framework provides reasonable test discovery features to generate a `TestSuite` for us, so we use those features instead of hardcoding a suite directly.
In practice, then, we create a series of `TestCase` subclasses for each class or standalone module in the project.
Each class/module's collection of `TestCase` subclasses goes in a single subfolder of the structure outlined above, and test discovery can be pointed at the folder to find the `TestCase`s.

#### Complexities of Testing Complicated Classes

This is all a fairly straightforward use of `unittest`, similar to what you'd find in any tutorial or intro walkthrough.
However, for a large codebase (or set of codebases), there are inevitably more complex cases that arise.
In particular, we've faced the issue where many test-worthy configurations of a class share what feels like 99% similarity with most of the other configurations, 99% similarity in what tests to run, but the 1% difference requires them to be different cases.

For example, consider one of the `Config` subclasses in `ogd-common`.
These each track various properties for configuration of some other class.
Some of these properties are optional, and all are meant to have some meaningful default value.
They are meant to be loadable from a variety of sources, and there is complex parsing logic to support this variety of source loading.
Typically, then, we would want to test loading similar data and checking for similar results, but never quite the _same_ results.

Our solution to this will be to insert an intermediate class between our "true" **Test Fixture** classes and the `TestCase` base class.
This intermediate class would implement the `SetUp` function to prepare a "base" **Fixture**, and then the true **Test Fixture** implementation will use the `SetUp` function to call the `super` version, before making whatever small tweak is needed to prepare the fixture.

In this way, we don't need excessive copy-pasting of **Fixture** preparation between very similar `TestCase` classes.
We will make these abstract, general descriptions of approach a more concrete treatment in the final section of this outline.

#### Naming Conventions

The folder containing all `TestCase` subclasses for a given class or module of the project should have a format like `<ModuleName>Suite`.
That is, it should have the name of the module, followed by the word "Suite."

Each `TestCase` subclass should have a name that describes the **Fixture** it implements, followed by the word "Case."
For example, if the **Fixture** is testing the class with all default values, the `TestCase` subclass could be `DefaultCase`.
If the **Fixture** is testing the class with a configuration for, say, a specific game (say Aqualab), then the subclass could be `AqualabCase` or similar.

In cases where we have an intermediate base class for a set of **Cases**, the "decription" part of the name should be a reasonable summary of the commonality between the **Cases**, and end in the word "Cases."
For example, if we have a collection of **Cases** related to using slight variations of configurations for different games, the base class could be `GameConfigCases`, and the "true" **Fixture** classes might be `AqualabCase`, `AstroCase`, etc.

#### Common Cases

There are a few basic **Fixtures** that appear quite frequently in our test suites, which we outline below:

* `BasicInitCase` : Very common **fixture** for config/schema-related classes. In this case, we provide a very basic, non-specific set of args to the class, and use them to test Properties and other "getter"-style functions.
* `EmptyCase`: A **fixture** in which no instance of the class is initialized. Used to test initialization functions, such as functions to create an instance from a loaded file.
* `StaticCase`: Related to the `EmptyCase`, this is a sort of non-**fixture** used for standalone modules that only contain functions, or utility classes with only static methods.
    * The `StaticCase` has a special violation of normal conventions.
      We create a `StaticCase.py` file, but instead of placing a single `StaticCase` class within, we create multiple `<FunctionName>Case` classes, each dedicated to testing a single function of the module (or class).
* `DefaultCase` : A **fixture** in which we initialize an instance only with class defaults, i.e. with an empty constructor call or with a call to a `.Default()` function.

### Individual Test Methods

Each test method in a `TestCase` subclass should represent a single call of a method of the class being tested, followed by as many **Checks** of the state of the class instance as needed to assure a correct result.
This means we don't, for example, call a function, check the result, and call another following function for further checks.

The name of each test method should have a prefix `test_`, and the remainder of the name should describe the **Stimulus** (i.e. which method we're calling), and something about the expected outcome.

For example, if we're writing an API test for requesting info on a game that does not exist, the full method name might be `test_get_game_not_exists`.
Note that, due to a strong existing convention with the `unittest` framework, we break from our standard function naming conventions and use snake_case instead of pascalCase or CamelCase.

### Full Outline of Python Testing Structure

Compiling the discussions of the three different levels of testing structure and convention, we can finally summarize our Python testing standard:

* We use `unittest` for testing.
* The `tests` folder should include subfolders for `cases` and `config`.
* The folder structure of `tests/cases` should mirror `src`, except for "singleton" folders (folders that exist alone inside the parent folder) that exist only for package namespacing.
* Each Python module (i.e. each `.py` file) should have its own subfolder in the structure, called `<ModuleName>Suite`, containing:
  * `<CaseName>Case.py` files for each **Fixture** being tested, containing a `TestCase` subclass.
  * `<GroupName>Cases.py` files wherever multiple closely-related **Fixtures** are implemented as a group under a common `TestCase` subclass.
* Each individual `TestCase` subclass should implement one test function per **Stimulus** of the **Fixture**, with as many **Checks** as needed. In other words, there should _not_ be individual test functions that each call the same method in the same way only to run a slightly different assert on the result.
* Test functions should have names formatted like `test_<description_of_test>`.

### Typical Structure of a `TestCase` subclass

The following example demonstrates, with inline notes in the comments, a typical structuring of the file containing a single `TestCase` subclass.

```python
# import standard libraries
import unittest
from unittest import TestCase
# import OGD library modules as needed, e.g. to set up logging
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# import the module being tested, through src.path.to.module.
# this ensures the test looks for the local file and not any installed copy.
from src.ogd.core.configs.generators.ExtractorConfig import ExtractorConfig
# import local test config
from tests.config.t_config import settings

def setUpModule():
    """Use setUpModule to initialize anything outside of the class, typically test configuration.
    """
    cfg   = TestConfig.FromDict(name="SchemaTestConfig", unparsed_elements=settings)
    level = logging.DEBUG if cfg.Verbose else logging.INFO
    Logger.std_logger.setLevel(level)

class BasicInitCase(TestCase):
    """Describe the test case broadly. In this case, we have a simple, hardcoded set of initialization params.
    
    Fixture:
    * Specify details of the test fixture captured by this case.
    
    Case Categories:
    * List the broad categories of test cases here. e.g. "Properties," "API request functions," etc. Include a one-sentence explanation of each.
    """

    @classmethod
    def setUp(self) -> None:
        """Set up the test fixture.
        """
        elems = {
            "threshold": 30,
            "enabled": True,
            "type": "ActiveTime",
            "description": "Active time of a player",
            "return_type": "timedelta",
            "subfeatures": {
                "Seconds": {
                    "description": "The number of seconds of active time.",
                    "return_type": "int"
                }
            }
        }
        self.instance = ExtractorConfig(
            name="ExampleConfig",
            unparsed_elements=elems
        )

    # *** Write individual test functions ***

    def test_Name(self):
        _str = self.test_schema.Name
        self.assertIsInstance(_str, str)
        self.assertEqual(_str, "ExampleConfig")

    def test_TypeName(self):
        _str = self.test_schema.TypeName
        self.assertIsInstance(_str, str)
        self.assertEqual(_str, "ActiveTime")
    
    # etc.
```

## Running Tests

When running locally, executing tests typically takes the form of running the following from the project root directory:

```bash
python -m unittest discover -t "./" -s "./tests/cases/<path>/<to>/<module_tests>/" -p "*Case.py"
```

Here, `-t` is used to indicate the top-level folder of the project (change as needed if running from a directory other than the top-levelfolder itself), `-s` is used to indicate the specific directory in which to search for tests, and `-p` is a pattern for selecting files in the directory to search. In this way, you can run the tests for any module in the project.

FOr a concrete example, consider the `DataTableConfig` class in `ogd-core`. In this case, the appropriate command, run from the `ogd-core/` base folder, is:

```bash
python -m unittest discover -t "./" -s "./tests/cases/configs/DataTableConfig/" -p "*Case.py"
```

Most IDEs have some form of built-in test explorer.
Refer to the documentation for your IDE of choice to determine how to configure the test discovery features of the built-in test explorer, if it exists.
In Visual Studio Code, it is usually sufficient to ensure the Python language extension is installed and active.
We use `unittest` test discovery in our GitHub automations to run tests as needed.

## Install OpenGameData

Once you have a valid Python installation on your system, you are ready to get **OpenGameData** itself installed.
Specifically, you'll be installing `opengamedata-core`, the tool that contains all the core data post-processing logic for generating post-hoc events and extracting feature data from a series of events.
It also serves as an effective way to export event data from a database of OGD-structured event data.

There are two approaches to getting/installing `opengamedata-core`:  
As a package, and as a local copy.

### Installation as Package

This is the approach to take if you are going to directly call `opengamedata-core` functions, e.g. in your own Python-based tool.

*Note* : In the future, the `opengamedata-core` Python package will support directly running data exports via command line. However, this feature is not yet implemented, so any data exports *must* be conducted with a local source copy.

Package-based installation is quite simple:  
The `opengamedata-core` package is hosted on the [**PyPi** package repository](https://pypi.org/project/opengamedata-core/).
To install, you need only invoke the `pip` Python package installer, as follows:

```bash
> pip install opengamedata-core
```

This will install the package in your Python environment, and you can then import any `core` modules from the `ogd.core` namespace.  
For example:

```python
from ogd.core.models.Events import Event
```

#### Installing a Specific Version

If for any reason you need a specific version of the package, simply use the `pip` syntax for version specificatino.  
For example, to install version 0.0.12:

```bash
> pip install opengamedata-core==0.0.12
```

### Installation as Local Source Copy

This is the approach to take if you need to run data exports, or intend to develop new data generation modules, such as [event detectors or feature extractors](../../03_detectors-and-features/index.rst).

In this case, you will get a local copy of the full `opengamedata-core` source code from the [**GitHub** repository](https://www.github.com/opengamedata/ogd-core).
You will also install the necessary libraries to run `opengamedata-core` exports.

**GitHub** is built for use with `Git`, a popular version control system we use for source control and distribution.
While it is possible to download and use the **OpenGameData** source without `Git`, we strongly recommend using `Git` to obtain the source.
This will allow you to track any changes you make, and to optionally contribute your changes back to the **OpenGameData** community.  
We *strongly* recommend [installing and using Git](#install-git) so that you can keep your OpenGameData code up-to-date, and participate in the OpenGameData community by contributing your innovations back the public.

#### Download or Clone OpenGameData

To actually get your copy of the source code, visit the home tab of the [`opengamedata-core` repository](http://www.github.com/opengamedata/ogd-core) on **GitHub**.
The page you see should look similar to the image below.

![GitHub interface for `opengamedata-core` repository](../../../assets/images/figures/ogd-core-github-main.png)

Notice the green "Code" button.
Click this, and ensure the "Local" tab is selected in the pop-up.
You will see a list of options.

![GitHub options for downloading `opengamedata-core`](../../../assets/images/figures/ogd-core-github-download-options.png)

If you want to simply download a copy *without* `Git`, select the "Download ZIP" option.
Save the `.zip` file to the folder you want to contain the copy of `opengamedata-core` code, and unzip the file there.

If you want to use `Git`, you can copy the link (`git@github.com:opengamedata/opengamedata-core`).
Then open a command line in the folder you want to contain the copy of the `opengamedata-core` code, and run the following, substituting the actual link you copied in place of `<GitHub link>`:

```bash
git clone <GitHub link>
```

This will copy all code into a new subfolder named `opengamedata-core`.

#### Install Python Libraries

<font style="color:tomato">STUB: This section is on the to-do list.</font>

## Other Tools

### Install Git

This step is necessary if you would like to submit changes back to the OpenGameData community for inclusion in the public repository.

We do not specify a minimum (or maximum) recommended version of `Git` to use.
You can obtain a `Git` installer from <https://git-scm.com/downloads>.  
If you are not comfortable working from a command line, consider downloading an installer for a GUI client (included in the linked page above).  

<font style='color:tomato'>TODO: add some recommendations for any customization options in installer.</font>  

## Build

### **Sphinx**

We use the **Sphinx** system to build the `opengamedata-doc` documentation from source into a usable HTML website.
The **Sphinx** build process is configured in `source/conf.py`
There's nothing particularly special about our configuration, but you can read about **Sphinx** configuration generally on the [sphinx-doc](https://www.sphinx-doc.org/en/master/usage/configuration.html) website.

We use several **Sphinx** extensions to support building various implementation languages into our documentation.
We will link to individual extensions' pages as they are discussed below; for general information on **Sphinx** extensions, see the sphinx-doc [extensions page](https://www.sphinx-doc.org/en/master/usage/extensions/)

#### **sphinx-apidoc**

We use the `sphinx-apidoc` command to prepare/update the reference section of the documentation from submodules containing the code from the various OpenGameData Python repositories.

We do the following, for example, to document the `ogd.core` module:

```bash
  > sphinx-apidoc -o src/reference/core --tocfile index-core --remove-old --implicit-namespaces opengamedata-core/src/ogd/
```

### **readthedocs**

Our build and deploy process uses the **readthedocs** provider to build and host our documentation project.
The `opengamedata-doc` repository communicates with **readthedocs** via a **GitHub** webhook.
Any changes pushed to the `opengamedata-doc` repository will trigger an automatic build and update on **readthedocs**.

### Submodules

At times, it is useful to include submodules in the `opengamedata-doc` repository, which contain code or documentation that can be parsed or otherwise included by the main Sphinx project.
Existing examples include the `opengamedata-core` and `platform` submodules included in the base `opengamedata-doc` directory.

While these are useful, it is important to note that when adding the submodule from a repository on GitHub:

```bash
> git submodule add <repository GH URL> <folder name>
```

You must use the `https` URL, not the more-common `ssh` URL.
If you use the `ssh` URL, the automatic build on **readthedocs** will fail on its `git submodule update` step, with a permissions error.

## Project Structures

### Project Naming Conventions

Projects should follow the naming convention `opengamedata-<subproject-name>`, where `<subproject-name>` is a specific name for the sub-project.
Multi-word project names should be dash-separated.

### File and Folder Structures

For standard projects, the following top-level folder structure should be used:

* .github
  * actions
    * Specific folders for project-specific custom actions
  * workflows
    * GitHub Actions workflow files
* src
  * All folders and files containing source code for the project
* tests
  * All folders and files containing unit and other tests for the project
* .gitignore
* LICENSE
* README.md

Any other project management files, such as a `pyproject.yml` for Python library projects, should go in the top-level folder alongside the license and readme.
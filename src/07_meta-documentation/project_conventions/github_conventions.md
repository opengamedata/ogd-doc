## GitHub Actions Conventions

### Workflow Naming

The naming convention for workflow files is to use an all-caps prefix indicating the general function of the workflow, joined by an underscore to a specific workflow name.

Typical prefixes include:

* `DEPLOY` : A script to deploy the project to a server or distribution site
* `CI` : A high-level script to run tests on a given development branch
* `TEST` : A "reusable workflow" script to run a specific testbed, which is typically called from a CI script (but may also run independently)

Generally, a `DEPLOY` or `CI` script's name will simply reflect the name of the project, for a name of the form `DEPLOY_<project-name>.yml` or `CI_<project-name>.yml`.
A `TEST` script's name should reflect the specific component checked by the testbed; for example, `TEST_api-response.yml`.
Then the general form is `TEST_<component-name>.yml`
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

#### Human-Readable Workflow Names

Within the workflow file, each workflow should use the `name` and `run-name` settings to create human-readable titles for the workflow runs as displayed in GitHub.
The general format for each is as follows:

1. `name: <Project Title> - <Workflow Function> Script`  
  For the base human-readable name, we use a dash separation between a project title and a title for the script itself.
  The script title here should be a brief title, followed by the word "Script."  
  Full example: `name: OGD Website - Release Script`
2. `run-name: ${{ format('{0} - {1}', github.workflow, github.event_name == 'push' && github.event.ref || 'Manual Run') }}`  
  For the human-readable title of the specific workflow run, we effectively append another dash-separated portion onto the base name.
  This will be either the GitHub "ref" if the workflow was triggered "normally," e.g. by a push, or the string 'Manual Run' if the workflow was manually triggered.
  Alternately, if there are multiple automatic triggers, the second parameter could theoretically be modified to `github.event_name == 'workflow_trigger' && 'Manual Run' || github.event.ref`.
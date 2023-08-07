# readme-to-test

A simple README to explain the tests flow.


## Installation

If you didn't follow the instruction on the main [README](../README.md).

Please run:

`make install` from the root of this project
```
Make install will install all the requirements in your local machine that you can use to run some make commands such as:

 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format
```

## Set up to run tests

Install get_token
-----------------------
You need an Apigee access token to run tests. `APIGEE_ACCESS_TOKEN` environment variable must contain this access token. In order to
get apigee access token you need `acurl` and a utility script called `get_token`. To install acurl and get_token:

1. Create an `install` directory on your machine or use the default usr/local/bin directory.
2. Download the installation ZIP file from Apigee:

`curl https://login.apigee.com/resources/scripts/sso-cli/ssocli-bundle.zip -O`

3. Unzip the downloaded file.
4. Execute the install script:

`sudo ./install -b /usr/local/bin`

<sub>The -b option specifies the location of the executable files. If you do not specify this option, the install script installs the utilities in /usr/local/bin.<sub>

5. Test the installations:

 `   acurl -h
    get_token -h`


If the install is successful, these commands return Help text for the utilities.

More info can be found at [get_token](https://docs.apigee.com/api-platform/system-administration/auth-tools#install).

Setup environment variables
-----------------------

Tests rely on environment variables being set.

Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

Variables you will require
- `ENVIRONMENT` e.g. internal-dev
- `APIGEE_USERNAME` - your username eg. ryan.thomas5@nhs.net
- `SSO_LOGIN_URL` - https://login.apigee.com
- `APIGEE_ACCESS_TOKEN` - `get_token -u ryan.thomas5@nhs.net`
- `PROXY_NAME=reasonable-adjustment-flag-$(APIGEE_ENVIRONMENT)`

You will also require some keys and secrets for some of the tests, these values can be found in AWS Secret Manager (please see .env.sample file in this directory for the Secret Manager paths)
- `INTERNAL_TESTING_WITHOUT_ODS_KEY`
- `INTERNAL_TESTING_WITHOUT_ODS_SECRET`
- `INTERNAL_TESTING_WITHOUT_ASID_KEY`
- `INTERNAL_TESTING_WITHOUT_ASID_SECRET`

If running tests against a deployed PR on internal-dev or internal-dev-sandbox environments `PROXY_NAME` and `ENVIRONMENT` will be as follows:

For internal-dev:
- `PROXY_NAME=reasonable-adjustment-flag-pr-$(PR_NO)` e.g. reasonable-adjustment-flag-pr-92
- `ENVIRONMENT=internal-dev`

Or for internal-dev-sandbox
- `PROXY_NAME=reasonable-adjustment-flag-pr-$(PR_NO)-sandbox` e.g. reasonable-adjustment-flag-pr-92-sandbox
- `ENVIRONMENT=internal-dev-sandbox`


## Command line

How to run the tests.
After you have sourced your environment variables, you can use the make targets defined in Makefile while in this directory

To run all tests
```
make run
```

[Pytest](https://docs.pytest.org/en/6.2.x/) allows us to use [markers](https://docs.pytest.org/en/6.2.x/example/markers.html) to decorate a test method. This way we define the scope of our tests.

To run a tests with specific markers eg. tests marked with 'integration'
```
make run-integration
```

you can use the marker listed in the [pytest.ini](../pytest.ini)


## TROUBLESHOOTING

 * If the test fail, check the following:

   - Are the environment variables been set?
   - Make sure your detail on the environment variables is the correct ones.
   - Make sure you run the commands to run the test inside the `api_tests/` folder.

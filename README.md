# Conduit Testing

This repo contains tests that are to be run whenever a version of
Conduit is deployed.

## Requirements

This project using Python 3.6.4 or greater and uses [Pipenv](https://pipenv.readthedocs.io/en/latest/)
to manage dependencies. To get started using this project, please
do the following

1. Make sure you have Python 3.6.4 or greater installed
2. Follow the instructions for Pipenv to install it
3. From inside this directory type the command `pipenv install`
4. Activate the Python environment with the command `pipenv shell`

You will also need the following:

* 2 sets of login/password credentials for accessing Phabricator in whatever evironment
you are testing in
* 2 sets of login/password credentials that are allowed to create, read, update, and delete security bugs on BugZilla in whatever environment you are testing
* 1 additional set of login/password credentials that are not allowed to access security bugs on BugZilla in whatever environment you are testing

This project uses [dotenv](https://github.com/theskumar/python-dotenv) to store credentials
and other values needed by the tests. Refer to the instructions for `python-dotenv` for
details on how it works and check the `.env-dist` file for the values that you need to set.

If you are going to run these tests on a build server, please consult the documentation for
that specific build server on how to set the environment variables this test is expecting to
exist.

## Running the tests

To run the tests, use the following command:

`pytest tests/`



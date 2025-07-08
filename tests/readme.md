This folder contains tests based on Python unittest. Tests are run from the root of the repo (pyfwimagebuilder not pyfwimagebuilder/pyfwimagebuilder or pyfwimagebuilder/pyfwimagebuilder/tests)

To run all tests:
~~~~
\pyfwimagebuilder>pytest
~~~~

To run a specific tests use the -k option of pytest to use a substring expression to mask tests.
For example to run all tests in test_cli_certificate.py:
~~~~
\pyfwimagebuilder>pytest -k test_cli
~~~~
To run a specific test:
~~~~
\pyfwimagebuilder>pytest -k test_pubkey_read_ok
~~~~

To get logging output when running tests use the --log-cli-level option.
Note that the -s option must also be added to get any printout from pytest
For example to turn on INFO level logging:
~~~~
\pyfwimagebuilder>pytest --log-cli-level INFO -s
~~~~

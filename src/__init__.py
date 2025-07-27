[pytest]
minversion = 6.0
testpaths = tests
python_files = test_*.py *_test.py
python_functions = test_*
addopts = -ra -q
pythonpath = src
log_cli = true
log_cli_level = INFO
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
markers =
    smoke: quick checks before full test runs
    integration: tests involving multiple modules
filterwarnings = ignore

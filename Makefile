TARGET?=test_default_python

test_default_python:
	PYTHONPATH=".:./src" py.test -v

compile:
	@echo Compiling python code
	python -m compileall src/

compile_optimized:
	@echo Compiling python code optimized
	python -O -m compileall src/

coverage:
	coverage erase
	PYTHONPATH=".:./src" coverage run --source='src' --omit='src/test.py,src/fakecube.py' --branch tests/__main__.py
	coverage report -m

travis: compile compile_optimized test_default_python coverage

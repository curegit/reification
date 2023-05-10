.PHONY: build install clean test

build: clean
	python3 -m build

install: build
	pip3 install .

clean:
	python3 -c 'import shutil; shutil.rmtree("dist", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("build", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("reification.egg-info", ignore_errors=True)'

test:
	python3 -m unittest discover tests

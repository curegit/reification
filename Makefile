.PHONY: build install clean test

build: clean
	python -m build

install: build
	echo

clean:
	python -c 'import shutil; shutil.rmtree("dist", ignore_errors=True)'

test:
	python -m unittest discover tests

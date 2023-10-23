.PHONY: build install preview publish clean test

build: clean
	python3 -m build

install: build
	pip3 install .

preview: build
	python3 -m twine upload --repository-url "https://test.pypi.org/legacy/" dist/*

publish: build
	python3 -m twine upload --repository "https://upload.pypi.org/legacy/" dist/*

clean:
	python3 -c 'import shutil; shutil.rmtree("dist", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("build", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("reification.egg-info", ignore_errors=True)'

test:
	python3 -m unittest discover -v tests

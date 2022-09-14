VERSION=1.0.0

PY_COMPILE_BIN=python -m py_compile

#BUILD_BIN=python -m build
BUILD_BIN=pyproject-build

#UNITTEST_FILE_BIN=python -m unittest
#UNITTEST_DIR_BIN=python -m unittest discover --top-level-directory .
UNITTEST_FILE_BIN=unittest --color
UNITTEST_DIR_BIN=unittest --color --working-directory .

#MYPY_BIN=python -m mypy
MYPY_BIN=MYPY_CACHE_DIR=hist/__mypycache__ mypy

#PIPX_BIN=python -m pipx
PIPX_BIN=pipx

.PHONY: clean
clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build *.egg-info

hist/cli.py: hist/cli.toml
	gap hist/cli.toml --no-debug-mode --output=hist/cli.py

.PHONY: test
test:
	$(PY_COMPILE_BIN) hist/*.py
	$(MYPY_BIN) -p hist

PY_FILES=hist/cli.py hist/__main__.py hist/histogram.py
PYBUILD_FILES=pyproject.toml LICENSE.md README.md

build/hist-$(VERSION)-py3-none-any.whl: $(PY_FILES) $(PYBUILD_FILES)
	mkdir -p build
	$(BUILD_BIN) --wheel --no-isolation --outdir build/

.PHONY: build
build: build/hist-$(VERSION)-py3-none-any.whl

.PHONY: reinstall
reinstall: uninstall install

.PHONY: install
install: build/hist-$(VERSION)-py3-none-any.whl
	$(PIPX_BIN) install build/hist-$(VERSION)-py3-none-any.whl

.PHONY: uninstall
uninstall:
	$(PIPX_BIN) uninstall hist


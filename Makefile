.DEFAULT_GOAL := help
SHELL := bash

DUTY = $(shell [ -n "${VIRTUAL_ENV}" ] || echo pdm run) duty

args = $(foreach a,$($(subst -,_,$1)_args),$(if $(value $a),$a="$($a)"))
check_quality_args = files
docs_serve_args = host port
release_args = version
test_args = match

BASIC_DUTIES = \
	changelog \
	check-dependencies \
	clean \
	coverage \
	docs \
	docs-deploy \
	docs-regen \
	docs-serve \
	format \
	release \
	tox

QUALITY_DUTIES = \
	check-quality \
	check-docs \
	check-types \
	test

.PHONY: help
help:
	@$(DUTY) --list

.PHONY: lock
lock:
	@pdm lock

.PHONY: check
check:
	@$(DUTY) check-quality check-types check-docs check-dependencies


.PHONY: install
install:
	pdm install
	conda create --prefix ./.venv python=3.11
	conda activate ./.venv
	conda env update --file conda-dependencies.yml --prune

.PHONY: uninstall
uninstall:
	rm -rf .coverage*
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf tests/.pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -rf pip-wheel-metadata
	rm -rf site
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type d -name __pypackages__ | xargs rm -rf
	find . -name '*.rej' -delete
	find . -name pdm.lock -delete
	find . -name .pdm.toml -delete


.PHONY: $(BASIC_DUTIES)
$(BASIC_DUTIES):
	@$(DUTY) $@ $(call args,$@)

.PHONY: $(QUALITY_DUTIES)
$(QUALITY_DUTIES):
	pdm run duty $@ $(call args,$@)

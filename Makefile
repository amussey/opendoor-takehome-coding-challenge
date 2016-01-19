SHELL := /bin/bash
MAKEFILE_RULES := $(shell cat Makefile | grep "^[A-Za-z]" | awk '{print $$1}' | sed "s/://g" | sort -u)
PYTHON_ENV := $${PYTHON_ENV_LOCATION-"./env"}
PYTHON_REQUIREMENTS := $${PYTHON_REQUIREMENTS_FILE-"./requirements.txt"}


DEFAULT: help

virtualenv:  ## Build the Python virtual environment.
	@echo -e "Building/verifying virtualenv at $(PYTHON_ENV) based on $(PYTHON_REQUIREMENTS)\n"
	@command -v pip >/dev/null 2>&1 || { echo >&2 "I require pip but it's not installed.  Aborting."; exit 1; }
	@if [ ! -f "$(PYTHON_ENV)/bin/activate" ] ; then \
	     virtualenv $(PYTHON_ENV) ; \
	fi
	@source $(PYTHON_ENV)/bin/activate ; \
	pip install -q -r $(PYTHON_REQUIREMENTS)

.PHONY: lint
lint:  ## Perform the linting tasks.
lint: pylint

.PHONY: pylint
pylint:  ## Lint the Python files.
pylint: virtualenv
	@source $(PYTHON_ENV)/bin/activate ; flake8 -v *.py api/

.PHONY: help
help:  ## This help dialog.
	@echo -e "         ___  ___ ___ _  _ ___   ___   ___  ___        " ; \
	echo -e  "        /   \| _ \ __| \| |   \ /   \ /   \| _ \       " ; \
	echo -e  "       | (_) |  _/ _|| .  | |) | (_) | (_) |   /       " ; \
	echo -e  "        \___/|_|_|___|_|\_|___/ \___/_\___/|_|_\       " ; \
	echo -e  "       |   \| __\ \ / / __| |  /   \| _ \ __| _ \      " ; \
	echo -e  "       | |) | _| \ V /| _|| |_| (_) |  _/ _||   /      " ; \
	echo -e  "       |___/|___|_\_/_|___|____\___/|_| |___|_|_\      " ; \
	echo -e  "                |_   _| __/ __|_   _|                  " ; \
	echo -e  "                  | | | _|\__ \ | |                    " ; \
	echo -e  "                  |_| |___|___/ |_|                    " ; \
	echo -e  "                                                       " ; \
	echo -e  "  You can run the following commands from this$(MAKEFILE_LIST):\n"
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`) ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf "  %-27s %s\n" $$help_command $$help_info ; \
	done

SHELL := /bin/bash # Tell Make this file is written with Bash as shell
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c # Bash strict mode
.DELETE_ON_ERROR:   # if a Make rule fails, it’s target file is deleted
.DEFAULT_GOAL := help
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


WORKDIR = $(shell pwd)
# Get package name from pwd
PACKAGE_NAME := $(shell basename $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))
VENV = .venv
VENV_DIR=$(WORKDIR)/${VENV}
VENV_BIN=$(VENV_DIR)/bin
PYTHON=${VENV_BIN}/python3
PIP=$(VENV)/bin/pip

GITIGNORE_PKGS=venv,python,JupyterNotebooks,Pycharm,VisualStudioCode,macOS
REPO_NAME=

SODA_IMAGE  = soda_checks
SODA_DOCKERFILE_DIR = src/soda
AIRFLOW_DOCKERFILE_DIR = src/docker
AIRFLOW_SCHEDULER=airflow-webserver


#################################### Functions ###########################################
# Function to check if package is installed else install it.
define install_pip_pkg_if_not_exist
	@for pkg in ${1} ${2} ${3}; do \
		echo ${1} ${2} ${3}
		# if ! command -v "$${pkg}" >/dev/null 2>&1; then \
		# 	echo "installing $${pkg}"; \
		# 	$(PYTHON) -m pip install $${pkg}; \
		# fi;\
	done
endef

# Function to create python virtualenv if it doesn't exist
define create-venv
	$(call install_pip_pkg_if_not_exist,virtualenv)

	@if [ ! -d ".$(PACKAGE_NAME)_venv" ]; then \
		$(PYTHON) -m virtualenv ".$(PACKAGE_NAME)_venv" -p $(PYTHON) -q; \
		.$(PACKAGE_NAME)_venv/bin/python -m pip install -qU pip; \
		echo "\".$(PACKAGE_NAME)_venv\": Created successfully!"; \
	fi;
	@echo "Source virtual environment before tinkering"
	@echo -e "\tRun: \`source .$(PACKAGE_NAME)_venv/bin/activate\`"
endef

########################################### END ##########################################

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

check:
	@echo "www.gitignore.io/api/venv,python,JupyterNotebooks,Pycharm,VisualStudioCode,macOS"


boilerplate:  ## Add simple 'README.md' and .gitignore
	@echo "# $(PACKAGE_NAME)" | sed 's/_/ /g' >> README.md
	@curl -sL https://www.gitignore.io/api/$(GITIGNORE_PKGS)> .gitignore

# ------------------------------------ Version Control -----------------------------------

git_init:  ## Create a new git repository and add boilerplate code.
	@git init -q
	@$(MAKE) -C $(CURDIR) boilerplate
	@git add .gitignore README.md
	git commit -nm'Add README and .gitignore files <automated msg>'

gh_init:
	gh repo create --public testRepo

$(ENV)/bin/activate: requirements.txt ## create virtual environment
	python3 -m venv $(ENV) \
		&& chmod +x $(VENV)/bin/activate \
		&& . ./$(VENV)/bin/activate \
		&& $(PIP) install -r requirements.txt

#venv: $(VENV)/bin/activate  ## activate virtual environment
#    . ./$(VENV)/bin/activate
#


venv-install: requirements.txt
	$(PIP) install -r requirements.txt

.PHONY: clean
clean:
	rm -rf __pycache__ *.pyc .pytest_cache;

.PHONY: clean-all
clean_all: ## cleanup files and remove virtual environment
	rm -rf __pycache__ *.pyc .pytest_cache;
	rm -rf $(VENV) || exit 0

.PHONY: airflow-start
airflow_start: ## start airflow containers
	docker compose -f ./$(AIRFLOW_DOCKERFILE_DIR)/docker-compose.yaml up -d

.PHONY: airflow-stop
airflow_stop: ## stop airflow containers
	docker compose -f ./$(AIRFLOW_DOCKERFILE_DIR)/docker-compose.yaml down

.PHONY: airflow-bash
airflow_bash: ## start airflow bash shell
	docker compose -f ./$(AIRFLOW_DOCKERFILE_DIR)/docker-compose.yaml exec -it $(AIRFLOW_SCHEDULER) /bin/bash

.PHONY: airflow-img
airflow_img: $(shell find src/docker -type f) ## build docker image for airflow
	docker compose build --no-cache

.PHONY: soda-img
soda_img: $(shell find src/soda -type f) ## build docker image for soda checks
	docker build -f $(SODA_DOCKERFILE_DIR)/Dockerfile -t $(SODA_IMAGE) .

.PHONY: meta-start
meta_start: ## start metabase docker container
	docker compose -f $(AIRFLOW_DOCKERFILE_DIR)/docker-compose.viz.yaml up -d

.PHONY: start
start:
	docker compose -f ./$(AIRFLOW_DOCKERFILE_DIR)/docker-compose.yaml -f $(AIRFLOW_DOCKERFILE_DIR)/docker-compose.viz.yaml up -d

.PHONY: stop
stop:
	docker compose -f ./$(AIRFLOW_DOCKERFILE_DIR)/docker-compose.yaml -f $(AIRFLOW_DOCKERFILE_DIR)/docker-compose.viz.yaml down

.PHONY: test
test:
	docker compose -f $(AIRFLOW_DOCKERFILE_DIR)/docker-compose.test.yaml up

SHELL=/bin/bash -euo pipefail

# make entrypoints for this API .. currently required by the common build pipeline are,  install, lint, publish, release, check-licences
# targets required by test steps are: sandbox, test

TEST_CMD := @APIGEE_ACCESS_TOKEN= \
		poetry run pytest -v \
		--color=yes \
		--api-name=reasonable-adjustment-flag \
		--proxy-name=$(PROXY_NAME) \
		--apigee-access-token=$(APIGEE_ACCESS_TOKEN) \
		-s

install: install-node install-python install-hooks

install-python:
	poetry install

install-node:
	npm install --legacy-peer-deps
	cd docker/reasonable-adjustment-flag-sandbox && npm install

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit

#Command to run end-to-end smoktests post-deployment to verify the environment is working
smoketest:
	$(TEST_CMD) \
	--junitxml=smoketest-report.xml \
	-m smoketest

test:
	$(TEST_CMD) \
	--junitxml=test-report.xml \

lint:
	npm run lint
	cd docker/reasonable-adjustment-flag-sandbox && npm run lint && cd ../..
	poetry run flake8 **/*.py

publish:
	rm -rf build
	mkdir -p build
	npm run publish 2> /dev/null

serve: update-examples
	npm run serve

clean:
	rm -rf build
	rm -rf dist

generate-examples: publish
	mkdir -p build/examples
	poetry run python scripts/generate_examples.py build/reasonable-adjustment-flag.json build/examples

update-examples: generate-examples
	jq -rM . <build/examples/resources/Greeting.json >specification/components/examples/Greeting.json
	make publish

check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh

deploy-proxy: update-examples
	scripts/deploy_proxy.sh

deploy-spec: update-examples
	scripts/deploy_spec.sh

format:
	poetry run black **/*.py

build-proxy:
	scripts/build_proxy.sh

#Files to loop over in release
_dist_include="poetry.lock poetry.toml pyproject.toml Makefile build/. api_tests specification"

#Create /dist/ sub-directory and copy files into directory
release: clean publish build-proxy
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml

sandbox: update-examples
	cd docker/reasonable-adjustment-flag-sandbox && npm run start

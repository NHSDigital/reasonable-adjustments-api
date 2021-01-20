SHELL=/bin/bash -euo pipefail

# make entrypoints for this API .. currently required by the common build pipeline are,  install, lint, publish, release, check-licences
# targets required by test steps are: sandbox, test

install: install-node install-python install-hooks

install-python:
	poetry install

install-node:
	npm install -g yarn
	yarn install
	cd docker/reasonable-adjustment-flag-sandbox && yarn install && cd ../../tests && yarn install

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit

test:
	yarn run test

lint:
	yarn run lint
	cd docker/reasonable-adjustment-flag-sandbox && yarn run lint && cd ..
	poetry run flake8 **/*.py

publish:
	yarn run publish 2> /dev/null

serve: update-examples
	yarn run serve

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
	yarn run check-licenses
	scripts/check_python_licenses.sh

deploy-proxy: update-examples
	scripts/deploy_proxy.sh

deploy-spec: update-examples
	scripts/deploy_spec.sh

format:
	poetry run black **/*.py

build-proxy:
	scripts/build_proxy.sh

release: clean publish build-proxy
	mkdir -p dist
	tar -zcvf dist/package.tar.gz build
	for env in internal-dev-sandbox internal-qa-sandbox sandbox; do \
		cp ecs-proxies-deploy-sandbox.yml dist/ecs-deploy-$$env.yml; \
	done

	cp -r build/. dist
	cp -r api_tests dist
	cp -r tests dist
	cp -r specification dist

sandbox: update-examples
	cd docker/reasonable-adjustment-flag-sandbox && yarn run start

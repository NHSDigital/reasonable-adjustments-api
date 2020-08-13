SHELL=/bin/bash -euo pipefail

install:
	 npm install

lint:
	npm run lint

build:
	docker build -t reasonable-adjustments-sandbox .

run:
	docker run -p 9000:9000 reasonable-adjustments-sandbox:latest

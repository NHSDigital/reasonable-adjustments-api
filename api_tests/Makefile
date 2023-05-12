-include .env

APIGEE_ACCESS_TOKEN ?= $(shell export SSO_LOGIN_URL=https://login.apigee.com && eval get_token -u $(APIGEE_USERNAME))

TEST_CMD := @APIGEE_ACCESS_TOKEN=$(APIGEE_ACCESS_TOKEN) \
	poetry run pytest tests/reasonable_adjustment_flag -v \
	--color=yes \
	--api-name=reasonable-adjustment-flag \
	--proxy-name=$(PROXY_NAME) \
	--apigee-access-token=$(APIGEE_ACCESS_TOKEN) \
	-s

run:
	$(TEST_CMD)

#  run tests with certain marker e.g. make run-sandbox runs tests marked with sandbox
run-%:
	$(TEST_CMD) -m "$*"

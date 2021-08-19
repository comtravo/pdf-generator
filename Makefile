#!make

ifneq ($(CI),true)
  GITHUB_SHA=latest
endif

build:
	docker build -t comtravo/pdf-generator:${GITHUB_SHA} .

push:
	docker push comtravo/pdf-generator:${GITHUB_SHA}

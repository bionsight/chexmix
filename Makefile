.PHONY: test build run

build:
	docker build -t chexmix:local .

run:
	docker run chexmix:local

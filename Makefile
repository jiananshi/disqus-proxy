.PHONY: clean build test

build:
	npm install
	service supervisor restart


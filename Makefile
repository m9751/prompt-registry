.PHONY: help bootstrap build verify lint

help:
	@echo "make bootstrap  — install Python deps"
	@echo "make build      — compile prompts → dist/"
	@echo "make verify     — build + footer check (CI parity)"
	@echo "make lint       — alias for verify"

bootstrap:
	pip install -r requirements.txt

build:
	python scripts/compile_prompts.py

verify: build
	./scripts/ci-verify-footer.sh

lint: verify

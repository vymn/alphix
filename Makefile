# CLI Hub Makefile
# Convenient commands for managing CLI Hub

PYTHON = .venv/bin/python
HUB = $(PYTHON) cli_hub.py

.PHONY: help install demo test clean status

help:
	@echo "CLI Hub - Central Command Manager"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install CLI Hub globally (creates 'hub' command)"
	@echo "  demo       - Run a demonstration of CLI Hub features"
	@echo "  test       - Test the CLI Hub functionality"
	@echo "  status     - Show current hub status"
	@echo "  clean      - Clean up configuration and logs"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "After installation, use 'hub --help' for CLI usage"

install:
	@echo "Installing CLI Hub..."
	$(PYTHON) setup.py
	@echo "Installation complete! You can now use 'hub' command"
	@echo "Restart your terminal or run: source ~/.zshrc"

demo:
	@echo "Running CLI Hub demo..."
	./demo.sh

test:
	@echo "Testing CLI Hub..."
	$(HUB) status
	$(HUB) add test-echo "echo 'Hello from CLI Hub!'" --description "Test script"
	$(HUB) list
	$(HUB) run test-echo
	$(HUB) remove test-echo
	@echo "Test completed successfully!"

status:
	$(HUB) status

clean:
	@echo "Cleaning up CLI Hub configuration..."
	rm -rf ~/.cli-hub
	@echo "Configuration cleaned!"

# Development targets
dev-setup:
	python -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

dev-test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m pylint cli_hub.py

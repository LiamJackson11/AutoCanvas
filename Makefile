# Makefile — AutoCanvas convenience targets for macOS and Linux

VENV    := .venv
PYTHON  := $(VENV)/bin/python3
PIP     := $(VENV)/bin/pip

.PHONY: install run setup monitor clean uninstall help

# ── Default target ────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  AutoCanvas — available targets"
	@echo ""
	@echo "  make install    Run the full installer (venv + dependencies)"
	@echo "  make run        Launch AutoCanvas"
	@echo "  make setup      Re-run the configuration wizard"
	@echo "  make monitor    Start the live dashboard"
	@echo "  make clean      Remove generated files (keeps .env and homework)"
	@echo "  make uninstall  Remove the virtual environment completely"
	@echo ""

# ── Install ───────────────────────────────────────────────────────────────────
install:
	bash install.sh

# ── Ensure venv exists before any run target ──────────────────────────────────
$(PYTHON):
	@echo "Virtual environment not found. Run:  make install"
	@exit 1

# ── Run targets ───────────────────────────────────────────────────────────────
run: $(PYTHON)
	$(PYTHON) run.py

setup: $(PYTHON)
	$(PYTHON) setup.py

monitor: $(PYTHON)
	$(PYTHON) monitor.py

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "TEMP_*" -delete 2>/dev/null || true
	rm -f sys_check.log dashboard.html
	@echo "Cleaned generated files."

uninstall:
	rm -rf $(VENV)
	@echo "Virtual environment removed. Run 'make install' to reinstall."

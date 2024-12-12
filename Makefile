.PHONY: help venv install test coverage clean activate

# Variables - Windows paths
PYTHON = python
VENV = venv
BIN = $(VENV)\Scripts
PYTHON_VENV = $(BIN)\python
PIP = $(BIN)\pip
PYTEST = $(BIN)\pytest
COVERAGE = $(BIN)\coverage
ACTIVATE = $(BIN)\activate.bat

help:
	@echo "Commandes disponibles:"
	@echo "  make venv      - Cree l'environnement virtuel"
	@echo "  make install   - Installe les dependances"
	@echo "  make test      - Lance tous les tests"
	@echo "  make coverage  - Lance les tests avec rapport de couverture"
	@echo "  make clean     - Nettoie les fichiers temporaires"
	@echo "  make activate  - Affiche la commande pour activer le venv"

venv:
	$(PYTHON) -m venv $(VENV)
	$(PYTHON_VENV) -m pip install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) -v tests/

coverage:
	$(PYTEST) --cov=inventory_manager tests/ -v
	$(COVERAGE) html
	@echo "Rapport HTML genere dans htmlcov/index.html"

clean:
	if exist "__pycache__" rmdir /s /q "__pycache__"
	if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
	if exist ".coverage" del /f .coverage
	if exist "htmlcov" rmdir /s /q "htmlcov"
	if exist "$(VENV)" rmdir /s /q "$(VENV)"
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	del /s /q *.pyc 2>nul

activate:
	@echo "Pour activer l'environnement virtuel, executez la commande suivante:"
	@echo "$(ACTIVATE)"
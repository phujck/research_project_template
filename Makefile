.PHONY: install paper sim clean

PYTHON := python
PIP := pip

install:
	$(PIP) install -r requirements.txt

paper:
	$(PYTHON) utils/build_paper.py --paper manuscript/paper.json

sim:
	$(PYTHON) simulation/src/main.py

clean:
	rm -rf manuscript/build/*

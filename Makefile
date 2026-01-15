.PHONY: install paper sim clean

PYTHON := python
PIP := pip

install:
	$(PIP) install -r requirements.txt

paper:
	cd manuscript/tex && pdflatex -output-directory ../build main.tex
	cd manuscript/tex && bibtex ../build/main
	cd manuscript/tex && pdflatex -output-directory ../build main.tex
	cd manuscript/tex && pdflatex -output-directory ../build main.tex

sim:
	$(PYTHON) simulation/src/main.py

clean:
	rm -rf manuscript/build/*

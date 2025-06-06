# Makefile for LaTeX project report compilation

LATEX = pdflatex
BIBTEX = bibtex
TARGET = project_report

all: $(TARGET).pdf

$(TARGET).pdf: $(TARGET).tex
	$(LATEX) $(TARGET).tex
	$(LATEX) $(TARGET).tex
	$(LATEX) $(TARGET).tex

clean:
	rm -f $(TARGET).aux $(TARGET).log $(TARGET).out $(TARGET).toc $(TARGET).bbl $(TARGET).blg

distclean: clean
	rm -f $(TARGET).pdf

.PHONY: all clean distclean
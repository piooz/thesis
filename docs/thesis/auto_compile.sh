#!/bin/bash


ls "$1" | entr -c pandoc \
  --citeproc \
  --bibliography=biblio.bib \
  --pdf-engine pdflatex \
  --listings \
  /_ \
  -o thesis.tex
  # --csl ./csl/computing-surveys.csl \
  # --listings \
  # -F pandoc-crossref \

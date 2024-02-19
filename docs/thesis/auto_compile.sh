#!/bin/bash


ls "$1" | entr -c pandoc \
  -F pandoc-crossref \
  --citeproc \
  --bibliography=biblio.bib \
  --pdf-engine tectonic \
  /_ \
  -o thesis.pdf
  # --csl ./csl/computing-surveys.csl \
  # --listings \

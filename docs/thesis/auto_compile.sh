#!/bin/bash


ls "$1" | entr -c pandoc \
  --citeproc \
  --bibliography=biblio.bib \
  --csl ./csl/computing-surveys.csl \
  --pdf-engine tectonic \
  /_ \
  -o thesis.pdf

#!/bin/bash


ls "$1" | entr pandoc --csl computers-in-entertainment.csl --citeproc --bibliography=biblio.bib --pdf-engine tectonic /_ -o thesis.pdf

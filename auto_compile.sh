#!/bin/bash


ls "$1" | entr pandoc --citeproc --bibliography=biblio.bib --pdf-engine tectonic /_ -o thesis.pdf

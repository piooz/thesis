#!/bin/bash


ls "$1" | entr pandoc --csl ./iso690-numeric-pl_Mendeley.csl --citeproc --bibliography=biblio.bib --pdf-engine tectonic /_ -o thesis.pdf

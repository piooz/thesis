#!bin/bash

ls thesis.md | entr pandoc --pdf-engine tectonic /_ -o thesis.pdf

BUILDDIR=build
FILENAME=test
.RECIPEPREFIX= >

pdf:
> mkdir $(BUILDDIR) -p
> pandoc $(FILENAME).md \
> --template=template.latex \
> --listings \
> --citeproc \
> --from=markdown+tex_math_single_backslash+tex_math_dollars+raw_tex \
> --to=latex \
> --output=$(BUILDDIR)/$(FILENAME).pdf \
> --pdf-engine=tectonic
# > -F pandoc-crossref \

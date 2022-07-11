# Makefile for generating pandoc documents, with the right name, configuration, etc.
  
PDFS = $(patsubst %.md,%.pdf,$(wildcard *.md)) # Grabs collection of all markdown files in top-level directory, and replaces file extension with *.pdf

all: $(PDFS)

%.pdf: %.md
	pandoc $< -s -o "pdfs/$@" --defaults=defaults.yaml --metadata=pythonPath:"python3"
	
%.docx: %.md
	pandoc $< -s -o "docx/$@" --defaults=defaults.yaml --metadata=pythonPath:"python3"

%: %.pdf
	open $<

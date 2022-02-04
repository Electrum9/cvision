# Pandoc Config: All the options for pandoc are in defaults.yaml, to make things more convenient
PDFS = $(patsubst %.md,%.pdf,$(wildcard *.md)) # all PDF files corresponding to Markdown files

all: $(PDFS)

%.pdf: %.md
	pandoc $< -s -o "pdfs/$@" --defaults=defaults.yaml --metadata=pythonPath:"python3"
	
%.docx: %.md
	pandoc $< -s -o "docx/$@" --defaults=defaults.yaml --metadata=pythonPath:"python3"

%: %.pdf
	open $<

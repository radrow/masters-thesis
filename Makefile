TEX = pdflatex -shell-escape -interaction nonstopmode -halt-on-error -file-line-error
CHK = chktex -shell-escape -interaction nonstopmode -halt-on-error -file-line-error
BIB = bibtex
MAIN = thesis
SRC = $(MAIN).tex
OUT = $(MAIN).pdf
SRCS = $(shell find . -name "*.tex" -not -name ".*")
TEXTDIR = ./chapters
TEXT = $(shell find $(TEXTDIR) -name "*.tex" -not -name ".*")
DICT = $(TEXTDIR)/.aspell.en.pws
REPL = $(TEXTDIR)/.aspell.en.prepl

.PHONY : all clean splchk

all : $(OUT) # check splchk

check: $(SRCS)
	! $(CHK) $(MAIN) | grep .

clean :
	-rm -rf {,$(TEXTDIR)}{*.{aux,log,pdf,toc,out,bbl,blg,lof},auto} _minted-thesis

$(OUT) : $(SRCS)
	$(TEX) $(SRC) && $(BIB) $(MAIN) && $(TEX) $(SRC) && $(TEX) $(SRC)

%.chk: %.tex
	aspell \
		--home-dir=./$(TEXTDIR) \
		--personal=$(DICT) \
		--repl=$(REPL) \
		--lang=en_GB \
		--mode=tex \
		--add-tex-command="autoref op" \
		-x \
		check $<

splchk: $(DICT) $(REPL) $(addsuffix .chk,$(basename $(TEXT)))

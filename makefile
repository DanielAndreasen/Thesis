update:
	git push
	git add thesis.pdf
	git commit -m "New update"
	git push

all:
	git add .
	git commit -m "Added all"
	git push

clean:
	rm -f *fdb_latexmk *.log *.bbl *.blg *.fls *.lof *.lot *.out

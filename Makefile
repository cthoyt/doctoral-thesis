.PHONY: pdf
pdf:
	pdflatex main.tex

.PHONY: clean
clean:
	rm main.aux main.bcf main.log main.out main.run.xml main.toc others/*.aux

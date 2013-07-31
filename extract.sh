#!/bin/bash
SRC=~/Code/papers/pdfs
OUT=~/Code/papers/text/

files="$(find "$SRC" -iname "*.pdf" -type f -print)"

for f in $files;
do
		filename=$(basename "$f")
		filename="${filename%.*}"
		echo $f
		pdf2txt.py -o "$OUT/$filename.txt" $f 
done

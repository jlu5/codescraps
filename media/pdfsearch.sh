#!/bin/bash
# Searches a string of text (first argument) through a list of PDF files.

QUERY="$1"

shift

for pdf in "$@"; do
	echo "SEARCHING: $pdf"
	pdftotext "$pdf" - | grep -i "$QUERY"
	echo ""
done

#!/bin/bash
# Searches a string of text (first argument) through a list of documents.

QUERY="$1"

shift

bold="$(tput bold)"
normal="$(tput sgr0)"

search () {
	while read data; do
		grep --color -i "$QUERY" <<< "$data"
	done
}

for file in "$@"; do
	echo ""
	echo "${bold}SEARCHING: ${file}${normal}"

	# Use pdftotext for PDFs, or pandoc for everything else
	if [[ "$(file --mime-type -b "$file")" == "application/pdf" ]]; then
		pdftotext "$file" - | search
	else
		pandoc "$file" -t plain --wrap=none -o - | search
	fi
done

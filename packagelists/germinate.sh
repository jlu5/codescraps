#!/bin/bash
MIRROR=http://www.deb-multimedia.org
DISTS=jessie
ARCH=("amd64" "i386")

for a in $ARCH; do
	germinate -S file:///srv/reprepro/germinate/seeds -s ${1} -m $MIRROR -d $DISTS -a $a -c main -v --no-rdepends
	echo "Getting sources for ${a}"
	for pkg in $(cat required | tail -n +3 | head -n -2 | cut -d '|' -f 2 | sort | uniq); do echo $pkg install; done | tee deb-multimedia.sources.packages.${a}
	echo "Getting binaries for ${a}"
	for pkg in $(cat required | tail -n +3 | head -n -2 | cut -d '|' -f 1); do echo $pkg install; done | tee deb-multimedia.mirror.packages.${a};
done

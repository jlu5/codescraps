## packagelists/

This folder contains some scripts I use for my personal APT repository @ http://packages.overdrive.pw/

Most of these scripts use stdout for their output, meaning it can be automated/crontabbed using pipes.

### Highlights
##### pparse.py & pparse2.py
 * Scripts used to get lists of packages in a repository (package name, architecture, version) from the repository handling tool. 
 * **pparse.py** handles '[reprepro](//mirrorer.alioth.debian.org/) list' output, and **pparse2.py** handles lists for [aptly](http://www.aptly.info/). * The latter is the one currently being used as of September 6, 2014.
##### rplist.sh
 * Automates the above process using bash for loops.
 
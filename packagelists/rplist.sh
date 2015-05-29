WRAPPER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$WRAPPER_DIR"

pparse () {
	python2 pparse2.py > /srv/aptly/public/${DIST}_list.html
}

DISTS=$(aptly repo list -raw | sed 's/sid-extras/sid-imports/g')

for DIST in $DISTS
do
    echo Processing lists for $DIST
    distname=`aptly snapshot list -raw | egrep -i ${DIST}-.{4}-.{2}-.{2} | sort -r | cut -d$'\n' -f1`
    if [[ ! -z "$distname" ]]; then
        echo "Using packages in snapshot ${distname} for $DIST"
        aptly snapshot show -with-packages ${distname} | pparse
    else
        echo "Using packages in repo $DIST for $DIST"
        aptly repo show -with-packages $DIST | pparse
    fi
done

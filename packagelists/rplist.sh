for DIST in $(aptly repo list -raw)
do
    echo Processing lists for $DIST
    distname=`aptly snapshot list -raw | egrep -i ${DIST}-.{4}-.{2}-.{2} | sort -r | cut -d$'\n' -f1`
    if [[ ! -z "$distname" ]]; then
        echo "Using packages in snapshot ${distname} for $DIST"
        aptly snapshot show -with-packages ${distname} | python2 ~/utils/pparse2.py > /srv/aptly/public/${DIST}_list.html
    else
        echo "Using packages in repo $DIST for $DIST"
        aptly repo show -with-packages $DIST | python2 ~/utils/pparse2.py > /srv/aptly/public/${DIST}_list.html
    fi
done

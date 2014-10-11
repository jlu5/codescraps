for DIST in "sid" "sid-imports"
# for DIST in "wheezy" "sid" "wheezy-imports" "sid-imports"
do
    echo Processing lists for $DIST
    distname=`aptly snapshot list -raw | egrep -i ${DIST}-.{4}-.{2}-.{2} | sort -r | cut -d$'\n' -f1`
    echo "Using packages in snapshot ${distname} for $DIST"
    aptly snapshot show -with-packages ${distname} | python2 ~/utils/pparse2.py > /srv/aptly/public/${DIST}_list.html
done

# for DIST in "wheezy" "jessie"
for DIST in "wheezy" "sid" "wheezy-imports" "sid-imports"
do
    echo Processing lists for $DIST
    aptly repo show -with-packages $DIST | python2 ~/utils/pparse2.py > /srv/aptly/public/${DIST}_list.html
done

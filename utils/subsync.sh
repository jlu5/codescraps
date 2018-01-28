#!/bin/bash
# Resyncs all submodules in the target folder.
AUTHOR="overdrivenetworks subsync robot"
AUTHOREMAIL="webmaster@overdrivenetworks.com"
COMMITMSG="Refresh submodules"
#COMMITMSG="Automatically syncing submodules at $(date -Iseconds)"

if [[ ! -z "$1" ]]; then
    TARGETDIR="$1"
    pushd "$TARGETDIR"
fi

git submodule foreach git pull origin master

modules=$(grep 'path =' .gitmodules | cut -d '=' -f 2 | xargs)
#GIT_COMMITTER_NAME="$AUTHOR" GIT_COMMITTER_EMAIL="$AUTHOREMAIL" git commit $MODULES -m "$COMMITMSG" --author="$AUTHOR <$AUTHOREMAIL>"
git commit $modules -m "$COMMITMSG" --author="$AUTHOR <$AUTHOREMAIL>"

if [[ ! -z "$1" ]]; then
    popd
fi

#!/usr/bin/bash

#BASEDIR=$(dirname $0)
#echo "Script location: ${BASEDIR}"

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && cd .. && cd .. && pwd  )"
PROGRAMDIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && cd .. && pwd  )"
DIRNAME="backupper"


find $PROGRAMDIR | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

if [[ -n "$1" ]]; then
	tar cfvJ ${BASEDIR}/backupper-${1}.tar.xz --exclude .git --exclude .gitignore -C ${BASEDIR} --transform 's,'${DIRNAME}',backupper-'$1',' ${DIRNAME}
fi


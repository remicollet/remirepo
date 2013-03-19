#!/bin/bash

if [ $# != 2 ]; then
	echo "Usage: $0 VERSION GITHUB_COMMIT" 1>&2
	exit 1
fi

VERSION=$1
GITHUB_COMMIT=$2

ORIGINAL_SOURCE_FILE="${GITHUB_COMMIT}.tar.gz"
NEW_SOURCE_FILE="php-JMSParser-${VERSION}-${GITHUB_COMMIT}.tar.gz"

if [ ! -f "$ORIGINAL_SOURCE_FILE" ]; then
	echo "ERROR: Original source file '${ORIGINAL_SOURCE_FILE}' not found" 1>&2
	exit 1
fi

TAR=`which tar`

$TAR -xzf "$ORIGINAL_SOURCE_FILE"
rm -rf "parser-lib-${GITHUB_COMMIT}/doc" "$NEW_SOURCE_FILE"
$TAR -czf "$NEW_SOURCE_FILE" "parser-lib-${GITHUB_COMMIT}"

echo "${NEW_SOURCE_FILE} created"
exit 0

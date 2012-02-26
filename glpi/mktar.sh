#!/bin/bash

if [ "$1" = "" ]; then
	echo mising rev number
	exit 1
fi

svn export -r $1 https://forge.indepnet.net/svn/glpi/branches/0.83-bugfixes glpi
rm -rf glpi/tools
mv glpi/install/mysql/glpi-0.83-empty.sql .
rm -f glpi/install/mysql/*.sql
mv glpi-0.83-empty.sql glpi/install/mysql/
tar czf glpi-0.83-$1.tar.gz glpi && echo glpi-0.83-$1.tar.gz created
rm -rf glpi


#!/bin/sh
exec /sbin/apachectl -k graceful "$@"

#!/bin/sh

/usr/lib/rpm/perl.req $* | \
    grep -v -e "perl(th" \
    -e "perl(lib::mtr" -e "perl(lib::v1/mtr" -e "perl(mtr"

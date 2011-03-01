#!/bin/bash

set -x 

if [ ! -d /tmp/comm-1.9.2 ]; then
	tar xjf thunderbird-3.1.8.source.tar.bz2 -C /tmp && echo Sources extracted
fi

DIR=/tmp/testfixlang
rm -rf $DIR
mkdir -p $DIR/chrome

touch $DIR/gdata.mani

php ./fixlang.php \
    --xpi=gdata-provider.xpi \
    --gdata-provider=/tmp/comm-1.9.2/calendar/locales/en-US/chrome/calendar/providers/gdata \
    --manifest=/tmp/testfixlang/gdata.mani \
    --output=$DIR \
    --debug=0

touch $DIR/lightning.mani

php ./fixlang.php \
    --xpi=lightning.xpi \
    --lightning=/tmp/comm-1.9.2/calendar/locales/en-US/chrome/lightning \
    --calendar=/tmp/comm-1.9.2/calendar/locales/en-US/chrome/calendar \
    --manifest=/tmp/testfixlang/lightning.mani \
    --output=$DIR \
    --debug=0


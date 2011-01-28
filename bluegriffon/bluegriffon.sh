#!/bin/sh
#
# Startup script for the BlueGriffon RPM
#

##
## Variables
##
MOZ_ARCH=$(uname -m)
case $MOZ_ARCH in
        x86_64 | s390x | sparc64 )
                MOZ_LIB_DIR="/usr/lib64"
                SECONDARY_LIB_DIR="/usr/lib"
                ;;
        * )
                MOZ_LIB_DIR="/usr/lib"
                SECONDARY_LIB_DIR="/usr/lib64"
                ;;
esac

if [ ! -x $MOZ_LIB_DIR/bluegriffon/bluegriffon ]; then
    if [ ! -x $SECONDARY_LIB_DIR/bluegriffon/bluegriffon ]; then
        echo "Error: $MOZ_LIB_DIR/bluegriffon/bluegriffon not found"
        exit 1
    fi
    MOZ_LIB_DIR="$SECONDARY_LIB_DIR"
fi

MOZ_DIST_BIN="$MOZ_LIB_DIR/bluegriffon"
MOZ_PROGRAM="$MOZ_DIST_BIN/bluegriffon"

##
## Set MOZ_ENABLE_PANGO is no longer used because Pango is enabled by default
## you may use MOZ_DISABLE_PANGO=1 to force disabling of pango
##
#MOZ_DISABLE_PANGO=1
#export MOZ_DISABLE_PANGO

##
## Set MOZ_APP_LAUNCHER for gnome-session
##
export MOZ_APP_LAUNCHER="/usr/bin/bluegriffon"

##
## Disable the GNOME crash dialog, Moz has it's own
## 
GNOME_DISABLE_CRASH_DIALOG=1
export GNOME_DISABLE_CRASH_DIALOG


exec $MOZ_PROGRAM "$@"

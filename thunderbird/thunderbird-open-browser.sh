#!/bin/bash
## Copyright (C) 2004 Warren Togami <wtogami@redhat.com>
## Contributors:   David Hill <djh[at]ii.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

#
# open-browser.sh for MozillaThunderbird
# Release 5
#
# This script is called by MozillaThunderbird in order to launch the web 
# browser specified in gconf key /desktop/gnome/url-handlers/http/command
#

# Exit with Error Message
function error_exit() {
    echo "$1"
    if [ -a /usr/bin/zenity ]; then
        /usr/bin/zenity --error --text="$1"
    else
        xmessage "$1" &
    fi
    exit 1
}

# No URL specified so set to blank
url=$1
if [ -z $url ]; then
    url=about:blank
fi

# Use xdg-open if it exists (Gnome 2.6+ only)
if [ -f /usr/bin/xdg-open ]; then
    OUTPUT="$(/usr/bin/xdg-open "$url" 2>&1)"
    if [ $? -ne 0 ]; then
        error_exit "$OUTPUT"
    fi
    exit 0
fi

# Pull key from gconf, remove %s or "%s", trim leading & trailing spaces
GCONF=$(gconftool-2 -g /desktop/gnome/url-handlers/http/command 2>/dev/null | sed -e 's/%s//; s/\"\"//; s/^\ *//; s/\ *$//')
NEEDTERM=$(gconftool-2 -g /desktop/gnome/url-handlers/http/need-terminal 2>/dev/null | sed -e 's/^\ *//; s/\ *$//')

# Check if browser really exists
which $GCONF 2> /dev/null > /dev/null
if [ $? -ne 0 ]; then
    error_exit "ERROR: The browser $GCONF specified in Preferences -> Preferred Applications does not exist."
fi

# Check if text-mode browser
if [ "$NEEDTERM" == "true" ]; then
    PREFTERM=$(gconftool-2 -g /desktop/gnome/applications/terminal/exec 2>/dev/null | sed -e 's/^\ *//; s/\ *$//')
    TERMARGS=$(gconftool-2 -g /desktop/gnome/applications/terminal/exec_arg 2>/dev/null | sed -e 's/^\ *//; s/\ *$//')
    # Check if terminal exists
    which $PREFTERM 2> /dev/null > /dev/null
    if [ $? -ne 0 ]; then
        error_exit "ERROR: The terminal $GCONF specified in Preferences -> Preferred Applications does not exist."
    fi
    # Execute
    exec $PREFTERM $TERMARGS $GCONF "$url"
fi

exec $GCONF "$url"


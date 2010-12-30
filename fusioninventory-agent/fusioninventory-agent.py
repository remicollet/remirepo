# A plugin for yum which notifies the FusionInventory Agent to send a inventory
#
# Copyright (c) 2010 Remi Collet <Fedora@FamilleCollet.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# version 0.1

from yum.plugins import TYPE_CORE
from urlgrabber.grabber import urlread
from urlgrabber.grabber import URLGrabError

requires_api_version = '2.1'
plugin_type = TYPE_CORE

def posttrans_hook(conduit):
    """
    Tell FusionInventory Agent to send an inventory
    Run only after an rpm transaction.
    """
    try:
        port = conduit.confInt('main', 'port', default=62354)
        url = "http://localhost:%d/now" % port
        conduit.info(9, "calling %s" % url)
        res = urlread(url, 2048)

    except URLGrabError, e:
        conduit.info(4, "Unable to send connect to FusionInventory service")
        if '403' in e.args[1]:
            conduit.info(4, "Check than FusionInventory service runs with rpc-trust-localhost option")
        else:
            conduit.info(4, "Check than FusionInventory service is running")
        conduit.info(6, "Error %s: %s" % (e.args[0], e.args[1]))
        return

    if res and 'Done.' in res:
        conduit.info(2, "FusionInventory agent asked to run an inventory")

    elif res:
        conduit.info(4, "Bad anwser from FusionInventory agent")
        conduit.info(8, res)

    else:
        conduit.info(4, "No anwser from FusionInventory agent")


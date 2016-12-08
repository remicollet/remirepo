<?php
/* Autoloader for icewind/smb and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Icewind\\SMB\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Icewind/Streams/autoload.php',
));


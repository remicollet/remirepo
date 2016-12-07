<?php
/* Autoloader for mongodb/mongodb and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('MongoDB\\', __DIR__);
require_once __DIR__. '/functions.php';

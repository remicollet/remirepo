<?php
/* Autoloader for composer/ca-bundle and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Composer\\CaBundle\\', __DIR__);


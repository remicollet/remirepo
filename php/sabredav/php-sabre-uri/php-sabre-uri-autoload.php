<?php
/* Autoloader for sabre/uri and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Sabre\\Uri\\', __DIR__);

// Functions
require_once __DIR__ . '/functions.php';

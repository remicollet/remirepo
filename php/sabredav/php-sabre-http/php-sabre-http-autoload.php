<?php
/* Autoloader for sabre/http and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Sabre\\HTTP\\', __DIR__);

// Functions
require_once __DIR__ . '/functions.php';

\Fedora\Autoloader\Dependencies::required(array(
	'/usr/share/php/Sabre/Event/autoload.php',
	'/usr/share/php/Sabre/Uri/autoload.php',
));


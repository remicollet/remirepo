<?php
/* Autoloader for sabre/xml and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Sabre\\Xml\\', __DIR__);

// Functions
require_once __DIR__ . '/Deserializer/functions.php';
require_once __DIR__ . '/Serializer/functions.php';

\Fedora\Autoloader\Dependencies::required(array(
	'/usr/share/php/Sabre/Uri/autoload.php',
));


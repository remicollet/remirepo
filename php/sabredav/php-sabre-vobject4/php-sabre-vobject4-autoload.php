<?php
/* Autoloader for sabre/vobject v4 and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Sabre\\VObject\\', __DIR__);
\Fedora\Autoloader\Dependencies::required([
	'/usr/share/php/Sabre/Xml/autoload.php',
]);


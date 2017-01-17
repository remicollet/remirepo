<?php
/* Autoloader for sabre/dav and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Sabre\\DAV\\',     dirname(__DIR__) . '/DAV');
\Fedora\Autoloader\Autoload::addPsr4('Sabre\\DAVACL\\',  dirname(__DIR__) . '/DAVACL');
\Fedora\Autoloader\Autoload::addPsr4('Sabre\\CalDAV\\',  dirname(__DIR__) . '/CalDAV');
\Fedora\Autoloader\Autoload::addPsr4('Sabre\\CardDAV\\', dirname(__DIR__) . '/CardDAV');

\Fedora\Autoloader\Dependencies::required([
	'/usr/share/php/Sabre/Event/autoload.php',
	'/usr/share/php/Sabre/HTTP/autoload.php',
	'/usr/share/php/Sabre/VObject4/autoload.php',
	'/usr/share/php/Sabre/Xml/autoload.php',
	'/usr/share/php/Sabre/Uri/autoload.php',
	'/usr/share/php/Psr/Log/autoload.php',
]);


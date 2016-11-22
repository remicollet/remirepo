<?php
/* Autoloader for pdepend/pdepend and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('PHPMD\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
	'/usr/share/php/PDepend/autoload.php',
));


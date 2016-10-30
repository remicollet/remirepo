<?php
/* Autoloader for friendsofphp/php-cs-fixer and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Symfony\\CS\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
	'/usr/share/php/Symfony/Component/autoload.php',
	'/usr/share/php/SebastianBergmann/Diff/autoload.php',
));


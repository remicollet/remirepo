<?php
/**
 * Autoloader php-bartlett-php-compatinfo-db and its dependencies
 */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Bartlett\\CompatInfoDb\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
        '/usr/share/php/Composer/Semver/autoload.php',
));


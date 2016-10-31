<?php
/**
 * Autoloader for bartlett/php-compatinfo and its dependencies
 */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Bartlett\\CompatInfo\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Bartlett/Reflect/autoload.php',
    '/usr/share/php/Bartlett/CompatInfoDb/autoload.php',
));


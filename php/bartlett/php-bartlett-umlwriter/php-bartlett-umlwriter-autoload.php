<?php
/**
 * Autoloader for bartlett/umlwriter and its dependencies
 */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Bartlett\\UmlWriter\\', dirname(__DIR__));
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Symfony/Component/autoload.php',
    '/usr/share/php/TokenReflection/autoload.php',
    '/usr/share/php/SebastianBergmann/Version/autoload.php',
    '/usr/share/php/Bartlett/Reflect/autoload.php',
));


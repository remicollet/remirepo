<?php
/* Autoloader for jeremeamia/superclosure and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('SuperClosure\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php//Symfony/Polyfill/autoload.php',
    array(
        '/usr/share/php/PhpParser3/autoload.php',
        '/usr/share/php/PhpParser2/autoload.php',
        '/usr/share/php/PhpParser/autoload.php',
)));


<?php
/* Autoloader for phpspec/phpspec and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('PhpSpec\\', __DIR__);
$vendorDir = stream_resolve_include_path('Symfony/Component/Console/Application.php');
\Fedora\Autoloader\Autoload::addPsr4('Symfony\\Component\\', dirname(dirname($vendorDir)));

/* spec tree in current dir, when exists */
if (is_dir(getcwd().'/spec')) {
    \Fedora\Autoloader\Autoload::addPsr4('spec\\', getcwd().'/spec');
}

// Dependencies (Rely on include_path as in PHPUnit dependencies + circular dependencies)
require_once 'phpspec/php-diff/autoload.php';
require_once 'SebastianBergmann/Exporter/autoload.php';
require_once 'Prophecy/autoload.php'; // After exporter to avoid newer version
require_once 'Doctrine/Instantiator/autoload.php';

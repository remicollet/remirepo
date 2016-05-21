<?php
/* Autoloader for jeremeamia/superclosure and its dependencies */

$vendorDir = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('SuperClosure\\', dirname(__DIR__));

// Dependencies
if (file_exists($vendorDir . '/PhpParser2/autoload.php')) {
    require_once $vendorDir . '/PhpParser2/autoload.php';
} else {
    require_once $vendorDir . '/PhpParser/autoload.php';
}
require_once $vendorDir . '/Symfony/Polyfill/autoload.php';

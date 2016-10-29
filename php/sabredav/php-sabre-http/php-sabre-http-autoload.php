<?php
/**
 * Autoloader for sabre/http and its dependencies
 */

$vendorDir = '/usr/share/php';

// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Sabre\\HTTP\\', dirname(dirname(__DIR__)));

// Functions
require_once __DIR__ . '/functions.php';

// dependencies
require_once $vendorDir . '/Sabre/Event/autoload.php';
require_once $vendorDir . '/Sabre/Uri/autoload.php';


<?php
/**
 * Autoloader for sabre/xml and its dependencies
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

$fedoraClassLoader->addPrefix('Sabre\\Xml\\', dirname(dirname(__DIR__)));

// Functions
require_once __DIR__ . '/Deserializer/functions.php';
require_once __DIR__ . '/Serializer/functions.php';

// Dependencies
require_once $vendorDir . '/Sabre/Uri/autoload.php';


<?php
/* Autoloader for herrera-io/json and its dependencies */

$vendorDir = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Herrera\\Json\\', dirname(dirname(__DIR__)));
require_once __DIR__ . '/json_version.php';

// Dependencies
require_once $vendorDir . '/Seld/JsonLint/autoload.php';
require_once $vendorDir . '/JsonSchema/autoload.php';

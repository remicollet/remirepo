<?php
/* Autoloader for friendsofphp/php-cs-fixer and its dependencies */

$vendorDir = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Symfony\\CS\\', dirname(dirname(__DIR__)));

// Dependencies
require_once $vendorDir . '/Symfony/Component/autoload.php';
require_once $vendorDir . '/SebastianBergmann/Diff/autoload.php';


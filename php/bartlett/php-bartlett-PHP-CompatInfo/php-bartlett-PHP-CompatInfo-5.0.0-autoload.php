<?php
/**
 * Autoloader for bartlett/php-compatinfo and its dependencies
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
$fedoraClassLoader->addPrefixes(array(
    'Bartlett\\CompatInfo'                  => dirname(dirname(__DIR__)),
));

// Dependencies
require_once $vendorDir . '/Bartlett/Reflect/autoload.php';
require_once $vendorDir . '/Bartlett/CompatInfoDb/autoload.php';

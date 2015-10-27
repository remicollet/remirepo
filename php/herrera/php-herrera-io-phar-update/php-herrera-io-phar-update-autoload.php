<?php
/* Autoloader for herrera-io/phar-update and its dependencies */

$vendorDir = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Herrera\\Phar\\Update\\', dirname(dirname(dirname(__DIR__))));

// Dependencies
require_once $vendorDir . '/Herrera/Json/autoload.php';
require_once $vendorDir . '/Herrera/Version/autoload.php';

// Adpated from upstream constants.php
if (!defined('PHAR_UPDATE_MANIFEST_SCHEMA')) {
    define('PHAR_UPDATE_MANIFEST_SCHEMA', '/usr/share/php-herrera-io-phar-update/res/schema.json');
}
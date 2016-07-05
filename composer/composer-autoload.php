<?php
/* Autoloader for composer/composer and its dependencies */

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
    'Symfony\\Component\\'         => $vendorDir,
    'Composer\\'                   => dirname(__DIR__)
));

// Dependencies
require_once $vendorDir . '/Seld/JsonLint/autoload.php';
require_once $vendorDir . '/Seld/PharUtils/autoload.php';
require_once $vendorDir . '/Seld/CliPrompt/autoload.php';
require_once $vendorDir . '/Composer/CaBundle/autoload.php';
require_once $vendorDir . '/Composer/Spdx/autoload.php';
require_once $vendorDir . '/Composer/Semver/autoload.php';
require_once $vendorDir . '/JsonSchema2/autoload.php';
require_once $vendorDir . '/Psr/Log/autoload.php';


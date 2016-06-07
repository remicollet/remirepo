<?php

/**
 * Autoloader for phpseclib/phpseclib.
 */
$vendorDir = '/usr/share/php';

// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir.'/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

// composer.json: "autoload": { "files": [ "phpseclib/bootstrap.php" ], "psr-4": { "phpseclib\\": "phpseclib/" }
require_once __DIR__ . '/bootstrap.php';

$fedoraClassLoader->addPrefixes(array(
    'phpseclib' => dirname(__DIR__),
));


<?php
/* Autoloader for pdepend/pdepend and its dependencies */

$vendorDir = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

/* PHPMD */
$fedoraClassLoader->addPrefix('PHPMD\\', dirname(__DIR__));

/* for symfony/dependency-injection, filesystem and config */
$fedoraClassLoader->addPrefix('Symfony\\Component\\', $vendorDir);

/* PDepend */
require_once $vendorDir . '/PDepend/autoload.php';

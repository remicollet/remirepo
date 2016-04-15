<?php
/**
 * Autoloader for nikic/php-parser and its dependencies
 */

$vendorDir = '/usr/share/php';

// Use Symfony PSR4 autoloader
if (!isset($fedoraPsr4ClassLoader) || !($fedoraPsr4ClassLoader instanceof \Symfony\Component\ClassLoader\Psr4ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\Psr4ClassLoader', false)) {
        require_once '/usr/share/php/Symfony/Component/ClassLoader/Psr4ClassLoader.php';
    }

    $fedoraPsr4ClassLoader = new \Symfony\Component\ClassLoader\Psr4ClassLoader();
    $fedoraPsr4ClassLoader->register(true);
}

$fedoraPsr4ClassLoader->addPrefix('PhpParser\\', __DIR__);


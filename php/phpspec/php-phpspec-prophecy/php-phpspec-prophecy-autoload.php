<?php
/* Autoloader for phpspec/prophecy and its dependencies */

// Rely on include_path as in PHPUnit dependencies + circular dependencies

// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once 'Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Prophecy\\', dirname(__DIR__));

// Dependencies
require_once 'Doctrine/Instantiator/autoload.php';
require_once 'SebastianBergmann/Comparator/autoload.php';
require_once 'SebastianBergmann/RecursionContext/autoload.php';
require_once 'phpDocumentor/Reflection/DocBlock/autoload.php';

<?php
/* Autoloader for phpspec/phpspec and its dependencies */

$vendorDir = stream_resolve_include_path('Symfony/Component/ClassLoader/ClassLoader.php');
$vendorDir = dirname(dirname(dirname(dirname($vendorDir))));
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefixes(array(
    'Symfony\\Component\\'                  => $vendorDir,
    'PhpSpec\\'                             => dirname(__DIR__),
));

/* spec tree in current dir, when exists */
if (is_dir(getcwd().'/spec')) {
    $fedoraClassLoader->addPrefix('spec', getcwd());
}

// Dependencies (Rely on include_path as in PHPUnit dependencies + circular dependencies)
require_once 'phpspec/php-diff/autoload.php';
require_once 'Prophecy/autoload.php';
require_once 'SebastianBergmann/Exporter/autoload.php';
require_once 'Doctrine/Instantiator/autoload.php';

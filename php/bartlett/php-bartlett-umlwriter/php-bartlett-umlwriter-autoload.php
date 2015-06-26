<?php
/**
 * Autoloader for bartlett/umlwriter and its dependencies
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
    'Symfony\\Component'                  => $vendorDir,
    'TokenReflection'                     => $vendorDir,
    'Bartlett\\Umlwiter'                  => dirname(dirname(__DIR__)),
));
if (is_file('/usr/share/php-bartlett-PHP-CompatInfo/compatinfo.sqlite')) {
    putenv('BARTLETT_COMPATINFO_DB=/usr/share/php-bartlett-PHP-CompatInfo/compatinfo.sqlite');
}

// Dependencies
require_once $vendorDir . '/SebastianBergmann/Version/autoload.php';
require_once $vendorDir . '/Bartlett/Reflect/autoload.php';

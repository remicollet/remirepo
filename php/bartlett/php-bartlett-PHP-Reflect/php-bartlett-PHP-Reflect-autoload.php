<?php
/**
 * Autoloader for bartlett/php-reflect and its dependencies
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
    'JsonSchema'                          => $vendorDir,
    'Seld\\JsonLint'                      => $vendorDir,
    'Bartlett'                            => dirname(dirname(__DIR__)),
));

// Mandatory dependencies
require_once $vendorDir . '/PhpParser/Autoloader.php';
PhpParser\Autoloader::register();
require_once $vendorDir . '/SebastianBergmann/Version/autoload.php';
require_once $vendorDir . '/Doctrine/Common/Collections/autoload.php';
require_once $vendorDir . '/Doctrine/Common/Cache/autoload.php';
require_once $vendorDir . '/phpDocumentor/Reflection/DocBlock/autoload.php';

// Needed when installed for 'Bartlett\CompatInfo\Analyser\CompatibilityAnalyser'
if (is_dir($vendorDir . '/Bartlett/CompatInfo')) {
   $fedoraClassLoader->addPrefix('Bartlett\\CompatInfo', $vendorDir);
}

// Optional dependencies
if (file_exists($vendorDir . '/Bartlett/UmlWriter/autoload.php')) {
   require_once $vendorDir . '/Bartlett/UmlWriter/autoload.php';
}
if (is_dir($vendorDir . '/Psr/Log')) {
   $fedoraClassLoader->addPrefix('Psr\\Log', $vendorDir);
}
if (is_dir($vendorDir . '/Monolog')) {
   $fedoraClassLoader->addPrefix('Monolog', $vendorDir);
}

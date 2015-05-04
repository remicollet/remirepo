<?php
$vendorDir = '/usr/share/php';
require_once $vendorDir . '/Symfony/Component/ClassLoader/UniversalClassLoader.php';
use Symfony\Component\ClassLoader\UniversalClassLoader;

$loader = new UniversalClassLoader();
$loader->registerNamespaces(array(
    'Seld\\JsonLint'                      => $vendorDir,
    'Seld\\PharUtils'                     => $vendorDir,
    'Seld\\CliPrompt'                     => $vendorDir,
    'JsonSchema'                          => $vendorDir,
    'Symfony\\Component\\Console'         => $vendorDir,
    'Symfony\\Component\\Finder'          => $vendorDir,
    'Symfony\\Component\\Process'         => $vendorDir,
    'Symfony\\Component\\ClassLoader'     => $vendorDir,
    'Composer'                            => dirname(__DIR__)
));
$loader->register();

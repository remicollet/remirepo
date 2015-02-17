<?php
require_once 'phpspec/php-diff/autoload.php';
require_once 'Prophecy/autoload.php';

$vendorDir = '/usr/share/php';
require_once $vendorDir . '/Symfony/Component/ClassLoader/UniversalClassLoader.php';
use Symfony\Component\ClassLoader\UniversalClassLoader;

$loader = new UniversalClassLoader();
$loader->registerNamespaces(array(
    'Doctrine\\Instantiator'              => $vendorDir,
    'SebastianBergmann'                   => $vendorDir,
    'Symfony\\Component'                  => $vendorDir,
    'PhpSpec'                             => dirname(__DIR__),
));
$loader->register();
